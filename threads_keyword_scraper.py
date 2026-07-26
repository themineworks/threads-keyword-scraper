#!/usr/bin/env python3
"""Scrape Threads posts, profiles and tags, monitor keywords — no login.
CLI for the themineworks/threads-scraper Apify actor: runs it, waits, saves JSON + CSV.
Free Apify account + API token: https://console.apify.com/sign-up
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/threads-scraper"

def main():
    ap = argparse.ArgumentParser(description="scrape Threads posts, profiles and tags, monitor keywords — no login")
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"),
                    help="Apify API token (or set APIFY_TOKEN env var)")
    ap.add_argument("--out", default="results", help="Output basename (.json and .csv)")
    ap.add_argument("--mode", default="profile", help="Which type of scrape to run: profile, post, search, or hashtag")
    ap.add_argument("--profile-usernames", help="Comma-separated. List of Threads usernames (without @) to scrape e.g. zuck")
    ap.add_argument("--post-urls", help="Comma-separated. List of full Threads post URLs to scrape e.g. one,two")
    ap.add_argument("--search-query", help="Search keyword")
    ap.add_argument("--hashtag", help="Hashtag to scrape, without the leading #")
    ap.add_argument("--max-posts", type=int, default=3, help="Maximum number of posts to return across the whole run")
    ap.add_argument("--include-replies", action="store_true", help="If true, include reply posts in the output")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN — free token at https://console.apify.com/sign-up")

    run_input = {}
    if a.mode is not None: run_input["mode"] = a.mode
    if a.profile_usernames is not None: run_input["profileUsernames"] = [s.strip() for s in a.profile_usernames.split(",") if s.strip()]
    if a.post_urls is not None: run_input["postUrls"] = [s.strip() for s in a.post_urls.split(",") if s.strip()]
    if a.search_query is not None: run_input["searchQuery"] = a.search_query
    if a.hashtag is not None: run_input["hashtag"] = a.hashtag
    if a.max_posts is not None: run_input["maxPosts"] = a.max_posts
    if a.include_replies: run_input["includeReplies"] = True

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    if items:
        keys = []
        for it in items:
            for k in it:
                if k not in keys: keys.append(k)
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: ("" if v is None else v) for k, v in it.items()})
    print(f"Done: {len(items)} results -> {a.out}.json / {a.out}.csv")

if __name__ == "__main__":
    main()
