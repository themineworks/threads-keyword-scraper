# Threads Scraper: Posts, Profiles, Hashtags & Search

Threads has no public API, so this reads the same data a logged-out visitor sees and returns it as structured JSON. Profile, post, search, and hashtag modes. Full post schema with reposts, replies, hashtags, mentions, external URLs. Cursor-based pagination.

**Run it on Apify:** [apify.com/themineworks/threads-scraper](https://apify.com/themineworks/threads-scraper)
**Docs, FAQ and pricing:** [themineworks.com/actors/threads-scraper](https://themineworks.com/actors/threads-scraper/)

**Price:** From $1.20 per 1,000 posts on Apify's higher plans ($2.00 on the free plan), plus a $0.0025 start fee per run. Failed and empty results are never charged.

## What it returns

* 4 modes: profile, post, search, hashtag
* Full nested schema with reposts and replies
* Hashtags, mentions, external URLs extracted
* Cursor pagination for backfill
* Empty results are never charged

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/threads-scraper").call(run_input={
    "mode": "profile",
    "profileUsernames": [
        "zuck"
    ],
    "maxPosts": 25
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/threads-scraper').call({
    "mode": "profile",
    "profileUsernames": [
        "zuck"
    ],
    "maxPosts": 25
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~threads-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mode": "profile", "profileUsernames": ["zuck"], "maxPosts": 25}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 threads_keyword_scraper.py --token YOUR_APIFY_TOKEN --mode "profile" --profile-usernames "zuck" --max-posts "25"
node threads_keyword_scraper.mjs --token YOUR_APIFY_TOKEN --mode "profile" --profile-usernames "zuck" --max-posts "25"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `mode` (required) | string | `"profile"` | Which type of scrape to run |
| `profileUsernames` | array | `["zuck"]` | Threads usernames (without @) to scrape, used when mode=profile |
| `postUrls` | array | `[]` | List of full Threads post URLs to scrape |
| `searchQuery` | string | `""` | Search keyword |
| `hashtag` | string | `""` | Hashtag to scrape, without the leading # |
| `maxPosts` | integer | `25` | Maximum posts to return across the whole run |
| `includeReplies` | boolean | `false` | If true, include reply posts in the output |
| `includeReposts` | boolean | `false` | If true, include reposts in the output |
| `includeTagWindow` | boolean | `true` | Search mode also reads the tag feed for the query, which can surface posts that carry the tag without… |
| `resultType` | string | `"recent"` | For search and hashtag modes: 'recent' or 'top' |
| `monitorMode` | boolean | `false` | Run on a schedule and deliver ONLY results not seen in a previous run |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `post_id` | string | Unique numeric post ID |
| `code` | string | Threads post shortcode |
| `url` | string | Full URL to the Threads post |
| `username` | string | Username of the post author |
| `user_full_name` | string | Display name of the post author |
| `text` | string | Text content of the post |
| `posted_at` | string | ISO 8601 timestamp when the post was published |
| `like_count` | integer | Number of likes on the post |
| `reply_count` | integer | Number of replies to the post |
| `repost_count` | integer | Number of reposts |
| `quote_count` | integer | Number of quote posts |
| `media_type` | string | Type of media attached (text, image, video, carousel) |
| `hashtags` | array | List of hashtags used in the post |
| `scraped_at` | string | ISO 8601 timestamp of when the record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/threads-scraper
```

## FAQ

### Does Threads have a public API?

No. Meta has not released a public Threads API as of 2025. Profile and post data is accessible via web scraping of the public-facing pages.

### What data can I get from Threads without an API?

Public profile information (username, bio, follower count), post text, like counts, reply counts, timestamps, and media attachments from public accounts.

### Does the Threads scraper require a login?

No. The scraper accesses publicly visible Threads pages without authentication. Private accounts and follower lists require login and are not supported.

### What is the output format?

Structured JSON with one record per post: post ID, text content, like count, reply count, timestamp, media URLs, and author profile data.

### Which of the four modes should I use?

Profile pulls one account timeline, post fetches a single post and its replies, search runs a keyword query, and hashtag follows a tag feed. All four return the same post schema.

### How far back can I go?

As far as the feed exposes. Pagination is cursor based, so a backfill run keeps requesting the next page until the cursor runs out rather than stopping at the first screen.

### What is captured beyond the post text?

Reposts and replies as nested records, plus hashtags, mentions and any external URLs pulled out as their own fields.

### How much does the Threads Scraper cost?

From $1.20 per 1,000 posts on Apify's higher plans ($2.00 on the free plan), plus a $0.0025 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [Reddit Scraper](https://themineworks.com/actors/reddit-scraper/): Free Reddit data with full comment trees
* [LinkedIn Post Scraper](https://themineworks.com/actors/linkedin-post-search/): Search LinkedIn posts by keyword without login
* [Threads Search Scraper](https://themineworks.com/actors/threads-search-scraper/): Threads posts by keyword, with a standing brand watch

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
