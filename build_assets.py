#!/usr/bin/env python3
"""Generates the animated SVG assets for the GitHub profile README.
Palette: plum / rose / lilac holographic (portfolio style).
Run:  python3 build_assets.py   -> writes ./assets/*.svg
"""
import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(os.path.join(OUT, "projects"), exist_ok=True)

# ---------- palette ----------
BG0 = "#0c0814"     # deep plum night
BG1 = "#22092d"
PLUM = "#a21caf"
ROSE = "#f472b6"
PINK = "#f9a8d4"
LILAC = "#c4b5fd"
VIOLET = "#a78bfa"
CYAN = "#67e8f9"    # holographic glint
TEXT = "#f5e8ff"
MUTED = "#c9b3d9"

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'DejaVu Sans Mono', monospace"


def holo_gradient(gid, dur="6s", w=1200):
    """Animated holographic linear gradient that slides horizontally."""
    return f"""
    <linearGradient id="{gid}" x1="0" y1="0" x2="{w}" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
      <stop offset="0" stop-color="{ROSE}"/>
      <stop offset="0.25" stop-color="{LILAC}"/>
      <stop offset="0.5" stop-color="{CYAN}"/>
      <stop offset="0.75" stop-color="{VIOLET}"/>
      <stop offset="1" stop-color="{ROSE}"/>
      <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="{w} 0" dur="{dur}" repeatCount="indefinite"/>
    </linearGradient>"""


def sparkles(points, color=PINK):
    out = []
    for i, (x, y, s) in enumerate(points):
        d = 2.2 + (i % 4) * 0.7
        b = (i * 0.37) % 2
        out.append(f"""
    <g transform="translate({x} {y})">
      <path d="M0 -{s} L{s*0.25} -{s*0.25} L{s} 0 L{s*0.25} {s*0.25} L0 {s} L-{s*0.25} {s*0.25} L-{s} 0 L-{s*0.25} -{s*0.25} Z" fill="{color}">
        <animate attributeName="opacity" values="0;1;0" dur="{d:.1f}s" begin="{b:.2f}s" repeatCount="indefinite"/>
        <animateTransform attributeName="transform" type="scale" values="0.4;1;0.4" dur="{d:.1f}s" begin="{b:.2f}s" repeatCount="indefinite"/>
      </path>
    </g>""")
    return "".join(out)


