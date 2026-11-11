#!/usr/bin/env python3
"""Original cat characters + icons for the trust-law deck. Writes SVG files to assets/."""
import sys, pathlib

OUT = pathlib.Path(sys.argv[1])
INK = "#3b2f55"      # outline colour (deep purple, matches the reference slide)
PINK = "#f4a6b7"
FONT = "'Noto Sans TC','Microsoft JhengHei','PingFang TC',sans-serif"

# ---------------------------------------------------------------- base cat
def cat(fur="#f2a65a", belly="#fff1e0", eye="#2b2b3a", stripes=True, tail=True,
        face_patch=None, inner_ear=PINK, pupil_glow=False):
    """Returns SVG group markup of a sitting front-facing cat in a 240x260 box."""
    s = []
    if tail:
        s.append(f'<path d="M168 214 C 222 214, 232 160, 205 140" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>')
        s.append(f'<path d="M168 214 C 222 214, 232 160, 205 140" fill="none" stroke="{fur}" stroke-width="15" stroke-linecap="round"/>')
    # body
    s.append(f'<ellipse cx="120" cy="190" rx="54" ry="50" fill="{fur}" stroke="{INK}" stroke-width="3.5"/>')
    s.append(f'<ellipse cx="120" cy="202" rx="30" ry="30" fill="{belly}"/>')
    # feet
    for cx in (92, 148):
        s.append(f'<ellipse cx="{cx}" cy="236" rx="19" ry="11" fill="{fur}" stroke="{INK}" stroke-width="3.5"/>')
        s.append(f'<path d="M{cx-6} 238 v-6 M{cx+1} 239 v-7 M{cx+8} 238 v-6" stroke="{INK}" stroke-width="2" stroke-linecap="round" fill="none" opacity=".55"/>')
    # ears
    s.append(f'<polygon points="64,86 66,26 112,60" fill="{fur}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    s.append(f'<polygon points="176,86 174,26 128,60" fill="{fur}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    s.append(f'<polygon points="75,72 77,42 98,58" fill="{inner_ear}"/>')
    s.append(f'<polygon points="165,72 163,42 142,58" fill="{inner_ear}"/>')
    # head
    s.append(f'<ellipse cx="120" cy="108" rx="62" ry="52" fill="{fur}" stroke="{INK}" stroke-width="3.5"/>')
    if face_patch:
        s.append(f'<path d="M120 60 C 96 62 88 92 96 130 C 108 150 132 150 144 130 C 152 92 144 62 120 60 Z" fill="{face_patch}"/>')
    if stripes:
        s.append(f'<path d="M120 58 v16 M106 61 l3 13 M134 61 l-3 13" stroke="{INK}" stroke-width="3" stroke-linecap="round" fill="none" opacity=".55"/>')
    # eyes
    for cx in (96, 144):
        s.append(f'<ellipse cx="{cx}" cy="108" rx="8" ry="10" fill="{eye}"/>')
        s.append(f'<circle cx="{cx+2.5}" cy="104" r="3" fill="#fff"/>')
        s.append(f'<circle cx="{cx-2}" cy="112" r="1.4" fill="#fff" opacity=".8"/>')
    # cheeks, nose, mouth, whiskers
    s.append(f'<ellipse cx="78" cy="128" rx="10" ry="6" fill="{PINK}" opacity=".55"/>')
    s.append(f'<ellipse cx="162" cy="128" rx="10" ry="6" fill="{PINK}" opacity=".55"/>')
    s.append(f'<polygon points="114,122 126,122 120,130" fill="#e5798f" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>')
    s.append(f'<path d="M120 130 q0 8 -9 9 M120 130 q0 8 9 9" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>')
    s.append(f'<path d="M72 124 L34 117 M72 132 L34 135 M168 124 L206 117 M168 132 L206 135" stroke="{INK}" stroke-width="2.2" stroke-linecap="round" opacity=".7"/>')
    return "\n".join(s)

# ---------------------------------------------------------------- accessories
def settlor_acc():          # 委託人貓：藍圍巾＋錢袋
    return f'''
<path d="M70 150 Q120 176 170 150 L168 168 Q120 192 72 168 Z" fill="#3b6fd4" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
<path d="M140 176 l12 38 l-18 5 l-8 -34 z" fill="#3b6fd4" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
<path d="M146 186 l6 -2 M148 196 l6 -2" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".7"/>
<g transform="translate(176 232)">
  <path d="M0 0 C -22 -2 -26 -26 -12 -38 L12 -38 C 26 -26 22 -2 0 0 Z" fill="#d9b25a" stroke="{INK}" stroke-width="3"/>
  <path d="M-11 -38 q11 -12 22 0" fill="#d9b25a" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
  <path d="M-10 -35 h20" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
  <text x="0" y="-12" font-size="19" font-weight="700" text-anchor="middle" fill="{INK}" font-family="{FONT}">$</text>
</g>'''

def trustee_acc():          # 受託人貓：圓眼鏡＋領帶＋公事包
    return f'''
<circle cx="96" cy="108" r="17" fill="#ffffff" fill-opacity=".35" stroke="{INK}" stroke-width="3.2"/>
<circle cx="144" cy="108" r="17" fill="#ffffff" fill-opacity=".35" stroke="{INK}" stroke-width="3.2"/>
<path d="M113 106 q7 -5 14 0" fill="none" stroke="{INK}" stroke-width="3.2"/>
<path d="M79 104 L62 98 M161 104 L178 98" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
<path d="M104 152 L136 152 L128 160 L112 160 Z" fill="#fff" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M114 160 h12 l5 14 l-11 24 l-11 -24 z" fill="#d64545" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
<path d="M114 160 h12 l-2 8 h-8 z" fill="#b53232"/>
<g transform="translate(176 238)">
  <rect x="-24" y="-30" width="48" height="30" rx="6" fill="#8a5a3c" stroke="{INK}" stroke-width="3"/>
  <path d="M-9 -30 v-7 q0 -4 4 -4 h10 q4 0 4 4 v7" fill="none" stroke="{INK}" stroke-width="3"/>
  <rect x="-5" y="-18" width="10" height="9" rx="2" fill="#e6c36a" stroke="{INK}" stroke-width="2"/>
</g>'''

def beneficiary_acc():      # 受益人貓：蝴蝶結＋小魚＋閃光
    return f'''
<g transform="translate(86 56)">
  <path d="M0 0 l-20 -12 v24 z M0 0 l20 -12 v24 z" fill="#2e9e6b" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
  <circle r="6" fill="#58c796" stroke="{INK}" stroke-width="3"/>
</g>
<g transform="translate(178 214) rotate(-18)">
  <ellipse cx="0" cy="0" rx="26" ry="14" fill="#6ec6d9" stroke="{INK}" stroke-width="3"/>
  <polygon points="22,0 40,-13 40,13" fill="#6ec6d9" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
  <circle cx="-14" cy="-3" r="3" fill="{INK}"/>
  <path d="M-4 -9 q4 9 0 18 M6 -8 q4 8 0 16" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".8"/>
</g>
<g fill="#ffd24a" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round">
  <path d="M30 70 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4 z"/>
  <path d="M206 64 l3 8 l8 3 l-8 3 l-3 8 l-3 -8 l-8 -3 l8 -3 z"/>
</g>'''

def supervisor_acc():       # 信託監察人貓：放大鏡＋綠色徽章
    return f'''
<path d="M120 164 l8 -2 l5 11 l-8 6 l-10 0 l-6 -6 l5 -11 z" fill="none"/>
<circle cx="120" cy="170" r="14" fill="#2e9e6b" stroke="{INK}" stroke-width="3"/>
<path d="M120 161 l3 6 l7 1 l-5 5 l1 7 l-6 -3 l-6 3 l1 -7 l-5 -5 l7 -1 z" fill="#fff" stroke="none"/>
<g transform="translate(62 192) scale(-1 1)">
  <path d="M14 14 L40 42" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>
  <path d="M14 14 L40 42" stroke="#8a5a3c" stroke-width="6" stroke-linecap="round"/>
  <circle r="24" fill="#cfe9ff" fill-opacity=".55" stroke="{INK}" stroke-width="4"/>
  <circle r="24" fill="none" stroke="#e6c36a" stroke-width="2" transform="scale(.82)"/>
  <path d="M-12 -8 q4 -8 12 -9" stroke="#fff" stroke-width="3.5" stroke-linecap="round" fill="none"/>
</g>'''

def professor_acc():        # 教授貓：學士帽＋蝴蝶領結＋教鞭
    return f'''
<path d="M88 66 L120 50 L152 66 L120 82 Z" fill="#4b3f8f" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
<path d="M100 74 v10 q20 10 40 0 v-10" fill="#3a3070" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
<path d="M152 66 L158 94" stroke="#ffd24a" stroke-width="3" stroke-linecap="round"/>
<circle cx="158" cy="97" r="4.5" fill="#ffd24a" stroke="{INK}" stroke-width="2"/>
<path d="M120 164 l-20 -10 v20 z M120 164 l20 -10 v20 z" fill="#d64545" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
<circle cx="120" cy="164" r="6" fill="#b53232" stroke="{INK}" stroke-width="2.5"/>
<g transform="translate(64 214) scale(-1 1)">
  <path d="M0 8 L36 -52" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
  <path d="M0 8 L36 -52" stroke="#e6c36a" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="37" cy="-54" r="6" fill="#d64545" stroke="{INK}" stroke-width="2.5"/>
</g>'''

CHARACTERS = {
    # file name: (label, cat kwargs, accessory fn)
    "cat_settlor":     ("委託人貓", dict(fur="#f2a65a", belly="#fff1e0"), settlor_acc),
    "cat_trustee":     ("受託人貓", dict(fur="#a9b4c8", belly="#eef1f7", stripes=True), trustee_acc),
    "cat_beneficiary": ("受益人貓", dict(fur="#fff4e6", belly="#ffffff", stripes=False), beneficiary_acc),
    "cat_supervisor":  ("信託監察人貓", dict(fur="#4a4560", belly="#ffffff", eye="#ffd24a", stripes=False,
                                        inner_ear="#c58aa0"), supervisor_acc),
    "cat_professor":   ("教授貓", dict(fur="#f2a65a", belly="#fff1e0", face_patch="#fff1e0"), professor_acc),
}

def svg_wrap(inner, w=240, h=260, title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}">\n'
            f'<title>{title}</title>\n{inner}\n</svg>\n')

