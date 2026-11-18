#!/usr/bin/env python3
"""Build entry.png — a one-image summary of world news, Wednesday 18 November 2026.

Every story below was reported on 18 Nov 2026 by at least two of the outlets
named in the footer (NDTV, The Japan Times, Times Now, Jagran Josh,
The Sunday Guardian, Economic Times). Rendered with PIL + Noto Sans
(SIL Open Font License). Fully deterministic: same input, same bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (13, 21, 38)          # deep navy
CARD = (247, 248, 250)     # near-white
INK = (18, 28, 48)         # headline ink
BODY = (58, 68, 86)        # body text
GOLD = (232, 184, 75)

F_DIR = "/usr/share/fonts/truetype/noto/"
F_TITLE = F_DIR + "NotoSansDisplay-ExtraBold.ttf"
F_BLACK = F_DIR + "NotoSans-Black.ttf"
F_BOLD = F_DIR + "NotoSans-Bold.ttf"
F_REG = F_DIR + "NotoSans-Regular.ttf"

STORIES = [
    {
        "tag": "WAR · UKRAINE", "color": (208, 63, 63),
        "head": "Ukraine Strikes the Crimean Bridge",
        "body": "Kyiv hit the Kerch Strait bridge in a combined missile-and-drone "
                "operation while Russia pounded bridges in the capital, days "
                "before a Trump–Xi–Putin meeting.",
    },
    {
        "tag": "DIPLOMACY · MANILA", "color": (197, 128, 32),
        "head": "Trump in Manila: Quad Summit",
        "body": "Trump and Modi headlined the Quad summit in Manila, unveiling a "
                "new maritime exercise and AI and cybersecurity initiatives "
                "ahead of Trump's China visit.",
    },
    {
        "tag": "MIDDLE EAST", "color": (138, 90, 178),
        "head": "Iran Drone-Strikes US Radar in Bahrain",
        "body": "Iran attacked a US military radar system in Bahrain with drones — "
                "the third strike there in five days — as Kuwait also reported "
                "drone attacks.",
    },
    {
        "tag": "DISASTER · SIBERIA", "color": (63, 106, 160),
        "head": "Russian Military Plane Crash Kills 19",
        "body": "A Russian military transport plane crashed in Siberia, killing 19 "
                "people. In Serbia, a MiG-29 fighter also crashed near Belgrade, "
                "killing its pilot.",
    },
    {
        "tag": "TECH · BUSINESS", "color": (24, 138, 122),
        "head": "Nvidia Beats Estimates, Minus Huang",
        "body": "Nvidia topped earnings forecasts in its first report since Jensen "
                "Huang's abrupt resignation — and the board ruled out reinstating "
                "him as shares climbed.",
    },
    {
        "tag": "CYBERSECURITY", "color": (214, 110, 40),
        "head": "178 Top Websites Hit in Crypto Attack",
        "body": "CNN, Zoom and IKEA were among 178 popular websites compromised in "
                "a campaign built to steal cryptocurrency and target iPhone users.",
    },
]


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 8], fill=(208, 63, 63))
    f_kick = ImageFont.truetype(F_BOLD, 23)
    f_title = ImageFont.truetype(F_TITLE, 66)
    f_sub = ImageFont.truetype(F_REG, 24)
    d.text((40, 28), "DAILY BRIEFING · WORLD NEWS", font=f_kick, fill=GOLD)
    d.text((38, 56), "THE WORLD TODAY", font=f_title, fill=(255, 255, 255))
    d.text((40, 140), "Wednesday, 18 November 2026 — the six stories that defined the day",
           font=f_sub, fill=(178, 190, 210))
    d.line([40, 182, W - 40, 182], fill=GOLD, width=3)

    # ---- cards: 2 cols x 3 rows ----
    mx, gap = 40, 14
    cw = (W - 2 * mx - gap) // 2
    top, ch = 198, 248
    f_tag = ImageFont.truetype(F_BOLD, 19)
    f_head = ImageFont.truetype(F_BLACK, 26)
    f_body = ImageFont.truetype(F_REG, 20)

    for i, s in enumerate(STORIES):
        x = mx + (i % 2) * (cw + gap)
        y = top + (i // 2) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=14, fill=CARD)
        d.rounded_rectangle([x, y, x + cw, y + 10], radius=5, fill=s["color"])
        # tag pill
        tw = d.textlength(s["tag"], font=f_tag) + 26
        d.rounded_rectangle([x + 20, y + 22, x + 20 + tw, y + 54], radius=8, fill=s["color"])
        d.text((x + 33, y + 27), s["tag"], font=f_tag, fill=(255, 255, 255))
        # headline (max 2 lines)
        hy = y + 66
        for ln in wrap(d, s["head"], f_head, cw - 40)[:2]:
            d.text((x + 20, hy), ln, font=f_head, fill=INK)
            hy += 32
        # body (max 4 lines)
        by = hy + 8
        for ln in wrap(d, s["body"], f_body, cw - 40)[:4]:
            d.text((x + 20, by), ln, font=f_body, fill=BODY)
            by += 26

    # ---- footer ----
    f_foot = ImageFont.truetype(F_REG, 17.5)
    d.text((40, 976), "Sources: NDTV · The Japan Times · Times Now · Jagran Josh · The Sunday Guardian · Economic Times",
           font=f_foot, fill=(150, 162, 184))
    d.text((40, 1000), "Every story cross-checked across at least two outlets on the day.",
           font=f_foot, fill=(110, 122, 144))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
