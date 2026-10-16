#!/usr/bin/env python3
"""Post the next item in queue/posts.json to a Facebook Page and an Instagram professional account.
Secrets (GitHub repo secrets / env): FB_PAGE_ID, FB_PAGE_TOKEN, IG_USER_ID.
A channel with missing secrets is skipped. Use --dry-run to print without posting.
State in queue/state.json records which channels already succeeded for the current post,
so a retry never double-posts."""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = "https://graph.facebook.com/v24.0"
DRY = "--dry-run" in sys.argv

def call(method, path, params):
    data = urllib.parse.urlencode(params).encode() if method == "POST" else None
    url = f"{GRAPH}/{path}" + ("" if method == "POST" else "?" + urllib.parse.urlencode(params))
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method), timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode()[:400]}")

def post_facebook(page_id, token, image_url, text):
    return call("POST", f"{page_id}/photos", {"url": image_url, "caption": text, "access_token": token})

def post_instagram(ig_id, token, image_url, text):
    c = call("POST", f"{ig_id}/media", {"image_url": image_url, "caption": text, "access_token": token})
    cid = c["id"]
    for _ in range(20):  # wait for the container to finish processing
        st = call("GET", cid, {"fields": "status_code", "access_token": token}).get("status_code")
        if st == "FINISHED": break
        if st in ("ERROR", "EXPIRED"): raise RuntimeError(f"instagram container {st}")
        time.sleep(3)
    return call("POST", f"{ig_id}/media_publish", {"creation_id": cid, "access_token": token})

def main():
    posts = json.load(open(os.path.join(ROOT, "queue", "posts.json"), encoding="utf-8"))
    sp = os.path.join(ROOT, "queue", "state.json")
    state = json.load(open(sp)) if os.path.exists(sp) else {"next": 0, "done": {}, "log": []}
    p = posts[state["next"] % len(posts)]
    repo = os.environ.get("GITHUB_REPOSITORY", "OWNER/REPO")
    base = os.environ.get("IMAGE_BASE", f"https://raw.githubusercontent.com/{repo}/main")
    image_url = f"{base}/{p['image']}"
    page, ftoken, ig = os.environ.get("FB_PAGE_ID"), os.environ.get("FB_PAGE_TOKEN"), os.environ.get("IG_USER_ID")
    channels = []
    if page and ftoken: channels.append(("facebook", lambda: post_facebook(page, ftoken, image_url, p["fb_text"])))
    if ig and ftoken: channels.append(("instagram", lambda: post_instagram(ig, ftoken, image_url, p["ig_text"])))
    print(f"post {state['next']}: {p['id']} ({p['kind']}) -> {image_url}")
    if DRY or not channels:
        print("--- facebook ---\n" + p["fb_text"] + "\n--- instagram ---\n" + p["ig_text"])
        if not DRY: print("No channels configured; nothing posted.")
        return 0
    failed = False
    for name, fn in channels:
        if state["done"].get(name): continue
        try:
            res = fn(); state["done"][name] = True
            state["log"].append({"post": p["id"], "channel": name, "result": res, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
            print(name, "ok", res)
        except Exception as e:
            failed = True; print(name, "FAILED:", e, file=sys.stderr)
    if not failed:
        state["next"] += 1; state["done"] = {}
    state["log"] = state["log"][-50:]
    json.dump(state, open(sp, "w"), indent=2)
    return 1 if failed else 0

sys.exit(main())
