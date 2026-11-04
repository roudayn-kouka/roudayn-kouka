#!/usr/bin/env python3
"""Generates the three profile cards from the GitHub GraphQL API, in the
plum / rose / lilac theme — no external card service:

  <out>/stats.svg           stars, commits, PRs, issues, repos, contributions
  <out>/streak.svg          all-time total, current streak, longest streak
  <out>/activity-graph.svg  last 31 days curve

Token: PROFILE_TOKEN (your own PAT -> includes PRIVATE contributions, same
numbers as your GitHub calendar). Falls back to GITHUB_TOKEN (public only).

  PROFILE_TOKEN=... GH_USER=roudayn-kouka python3 scripts/profile_cards.py dist
  python3 scripts/profile_cards.py out --demo     # local preview, fake data
"""
import datetime as dt
import json
import os
import random
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import activity_graph  # noqa: E402  (same folder: renders the 31-day curve)

BG0, BG1 = "#0c0814", "#1a0b24"
ROSE, PINK, LILAC, CYAN, PLUM = "#f472b6", "#f9a8d4", "#c4b5fd", "#67e8f9", "#a21caf"
TEXT, MUTED, GRID = "#f5e8ff", "#c9b3d9", "#2a1438"
SANS = activity_graph.SANS
MONO = activity_graph.MONO


# ------------------------------------------------------------------ API
def gql(token, query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-cards"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if data.get("errors"):
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]


Q_PROFILE = """query($login:String!){ user(login:$login){
  createdAt
  followers{ totalCount }
  pullRequests{ totalCount }
  issues{ totalCount }
  repositories(ownerAffiliations:OWNER, isFork:false, first:100){
    totalCount nodes{ stargazerCount } }
  repositoriesContributedTo(contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,REPOSITORY]){ totalCount }
}}"""

Q_YEAR = """query($login:String!,$from:DateTime!,$to:DateTime!){ user(login:$login){
  contributionsCollection(from:$from,to:$to){
    totalCommitContributions restrictedContributionsCount
    contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } }
}}}"""


