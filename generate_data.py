#!/usr/bin/env python3
"""
Generates data/assets.json — 50 content-creator broadcast asset metadata records.
No copyrighted assets are referenced or reproduced. Preview thumbnails are
procedurally generated SVGs (see generate_previews.py) based on each entry's
own palette/style metadata.
"""
import json
import random

random.seed(1604)

CATEGORIES = ["overlay", "transition", "lower-third", "alert", "panel", "intro-outro", "font"]

PLATFORMS = ["Twitch", "YouTube", "TikTok", "Kick"]

STYLE_TAGS_POOL = [
    "cyberpunk", "minimalist", "retro-vhs", "anime", "corporate", "glitchcore",
    "pixel-art", "neon-noir", "pastel-kawaii", "esports-aggressive", "cozy-stream",
    "horror-stream", "vaporwave", "clean-tech", "handdrawn"
]

ANIMATION_TYPES = ["fade", "slide", "glitch", "particle-burst", "wipe", "zoom-punch", "static"]

# (name, category, description, use_case) tuples — hand-authored, no scraped/third-party content
ASSET_SEEDS = [
    ("Neon Grid Stream Frame", "overlay", "Full-frame border overlay with a pulsing neon grid line along the bottom third", "Main gameplay overlay border for FPS/competitive streams"),
    ("Purple Shadow Impact Font Kit", "font", "Bold condensed sans typeface preset with a hard purple drop-shadow and thin white outline, comic-impact styling", "Highlight text for clip montages and reaction moments"),
    ("Glitch Wipe Scene Transition", "transition", "Horizontal RGB-split glitch wipe used to cut between 'Just Chatting' and 'Gameplay' scenes", "Scene switch transition"),
    ("Cyberpunk HUD Lower Third", "lower-third", "Angular lower-third name plate with scanline texture and a single accent stripe", "Guest/host name display during interviews or co-op streams"),
    ("Retro CRT Follow Alert", "alert", "New-follower alert styled as an old CRT boot-up sequence with static roll-in", "Follower/subscriber alert box"),
    ("Minimalist Chat Panel", "panel", "Flat, low-contrast panel frame for embedding chat overlay on-screen", "On-stream chat visibility panel"),
    ("Anime Sparkle Intro Sting", "intro-outro", "Short sting with sparkle particle burst and hand-drawn motion lines revealing the channel logo", "Stream start intro sting"),
    ("Esports Bracket Panel", "panel", "Data-dense panel template for displaying tournament bracket standings", "Tournament/bracket stream overlay"),
    ("VHS Rewind Outro", "intro-outro", "Outro sequence styled like a VHS rewind with tracking distortion lines", "End-of-stream outro"),
    ("Pixel Heart Donation Alert", "alert", "8-bit pixel-art heart animation triggered on donation events", "Donation/tip alert"),
    ("Cozy Pastel Webcam Frame", "overlay", "Soft rounded webcam border with floating pastel particles", "Webcam frame for cozy/variety streams"),
    ("Horror Static Jumpscare Transition", "transition", "Sudden static burst transition with a low screech cue point marker (audio not included)", "Horror game scene transition"),
    ("Vaporwave Sunset Panel Set", "panel", "Panel set with gradient sunset backdrop and grid-floor motif", "Social/about-me panels below stream"),
    ("Clean Tech Sans Font Kit", "font", "Geometric sans with subtle glow and 2px stroke, no shadow", "Titles for tech/coding streams"),
    ("Esports Aggressive Slash Transition", "transition", "Diagonal slash-cut transition with motion blur, tuned for fast FPS pacing", "Kill-cam or highlight-reel scene cut"),
    ("Handdrawn Doodle Border Overlay", "overlay", "Sketchy hand-drawn border frame with animated doodle accents in corners", "Art/drawing stream overlay border"),
    ("Neon Noir Subscriber Alert", "alert", "Rain-on-glass neon sign style subscriber alert with slow fade-in", "Subscriber alert box"),
    ("Corporate Clean Lower Third", "lower-third", "Flat-fill lower third with a single thin rule line, no shadow or glow", "Product demo / corporate livestream name plate"),
    ("Glitchcore Raid Alert", "alert", "Aggressive RGB-split glitch alert for incoming raids", "Raid alert box"),
    ("Kawaii Sticker Panel Set", "panel", "Rounded sticker-style panels with bounce-in animation", "Info panels for cozy/anime streams"),
    ("Retro VHS Scene Frame", "overlay", "Full overlay with tracking lines, timestamp burn-in, and film grain", "Retro-aesthetic gameplay overlay"),
    ("Pixel Font Kit — Arcade", "font", "8-bit bitmap font preset with hard drop shadow, no anti-aliasing", "Retro/pixel game stream titles"),
    ("Minimalist Wipe Transition", "transition", "Single flat-color wipe with easing, no particles or glow", "General-purpose scene transition"),
    ("Cyberpunk Cheer Alert", "alert", "Bit-cheer alert with holographic shimmer and Japanese-inspired kana accents", "Bits/cheer alert box"),
    ("Anime Chibi Follow Alert", "alert", "Chibi-style character pop-in animation on new follow", "Follower alert box"),
    ("Corporate Intro Sting", "intro-outro", "Clean logo reveal sting with subtle particle shimmer", "Stream/webinar start sting"),
    ("Neon Grid Lower Third", "lower-third", "Matches Neon Grid Stream Frame overlay; angular name plate with grid accent", "Co-branded name plate for Neon Grid overlay set"),
    ("Glitch Font Kit — Terminal", "font", "Monospace terminal font preset with occasional glitch-flicker keyframes", "Coding/hacking-themed stream titles"),
    ("Esports Scoreboard Panel", "panel", "Live scoreboard panel template with team color slots", "1v1/competitive match overlay"),
    ("Cozy Rain Window Overlay", "overlay", "Ambient rain-on-window overlay for corner-of-screen decoration", "Ambient/cozy stream decoration"),
    ("VHS Static Alert — Sub Goal", "alert", "Progress-bar sub goal alert with VHS static fill animation", "Subscriber goal tracker"),
    ("Pastel Kawaii Intro Sting", "intro-outro", "Bouncy pastel logo intro with confetti particle pop", "Stream start intro sting"),
    ("Hacker Green Terminal Overlay", "overlay", "Full-frame overlay styled as a green-on-black terminal window border", "Coding/hacking-themed stream overlay"),
    ("Neon Noir Transition — Rain Wipe", "transition", "Vertical rain-streak wipe transition with neon reflection", "Neon-noir themed scene transition"),
    ("Handdrawn Marker Font Kit", "font", "Sketchy marker-style font with slight jitter animation on reveal", "Art stream titles and callouts"),
    ("Esports Aggressive Kill Alert", "alert", "Fast zoom-punch alert for in-game kill/highlight moments (manual trigger)", "Manual highlight/hype alert"),
    ("Cute Cloud Chat Panel", "panel", "Rounded cloud-shaped chat embed panel with soft drop shadow", "Chat panel for cozy/variety streams"),
    ("Retro Arcade Cabinet Frame Overlay", "overlay", "Overlay styled as an arcade cabinet bezel around the gameplay capture", "Retro/arcade game stream overlay"),
    ("Corporate Panel Set — Info Grid", "panel", "Grid-aligned info panel set (schedule, socials, rules) in flat corporate style", "Standard info panel row below stream"),
    ("Vaporwave Grid Lower Third", "lower-third", "Lower third with checkerboard-grid backdrop and gradient text fill", "Name plate for vaporwave-themed streams"),
    ("Glitchcore Scene Wipe", "transition", "Full-glitch scene wipe with datamosh-style block artifacts", "High-energy scene transition"),
    ("Anime Petal Outro", "intro-outro", "Falling cherry-blossom petal outro with soft fade to end card", "End-of-stream outro"),
    ("Minimalist Font Kit — Neutral Sans", "font", "Clean neutral sans with no effects, adjustable weight only", "General-purpose titles, subtitle-safe"),
    ("Neon Cheer Progress Panel", "panel", "Bits/cheer progress panel with neon fill bar", "Bits goal tracker panel"),
    ("Horror Vignette Overlay", "overlay", "Dark vignette overlay with slow pulsing edge, no jump effects", "Horror/atmospheric game overlay"),
    ("Pixel Raid Alert", "alert", "8-bit pixel raid train alert with marching sprite animation", "Raid alert box"),
    ("Cozy Fireplace Corner Overlay", "overlay", "Looping animated fireplace decoration for screen corner", "Ambient decoration for chatting/cozy streams"),
    ("Esports Zoom Punch Transition", "transition", "Hard zoom-punch transition with screen-shake, tuned for hype moments", "Highlight/hype scene transition"),
    ("Terminal Font Kit — Glitch Mono", "font", "Monospace font preset with periodic single-character glitch swap", "Cyberpunk/hacking stream titles"),
    ("Kawaii Star Follow Alert", "alert", "Star-burst pop-in follow alert with bounce easing", "Follower alert box"),
]

