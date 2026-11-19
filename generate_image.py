#!/usr/bin/env python3
"""Build entry.png — a one-image summary of world news, Wednesday 18 November 2026.

Final six, each reported on 18 Nov 2026 by at least two outlets:
  1. Iran's drones hit US sites at Kuwait's Ali Al Salem base and Bahrain
     intercepted more attacks, a day after US jets struck Iran's Qeshm
     Island (Reuters, AP, Gulf News, CNA).
  2. Israel opened its first broad ground offensive in central Gaza since
     the October 2025 ceasefire, pushing past the "yellow line" near
     Nuseirat and Bureij (Al Jazeera, TRT World, Outlook India).
  3. Xi Jinping and Vladimir Putin met at the APEC summit in Shenzhen, a
     day before their first three-way talks with Donald Trump on 19 Nov
     (Reuters, BBC, The Hindu).
  4. Quad leaders held their first summit in over two years in Manila, as
     Trump announced a major US-Philippines trade deal (Anadolu, AP, TOI).
  5. Anthropic priced its IPO at $83 a share, above its $70-$78 range,
     valuing it at about $1.5 trillion; trading starts Thursday as ANT
     (CNBC, Reuters, Bloomberg, BBC). Priced Wednesday evening, 18 Nov US.
  6. Democrat Mary Peltola won Alaska's Senate race, the last undecided
     midterm contest, giving Democrats a 56-44 majority (AP, Al Jazeera,
     NPR). Called late Tuesday in the US, Wednesday 18 Nov in UTC/Asia.

Dropped from the morning draft after a full-day re-check: the Kerch bridge
arch fell on 17 Nov (strikes 16-17 Nov), the Siberian plane crash was 17 Nov,
and the 178-website crypto attack was 16 Nov. The 19 Nov Shenzhen trilateral
is NOT presented as an 18 Nov event — only the 18 Nov Xi-Putin meeting is.

Design: Swiss/editorial system per the ui_ux_pro_max skill — white paper,
near-black ink, breaking-news red masthead, serif display headlines
(Noto Serif Display) with sans body (Noto Sans), 8pt spacing grid, one
semantic colour per story (tag text + top bar; colour never the only
carrier — every card also carries a numbered label and a text tag).
Contrast: body ink on white ~9:1; white tag text on every story colour
>= 4.5:1. Rendered with PIL + Noto (SIL Open Font License).
Fully deterministic: same input, same bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (253, 252, 250)    # warm white
CARD = (255, 255, 255)
BORDER = (229, 224, 216)   # hairline
INK = (20, 20, 20)         # masthead ink
BODY = (61, 68, 81)        # body text, ~9:1 on white
MUTED = (107, 114, 128)    # secondary text, ~4.8:1 on white
RED = (220, 38, 38)        # breaking-news red (catalog primary)

F_DIR = "/usr/share/fonts/truetype/noto/"
F_TITLE = F_DIR + "NotoSerifDisplay-Black.ttf"
F_HEAD = F_DIR + "NotoSerifDisplay-Bold.ttf"
F_NUM = F_DIR + "NotoSerifDisplay-Bold.ttf"
F_BOLD = F_DIR + "NotoSans-Bold.ttf"
F_REG = F_DIR + "NotoSans-Regular.ttf"

STORIES = [
    {
        "tag": "WAR · THE GULF", "color": (185, 28, 28),
        "head": "Iran Hits US Bases in Kuwait and Bahrain",
        "body": "Iran said its drones struck US sites at Kuwait's Ali Al Salem "
                "base, and Bahrain intercepted more attacks — a day after US "
                "jets hit a site on Iran's Qeshm Island.",
    },
    {
        "tag": "WAR · GAZA", "color": (154, 52, 18),
        "head": "Israel Opens Ground Offensive in Central Gaza",
        "body": "Tanks pushed past the ceasefire's \u201cyellow line\u201d near "
                "Nuseirat and Bureij in the first broad ground offensive "
                "since the October 2025 ceasefire, forcing families to flee.",
    },
    {
        "tag": "DIPLOMACY · SHENZHEN", "color": (29, 78, 216),
        "head": "Xi and Putin Meet Before Trump Talks",
        "body": "Xi Jinping and Vladimir Putin met at the APEC summit in "
                "Shenzhen, a day before their first three-way talks with "
                "Donald Trump, with the Iran and Ukraine wars on the agenda.",
    },
    {
        "tag": "DIPLOMACY · MANILA", "color": (15, 118, 110),
        "head": "Quad Meets as Trump Seals Philippines Deal",
        "body": "Quad leaders held their first summit in over two years in "
                "Manila, as Trump announced a major US\u2013Philippines trade "
                "deal and new maritime and AI cooperation.",
    },
    {
        "tag": "TECH · FINANCE", "color": (107, 33, 168),
        "head": "Anthropic Prices IPO at $83 a Share",
        "body": "The Claude-maker priced its listing above its $70\u2013$78 "
                "range, valuing it at about $1.5 trillion, with shares due "
                "to start trading on Nasdaq on Thursday as ANT.",
    },
    {
        "tag": "POLITICS · USA", "color": (21, 94, 117),
        "head": "Peltola Wins Alaska, Sealing 56\u201344 Senate",
        "body": "Democrat Mary Peltola beat Republican Dan Sullivan in the "
                "last undecided Senate race, giving Democrats a 56\u201344 "
                "majority and making her the first Alaska Native senator.",
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


def tracked(d, xy, text, font, fill, tracking=4):
    """Draw text with extra letter spacing (Swiss-style kicker)."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    return x


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 10], fill=RED)
    f_kick = ImageFont.truetype(F_BOLD, 20)
    f_title = ImageFont.truetype(F_TITLE, 64)
    f_date = ImageFont.truetype(F_BOLD, 24)
    f_sub = ImageFont.truetype(F_REG, 24)
    tracked(d, (40, 30), "DAILY BRIEFING · WORLD NEWS", f_kick, RED)
    d.text((38, 58), "THE WORLD TODAY", font=f_title, fill=INK)
    d.text((40, 138), "Wednesday, 18 November 2026", font=f_date, fill=INK)
    dw = d.textlength("Wednesday, 18 November 2026", font=f_date)
    d.text((40 + dw + 12, 138), "— six stories that defined the day",
           font=f_sub, fill=MUTED)
    d.line([40, 180, W - 40, 180], fill=INK, width=3)
    d.line([40, 186, W - 40, 186], fill=INK, width=1)

    # ---- cards: 2 cols x 3 rows, 8pt grid ----
    mx, gap = 40, 16
    cw = (W - 2 * mx - gap) // 2
    top, ch = 202, 244
    f_tag = ImageFont.truetype(F_BOLD, 18)
    f_num = ImageFont.truetype(F_NUM, 30)
    f_head = ImageFont.truetype(F_HEAD, 26)
    f_body = ImageFont.truetype(F_REG, 19)

    for i, s in enumerate(STORIES):
        x = mx + (i % 2) * (cw + gap)
        y = top + (i // 2) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=10,
                            fill=CARD, outline=BORDER, width=1)
        d.rectangle([x + 10, y, x + cw - 10, y + 6], fill=s["color"])
        # tag pill (text label: colour is never the only carrier)
        tw = d.textlength(s["tag"], font=f_tag) + 24
        d.rounded_rectangle([x + 20, y + 22, x + 20 + tw, y + 52],
                            radius=6, fill=s["color"])
        d.text((x + 32, y + 27), s["tag"], font=f_tag, fill=(255, 255, 255))
        # story number, serif, right-aligned
        num = f"{i + 1:02d}"
        nw = d.textlength(num, font=f_num)
        d.text((x + cw - 20 - nw, y + 20), num, font=f_num, fill=MUTED)
        # headline (max 2 lines)
        hy = y + 64
        for ln in wrap(d, s["head"], f_head, cw - 40)[:2]:
            d.text((x + 20, hy), ln, font=f_head, fill=INK)
            hy += 32
        # body (max 4 lines, line-height 1.5)
        by = y + 134
        for ln in wrap(d, s["body"], f_body, cw - 40)[:4]:
            d.text((x + 20, by), ln, font=f_body, fill=BODY)
            by += 27

    # ---- footer ----
    f_foot = ImageFont.truetype(F_REG, 16)
    d.text((40, 972), "Sources: Reuters · AP · BBC · Al Jazeera · Gulf News · CNBC · The Hindu",
           font=f_foot, fill=MUTED)
    d.text((40, 996), "Every story was reported on 18 November 2026 by at least two outlets.",
           font=f_foot, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