# =====================================================================
# 1. HEADER
# =====================================================================
def header():
    W, H = 1200, 340
    # isometric holographic cube (fake 3D) ---------------------------
    cx, cy, s = 985, 165, 70
    import math
    c30, s30 = math.cos(math.pi / 6) * s, math.sin(math.pi / 6) * s
    top = f"M{cx} {cy-s} L{cx+c30} {cy-s+s30} L{cx} {cy} L{cx-c30} {cy-s+s30} Z"
    left = f"M{cx-c30} {cy-s+s30} L{cx} {cy} L{cx} {cy+s} L{cx-c30} {cy+s30} Z"
    right = f"M{cx+c30} {cy-s+s30} L{cx} {cy} L{cx} {cy+s} L{cx+c30} {cy+s30} Z"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Roudayna Kouka — Cloud, DevOps &amp; DevSecOps">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG0}"/>
      <stop offset="0.55" stop-color="{BG1}"/>
      <stop offset="1" stop-color="#2d0b3a"/>
    </linearGradient>
    {holo_gradient("holo", "7s")}
    {holo_gradient("holoFast", "4s", 600)}
    <radialGradient id="orbRose"><stop offset="0" stop-color="{ROSE}" stop-opacity="0.55"/><stop offset="1" stop-color="{ROSE}" stop-opacity="0"/></radialGradient>
    <radialGradient id="orbLilac"><stop offset="0" stop-color="{LILAC}" stop-opacity="0.45"/><stop offset="1" stop-color="{LILAC}" stop-opacity="0"/></radialGradient>
    <radialGradient id="orbPlum"><stop offset="0" stop-color="{PLUM}" stop-opacity="0.6"/><stop offset="1" stop-color="{PLUM}" stop-opacity="0"/></radialGradient>
    <linearGradient id="faceTop" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PINK}"/><stop offset="1" stop-color="{LILAC}"/>
      <animate attributeName="x1" values="0;1;0" dur="5s" repeatCount="indefinite"/></linearGradient>
    <linearGradient id="faceLeft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ROSE}"/><stop offset="1" stop-color="{PLUM}"/></linearGradient>
    <linearGradient id="faceRight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="#5b1a77"/></linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0 L0 0 0 40" fill="none" stroke="{LILAC}" stroke-opacity="0.07" stroke-width="1"/>
    </pattern>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="soft"><feGaussianBlur stdDeviation="28"/></filter>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="22"/></clipPath>
  </defs>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#grid)"/>

    <!-- drifting aurora orbs -->
    <g filter="url(#soft)">
      <circle cx="180" cy="60" r="190" fill="url(#orbPlum)">
        <animate attributeName="cx" values="180;320;180" dur="14s" repeatCount="indefinite"/>
      </circle>
      <circle cx="760" cy="300" r="220" fill="url(#orbRose)">
        <animate attributeName="cx" values="760;600;760" dur="16s" repeatCount="indefinite"/>
        <animate attributeName="cy" values="300;250;300" dur="11s" repeatCount="indefinite"/>
      </circle>
      <circle cx="1050" cy="80" r="200" fill="url(#orbLilac)">
        <animate attributeName="cy" values="80;150;80" dur="12s" repeatCount="indefinite"/>
      </circle>
    </g>

    <!-- holographic top line -->
    <rect x="0" y="0" width="{W}" height="4" fill="url(#holo)"/>

    <!-- name -->
    <text x="70" y="118" font-family="{MONO}" font-size="17" fill="{PINK}" letter-spacing="3">&gt; kubectl apply -f roudayna.yaml</text>
    <text x="68" y="190" font-family="{SANS}" font-size="72" font-weight="800" fill="url(#holo)" letter-spacing="-1">Roudayna Kouka</text>
    <text x="70" y="236" font-family="{SANS}" font-size="25" font-weight="600" fill="{TEXT}">Cloud <tspan fill="{ROSE}">·</tspan> DevOps <tspan fill="{ROSE}">·</tspan> DevSecOps Engineer</text>
    <text x="70" y="270" font-family="{SANS}" font-size="17" fill="{MUTED}">Secure CI/CD · Infrastructure as Code · GitOps on Kubernetes · AWS · Azure · GCP</text>

    <!-- chips -->
    <g font-family="{MONO}" font-size="14" font-weight="600">
      <g transform="translate(70 290)">
        <rect width="98" height="30" rx="15" fill="{ROSE}" fill-opacity="0.14" stroke="{ROSE}" stroke-opacity="0.6"/>
        <text x="49" y="20" text-anchor="middle" fill="{PINK}">☁ cloud</text>
      </g>
      <g transform="translate(180 290)">
        <rect width="104" height="30" rx="15" fill="{LILAC}" fill-opacity="0.12" stroke="{LILAC}" stroke-opacity="0.6"/>
        <text x="52" y="20" text-anchor="middle" fill="{LILAC}">⎈ gitops</text>
      </g>
      <g transform="translate(296 290)">
        <rect width="104" height="30" rx="15" fill="{CYAN}" fill-opacity="0.10" stroke="{CYAN}" stroke-opacity="0.55"/>
        <text x="52" y="20" text-anchor="middle" fill="{CYAN}">⟳ ci/cd</text>
      </g>
      <g transform="translate(412 290)">
        <rect width="118" height="30" rx="15" fill="{VIOLET}" fill-opacity="0.12" stroke="{VIOLET}" stroke-opacity="0.6"/>
        <text x="59" y="20" text-anchor="middle" fill="{VIOLET}">⛨ secops</text>
      </g>
    </g>

    <!-- orbit rings -->
    <g transform="translate({cx} {cy})" fill="none">
      <ellipse rx="150" ry="46" stroke="url(#holoFast)" stroke-width="2" stroke-dasharray="6 10" opacity="0.8" transform="rotate(-18)">
        <animate attributeName="stroke-dashoffset" from="0" to="-160" dur="4s" repeatCount="indefinite"/>
      </ellipse>
      <ellipse rx="118" ry="128" stroke="{LILAC}" stroke-opacity="0.25" stroke-width="1.5" transform="rotate(30)"/>
      <!-- satellites -->
      <circle r="6" fill="{ROSE}" filter="url(#glow)">
        <animateMotion dur="6s" repeatCount="indefinite" path="M150 0 A150 46 0 1 1 -150 0 A150 46 0 1 1 150 0" rotate="0"/>
      </circle>
      <circle r="4.5" fill="{CYAN}" filter="url(#glow)">
        <animateMotion dur="9s" repeatCount="indefinite" path="M0 -128 A118 128 0 1 1 0 128 A118 128 0 1 1 0 -128"/>
      </circle>
    </g>

    <!-- floating holographic cube -->
    <g filter="url(#glow)">
      <animateTransform attributeName="transform" type="translate" values="0 0; 0 -12; 0 0" dur="5s" repeatCount="indefinite"/>
      <path d="{left}" fill="url(#faceLeft)" opacity="0.92"/>
      <path d="{right}" fill="url(#faceRight)" opacity="0.92"/>
      <path d="{top}" fill="url(#faceTop)"/>
      <path d="{top} {left} {right}" fill="none" stroke="#fff" stroke-opacity="0.55" stroke-width="1.5" stroke-linejoin="round"/>
      <!-- glint sweeping across the cube -->
      <path d="M{cx-c30} {cy-s+s30} L{cx-c30+18} {cy-s+s30-10} L{cx+8} {cy+s-10} L{cx-10} {cy+s} Z" fill="#fff" opacity="0">
        <animate attributeName="opacity" values="0;0;0.35;0" keyTimes="0;0.6;0.75;1" dur="5s" repeatCount="indefinite"/>
      </path>
    </g>
    <!-- cube shadow -->
    <ellipse cx="{cx}" cy="{cy+s+52}" rx="70" ry="9" fill="{PLUM}" opacity="0.45">
      <animate attributeName="rx" values="70;56;70" dur="5s" repeatCount="indefinite"/>
    </ellipse>

    {sparkles([(640, 70, 7), (860, 52, 5), (1130, 250, 6), (560, 300, 4), (1150, 40, 4), (720, 160, 3), (930, 300, 5)])}
  </g>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="{LILAC}" stroke-opacity="0.25"/>
