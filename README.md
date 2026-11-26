# Thursday 26 November 2026 — The World in One Page

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/keep0626/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/keep0626/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

A single 1024×1024 newspaper-style poster that gathers the world's
news for Thursday 26 November 2026 into one page. Thirty-two stories
share the sheet: a large dated masthead up top, one headline story
with a hand-drawn illustration, and the rest as short numbered
briefs, so a reader can take in the whole day at a glance.

## How it is made

`render.py` reads the day's stories from `stories.json` and draws
the finished poster with Pillow, saving it as `entry.png`.
`main.py` does no drawing at all — it only copies that finished
`entry.png` into the output directory, so what you see here is
exactly what the renderer produced.
