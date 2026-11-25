#!/usr/bin/env python3
"""Draw 'The World Gazette' front-page poster for Wednesday 25 November 2026.

All stories were researched from live news sources on the day:
Reuters world summary (via Devdiscourse), Daily Summary Of (24 Nov final
edition), EventGraph daily brief, the 'What Happened in the World in the
Last 24 Hours' roundup (Reuters/AP/Euronews wires), Arab News front page.
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
    d.text((M, y), "TECH & GEOPOLITICS - NEW YORK", font=lf, fill=ACCENT)
    y += 24
    for line in wrap(d, "Huawei Convicted in US Trial: Guilty on 10 of 12 Counts", hf_lead, CW):
        d.text((M, y), line, font=hf_lead, fill=INK)
        y += 44
    for line in wrap(d, "A Brooklyn jury found China's Huawei guilty of bank fraud, trade-secret theft and "
                        "conspiring to violate Iran sanctions, acquitting it of racketeering. The telecom "
                        "giant, blacklisted by Washington since 2019, says it will appeal; sentencing is set "
                        "for September 2027.", sf_lead, CW):
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
            ("WAR IN EUROPE",
             "Zelenskiy Confirms Strike on Russian Ship",
             "Kyiv owned up to Saturday's drone hit on the cargo ship Sparta II in the Gulf of "
             "Finland; ally Norway urged caution."),
            ("MARKETS",
             "AI Trade Reverses as Nvidia Slides",
             "A day after surging on its CEO's return, Nvidia fell about 6%; the Nasdaq lost 1.5% "
             "as reports said Washington plans new tariffs."),
            ("MIDDLE EAST",
             "Houthis Hit Riyadh Tower, Near Aden",
             "A Houthi strike on Riyadh's tallest tower wounded 11. Yemen's military says the "
             "rebels are within 60 km of Aden but will not take it."),
        ],
        [
            ("GAZA",
             "Israeli Strike Kills Hamas Security Chief",
             "An air strike in western Gaza City killed Naeem Abu Nahel, head of Hamas's internal "
             "security apparatus. Medics said at least seven Palestinians were killed on Tuesday."),
            ("FRANCE",
             "Sarkozy Corruption Case Sent to Trial",
             "Judges ordered ex-president Nicolas Sarkozy and wife Carla Bruni to stand trial over "
             "the retracted Gaddafi campaign-cash testimony. First hearing: 1 April 2027."),
            ("SPACE - ASIA",
             "Pakistani Pilot Blasts Off to Tiangong",
             "PAF pilot Muhammad Zeeshan Ali launched aboard China's Shenzhou-24 - the first "
             "Pakistani in orbit and Tiangong's first foreign astronaut - for a week of experiments."),
        ],
        [
            ("LATIN AMERICA",
             "25 Hostages Held in Cartagena Supermarket",
             "Armed men seized a supermarket after a failed armoured-car hijack; five older women "
             "were freed as police and soldiers surrounded the store, Colombia's president said."),
            ("ASIA",
             "Malaysia to Send 6,500 Rohingya Back",
             "PM Anwar Ibrahim told parliament Malaysia will return over 6,500 Rohingya refugees to "
             "Myanmar in December - days after the ICJ genocide ruling."),
            ("UNITED STATES",
             "Cyber Breach Hits CIA and Intelligence Office",
             "The CIA and the Director of National Intelligence's office suffered a breach exposing "
             "unclassified information, the latest in a string of US incidents."),
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
    e2 = draw_story(d, M + half + 18, row_y, half, "DISASTER - NEPAL",
                    "Magnitude 5.6 Earthquake Strikes Eastern Nepal",
                    "A 5.6 quake hit Koshi province near the Tibet border at 07:17 local time on "
                    "Tuesday, shaking towns across the Himalayan east.", hf, sf, lab, lh=22, sh=16)
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
        ("60 km", "Houthis' closest\napproach to Aden"),
        ("6,500+", "Rohingya Malaysia\nwill send back"),
        ("570,000", "AIDS deaths in 2025,\na 20-year low"),
        ("5.6", "magnitude of the\nearthquake in Nepal"),
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
    ticker = ("WIRE: Trump awards Giuliani the Medal of Freedom  ///  Senegal regain AFCON title after "
              "CAS ruling  ///  Trump pardons turkeys Freedom and Feathers")
    d.text((M, tick_y + 15), ticker, font=tf, fill=PAPER)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