</svg>"""
    return svg


# =====================================================================
# 2. TERMINAL (typing animation, loops)
# =====================================================================
def terminal():
    W = 900
    CH = 8.6          # approx monospace char width @ 14.5px
    LH = 25
    TYPE_CPS = 30     # chars per second when "typing" commands
    P = "roudayna@fst:~$ "

    # (kind, segments)  kind: cmd = typed, out = appears instantly
    # segments: list of (text, color, bold)
    lines = [
        ("cmd", [("whoami", TEXT, True)]),
        ("out", [("Roudayna Kouka", PINK, True), (" — Cloud · DevOps · DevSecOps Engineer", MUTED, False)]),
        ("gap", []),
        ("cmd", [("cat stack.yaml", TEXT, True)]),
        ("out", [("cloud:         ", LILAC, True), ("[ AWS · Azure · GCP ]", TEXT, False)]),
        ("out", [("iac:           ", LILAC, True), ("[ Terraform · Ansible ]", TEXT, False)]),
        ("out", [("ci_cd:         ", LILAC, True), ("[ Jenkins · GitHub Actions · Azure DevOps · GitLab CI ]", TEXT, False)]),
        ("out", [("gitops:        ", LILAC, True), ("[ Kubernetes · ArgoCD · Helm ]", TEXT, False)]),
        ("out", [("devsecops:     ", LILAC, True), ("[ SonarQube · Trivy · OWASP DC · OPA/Rego ]", TEXT, False)]),
        ("out", [("observability: ", LILAC, True), ("[ Prometheus · Grafana ]", TEXT, False)]),
        ("gap", []),
        ("cmd", [("trivy image roudayna:latest --severity HIGH,CRITICAL", TEXT, True)]),
        ("out", [("Total: 0 ", "#86efac", True), ("(HIGH: 0, CRITICAL: 0)", MUTED, False), ("  ✔ ship it", PINK, True)]),
        ("gap", []),
        ("cmd", [("kubectl get pods -n career", TEXT, True)]),
        ("out", [("NAME         READY   STATUS    MESSAGE", MUTED, True)]),
        ("out", [("roudayna-0   1/1     ", TEXT, False), ("Running", "#86efac", True), ("   open to internships & junior roles · 2027", PINK, False)]),
    ]

    top_pad = 64
    H = top_pad + LH * len(lines) + 44
    # timing
    t = 0.6
    sched = []
    for kind, segs in lines:
        text = "".join(s[0] for s in segs)
        if kind == "cmd":
            dur = max(0.5, len(text) / TYPE_CPS)
            sched.append((t, t + dur))
            t += dur + 0.45
        elif kind == "out":
            sched.append((t, t))
            t += 0.12
        else:
            sched.append((t, t))
            t += 0.25
    hold = 4.0
    T = t + hold

    def kt(x):
        return f"{min(max(x / T, 0), 1):.4f}"

    body = []
    for i, ((kind, segs), (a, b)) in enumerate(zip(lines, sched)):
        y = top_pad + i * LH
        if kind == "gap":
            continue
        if kind == "cmd":
            x0 = 28 + len(P) * CH
            text = "".join(s[0] for s in segs)
            wfull = len(text) * CH + 4
            body.append(f'<clipPath id="c{i}"><rect x="{x0}" y="{y-18}" height="{LH}" width="0">'
                        f'<animate attributeName="width" values="0;0;{wfull:.1f};{wfull:.1f};0" keyTimes="0;{kt(a)};{kt(b)};{kt(T-0.35)};1" dur="{T:.2f}s" repeatCount="indefinite"/></rect></clipPath>')
            # prompt appears at a
            body.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{kt(a-0.01)};{kt(a)};{kt(T-0.35)};1" dur="{T:.2f}s" repeatCount="indefinite"/>'
                        f'<text x="28" y="{y}" font-family="{MONO}" font-size="14.5"><tspan fill="{ROSE}" font-weight="700">roudayna</tspan><tspan fill="{MUTED}">@</tspan><tspan fill="{LILAC}" font-weight="700">fst</tspan><tspan fill="{MUTED}">:</tspan><tspan fill="{CYAN}">~</tspan><tspan fill="{TEXT}">$ </tspan></text>'
                        f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="14.5" clip-path="url(#c{i})" fill="{TEXT}" font-weight="700">{escape(text)}</text></g>')
            # typing cursor that follows
            body.append(f'<rect y="{y-14}" width="8" height="17" fill="{PINK}" opacity="0">'
                        f'<animate attributeName="x" values="{x0};{x0};{x0+wfull-4:.1f};{x0+wfull-4:.1f}" keyTimes="0;{kt(a)};{kt(b)};1" dur="{T:.2f}s" repeatCount="indefinite"/>'
                        f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(a-0.01)};{kt(a)};{kt(b+0.4)};{kt(b+0.41)};1" dur="{T:.2f}s" repeatCount="indefinite"/></rect>')
        else:
            fw = ' font-weight="700"'
            spans = "".join(f'<tspan fill="{c}"{fw if bold else ""}>{escape(txt)}</tspan>' for txt, c, bold in segs)
            body.append(f'<text x="28" y="{y}" font-family="{MONO}" font-size="14.5" xml:space="preserve" opacity="0">{spans}'
                        f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{kt(a-0.01)};{kt(a)};{kt(T-0.35)};1" dur="{T:.2f}s" repeatCount="indefinite"/></text>')

    # final idle prompt + blinking cursor
    yl = top_pad + len(lines) * LH
    endt = sched[-1][1] + 0.4
    x0 = 28 + len(P) * CH
    body.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{kt(endt-0.01)};{kt(endt)};{kt(T-0.35)};1" dur="{T:.2f}s" repeatCount="indefinite"/>'
                f'<text x="28" y="{yl}" font-family="{MONO}" font-size="14.5"><tspan fill="{ROSE}" font-weight="700">roudayna</tspan><tspan fill="{MUTED}">@</tspan><tspan fill="{LILAC}" font-weight="700">fst</tspan><tspan fill="{MUTED}">:</tspan><tspan fill="{CYAN}">~</tspan><tspan fill="{TEXT}">$ </tspan></text>'
                f'<rect x="{x0}" y="{yl-14}" width="8" height="17" fill="{PINK}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect></g>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: whoami, focus.yaml, mission">
  <defs>
    <linearGradient id="tbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b0824"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
    {holo_gradient("tholo", "6s", W)}
    <clipPath id="tclip"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#tclip)">
    <rect width="{W}" height="{H}" fill="url(#tbg)"/>
    <rect width="{W}" height="38" fill="#2a0f36"/>
    <rect y="37" width="{W}" height="1.5" fill="url(#tholo)"/>
    <circle cx="24" cy="19" r="6.5" fill="#ff5f87"/>
    <circle cx="46" cy="19" r="6.5" fill="#fbbf77"/>
    <circle cx="68" cy="19" r="6.5" fill="#a78bfa"/>
    <text x="{W/2}" y="24" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">roudayna@fst — zsh — 120×30</text>
    {''.join(body)}
  </g>
  <rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="16" fill="none" stroke="url(#tholo)" stroke-opacity="0.7" stroke-width="1.5"/>
</svg>"""
    return svg


