# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/exrazor01-creator/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/exrazor01-creator/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A pure-stdlib Python program that draws a one-page newspaper front page, "THE WORLD TODAY", summing up Wednesday 25 November 2026 in a single 1024x1024 image: six stories from the Gulf of Finland to the White House turkey pardon, each with a hand-drawn pictogram, headline, and short summary. It writes the PNG byte-for-byte deterministically, with no network and no third-party libraries.

## The six stories

1. **Zelenskiy confirms Ukraine hit Russian ship in the Gulf of Finland** — Ukraine's president confirmed Kyiv's drone struck the Russian cargo ship Sparta II (hit Saturday 21 Nov, confirmation reported 24 Nov); he said the ship was a legitimate target because it carried weapons. Norway urged caution. *Reuters, 24–25 Nov 2026* — https://www.reuters.com/world/europe/ukraine-insists-attack-russian-ships-libya-was-self-defence-2026-11-24/
2. **CIA and ODNI hit by cyberattack** — an apparent hack affecting unclassified open-source intelligence systems; no classified data hit, CNN reported. *CNN / New York Times, 24–25 Nov 2026* — https://www.cnn.com/2026/11/24/politics/cia-odni-hack-unclassified-information
3. **Houthi drone hits Riyadh's tallest tower, 11 hurt** — second strike on the PIF Tower in less than a week, Saudi Civil Defense said. *Reuters, 24 Nov 2026* — https://www.tbsnews.net/worldbiz/middle-east/11-injured-second-suspected-houthi-strike-riyadhs-tallest-tower-days-1613121
4. **Huawei guilty in US criminal trial** — a New York jury found Huawei guilty on 10 of 12 counts, including bank fraud and conspiracy to steal trade secrets. *US Department of Justice / AFP, verdict 24 Nov 2026* — https://stockbiz.vn/en/news/international-news-on-november-25-new-developments-in-the-us-and-the-democratic-republic-of-the-congo/42897426
5. **WHO staff flee Congo hospital amid fighting** — health workers were evacuated from a hospital in Akwe, Ituri province, after sheltering three days from fierce fighting; WHO also temporarily relocated its Ebola response team from Mongbwalu. *WHO Director-General Tedros Adhanom Ghebreyesus, 24–25 Nov 2026* — https://stockbiz.vn/en/news/international-news-on-november-25-new-developments-in-the-us-and-the-democratic-republic-of-the-congo/42897426
6. **Trump pardons turkeys Freedom and Feathers for Thanksgiving** — the White House pardoning on Tuesday 24 Nov, ahead of Thanksgiving on Thursday 26 Nov; Feathers fled into the bushes before the ceremony, but both birds were pardoned. *Reuters, 24–25 Nov 2026* — https://www.reuters.com/legal/government/trump-spares-turkeys-freedom-feathers-fowl-thanksgiving-fate-2026-11-24/

Note on timing: several of these events happened late on 24 November in Western time zones and were first reported across Asia on 25 November; all six led the world-news roundups dated 25 November 2026.

## Run it

```sh
python3 main.py
```

This writes `entry.png` (to `/output/entry.png` when `/output` exists, otherwise `./entry.png`).

<sub>Entered on [make.fun](https://make.fun/?ref=9taf1vak&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