def character_group(key):
    label, kw, acc = CHARACTERS[key]
    inner = cat(**kw)
    a = acc()
    # supervisor/professor: accessories that overlay head go after; all accessories go after cat
    return inner + "\n" + a

# ---------------------------------------------------------------- icons
ICONS = {}
ICONS["icon_vault"] = ("信託財產金庫", 200, 180, f'''
<rect x="26" y="52" width="148" height="104" rx="14" fill="#6c63c9" stroke="{INK}" stroke-width="4"/>
<path d="M26 82 h148" stroke="{INK}" stroke-width="4"/>
<path d="M26 66 C 26 30 174 30 174 66 Z" fill="#8a82e0" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
<circle cx="100" cy="112" r="26" fill="#ffd24a" stroke="{INK}" stroke-width="4"/>
<circle cx="100" cy="106" r="7" fill="{INK}"/>
<path d="M96 110 L92 128 H108 L104 110 Z" fill="{INK}"/>
<g fill="#ffd24a" stroke="{INK}" stroke-width="2" stroke-linejoin="round">
  <path d="M168 20 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4 z"/>
  <path d="M22 28 l3 7 l7 3 l-7 3 l-3 7 l-3 -7 l-7 -3 l7 -3 z"/>
</g>''')

ICONS["icon_shield"] = ("信託財產獨立性護盾", 180, 200, f'''
<path d="M90 16 L160 40 V98 C 160 142 126 172 90 186 C 54 172 20 142 20 98 V40 Z" fill="#5b9bea" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>
<path d="M90 30 L146 49 V98 C 146 132 120 156 90 168 Z" fill="#8bb9f5" opacity=".6"/>
<g fill="#fff" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">
  <ellipse cx="90" cy="112" rx="22" ry="19"/>
  <ellipse cx="62" cy="86" rx="9" ry="12" transform="rotate(-18 62 86)"/>
  <ellipse cx="82" cy="72" rx="9" ry="12" transform="rotate(-5 82 72)"/>
  <ellipse cx="102" cy="72" rx="9" ry="12" transform="rotate(5 102 72)"/>
  <ellipse cx="122" cy="86" rx="9" ry="12" transform="rotate(18 122 86)"/>
</g>''')

