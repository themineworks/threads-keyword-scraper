# Threads Scraper: Posts, Profiles, Tags & Keyword Monitor

Python client for **[Threads Scraper: Posts, Profiles, Tags & Keyword Monitor](https://apify.com/themineworks/threads-scraper)** — scrape Threads posts, profiles and tags, monitor keywords — no login.

> ⚡ No login, no cookies, no ban risk · runs in the cloud on [Apify](https://apify.com/themineworks/threads-scraper)
>
> 💸 From **$1.0 per 1,000 results** (volume discounts on paid Apify plans). You are only charged for delivered results — empty searches and failed pages are never billed.

## Quick start

```bash
pip install apify-client
python3 threads_keyword_scraper.py --token YOUR_APIFY_TOKEN --mode "profile"
```
### Node.js

```bash
npm install apify-client
node threads_keyword_scraper.mjs --token YOUR_APIFY_TOKEN --token YOUR_APIFY_TOKEN --mode "profile"
```


Get a free API token: [console.apify.com/sign-up](https://console.apify.com/sign-up) — then find it under **Settings → API & Integrations**.

## Options

| Flag | Type | Description |
|---|---|---|
| `--token` | string | Apify API token (or `APIFY_TOKEN` env var) |
| `--out` | string | Output basename — writes `results.json` + `results.csv` |
| `--mode` | string | Which type of scrape to run: profile, post, search, or hashtag. |
| `--profile-usernames` | array | List of Threads usernames (without @) to scrape. Used when mode=profile. Example: ["zuck", |
| `--post-urls` | array | List of full Threads post URLs to scrape. Used when mode=post. Example: ["https://www.thre |
| `--search-query` | string | Search keyword. Used when mode=search. |
| `--hashtag` | string | Hashtag to scrape, without the leading #. Used when mode=hashtag. |
| `--max-posts` | integer | Maximum number of posts to return across the whole run. |
| `--include-replies` | boolean | If true, include reply posts in the output. |

Flags map 1:1 to the actor's input schema — full reference and a live output sample on the [Store listing](https://apify.com/themineworks/threads-scraper).

## Output

One row per result, saved as both JSON and CSV with every field the actor returns. Preview the exact fields on the [listing's output tab](https://apify.com/themineworks/threads-scraper).

## Why this actor

- **HTTP-native** — fast, stable, no headless-browser overhead
- **No account risk** — never asks for your login or cookies
- **Fair billing** — pay per delivered result only

MIT © [The Mine Works](https://apify.com/themineworks) — part of a 69-scraper suite trusted by 450+ developers.
