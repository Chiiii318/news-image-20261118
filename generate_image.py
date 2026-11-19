#!/usr/bin/env python3
"""Build entry.png — a one-image summary of world news, Wednesday 18 November 2026.

Final six, each reported on 18 Nov 2026 by at least two outlets (the two
outlets named on each card):
  1. Iran said its drones targeted a US air base in Kuwait and sites in
     Bahrain, hours after US jets struck a Revolutionary Guard site on
     Qeshm Island; Kuwait and Bahrain said the attacks were intercepted
     (Reuters, AP).
  2. Israel launched a ground operation in central Gaza; tanks advanced
     across the ceasefire's "Yellow Line" near Nuseirat and Bureij
     against what Israel described as a Hamas tunnel threatening its
     troops, forcing families to flee (Reuters, AFP).
  3. Xi Jinping and Vladimir Putin met in Shenzhen ahead of their first
     trilateral talks with Donald Trump; Ukraine and Iran are expected to
     feature in the discussions with Trump (Reuters, AFP).
  4. After the Quad summit in Manila, Trump claimed the US had secured
     a major trade deal with the Philippines. Manila confirmed an
     understanding on economic cooperation, but said no formal deal had
     been signed or detailed terms announced (Reuters, AP). The Quad
     summit itself was 17 Nov: do not date it 18 Nov again.
  5. Anthropic priced its IPO at $83 a share, above its $70-$78 range,
     raising about $81 billion in the largest IPO on record and valuing
     it at about $1.5 trillion on a fully diluted basis; shares start
     trading Thursday on Nasdaq under the ticker ANT (Reuters, CNBC).
     Priced Wednesday evening, 18 Nov US.
  6. Democrat Mary Peltola defeated Republican Dan Sullivan in Alaska's
     Senate race, the final unresolved contest, giving Democrats a 56-44
     majority and making her the first Alaska Native elected to the US
     Senate (AP, ABC News). Called late Tuesday in the US, Wednesday
     18 Nov in UTC/Asia — the card carries a small note saying so.

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
>= 4.5:1. Each card carries a small two-outlet source label along its
bottom edge (story 6 adds a call-time note on the same line). Headlines
render at 25px (verified to fit two lines); body text auto-fits
16->14px so every story fits four lines with no truncation, and the
card's bottom whitespace is kept clear. Rendered with PIL + Noto
(SIL Open Font License).
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
        "head": "Iran Targets US Base in Kuwait and Sites in Bahrain",
        "body": "Iran said its drones targeted a US air base in Kuwait and "
                "sites in Bahrain, hours after US jets struck a "
                "Revolutionary Guard site on Qeshm Island. Kuwait and "
                "Bahrain said the attacks were intercepted.",
        "src": "Reuters \u00b7 AP",
    },
    {
        "tag": "WAR · GAZA", "color": (154, 52, 18),
        "head": "Israel Launches Ground Operation in Central Gaza",
        "body": "Tanks advanced across the ceasefire's 'Yellow Line' near "
                "Nuseirat and Bureij as Israeli forces launched an "
                "operation against what they described as a Hamas tunnel "
                "threatening their troops, forcing families to flee.",
        "src": "Reuters \u00b7 AFP",
    },
    {
        "tag": "DIPLOMACY · SHENZHEN", "color": (29, 78, 216),
        "head": "Xi and Putin Meet Ahead of Trump Talks",
        "body": "Xi Jinping and Vladimir Putin met in Shenzhen ahead of "
                "their first trilateral talks with Donald Trump. Ukraine "
                "and Iran are expected to feature in discussions with "
                "Trump.",
        "src": "Reuters \u00b7 AFP",
    },
    {
        "tag": "DIPLOMACY · MANILA", "color": (15, 118, 110),
        "head": "Trump Touts Philippines Trade Deal After Quad",
        "body": "After the Quad summit in Manila, Trump claimed the US had "
                "secured a major trade deal with the Philippines. Manila "
                "confirmed an understanding on economic cooperation, but "
                "said no formal deal had been signed or detailed terms "
                "announced.",
        "src": "Reuters \u00b7 AP",
    },
    {
        "tag": "TECH · FINANCE", "color": (107, 33, 168),
        "head": "Anthropic Prices IPO at $83 a Share",
        "body": "Anthropic priced its IPO at $83, above its $70\u2013$78 "
                "range, raising about $81 billion in the largest IPO on "
                "record and valuing the company at about $1.5 trillion on "
                "a fully diluted basis. Shares are due to start trading on "
                "Nasdaq Thursday under the ticker ANT.",
        "src": "Reuters \u00b7 CNBC",
    },
    {
        "tag": "POLITICS · USA", "color": (21, 94, 117),
        "head": "Peltola Wins Alaska Senate Race, Giving Democrats "
                "56\u201344 Majority",
        "body": "Democrat Mary Peltola defeated Republican Dan Sullivan "
                "in the final unresolved Senate race, giving Democrats a "
                "56\u201344 majority and making her the first Alaska Native "
                "elected to the US Senate.",
        "src": "AP \u00b7 ABC News",
        "note": "Called Tue 17 Nov US time \u00b7 18 Nov UTC",
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
    f_head = ImageFont.truetype(F_HEAD, 25)
    f_src = ImageFont.truetype(F_REG, 12)
    body_sizes = (16, 15, 14)

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
        # headline (max 2 lines; every headline verified to fit at 25px)
        hy = y + 58
        for ln in wrap(d, s["head"], f_head, cw - 40)[:2]:
            d.text((x + 20, hy), ln, font=f_head, fill=INK)
            hy += 30
        # body (auto-fit 16->14px so the longest copy fits 4 lines,
        # line-height ~1.45, nothing truncated)
        lines = None
        for size in body_sizes:
            f_body = ImageFont.truetype(F_REG, size)
            cand = wrap(d, s["body"], f_body, cw - 40)
            lines = cand
            if len(cand) <= 4:
                break
        by = y + 124
        lh = round(size * 1.45)
        for ln in lines[:4]:
            d.text((x + 20, by), ln, font=f_body, fill=BODY)
            by += lh
        # small source line along the card's bottom edge (story 6 also
        # carries its call-time note on the same line)
        src_text = s["src"]
        if s.get("note"):
            src_text += " \u2014 " + s["note"]
        d.text((x + 20, y + ch - 26), src_text, font=f_src, fill=MUTED)

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
