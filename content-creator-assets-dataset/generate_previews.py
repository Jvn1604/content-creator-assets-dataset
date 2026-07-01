#!/usr/bin/env python3
"""
Generates one original SVG preview per entry in data/assets.json.
Previews are abstract, procedurally-composed graphics built only from each
entry's own metadata (palette, category, animation_type) — no third-party
or copyrighted artwork is used or referenced.
"""
import json
import random

with open("data/assets.json") as f:
    ENTRIES = json.load(f)

W, H = 320, 180

CATEGORY_GLYPH = {
    "overlay": "square-frame",
    "transition": "diagonal-wipe",
    "lower-third": "bottom-bar",
    "alert": "burst",
    "panel": "stacked-blocks",
    "intro-outro": "concentric",
    "font": "glyph-stack",
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def svg_header(bg):
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">' \
           f'<rect width="{W}" height="{H}" fill="{bg}"/>'

def scanlines(color, opacity=0.06):
    lines = []
    y = 0
    while y < H:
        lines.append(f'<rect x="0" y="{y}" width="{W}" height="1" fill="{color}" opacity="{opacity}"/>')
        y += 4
    return "".join(lines)

def monitor_chrome(accent):
    # tiny broadcast-monitor bezel detail: rec dot + corner ticks
    return (
        f'<circle cx="14" cy="14" r="4" fill="{accent}"/>'
        f'<circle cx="14" cy="14" r="4" fill="{accent}" opacity="0.5">'
        f'<animate attributeName="r" values="4;7;4" dur="2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.5;0;0.5" dur="2s" repeatCount="indefinite"/>'
        f'</circle>'
        f'<path d="M {W-20} 8 h 12 v 12" stroke="{accent}" stroke-width="1.5" fill="none" opacity="0.7"/>'
        f'<path d="M {W-20} {H-8} h 12 v -12" stroke="{accent}" stroke-width="1.5" fill="none" opacity="0.7"/>'
    )

def glyph_square_frame(palette, animation_type):
    bg, a, b, c = palette
    inset = 24
    return (
        f'<rect x="{inset}" y="{inset}" width="{W-2*inset}" height="{H-2*inset}" '
        f'fill="none" stroke="{a}" stroke-width="3"/>'
        f'<rect x="{inset+6}" y="{inset+6}" width="{W-2*inset-12}" height="{H-2*inset-12}" '
        f'fill="none" stroke="{b}" stroke-width="1" opacity="0.5"/>'
        f'<line x1="{inset}" y1="{H-inset}" x2="{W-inset}" y2="{H-inset}" stroke="{c}" stroke-width="4"/>'
    )

def glyph_diagonal_wipe(palette, animation_type):
    bg, a, b, c = palette
    return (
        f'<polygon points="0,0 {W*0.6},0 {W*0.35},{H} 0,{H}" fill="{a}" opacity="0.9"/>'
        f'<polygon points="{W*0.55},0 {W},0 {W},{H} {W*0.3},{H}" fill="{b}" opacity="0.55"/>'
        f'<line x1="{W*0.6}" y1="0" x2="{W*0.35}" y2="{H}" stroke="{c}" stroke-width="2"/>'
    )

def glyph_bottom_bar(palette, animation_type):
    bg, a, b, c = palette
    bar_y = H - 46
    return (
        f'<rect x="18" y="{bar_y}" width="{W-36}" height="30" fill="{a}"/>'
        f'<rect x="18" y="{bar_y}" width="60" height="30" fill="{c}"/>'
        f'<rect x="18" y="{bar_y-4}" width="{W-36}" height="2" fill="{b}"/>'
        f'<rect x="30" y="{bar_y+10}" width="120" height="8" rx="2" fill="{bg}" opacity="0.85"/>'
    )

def glyph_burst(palette, animation_type):
    bg, a, b, c = palette
    cx, cy = W/2, H/2
    rays = []
    for i in range(10):
        import math
        ang = (i / 10) * 2 * math.pi
        x2 = cx + math.cos(ang) * 70
        y2 = cy + math.sin(ang) * 70
        rays.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{a}" stroke-width="3" opacity="0.7"/>')
    return "".join(rays) + f'<circle cx="{cx}" cy="{cy}" r="26" fill="{b}"/><circle cx="{cx}" cy="{cy}" r="26" fill="none" stroke="{c}" stroke-width="2"/>'

def glyph_stacked_blocks(palette, animation_type):
    bg, a, b, c = palette
    blocks = []
    colors = [a, b, c]
    for i in range(3):
        y = 30 + i * 42
        blocks.append(f'<rect x="24" y="{y}" width="{W-48}" height="30" rx="6" fill="{colors[i % 3]}" opacity="0.85"/>')
    return "".join(blocks)

def glyph_concentric(palette, animation_type):
    bg, a, b, c = palette
    cx, cy = W/2, H/2
    return (
        f'<circle cx="{cx}" cy="{cy}" r="60" fill="none" stroke="{a}" stroke-width="2" opacity="0.8"/>'
        f'<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{b}" stroke-width="2" opacity="0.8"/>'
        f'<circle cx="{cx}" cy="{cy}" r="20" fill="{c}" opacity="0.9"/>'
    )

def glyph_glyph_stack(palette, animation_type):
    bg, a, b, c = palette
    return (
        f'<text x="50%" y="54%" text-anchor="middle" font-family="Georgia, serif" '
        f'font-size="64" font-weight="700" fill="{a}" stroke="{c}" stroke-width="1">Aa</text>'
        f'<text x="50%" y="80%" text-anchor="middle" font-family="monospace" '
        f'font-size="14" letter-spacing="4" fill="{b}" opacity="0.8">ABCDEFG</text>'
    )

GLYPH_FN = {
    "square-frame": glyph_square_frame,
    "diagonal-wipe": glyph_diagonal_wipe,
    "bottom-bar": glyph_bottom_bar,
    "burst": glyph_burst,
    "stacked-blocks": glyph_stacked_blocks,
    "concentric": glyph_concentric,
    "glyph-stack": glyph_glyph_stack,
}

def build_svg(entry):
    palette = entry["color_palette"]
    bg = palette[0]
    accent = palette[2] if len(palette) > 2 else palette[1]
    glyph_key = CATEGORY_GLYPH.get(entry["category"], "square-frame")
    body = GLYPH_FN[glyph_key](palette, entry["animation_type"])
    label = esc(entry["category"].upper())
    parts = [
        svg_header(bg),
        body,
        scanlines("#FFFFFF", 0.04),
        monitor_chrome(accent),
        f'<text x="{W-14}" y="{H-14}" text-anchor="end" font-family="monospace" '
        f'font-size="10" letter-spacing="2" fill="{accent}" opacity="0.85">{label}</text>',
        "</svg>",
    ]
    return "".join(parts)

def main():
    for entry in ENTRIES:
        svg = build_svg(entry)
        path = entry["preview_image"]
        with open(path, "w") as f:
            f.write(svg)
    print(f"Wrote {len(ENTRIES)} preview SVGs to assets/previews/")

if __name__ == "__main__":
    main()
