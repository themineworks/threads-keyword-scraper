#!/usr/bin/env node
// Node.js client for the themineworks/threads-scraper actor on Apify: runs it and saves results.json.
// Flags map 1:1 to the actor's input. Free API token: https://console.apify.com/sign-up
// Docs and pricing: https://themineworks.com/actors/threads-scraper/
import { ApifyClient } from 'apify-client';
import { writeFileSync } from 'node:fs';

const ACTOR = 'themineworks/threads-scraper';

function parseArgs(argv) {
    const out = {};
    for (let i = 0; i < argv.length; i++) {
        if (!argv[i].startsWith('--')) continue;
        const key = argv[i].slice(2);
        out[key] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    }
    return out;
}

const args = parseArgs(process.argv.slice(2));
const token = args.token || process.env.APIFY_TOKEN;
if (!token) {
    console.error('Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up');
    process.exit(1);
}

const runInput = {};
if (args['mode'] !== undefined) runInput.mode = String(args['mode']);
if (args['profile-usernames'] !== undefined) runInput.profileUsernames = String(args['profile-usernames']).split(',').map((s) => s.trim());
if (args['post-urls'] !== undefined) runInput.postUrls = String(args['post-urls']).split(',').map((s) => s.trim());
if (args['search-query'] !== undefined) runInput.searchQuery = String(args['search-query']);
if (args['hashtag'] !== undefined) runInput.hashtag = String(args['hashtag']);
if (args['max-posts'] !== undefined) runInput.maxPosts = parseInt(args['max-posts'], 10);
if (args['include-replies'] !== undefined) runInput.includeReplies = args['include-replies'] === true || args['include-replies'] === 'true';
if (args['include-reposts'] !== undefined) runInput.includeReposts = args['include-reposts'] === true || args['include-reposts'] === 'true';
if (args['include-tag-window'] !== undefined) runInput.includeTagWindow = args['include-tag-window'] === true || args['include-tag-window'] === 'true';
if (args['result-type'] !== undefined) runInput.resultType = String(args['result-type']);
if (args['monitor-mode'] !== undefined) runInput.monitorMode = args['monitor-mode'] === true || args['monitor-mode'] === 'true';

const client = new ApifyClient({ token });
console.log(`Running ${ACTOR} ...`);
const run = await client.actor(ACTOR).call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
writeFileSync('results.json', JSON.stringify(items, null, 2));
console.log(`Saved ${items.length} results to results.json`);