# =====================================================================
# 3. PROJECT CARDS
# =====================================================================
def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur.strip()); cur = ""
        cur += w + " "
    if cur.strip():
        lines.append(cur.strip())
    return lines


def project_card(slug, kicker, title, desc, tags, accent, badge=None):
    W, H = 440, 230
    dlines = wrap(desc, 52)[:3]
    desc_svg = "".join(f'<text x="26" y="{110 + i*21}" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{escape(l)}</text>' for i, l in enumerate(dlines))
    # tags
    tx, tg = 26, []
    for t in tags:
        w = len(t) * 7.6 + 22
        if tx + w > W - 20:
            break
        tg.append(f'<g transform="translate({tx:.0f} 182)"><rect width="{w:.0f}" height="26" rx="13" fill="{accent}" fill-opacity="0.13" stroke="{accent}" stroke-opacity="0.5"/>'
                  f'<text x="{w/2:.0f}" y="17.5" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{accent}">{escape(t)}</text></g>')
        tx += w + 8
    badge_svg = ""
    if badge:
        bw = len(badge) * 7.4 + 22
        badge_svg = (f'<g transform="translate({W-26-bw:.0f} 22)"><rect width="{bw:.0f}" height="24" rx="12" fill="{BG0}" stroke="{PINK}" stroke-opacity="0.55"/>'
                     f'<text x="{bw/2:.0f}" y="16.5" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{PINK}">{escape(badge)}</text></g>')
    gid = f"h_{slug}"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">
  <defs>
    <linearGradient id="bg_{slug}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1e0828"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
    {holo_gradient(gid, "5s", W)}
    <radialGradient id="glow_{slug}" cx="1" cy="0" r="0.9"><stop offset="0" stop-color="{accent}" stop-opacity="0.35"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="18" fill="url(#bg_{slug})"/>
  <rect width="{W}" height="{H}" rx="18" fill="url(#glow_{slug})">
    <animate attributeName="opacity" values="0.6;1;0.6" dur="4s" repeatCount="indefinite"/>
  </rect>
  <text x="26" y="40" font-family="{MONO}" font-size="12.5" letter-spacing="2" fill="{accent}">{escape(kicker.upper())}</text>
  <text x="26" y="76" font-family="{SANS}" font-size="23" font-weight="800" fill="{TEXT}">{escape(title)}</text>
  {badge_svg}
  {desc_svg}
  {''.join(tg)}
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="none" stroke="url(#{gid})" stroke-width="2"/>
</svg>"""
    with open(os.path.join(OUT, "projects", f"{slug}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


PROJECTS = [
    ("eks-three-tier", "DevSecOps · AWS EKS", "Three-Tier App on EKS",
     "MERN app on Amazon EKS: Terraform infra, Jenkins CI with SonarQube & Trivy gates, ECR, GitOps with ArgoCD, Prometheus/Grafana monitoring.",
     ["Terraform", "Jenkins", "ArgoCD", "Trivy"], ROSE, None),
    ("netflix-devsecops", "DevSecOps · Kubernetes", "Netflix Clone DevSecOps",
     "End-to-end DevSecOps delivery: SAST, dependency, filesystem and image scans in CI, deployed to Kubernetes with Helm and ArgoCD.",
     ["SonarQube", "OWASP DC", "Helm", "ArgoCD"], LILAC, None),
    ("azdo-solution-pipeline", "CI/CD · Azure DevOps", "D365 Solution Pipeline",
     "Azure DevOps YAML pipeline for Dynamics 365 solutions: validation, packaging, backup, health checks and automated rollback.",
     ["Azure DevOps", "YAML", "PowerShell", ".NET 8"], CYAN, None),
    ("terraform-iac", "IaC · AWS", "Terraform IaC + CodePipeline",
     "Infrastructure as Code on AWS with Terraform, delivered through an automated AWS CodePipeline workflow.",
     ["Terraform", "AWS", "CodePipeline", "IaC"], VIOLET, None),
    ("aws-ecs-three-tier", "Cloud architecture · AWS", "Containerized 3-Tier on AWS",
     "Highly available ECS architecture behind CloudFront and WAF, with RDS Multi-AZ and ElastiCache.",
     ["ECS", "WAF", "CloudFront", "RDS Multi-AZ"], PINK, "private"),
    ("jenkins-ansible", "CI/CD · Automation", "Jenkins · Ansible · K8s CI/CD",
     "Classic DevOps chain: Maven builds in Jenkins, configuration with Ansible, Docker images deployed on Kubernetes.",
     ["Jenkins", "Maven", "Ansible", "Docker"], ROSE, None),
    ("bh-agentic-ai", "AI · Event-driven", "BH Assurance Agentic AI",
     "Agentic AI platform for insurance engagement: LLM agents, RAG, FastAPI microservices and Kafka event streams. Hackathon winner.",
     ["LLMs", "RAG", "FastAPI", "Kafka"], LILAC, "1st place"),
    ("secure-graphql", "AppSec · API", "Secure GraphQL API",
     "Recipe API on an Apollo GraphQL server, secured with Keycloak authentication and role-based access control (RBAC).",
     ["Keycloak", "RBAC", "GraphQL", "Apollo"], CYAN, None),
]


# =====================================================================
# 4. DIVIDER + FOOTER + section titles
# =====================================================================
def divider():
    W, H = 1200, 24
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>{holo_gradient("dh", "5s", W)}
    <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.15" stop-color="#fff"/><stop offset="0.85" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask></defs>
  <g mask="url(#m)">
    <rect x="0" y="11" width="{W}" height="2" fill="url(#dh)"/>
  </g>
  <g transform="translate({W/2} 12)">
    <path d="M0 -8 L2.5 -2.5 L8 0 L2.5 2.5 L0 8 L-2.5 2.5 L-8 0 L-2.5 -2.5 Z" fill="{PINK}">
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/>
    </path>
  </g>
</svg>"""


