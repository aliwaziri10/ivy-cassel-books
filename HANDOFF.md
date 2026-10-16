# HANDOFF: social posting for Ivy Cassel and Elif Kessler (written 2026-10-16)

Read this first. It covers both repos: aliwaziri10/ivy-cassel-books and aliwaziri10/elif-kessler-books.

## Who and how to work with him
- The user is **Zia Waziri** (Z-I-A, W-A-Z-I-R-I). Voice-to-text garbles names; verify spellings. Pen name is **Elif Kessler** (with an E), not Alif or Alex.
- He wants **one step at a time**, and **every copyable item (URL, name, text) in its own code block** so it has a copy button.
- He gets frustrated when steps are skipped or guessed. Do not assume he has an account; ask.
- Memory is off on his Claude account, so nothing carries over except this file.

## Hard rules (from novels/FROZEN_DO_NOT_EDIT.md in aliwaziri10/Voxel, dated 2026-10-16)
- Never edit or push to any Kindling Line or Amity Falls folder in Voxel. Read-only.
- Two pen names, two separate reader promises. Never mix them or link them.
  - Ivy Cassel = romantasy, series The Kindling Line.
  - Elif Kessler = slow-burn small-town romance, series The Amity Falls Series (4 books, finished).
- The real repo is aliwaziri10/Voxel, NOT Wazzaboyzz/Voxel.
- Never ask him to paste tokens or keys in chat. They go only into GitHub repo secrets.
- Do not use fake Facebook profiles or fake birth dates. Everything is owned by his one real Facebook account (Zia Waziri); Pages carry the pen names.

## Books and links (links given by Zia; Amazon blocks automated reading, so titles were matched by ORDER, not verified)
Elif Kessler, Amity Falls: 1 Where the Frost Doesn't Reach https://a.co/d/0gndbYmd, 2 What the Valley Still Owes https://a.co/d/02KQnb51, 3 What the Blood Remembers https://a.co/d/0gKBZ0so, 4 The Secret She Kept Forever https://a.co/d/04fD8jSn
Ivy Cassel, Kindling Line: 1 Borrowed Years https://a.co/d/015rGBsc, 2 Keep Me Past the Fire https://a.co/d/0c839mM0, 3 Count Me Through the Dark (proofread, NOT yet published, shown as coming soon).
ACTION: ask Zia to click all 6 links and confirm each opens the right book.

## CONFIRMED done this session
- Both repos exist and are pushed: tools/make_queue.py, tools/poster.py, config.json, images/, queue/posts.json, queue/group_posts.md, SETUP.md, .github/workflows/post.yml (cron Tue/Thu/Sat 14:30 UTC) and build.yml. Ivy queue = 11 posts, Elif = 16. Dry run tested locally.
- Facebook Page "Elif Kessler" created under Zia's account: author category, short bio, profile picture (green "EK" monogram), cover photo (text above the profile circle). He was on Step 3 of 5 of the Page setup (WhatsApp step: told him to skip) and was choosing an Action Button.
- Action button advice: "Shop now" only connects store tools (not Amazon). Use "Learn more" with the Book 1 link if listed, otherwise "Send message".

## NOT done (everything below is still to do)
1. Finish Facebook Page setup (steps 4 and 5 of 5, action button).
2. Elif Kessler Instagram account: email elifkessler123@gmail.com, name Elif Kessler, username elifkessler.books (or with a number). Switch to Professional (Creator). Link it to the Elif Kessler Page (Instagram: Edit profile, Page, connect). Zia runs several Instagram accounts through Accounts Centre.
3. Meta developer app (developers.facebook.com), Graph API Explorer: permissions pages_manage_posts, pages_read_engagement, instagram_basic, instagram_content_publish. Get FB_PAGE_ID, FB_PAGE_TOKEN, IG_USER_ID. Make the token long-lived (verify on Meta's page). Add them as repo secrets in elif-kessler-books, then run the post-to-social workflow once.
4. The whole Ivy Cassel chain: he has NO Gmail for Ivy yet. Create one, then Instagram, then a Facebook Page "Ivy Cassel" (category Author), link them, then steps 3 above for ivy-cassel-books. Then make profile and cover images (reuse the Elif method in warm red/gold #2b1210, #7a2e1f, #f2b36b).
5. Repos must be PUBLIC (Instagram fetches card images from raw.githubusercontent.com). Confirm.
6. Author websites: a generator was built (two static sites with schema markup, sitemap, llms.txt) and sent as book-sites.zip, but NEVER deployed. Optional later: add to the repos and enable GitHub Pages.
7. TikTok: not started. Posts go private until TikTok's audit passes (takes weeks). Skip until Facebook and Instagram work.

## UNVERIFIED (treat as hypotheses)
- Click-by-click Facebook/Instagram steps came from a third-party guide (Leadsie), not Meta's own help pages (those returned no step text). Meta's screens change; ask what he sees.
- Whether Meta app review is needed for posting; the docs read did not say.
- Whether GitHub keeps scheduled workflows alive on a quiet repo. Check the Actions tab after a month.
- Amity Falls Book 2 blurb is thin (the notes in Voxel are archived stubs).

## Tooling notes
- The GitHub connector can read and write repos it has access to, but create_repository returns 403. New repos must be created by Zia on github.com/new, then attached to the session with add_repo (access: push), then cloned and pushed with git. Binary files (images) work through git, not through the file-upload tool.
- Plan is Free: no browser control, no computer control, no scheduled tasks. GitHub Actions does the scheduling.
- WebFetch cannot open a.co / Amazon links (robots disallow).
