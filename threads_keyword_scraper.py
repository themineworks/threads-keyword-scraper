#!/usr/bin/env python3
"""Meta Threads data that returns actual data. Python, Node.js and cURL clients for the Threads Scraper on Apify, pay per result.

Command-line client for the themineworks/threads-scraper actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/threads-scraper/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/threads-scraper"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--mode", help="Which type of scrape to run")
    ap.add_argument("--profile-usernames", help="Comma-separated. Threads usernames (without @) to scrape, used when mode=profile")
    ap.add_argument("--post-urls", help="Comma-separated. List of full Threads post URLs to scrape")
    ap.add_argument("--search-query", help="Search keyword")
    ap.add_argument("--hashtag", help="Hashtag to scrape, without the leading #")
    ap.add_argument("--max-posts", type=int, help="Maximum posts to return across the whole run")
    ap.add_argument("--include-replies", action=argparse.BooleanOptionalAction, help="If true, include reply posts in the output")
    ap.add_argument("--include-reposts", action=argparse.BooleanOptionalAction, help="If true, include reposts in the output")
    ap.add_argument("--include-tag-window", action=argparse.BooleanOptionalAction, help="Search mode also reads the tag feed for the query, which can surface posts that carry the…")
    ap.add_argument("--result-type", help="For search and hashtag modes: 'recent' or 'top'")
    ap.add_argument("--monitor-mode", action=argparse.BooleanOptionalAction, help="Run on a schedule and deliver ONLY results not seen in a previous run")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.mode is not None: run_input["mode"] = a.mode
    if a.profile_usernames: run_input["profileUsernames"] = [s.strip() for s in a.profile_usernames.split(",") if s.strip()]
    if a.post_urls: run_input["postUrls"] = [s.strip() for s in a.post_urls.split(",") if s.strip()]
    if a.search_query is not None: run_input["searchQuery"] = a.search_query
    if a.hashtag is not None: run_input["hashtag"] = a.hashtag
    if a.max_posts is not None: run_input["maxPosts"] = a.max_posts
    if a.include_replies is not None: run_input["includeReplies"] = a.include_replies
    if a.include_reposts is not None: run_input["includeReposts"] = a.include_reposts
    if a.include_tag_window is not None: run_input["includeTagWindow"] = a.include_tag_window
    if a.result_type is not None: run_input["resultType"] = a.result_type
    if a.monitor_mode is not None: run_input["monitorMode"] = a.monitor_mode

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
