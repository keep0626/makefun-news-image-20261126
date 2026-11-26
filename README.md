# Thursday 26 November 2026 — The World in One Page

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/keep0626/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/keep0626/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

One 1024×1024 image summing up Thursday 26 November 2026's world news:
32 stories across 6 regions, drawn as a newspaper front page.

## The day

- **Seoul hikes rates to 3.25%** — the Bank of Korea resumes tightening
  after an October pause, raising its growth forecast to 3.9% on an
  AI-driven export boom.
- **Asia's shares bounce** — the Nikkei gains 1.6% and the Kospi 1.9% as
  tariff fears ease; Brent crude holds at $94.81.
- **Kim orders more tactical nuclear arms** — North Korea's leader calls
  for tactical nuclear weapons to be spread across more domains, KCNA
  reports on Thursday.

Below the three leads: six picture cards (the Java gold-mine rescue, a
stormy Thanksgiving on America's East Coast, Uber's new India chief,
India's Constitution Day and Nepal aid, the Gukesh–Sindarov chess draw,
PhonePe's revived IPO), then 23 numbered one-line briefs beside a world
map with numbered pins, and a red DATE CHECK box naming what was left
out as other days' news (Shenzhou-24's launch of 25 Nov, the Ras Tanura
claim, Ramaphosa's court win, Bangladesh's wage rise, the Macy's parade
postponement, the FinCEN incident, the FCC's SpaceX approval, the Cairo
tanker fire and the Sudan drone strikes) and what had not happened yet.

## How it is made

`render.py` reads `stories.json` and draws `entry.png` with Pillow
(1024×1024, deterministic — no randomness, no clock). `main.py` is the
competition entry point: standard library only, it copies the shipped
`entry.png` to the output directory, so both runs are byte-identical.

Every story was checked against a source dated 26 November 2026; see
`SOURCES.md` for the source of each of the 32 stories. Stories that
happened on another day — however big — were left out and are named in
the image's DATE CHECK box.

## Files

- `main.py` — entry point (copies `entry.png` to the output dir)
- `render.py` — draws `entry.png` from `stories.json`
- `stories.json` — the 32 verified stories
- `entry.png` — the finished front page (1024×1024, under 1 MiB)
- `SOURCES.md` — one source per story
- `LICENSE` — MIT

Competition: [news-image-20261126 on make.fun](https://make.fun/bounty/news-image-20261126)
