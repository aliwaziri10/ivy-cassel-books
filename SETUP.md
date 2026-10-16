# Setup (one time, about 30 minutes)

This repo posts the next item in `queue/posts.json` to your Facebook Page and Instagram account on a schedule
(Tue/Thu/Sat, see `.github/workflows/post.yml`). It never posts anything not in the queue.

1. **Create the repo on GitHub as PUBLIC** and upload everything in this folder (keep the `.github` folder).
   It must be public because Instagram downloads the card images from a public URL. This repo contains
   no manuscripts, only cards and captions.
2. **Accounts.** You need a Facebook Page and an Instagram *professional* account (Creator or Business) linked to that Page.
   Use a separate Page and Instagram for each pen name.
3. **Meta developer app.** Go to developers.facebook.com, create an app, and add the Facebook Login and Instagram permissions:
   `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`.
   Meta may require app review before posting works for accounts you don't own. Posting to your own Page/Instagram
   while you are the app admin works in development mode.
4. **Get three values** (Graph API Explorer is the easiest way):
   - `FB_PAGE_TOKEN`: a long-lived Page access token
   - `FB_PAGE_ID`: your Facebook Page ID
   - `IG_USER_ID`: your Instagram professional account ID
5. **Add them in GitHub:** Settings > Secrets and variables > Actions > New repository secret (one per value).
6. **Test:** Actions tab > "post-to-social" > Run workflow. Check your Page and Instagram.
   Until the secrets exist, the workflow only prints what it would post.
7. **Check the Actions tab now and then.** GitHub can pause scheduled workflows on repos that go quiet. The posting
   bot commits `queue/state.json` after each run, which should keep the repo active, but verify after a month.

## Maintenance
- When a book is published or its link changes, edit `config.json`, then run `pip install pillow && python3 tools/make_queue.py`
  and commit the new `queue/` and `images/`.
- The queue loops when it reaches the end. Add new angles to `tools/make_queue.py` over time to keep the feed fresh.
- `queue/group_posts.md` has drafts for reader groups. Post those by hand, only where group rules allow author promotion.
- Local test: `python3 tools/poster.py --dry-run`