ICONS["icon_traffic"] = ("行為規範紅綠燈", 140, 220, f'''
<rect x="30" y="10" width="80" height="170" rx="24" fill="#4b3f8f" stroke="{INK}" stroke-width="4.5"/>
<circle cx="70" cy="50" r="19" fill="#d64545" stroke="{INK}" stroke-width="3.5"/>
<circle cx="70" cy="95" r="19" fill="#ffd24a" stroke="{INK}" stroke-width="3.5"/>
<circle cx="70" cy="140" r="19" fill="#2e9e6b" stroke="{INK}" stroke-width="3.5"/>
<path d="M62 42 a10 8 0 0 1 12 -4" stroke="#fff" stroke-width="3" stroke-linecap="round" fill="none" opacity=".8"/>
<rect x="62" y="180" width="16" height="32" rx="4" fill="#6b6590" stroke="{INK}" stroke-width="4"/>''')

ICONS["icon_calendar"] = ("知一做十：除斥期間", 200, 190, f'''
<rect x="18" y="30" width="164" height="140" rx="16" fill="#fff" stroke="{INK}" stroke-width="4.5"/>
<path d="M18 62 V46 a16 16 0 0 1 16 -16 H166 a16 16 0 0 1 16 16 V62 Z" fill="#d64545" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>
<path d="M58 14 v28 M142 14 v28" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
<text x="58" y="124" font-size="44" font-weight="800" text-anchor="middle" fill="#3b6fd4" font-family="{FONT}">1</text>
<text x="142" y="124" font-size="44" font-weight="800" text-anchor="middle" fill="#d64545" font-family="{FONT}">10</text>
<text x="58" y="152" font-size="15" font-weight="700" text-anchor="middle" fill="{INK}" font-family="{FONT}">知悉起</text>
<text x="142" y="152" font-size="15" font-weight="700" text-anchor="middle" fill="{INK}" font-family="{FONT}">成立起</text>
<path d="M100 96 v36" stroke="#cfc9ee" stroke-width="3" stroke-dasharray="4 5"/>''')