def section_title(slug, emoji_path, text, sub):
    W, H = 900, 64
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(text)}">
  <defs>{holo_gradient("st_" + slug, "6s", 500)}</defs>
  <text x="2" y="20" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{ROSE}">{escape(sub)}</text>
  <text x="0" y="54" font-family="{SANS}" font-size="30" font-weight="800" fill="url(#st_{slug})">{escape(text)}</text>
</svg>"""


def footer():
    W, H = 1200, 150
    def wave(a, ph, y):
        return (f"M0 {y} C 200 {y-a} 400 {y+a} 600 {y} S 1000 {y-a} 1200 {y} L1200 {H} L0 {H} Z")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="w1" x1="0" x2="1"><stop offset="0" stop-color="{PLUM}"/><stop offset="0.5" stop-color="{ROSE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
    <linearGradient id="w2" x1="0" x2="1"><stop offset="0" stop-color="{LILAC}"/><stop offset="1" stop-color="{PLUM}"/></linearGradient>
  </defs>
  <path fill="url(#w2)" opacity="0.35" d="{wave(30,0,70)}">
    <animate attributeName="d" dur="9s" repeatCount="indefinite" values="{wave(30,0,70)};{wave(-30,0,64)};{wave(30,0,70)}"/>
  </path>
  <path fill="url(#w1)" opacity="0.55" d="{wave(-24,0,88)}">
    <animate attributeName="d" dur="7s" repeatCount="indefinite" values="{wave(-24,0,88)};{wave(24,0,94)};{wave(-24,0,88)}"/>
  </path>
  <path fill="{BG1}" d="{wave(16,0,112)}">
    <animate attributeName="d" dur="11s" repeatCount="indefinite" values="{wave(16,0,112)};{wave(-16,0,108)};{wave(16,0,112)}"/>
  </path>
  <text x="{W/2}" y="138" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{PINK}">made with ♥ in Tunis · thanks for visiting ✨</text>
</svg>"""


