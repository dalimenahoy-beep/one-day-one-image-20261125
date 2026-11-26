#!/usr/bin/env python3
"""Draw 'The World Gazette' front-page poster for Wednesday 25 November 2026.

All stories were researched from live news sources on the day: Reuters world summary (Devdiscourse), Just Security Early Edition 25 Nov, Reuters tariffs and markets coverage, the 'What Happened in the World in the Last 24 Hours' evening roundup.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
GREY = (84, 80, 72)
ACCENT = (140, 26, 20)
RULE = (18, 18, 18)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_story(draw, x, y, w_, label, headline, sub, hf, sf, lf, lh=24, sh=19):
    draw.text((x, y), label, font=lf, fill=ACCENT)
    y += 20
    for line in wrap(draw, headline, hf, w_):
        draw.text((x, y), line, font=hf, fill=INK)
        y += lh
    for line in wrap(draw, sub, sf, w_):
        draw.text((x, y), line, font=sf, fill=GREY)
        y += sh
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    CW = W - 2 * M

    # ---- Masthead -------------------------------------------------------
    d.line([(M, 30), (W - M, 30)], fill=RULE, width=3)
    mast = font(SERIF_B, 66)
    title = "The World Gazette"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 40), title, font=mast, fill=INK)
    d.line([(M, 122), (W - M, 122)], fill=RULE, width=1)
    dateline = font(SANS_B, 15)
    left = "WEDNESDAY 25 NOVEMBER 2026"
    right = "ONE IMAGE - THE WHOLE DAY"
    d.text((M, 130), left, font=dateline, fill=INK)
    d.text((W - M - d.textlength(right, font=dateline), 130), right, font=dateline, fill=INK)
    d.line([(M, 154), (W - M, 154)], fill=RULE, width=3)

    # ---- Lead story -----------------------------------------------------
    y = 166
    lf = font(SANS_B, 13)
    hf_lead = font(SERIF_B, 37)
    sf_lead = font(SERIF, 16)
    d.text((M, y), "MIDDLE EAST - STRAIT OF HORMUZ", font=lf, fill=ACCENT)
    y += 24
    for line in wrap(d, "Tankers Hit Mines and Burn in Strait of Hormuz", hf_lead, CW):
        d.text((M, y), line, font=hf_lead, fill=INK)
        y += 44
    for line in wrap(d, "Iran's Revolutionary Guard said two oil tankers struck naval mines and caught fire "
                        "in the Strait of Hormuz early Wednesday, blaming an unauthorised route. Oil prices "
                        "jumped as shipping through the world's key energy chokepoint came under threat.",
                   sf_lead, CW):
        d.text((M, y), line, font=sf_lead, fill=GREY)
        y += 21
    y += 8
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 12

    # ---- Story grid: 3 columns x 3 rows --------------------------------
    hf = font(SERIF_B, 18)
    sf = font(SANS, 12)
    lab = font(SANS_B, 11)
    col_w = (CW - 2 * 18) // 3
    xs = [M, M + col_w + 18, M + 2 * (col_w + 18)]

    rows = [
        [
            ("TECH & GEOPOLITICS",
             "Huawei Convicted on 10 of 12 Counts",
             "A Brooklyn jury found China's Huawei guilty of bank fraud, trade-secret theft and "
             "conspiring to violate Iran sanctions, acquitting it of racketeering. Sentencing: "
             "September 2027."),
            ("TRADE",
             "US Proposes New Tariffs on 14 Partners",
             "Washington proposed tariffs of up to 40% on 14 trading partners to fight factory "
             "overcapacity, with the highest rates aimed at China. US stocks shed $2 trillion at "
             "the open."),
            ("MARKETS",
             "AI Rout Deepens as Nvidia Slides Again",
             "Nvidia fell 3.9% on Wednesday to $149.30, now $2.3 trillion below its October peak, "
             "as S&P put its credit rating on watch. South Korea's KOSPI plunged 6.2% and the "
             "Nikkei 2.8%."),
        ],
        [
            ("WAR IN EUROPE",
             "Ukraine Hits Russian Air Base, Damages Five Planes",
             "Ukrainian forces struck the Savasleyka air base east of Moscow, damaging five "
             "planes used to launch missiles at Ukraine, the General Staff said."),
            ("MIDDLE EAST",
             "Houthis Hit Saudi Arabia's Biggest Refinery",
             "The Houthis attacked the Ras Tanura refinery, causing fires, a day after a drone "
             "strike on Riyadh's tower wounded 11. Brent topped $94."),
            ("GAZA",
             "Israeli Strike Kills Hamas Security Chief",
             "An air strike on Gaza City's Shati camp killed a senior Hamas internal security "
             "chief, his wife and two children, medics and the ministry said."),
        ],
        [
            ("SPACE - ASIA",
             "Pakistani Pilot Docks at Tiangong Station",
             "Shenzhou-24 docked with Tiangong after launch, carrying pilot Zeeshan Ali - the "
             "first Pakistani in orbit and Tiangong's first foreign astronaut."),
            ("LATIN AMERICA",
             "Cartagena Hostages Freed in Dawn Raid",
             "Security forces stormed an Éxito supermarket in Cartagena, freeing all remaining "
             "hostages after a failed armoured-car hijack; one captor was killed."),
            ("UNITED STATES",
             "Microsoft Declares 'Code Red' After Outage",
             "Microsoft declared an internal 'Code Red' after a nearly 24-hour Outlook outage "
             "hit millions of users, caused by a bug present since July."),
        ],
    ]
    row_y = y
    for r, row in enumerate(rows):
        ends = []
        for c, (label, head, sub) in enumerate(row):
            ends.append(draw_story(d, xs[c], row_y, col_w, label, head, sub, hf, sf, lab, lh=22, sh=16))
        row_y = max(ends) + 6
        if r < 2:
            d.line([(M, row_y), (W - M, row_y)], fill=(190, 184, 168), width=1)
            row_y += 9

    # ---- Bottom row: health + disaster ----------------------------------
    d.line([(M, row_y), (W - M, row_y)], fill=RULE, width=1)
    row_y += 10
    half = (CW - 18) // 2
    e1 = draw_story(d, M, row_y, half, "GLOBAL HEALTH",
                    "AIDS Deaths Fall to 570,000 - a 20-Year Low",
                    "UNAIDS says AIDS deaths hit their lowest in over two decades in 2025, but warns "
                    "global HIV funding fell 18% and US funding 26%.", hf, sf, lab, lh=22, sh=16)
    e2 = draw_story(d, M + half + 18, row_y, half, "DISASTER - EGYPT",
                    "31 Killed in Fire After Fuel Truck Overturns",
                    "Thirty-one people were killed and 21 wounded in a fire after a fuel truck "
                    "overturned on a major ring road in Egypt, authorities said.", hf, sf, lab, lh=22, sh=16)
    row_y = max(e1, e2) + 8

    # ---- The Day in Numbers ---------------------------------------------
    d.line([(M, row_y), (W - M, row_y)], fill=RULE, width=3)
    row_y += 10
    nf = font(SERIF_B, 30)
    nlf = font(SANS, 11)
    d.text((M, row_y), "THE DAY IN NUMBERS", font=font(SANS_B, 13), fill=ACCENT)
    row_y += 22
    numbers = [
        ("10 of 12", "counts Huawei was\nconvicted on"),
        ("40%", "top tariff rate\nproposed on 14 partners"),
        ("$2T", "wiped off US stocks\nat Wednesday's open"),
        ("5", "planes damaged in the\nSavasleyka air base strike"),
        ("570,000", "AIDS deaths in 2025,\na 20-year low"),
    ]
    cell = CW // 5
    for i, (num, cap) in enumerate(numbers):
        x = M + i * cell
        d.text((x, row_y), num, font=nf, fill=INK)
        cy = row_y + 40
        for line in cap.split("\n"):
            d.text((x, cy), line, font=nlf, fill=GREY)
            cy += 14
    row_y += 74

    # ---- Wire ticker ------------------------------------------------------
    tick_y = H - 44
    d.rectangle([(0, tick_y), (W, H)], fill=INK)
    tf = font(SANS_B, 11)
    ticker = ("WIRE: Ukraine legalizes Bitcoin and crypto  ///  Dow closes above 50,000 for the first "
              "time  ///  Duran Duran guitarist Andy Taylor dies at 65")
    d.text((M, tick_y + 15), ticker, font=tf, fill=PAPER)

    img.save("entry.png", optimize=True)
    print("saved entry.png")
    print("final row_y (numbers end):", row_y, "| ticker starts at:", H - 44)


if __name__ == "__main__":
    main()