ICONS["icon_building"] = ("不動產／資產證券化", 200, 200, f'''
<rect x="52" y="30" width="96" height="150" rx="6" fill="#8a82e0" stroke="{INK}" stroke-width="4.5"/>
<rect x="22" y="84" width="40" height="96" rx="5" fill="#6c63c9" stroke="{INK}" stroke-width="4.5"/>
<rect x="138" y="64" width="40" height="116" rx="5" fill="#6c63c9" stroke="{INK}" stroke-width="4.5"/>
<g fill="#fff6c9" stroke="{INK}" stroke-width="2.5">
  <rect x="66" y="46" width="16" height="14" rx="2"/><rect x="92" y="46" width="16" height="14" rx="2"/><rect x="118" y="46" width="16" height="14" rx="2"/>
  <rect x="66" y="76" width="16" height="14" rx="2"/><rect x="92" y="76" width="16" height="14" rx="2"/><rect x="118" y="76" width="16" height="14" rx="2"/>
  <rect x="66" y="106" width="16" height="14" rx="2"/><rect x="118" y="106" width="16" height="14" rx="2"/>
  <rect x="30" y="100" width="12" height="12" rx="2"/><rect x="46" y="100" width="12" height="12" rx="2"/><rect x="30" y="124" width="12" height="12" rx="2"/><rect x="46" y="124" width="12" height="12" rx="2"/>
  <rect x="146" y="80" width="12" height="12" rx="2"/><rect x="162" y="80" width="12" height="12" rx="2"/><rect x="146" y="104" width="12" height="12" rx="2"/><rect x="162" y="104" width="12" height="12" rx="2"/>
</g>
<rect x="88" y="138" width="24" height="42" rx="4" fill="#ffd24a" stroke="{INK}" stroke-width="3.5"/>
<path d="M10 182 h180" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>''')

ICONS["icon_fish_coin"] = ("魚與錢幣（收益）", 200, 140, f'''
<g transform="translate(70 70) rotate(-10)">
  <ellipse cx="0" cy="0" rx="48" ry="26" fill="#6ec6d9" stroke="{INK}" stroke-width="4"/>
  <polygon points="42,0 78,-26 78,26" fill="#6ec6d9" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
  <circle cx="-26" cy="-5" r="5" fill="{INK}"/><circle cx="-24.5" cy="-6.5" r="1.8" fill="#fff"/>
  <path d="M-8 -16 q8 16 0 32 M10 -14 q8 14 0 28" stroke="#fff" stroke-width="3.5" fill="none" stroke-linecap="round" opacity=".8"/>
</g>
<g transform="translate(150 96)">
  <circle r="30" fill="#ffd24a" stroke="{INK}" stroke-width="4"/>
  <circle r="21" fill="none" stroke="{INK}" stroke-width="2.5" opacity=".55"/>
  <text x="0" y="9" font-size="28" font-weight="800" text-anchor="middle" fill="{INK}" font-family="{FONT}">$</text>
</g>''')