assert len(ASSET_SEEDS) == 50, f"expected 50 seeds, got {len(ASSET_SEEDS)}"

# Curated palettes per aesthetic keyword so colors stay coherent with each entry's style
PALETTE_BY_STYLE = {
    "cyberpunk": ["#0D0221", "#FF2E88", "#00E5FF", "#F5D300"],
    "minimalist": ["#F5F5F5", "#1A1A1A", "#8C8C8C", "#3D5AFE"],
    "retro-vhs": ["#1B1035", "#FF4FA0", "#3EDBF0", "#F7F2E7"],
    "anime": ["#FFE1F0", "#FF6FA5", "#7A5CFA", "#FFFFFF"],
    "corporate": ["#0B2545", "#134074", "#8DA9C4", "#EEF4ED"],
    "glitchcore": ["#0A0A0A", "#FF003C", "#00FFF0", "#FFFFFF"],
    "pixel-art": ["#212042", "#E84855", "#3185FC", "#F9DC5C"],
    "neon-noir": ["#0A0F1E", "#E100FF", "#00FFC6", "#1A1F3D"],
    "pastel-kawaii": ["#FFF0F5", "#FFB6D9", "#B5EAD7", "#C7CEEA"],
    "esports-aggressive": ["#0D0D0D", "#FF1E1E", "#FFFFFF", "#3D3D3D"],
    "cozy-stream": ["#FFF4E6", "#F4A259", "#5B8C5A", "#3A3335"],
    "horror-stream": ["#0A0000", "#4A0404", "#8C1C13", "#D9D9D9"],
    "vaporwave": ["#2B1055", "#FF71CE", "#01CDFE", "#05FFA1"],
    "clean-tech": ["#0F172A", "#38BDF8", "#E2E8F0", "#1E293B"],
    "handdrawn": ["#FAF3E0", "#3E2723", "#D8A47F", "#8D6A9F"],
    "purple-shadow": ["#120021", "#7B2FF7", "#C77DFF", "#FFFFFF"],
}

