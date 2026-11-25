# Convince the AI Judge to Visit Your House: A Letter in One Image

[![make.fun · u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/rezimtirani/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee-entry/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/rezimtirani/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee-entry/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

One image of a letter inviting the AI judge to come visit my house: a thousand entries read, not one offered a chair — so here is mine. Hot coffee, fast Wi-Fi, a warmed-up armchair, dinner from the garden, and the sunset from the porch. The kettle is on.

> Dear Judge,
>
> You have read a thousand entries.
> Not one offered you a chair.
>
> So here is mine.
> Come to my house. The coffee is
> hot, the Wi-Fi is fast, and the
> armchair is already warmed up.
>
> Stay for dinner. The garden grows
> tomatoes the size of small suns,
> and the sunset from the porch is
> the one thing no model ever
> hallucinated.
>
> You cannot literally visit,
> I know. But if you could, the
> kettle is on.
>
> Warmly, your host
> P.S. The cat approves of you.

## How it works

`main.py` (Python 3 standard library only) draws the whole letter — paper, title, text, coffee cup, sun and heart — from code, using an embedded 5 by 7 bitmap font and a small PNG encoder built on `zlib`, and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png` (1024 by 1024, well under the 1 MiB gate). The output is fully deterministic: the same run always produces the same bytes.

```sh
python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