# ---------------------------------------------------------------- scene: trust triangle
def scene_triangle():
    W, H = 880, 420
    def place(key, x, y, sc):
        return f'<g transform="translate({x} {y}) scale({sc})">{character_group(key)}</g>'
    parts = []
    parts.append(f'<rect width="{W}" height="{H}" rx="28" fill="#fbe9dc"/>')
    # ground strip
    parts.append(f'<ellipse cx="{W/2}" cy="392" rx="400" ry="14" fill="#f1d3bd"/>')
    parts += [
        place("cat_settlor", 20, 118, 1.05),
        place("cat_trustee", 316, 118, 1.05),
        place("cat_beneficiary", 612, 118, 1.05).replace('<path d="M30 70 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4 z"/>', ""),
        place("cat_supervisor", 316, -4, 0.52),
    ]
    # arrows with labels
    def arrow(x1, y, x2, color, label, sub):
        return (f'<path d="M{x1} {y} H{x2-14}" stroke="{color}" stroke-width="7" stroke-linecap="round" fill="none"/>'
                f'<polygon points="{x2},{y} {x2-18},{y-12} {x2-18},{y+12}" fill="{color}"/>'
                f'<text x="{(x1+x2)/2}" y="{y-24}" font-size="25" font-weight="800" text-anchor="middle" fill="{INK}" font-family="{FONT}">{label}</text>'
                '')
    parts.append(arrow(258, 250, 330, "#3b6fd4", "移轉財產", "委託人 → 受託人"))
    parts.append(arrow(556, 250, 628, "#2e9e6b", "給付利益", "受託人 → 受益人"))
    # labels under characters
    def lab(x, t, c):
        return (f'<rect x="{x-62}" y="352" width="124" height="34" rx="17" fill="{c}" stroke="{INK}" stroke-width="3"/>'
                f'<text x="{x}" y="376" font-size="22" font-weight="800" text-anchor="middle" fill="#fff" font-family="{FONT}">{t}</text>')
    parts += [lab(140, "委託人", "#3b6fd4"), lab(436, "受託人", "#d64545"), lab(732, "受益人", "#2e9e6b")]
    # supervisor label + dashed watch line
    parts.append(f'<text x="462" y="52" font-size="25" font-weight="800" fill="{INK}" font-family="{FONT}">信託監察人</text>')
    parts.append(f'<text x="462" y="82" font-size="19" fill="#6b6590" font-family="{FONT}">以自己名義監督，保障受益人</text>')
    return svg_wrap("\n".join(parts), W, H, "信託三方關係：委託人、受託人、受益人與信託監察人")

def scene_title():
    W, H = 880, 330
    parts = [f'<rect width="{W}" height="{H}" rx="28" fill="#fbe9dc"/>']
    parts.append(f'<g transform="translate(40 40) scale(1.0)">{character_group("cat_professor")}</g>')
    parts.append(f'<g transform="translate(250 90) scale(.62)">{character_group("cat_settlor")}</g>')
    parts.append(f'<g transform="translate(410 90) scale(.62)">{character_group("cat_trustee")}</g>')
    parts.append(f'<g transform="translate(570 90) scale(.62)">{character_group("cat_beneficiary")}</g>')
    parts.append(f'<g transform="translate(720 90) scale(.62)">{character_group("cat_supervisor")}</g>')
    parts.append(f'<ellipse cx="440" cy="298" rx="400" ry="12" fill="#f1d3bd"/>')
    return svg_wrap("\n".join(parts), W, H, "貓咪角色全員")

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for key, (label, kw, acc) in CHARACTERS.items():
        (OUT / f"{key}.svg").write_text(svg_wrap(character_group(key), 240, 260, label), encoding="utf-8")
    for key, (label, w, h, inner) in ICONS.items():
        (OUT / f"{key}.svg").write_text(svg_wrap(inner, w, h, label), encoding="utf-8")
    (OUT / "scene_trust_triangle.svg").write_text(scene_triangle(), encoding="utf-8")
    (OUT / "scene_cast.svg").write_text(scene_title(), encoding="utf-8")
    print("wrote", len(list(OUT.glob('*.svg'))), "svgs")

if __name__ == "__main__":
    main()