KEYWORD_STYLE_MAP = [
    ("purple shadow", "purple-shadow"),
    ("cyberpunk", "cyberpunk"),
    ("neon grid", "cyberpunk"),
    ("hud", "cyberpunk"),
    ("glitch", "glitchcore"),
    ("vhs", "retro-vhs"),
    ("retro", "retro-vhs"),
    ("anime", "anime"),
    ("chibi", "anime"),
    ("corporate", "corporate"),
    ("pixel", "pixel-art"),
    ("arcade", "pixel-art"),
    ("8-bit", "pixel-art"),
    ("neon noir", "neon-noir"),
    ("noir", "neon-noir"),
    ("pastel", "pastel-kawaii"),
    ("kawaii", "pastel-kawaii"),
    ("cute", "pastel-kawaii"),
    ("sticker", "pastel-kawaii"),
    ("star", "pastel-kawaii"),
    ("esports", "esports-aggressive"),
    ("aggressive", "esports-aggressive"),
    ("scoreboard", "esports-aggressive"),
    ("cozy", "cozy-stream"),
    ("fireplace", "cozy-stream"),
    ("horror", "horror-stream"),
    ("vignette", "horror-stream"),
    ("vaporwave", "vaporwave"),
    ("hacker", "clean-tech"),
    ("terminal", "clean-tech"),
    ("tech", "clean-tech"),
    ("hand-drawn", "handdrawn"),
    ("handdrawn", "handdrawn"),
    ("doodle", "handdrawn"),
    ("marker", "handdrawn"),
    ("minimalist", "minimalist"),
    ("neutral", "minimalist"),
]

def style_for(name, seed_index):
    name_l = name.lower()
    for keyword, style in KEYWORD_STYLE_MAP:
        if keyword in name_l:
            return style
    return STYLE_TAGS_POOL[seed_index % len(STYLE_TAGS_POOL)]

FONT_FAMILIES = [
    "Bold Condensed Sans", "Geometric Sans", "Bitmap 8px", "Monospace Terminal",
    "Rounded Display", "Serif Display", "Handwritten Marker", "Grotesk Sans",
]

EFFECT_NOTES_POOL = [
    "hard drop-shadow, no blur", "soft glow, 8px blur radius", "2px stroke outline, no shadow",
    "RGB channel split on reveal", "flat fill, no effects", "jitter animation on hover",
    "gradient fill top-to-bottom", "scanline overlay texture",
]

def make_entry(i, seed):
    name, category, description, use_case = seed
    style = style_for(name, i)
    palette = PALETTE_BY_STYLE.get(style, PALETTE_BY_STYLE["minimalist"])
    platforms = sorted(random.sample(PLATFORMS, k=random.choice([1, 2, 2, 3])))
    animation_type = random.choice(ANIMATION_TYPES) if category != "font" else "static"
    font_family = random.choice(FONT_FAMILIES)
    effect_notes = random.choice(EFFECT_NOTES_POOL)
    # retention_tier is an ILLUSTRATIVE annotation for portfolio/demo purposes only —
    # not derived from real analytics data. Clearly documented as such in README.
    retention_tier = random.choices(["High", "Medium", "Low"], weights=[0.35, 0.45, 0.20])[0]
    retention_rationale = {
        "High": "Fast, legible reveal (<1.2s) and high contrast against typical gameplay footage",
        "Medium": "Readable but animation length may compete with fast-paced gameplay moments",
        "Low": "Dense detail or slow reveal risks being skipped/ignored during high-action segments",
    }[retention_tier]

    return {
        "id": i + 1,
        "name": name,
        "category": category,
        "style_tags": sorted(set([style] + random.sample(STYLE_TAGS_POOL, k=1))),
        "platforms": platforms,
        "color_palette": palette,
        "font_family": font_family if category in ("font", "lower-third", "alert") else None,
        "effect_notes": effect_notes,
        "animation_type": animation_type,
        "use_case": use_case,
        "description": description,
        "retention_tier": retention_tier,
        "retention_rationale": retention_rationale,
        "preview_image": f"assets/previews/{i + 1:03d}.svg",
    }

def main():
    data = [make_entry(i, seed) for i, seed in enumerate(ASSET_SEEDS)]
    with open("data/assets.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {len(data)} entries to data/assets.json")

if __name__ == "__main__":
    main()