def fetch(user, token):
    p = gql(token, Q_PROFILE, {"login": user})["user"]
    created = dt.datetime.fromisoformat(p["createdAt"].replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    days, commits_last_year = {}, 0
    start = created
    while start < now:  # API allows at most 1 year per query
        end = min(start + dt.timedelta(days=365), now)
        c = gql(token, Q_YEAR, {"login": user, "from": start.isoformat(), "to": end.isoformat()})["user"]["contributionsCollection"]
        for w in c["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
        start = end
    # last 365 days, exactly like the profile calendar header
    last = gql(token, Q_YEAR, {"login": user, "from": (now - dt.timedelta(days=365)).isoformat(), "to": now.isoformat()})["user"]["contributionsCollection"]
    commits_last_year = last["totalCommitContributions"] + last["restrictedContributionsCount"]
    return {
        "created": created.date(),
        "days": dict(sorted(days.items())),
        "last_year_total": last["contributionCalendar"]["totalContributions"],
        "commits_last_year": commits_last_year,
        "stars": sum(n["stargazerCount"] for n in p["repositories"]["nodes"]),
        "repos": p["repositories"]["totalCount"],
        "prs": p["pullRequests"]["totalCount"],
        "issues": p["issues"]["totalCount"],
        "followers": p["followers"]["totalCount"],
        "contributed_to": p["repositoriesContributedTo"]["totalCount"],
    }


def demo():
    today = dt.date.today()
    start = today - dt.timedelta(days=870)
    days = {str(start + dt.timedelta(days=i)): random.choice([0, 0, 0, 1, 2, 4, 7]) for i in range(871)}
    return {"created": start, "days": days, "last_year_total": 235, "commits_last_year": 190, "stars": 3,
            "repos": 41, "prs": 6, "issues": 2, "followers": 3, "contributed_to": 5}


# ------------------------------------------------------------- streaks
def streaks(days):
    dates = [dt.date.fromisoformat(k) for k in days]
    counts = list(days.values())
    total = sum(counts)
    first_active = next((d for d, c in zip(dates, counts) if c), dates[0])
    # longest
    best, best_s, best_e, run, run_s = 0, None, None, 0, None
    for d, c in zip(dates, counts):
        if c:
            run += 1
            run_s = run_s or d
            if run > best:
                best, best_s, best_e = run, run_s, d
        else:
            run, run_s = 0, None
    # current (today may still be empty -> start from yesterday, like GitHub)
    i = len(counts) - 1
    if counts[i] == 0:
        i -= 1
    cur, cur_e = 0, dates[i] if i >= 0 else None
    while i >= 0 and counts[i]:
        cur += 1
        i -= 1
    cur_s = dates[i + 1] if cur else None
    return {"total": total, "first": first_active, "longest": best, "longest_range": (best_s, best_e),
            "current": cur, "current_range": (cur_s, cur_e)}


def fmt(d):
    return d.strftime("%b %-d") if d else "—"


def fmt_range(r):
    s, e = r
    if not s:
        return "—"
    return fmt(s) if s == e else f"{fmt(s)} – {fmt(e)}"


def holo(gid, w):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{w}" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="reflect">'
            f'<stop offset="0" stop-color="{ROSE}"/><stop offset="0.33" stop-color="{LILAC}"/><stop offset="0.66" stop-color="{CYAN}"/><stop offset="1" stop-color="{ROSE}"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="{w} 0" dur="6s" repeatCount="indefinite"/></linearGradient>')


def frame(W, H, body, label):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
    {holo("holo", W)}
  </defs>
  <rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/>
  <rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="20" fill="none" stroke="url(#holo)" stroke-opacity="0.55" stroke-width="1.5"/>
  {body}
</svg>"""


# --------------------------------------------------------------- stats
def render_stats(s, user):
    W, H = 600, 230
    rows = [
        ("★", "Stars earned", s["stars"]),
        ("⟳", "Commits (1 yr)", s["commits_last_year"]),
        ("⇄", "Pull requests", s["prs"]),
        ("!", "Issues", s["issues"]),
        ("▣", "Repositories", s["repos"]),
        ("⎇", "Contributed to", s["contributed_to"]),
    ]
    body = [f'<text x="30" y="44" font-family="{MONO}" font-size="12.5" letter-spacing="2.5" fill="{ROSE}">GITHUB STATS · @{user}</text>']
    for i, (ico, lab, val) in enumerate(rows):
        col, r = (0, i) if i < 3 else (1, i - 3)
        x, y = 30 + col * 205, 92 + r * 44
        body.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" begin="{0.15*i:.2f}s" fill="freeze"/>'
                    f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="15" fill="{LILAC}">{ico}</text>'
                    f'<text x="{x+24}" y="{y}" font-family="{SANS}" font-size="14" fill="{MUTED}">{lab}</text>'
                    f'<text x="{x+178}" y="{y}" text-anchor="end" font-family="{SANS}" font-size="17" font-weight="800" fill="{TEXT}">{val}</text></g>')
    # big ring: contributions last year
    cx, cy, R = 505, 125, 62
    circ = 2 * 3.14159 * R
    body.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{GRID}" stroke-width="9"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="url(#holo)" stroke-width="9" stroke-linecap="round" '
                f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}" transform="rotate(-90 {cx} {cy})">'
                f'<animate attributeName="stroke-dashoffset" from="{circ:.1f}" to="0" dur="1.6s" fill="freeze"/></circle>'
                f'<text x="{cx}" y="{cy+8}" text-anchor="middle" font-family="{SANS}" font-size="30" font-weight="800" fill="{TEXT}">{s["last_year_total"]}</text>'
                f'<text x="{cx}" y="{cy+30}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{MUTED}">contributions</text>'
                f'<text x="{cx}" y="{cy+R+30}" text-anchor="middle" font-family="{MONO}" font-size="10.5" letter-spacing="1" fill="{MUTED}">LAST 12 MONTHS</text>')
    return frame(W, H, "".join(body), f"GitHub stats for {user}")


# -------------------------------------------------------------- streak
def render_streak(st, user):
    W, H = 900, 220
    col_w = W / 3
    today = dt.date.today()

    def col(i, value, label, sub, color, big=False):
        x = col_w * i + col_w / 2
        return (f'<text x="{x:.0f}" y="{108 if not big else 112}" text-anchor="middle" font-family="{SANS}" font-size="{40 if not big else 44}" font-weight="800" fill="{TEXT}">{value}</text>'
                f'<text x="{x:.0f}" y="{150 if not big else 168}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="{700 if big else 500}" fill="{color}">{label}</text>'
                f'<text x="{x:.0f}" y="{176 if not big else 192}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">{sub}</text>')

    ring_x, ring_y, R = col_w * 1.5, 98, 52
    circ = 2 * 3.14159 * R
    body = [
        f'<line x1="{col_w:.0f}" y1="40" x2="{col_w:.0f}" y2="{H-40}" stroke="{GRID}" stroke-width="1.5"/>',
        f'<line x1="{2*col_w:.0f}" y1="40" x2="{2*col_w:.0f}" y2="{H-40}" stroke="{GRID}" stroke-width="1.5"/>',
        col(0, st["total"], "Total contributions", f"{fmt(st['first'])}, {st['first'].year} – Present", LILAC),
        f'<circle cx="{ring_x:.0f}" cy="{ring_y}" r="{R}" fill="none" stroke="{GRID}" stroke-width="8"/>'
        f'<circle cx="{ring_x:.0f}" cy="{ring_y}" r="{R}" fill="none" stroke="url(#holo)" stroke-width="8" stroke-linecap="round" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}" transform="rotate(-90 {ring_x:.0f} {ring_y})">'
        f'<animate attributeName="stroke-dashoffset" from="{circ:.1f}" to="0" dur="1.4s" fill="freeze"/></circle>'
        f'<text x="{ring_x:.0f}" y="{ring_y-R-6}" text-anchor="middle" font-family="{SANS}" font-size="20">🔥</text>',
        f'<text x="{ring_x:.0f}" y="{ring_y+14}" text-anchor="middle" font-family="{SANS}" font-size="40" font-weight="800" fill="{TEXT}">{st["current"]}</text>'
        f'<text x="{ring_x:.0f}" y="{ring_y+R+30}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{PINK}">Current streak</text>'
        f'<text x="{ring_x:.0f}" y="{ring_y+R+52}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">{fmt_range(st["current_range"]) if st["current"] else fmt(today)}</text>',
        col(2, st["longest"], "Longest streak", fmt_range(st["longest_range"]), LILAC),
    ]
    return frame(W, H, "".join(body), f"Contribution streaks for {user}")


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "dist"
    user = os.environ.get("GH_USER", "roudayn-kouka")
    if "--demo" in sys.argv:
        s = demo()
    else:
        token = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("PROFILE_TOKEN or GITHUB_TOKEN is required")
        print("token:", "PROFILE_TOKEN (public + private)" if os.environ.get("PROFILE_TOKEN") else "GITHUB_TOKEN (public only)")
        s = fetch(user, token)
    os.makedirs(out, exist_ok=True)
    st = streaks(s["days"])
    last31 = [{"date": k, "contributionCount": v} for k, v in list(s["days"].items())[-activity_graph.DAYS:]]
    files = {
        "stats.svg": render_stats(s, user),
        "streak.svg": render_streak(st, user),
        "activity-graph.svg": activity_graph.render(last31, s["last_year_total"], user),
    }
    for name, svg in files.items():
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(svg)
    print(f"last 12 months: {s['last_year_total']} | all-time: {st['total']} | current: {st['current']} | longest: {st['longest']}")
    print("wrote", ", ".join(files))