# =====================================================================
# 5. DEVSECOPS PIPELINE (animated packet flowing through stages)
# =====================================================================
def pipeline():
    W, H = 1200, 320
    stages = [
        ("01", "code", "Git", TEXT, False),
        ("02", "build", "Jenkins · GHA", TEXT, False),
        ("03", "SAST", "SonarQube", ROSE, True),
        ("04", "SCA", "OWASP DC", ROSE, True),
        ("05", "scan", "Trivy", ROSE, True),
        ("06", "push", "ECR · Docker", TEXT, False),
        ("07", "sync", "ArgoCD · Helm", CYAN, False),
        ("08", "run", "Kubernetes", CYAN, False),
        ("09", "observe", "Prometheus · Grafana", LILAC, False),
    ]
    x0, x1, y = 80, 1120, 150
    n = len(stages)
    step = (x1 - x0) / (n - 1)
    T = 9.0
    travel = 0.82
    nodes = []
    for i, (num, lab, tool, col, gate) in enumerate(stages):
        x = x0 + i * step
        f = travel * i / (n - 1)
        k = [0, max(f - 0.001, 0), f + 0.015, min(f + 0.13, 0.999), 1]
        if i == 0:
            k = [0, 0.0005, 0.015, 0.13, 1]
        kt = ";".join(f"{v:.4f}" for v in k)
        stroke = ROSE if gate else (CYAN if col == CYAN else LILAC)
        gate_svg = ""
        if gate:
            gate_svg = (f'<g transform="translate({x-26:.1f} {y-74})"><rect width="52" height="18" rx="9" fill="{ROSE}" fill-opacity="0.16" stroke="{ROSE}" stroke-opacity="0.6"/>'
                        f'<text x="26" y="13" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{PINK}">⛨ gate</text></g>')
        nodes.append(f"""
    <g>
      {gate_svg}
      <rect x="{x-38:.1f}" y="{y-38}" width="76" height="76" rx="18" fill="{stroke}" opacity="0.25" filter="url(#pglow)">
        <animate attributeName="opacity" values="0.15;0.15;0.9;0.15;0.15" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/>
      </rect>
      <rect x="{x-36:.1f}" y="{y-36}" width="72" height="72" rx="17" fill="#160a20" stroke="{stroke}" stroke-opacity="0.8" stroke-width="1.6"/>
      <text x="{x:.1f}" y="{y-12}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">{num}</text>
      <text x="{x:.1f}" y="{y+12}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{col if col != TEXT else PINK}">{lab}</text>
      <text x="{x:.1f}" y="{y+64}" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{TEXT}">{escape(tool)}</text>
    </g>""")
    loop = f"M{x1} {y+82} C {x1} {y+130}, {x0} {y+130}, {x0} {y+82}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="DevSecOps pipeline: code, build, SAST, SCA, image scan, push, GitOps sync, run on Kubernetes, observe">
  <defs>
    <linearGradient id="pbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#140920"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
    {holo_gradient("pholo", "5s", W)}
    <filter id="pglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
    <filter id="dotglow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="pclip"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  </defs>
  <g clip-path="url(#pclip)">
    <rect width="{W}" height="{H}" fill="url(#pbg)"/>
    <text x="32" y="40" font-family="{MONO}" font-size="13" letter-spacing="2.5" fill="{ROSE}">$ git push origin main</text>
    <text x="{W-32}" y="40" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTED}">security gates at every stage · zero manual deploys</text>
    <line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{LILAC}" stroke-opacity="0.25" stroke-width="2"/>
    <line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="url(#pholo)" stroke-width="2.5" stroke-dasharray="8 10">
      <animate attributeName="stroke-dashoffset" from="0" to="-180" dur="3s" repeatCount="indefinite"/>
    </line>
    <path d="{loop}" fill="none" stroke="{LILAC}" stroke-opacity="0.45" stroke-width="1.5" stroke-dasharray="4 6">
      <animate attributeName="stroke-dashoffset" from="0" to="60" dur="3s" repeatCount="indefinite"/>
    </path>
    <text x="{W/2}" y="{y+150}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">↺ feedback loop · metrics &amp; alerts drive the next commit</text>
    {''.join(nodes)}
    <circle r="7" fill="#fff" filter="url(#dotglow)">
      <animate attributeName="cx" values="{x0};{x1};{x1};{x0}" keyTimes="0;{travel};0.97;1" dur="{T}s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="{y};{y};{y};{y}" dur="{T}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{travel};{travel+0.02};1" dur="{T}s" repeatCount="indefinite"/>
      <animate attributeName="fill" values="#ffffff;{ROSE};{CYAN};{LILAC}" keyTimes="0;0.3;0.6;{travel}" dur="{T}s" repeatCount="indefinite"/>
    </circle>
  </g>
  <rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="20" fill="none" stroke="url(#pholo)" stroke-opacity="0.6" stroke-width="1.5"/>
</svg>"""


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    write("header.svg", header())
    write("terminal.svg", terminal())
    write("divider.svg", divider())
    write("footer.svg", footer())
    write("pipeline.svg", pipeline())
    for slug, sub, text in [
        ("about", "01 // about", "About me"),
        ("pipeline", "02 // how i ship", "Secure by default"),
        ("experience", "03 // experience", "Where I've shipped"),
        ("stack", "04 // stack", "Tech stack"),
        ("projects", "05 // projects", "Featured projects"),
        ("certs", "06 // certifications", "Certifications"),
        ("wins", "07 // highlights", "Wins & community"),
        ("stats", "08 // activity", "GitHub activity"),
        ("contact", "09 // contact", "Let's connect"),
    ]:
        write(f"title-{slug}.svg", section_title(slug, None, text, sub))
    for p in PROJECTS:
        project_card(*p)
    print("assets written to", OUT)
