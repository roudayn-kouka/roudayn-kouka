#!/usr/bin/env python3
"""Generates a plum/rose/lilac contribution activity graph (last 31 days)
from the GitHub GraphQL API. No external service, no dependencies.

Usage (in GitHub Actions):
  GITHUB_TOKEN=... GH_USER=roudayn-kouka python3 scripts/activity_graph.py dist/activity-graph.svg
Local test without network:
  python3 scripts/activity_graph.py out.svg --demo
"""
import datetime as dt
import json
import os
import random
import sys
import urllib.request

DAYS = 31
W, H = 1200, 360
PAD_L, PAD_R, PAD_T, PAD_B = 70, 40, 90, 60

BG0, BG1 = "#0c0814", "#1a0b24"
ROSE, PINK, LILAC, PLUM, TEXT, MUTED, GRID = "#f472b6", "#f9a8d4", "#c4b5fd", "#a21caf", "#f5e8ff", "#c9b3d9", "#2a1438"
SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'DejaVu Sans Mono', monospace"

QUERY = """query($login:String!){ user(login:$login){ contributionsCollection{
  contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } } } } }"""


def fetch(user, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "activity-graph"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    return days[-DAYS:], cal["totalContributions"]


def demo():
    today = dt.date.today()
    days = [{"date": str(today - dt.timedelta(days=DAYS - 1 - i)), "contributionCount": random.choice([0, 0, 1, 2, 3, 5, 8, 4])} for i in range(DAYS)]
    return days, 187


def smooth_path(pts):
    """Catmull-Rom -> cubic Bezier for a soft curve."""
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        # keep curve from dipping below baseline
        base = H - PAD_B
        c1 = (c1[0], min(c1[1], base)); c2 = (c2[0], min(c2[1], base))
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d


def render(days, total_year, user):
    counts = [d["contributionCount"] for d in days]
    peak = max(counts) or 1
    ymax = max(4, peak + (-peak % 4))  # round up to multiple of 4
    pw, ph = W - PAD_L - PAD_R, H - PAD_T - PAD_B
    step = pw / (len(days) - 1)
    pts = [(PAD_L + i * step, PAD_T + ph - c / ymax * ph) for i, c in enumerate(counts)]
    line = smooth_path(pts)
    area = f"{line} L{pts[-1][0]:.1f} {PAD_T + ph} L{pts[0][0]:.1f} {PAD_T + ph} Z"
    month_total = sum(counts)
    active = sum(1 for c in counts if c)
    best = max(range(len(counts)), key=lambda i: counts[i])

    grid = []
    for k in range(5):
        v = ymax * k / 4
        y = PAD_T + ph - v / ymax * ph
        grid.append(f'<line x1="{PAD_L}" y1="{y:.1f}" x2="{W-PAD_R}" y2="{y:.1f}" stroke="{GRID}" stroke-dasharray="{"0" if k == 0 else "4 6"}"/>'
                    f'<text x="{PAD_L-14}" y="{y+4:.1f}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">{int(v)}</text>')
    xl = []
    for i, d in enumerate(days):
        if i % 5 == 0 or i == len(days) - 1:
            day = dt.date.fromisoformat(d["date"])
            xl.append(f'<text x="{pts[i][0]:.1f}" y="{H-PAD_B+26}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">{day.strftime("%d %b")}</text>')
    dots = []
    for i, (x, y) in enumerate(pts):
        r = 5 if i == best and counts[i] else 3.2
        col = PINK if i == best and counts[i] else LILAC
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{BG0}" stroke="{col}" stroke-width="2">'
                    f'<animate attributeName="opacity" values="0;1" dur="0.4s" begin="{0.6 + i*0.04:.2f}s" fill="freeze"/>'
                    f'<title>{days[i]["date"]}: {counts[i]} contribution(s)</title></circle>')
    path_len = 4000
    gen = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def stat(x, label, value):
        return (f'<text x="{x}" y="52" font-family="{SANS}" font-size="26" font-weight="800" fill="{TEXT}">{value}</text>'
                f'<text x="{x}" y="72" font-family="{MONO}" font-size="11.5" letter-spacing="1.5" fill="{MUTED}">{label}</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{user}: {month_total} contributions in the last {DAYS} days">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
    <linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ROSE}" stop-opacity="0.45"/><stop offset="0.6" stop-color="{PLUM}" stop-opacity="0.15"/><stop offset="1" stop-color="{PLUM}" stop-opacity="0"/></linearGradient>
    <linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{LILAC}"/><stop offset="0.5" stop-color="{ROSE}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
    <filter id="glow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/>
  <rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="20" fill="none" stroke="{LILAC}" stroke-opacity="0.25"/>
  <text x="{PAD_L-40}" y="38" font-family="{MONO}" font-size="12.5" letter-spacing="2.5" fill="{ROSE}">CONTRIBUTIONS · LAST {DAYS} DAYS</text>
  {stat(W-560, "LAST 31 DAYS", month_total)}
  {stat(W-400, "ACTIVE DAYS", f"{active}/{DAYS}")}
  {stat(W-240, "LAST 12 MONTHS", total_year)}
  {''.join(grid)}
  <path d="{area}" fill="url(#area)" opacity="0">
    <animate attributeName="opacity" values="0;1" dur="1.2s" begin="0.4s" fill="freeze"/>
  </path>
  <path d="{line}" fill="none" stroke="url(#line)" stroke-width="3" stroke-linecap="round" filter="url(#glow)" stroke-dasharray="{path_len}" stroke-dashoffset="{path_len}">
    <animate attributeName="stroke-dashoffset" from="{path_len}" to="0" dur="2s" fill="freeze"/>
  </path>
  {''.join(dots)}
  {''.join(xl)}
  <text x="{W-PAD_R}" y="{H-12}" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{MUTED}" opacity="0.7">updated {gen}</text>
</svg>"""


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "activity-graph.svg"
    user = os.environ.get("GH_USER", "roudayn-kouka")
    if "--demo" in sys.argv:
        days, total = demo()
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("GITHUB_TOKEN is required")
        days, total = fetch(user, token)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(render(days, total, user))
    print("wrote", out)
