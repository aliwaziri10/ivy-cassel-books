#!/usr/bin/env python3
"""Build the post queue and the card images from config.json.
Run:  pip install pillow && python3 tools/make_queue.py
Re-run after editing config.json (e.g. when a book goes from "coming-soon" to "published")."""
import json, os, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
os.makedirs(os.path.join(ROOT, "images"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "queue"), exist_ok=True)

W, H = 1080, 1350
FONTS = ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]

def font(size, bold=True):
    for p in FONTS if bold else FONTS[::-1]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def card(name, blocks):
    """blocks: list of (text, size, bold, color_key). Text is wrapped to fit."""
    c = cfg["colors"]
    top, bot = hexrgb(c["bg1"]), hexrgb(c["bg2"])
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(top, bot, y / H))
    d.rectangle([60, 60, W - 60, H - 60], outline=hexrgb(c["accent"]), width=4)
    # measure
    laid = []
    total = 0
    for text, size, bold, ck in blocks:
        f = font(size, bold)
        width_chars = max(8, int((W - 240) / (size * 0.56)))
        lines = textwrap.wrap(text, width=width_chars) or [""]
        h = int(size * 1.3) * len(lines)
        laid.append((lines, f, size, ck, h))
        total += h + 36
    y = (H - total) // 2
    for lines, f, size, ck, h in laid:
        for ln in lines:
            w = d.textlength(ln, font=f)
            d.text(((W - w) / 2, y), ln, font=f, fill=hexrgb(c[ck]))
            y += int(size * 1.3)
        y += 36
    img.save(os.path.join(ROOT, "images", name), "JPEG", quality=92)  # Instagram needs JPEG
    return f"images/{name}"

author, series, total = cfg["author"], cfg["series"], len(cfg["books"])
tags = " ".join(cfg["hashtags"])
posts, groups = [], []

def add(pid, kind, image, body, link=None, group_hook=False):
    fb = body + (f"\n\nGet it on Amazon: {link}" if link else "")
    ig = body + ("\n\nLink in bio." if link else "") + f"\n\n{tags}"
    posts.append({"id": pid, "kind": kind, "image": image, "fb_text": fb, "ig_text": ig})
    if group_hook:
        groups.append(f"### {pid}\n\n{fb}\n\n(image: {image})\n")

def slug(t): return "".join(ch if ch.isalnum() else "-" for ch in t.lower()).strip("-")

per_book = []
for b in cfg["books"]:
    s = slug(b["title"])
    live = b["status"] == "published" and b.get("link")
    seq = []
    # 1 hook
    if live:
        img = card(f"{s}-hook.jpg", [(series.upper(), 30, False, "accent"), (b["title"], 78, True, "fg"),
                                      (f"Book {b['n']} of {total}", 34, False, "muted"), (b["short"], 36, False, "fg"),
                                      (f"by {author}", 38, True, "accent")])
        seq.append(add(f"{s}-hook", "hook", img,
            f"{b['short']}\n\n{b['title']} is book {b['n']} of {total} in {series} by {author}.\n\nWould you read it?", b["link"], True))
        # 2 tropes
        img = card(f"{s}-tropes.jpg", [(b["title"], 64, True, "fg"), ("TROPES", 30, False, "accent")] +
                   [(t, 40, False, "fg") for t in b["tropes"][:6]] + [(f"by {author}", 34, True, "accent")])
        seq.append(add(f"{s}-tropes", "tropes", img,
            f"What's inside {b['title']}:\n" + "\n".join(f"- {t}" for t in b["tropes"]) + "\n\nWhich one gets you every time?", b["link"], True))
        # 3 buy
        img = card(f"{s}-buy.jpg", [(b["title"], 78, True, "fg"), (f"{series}, Book {b['n']}", 34, False, "muted"),
                                     ("Available on Amazon", 42, True, "accent"), (f"by {author}", 38, False, "fg")])
        seq.append(add(f"{s}-buy", "buy", img,
            f"{b['title']} by {author} is available on Amazon.\n\n{b['short']}", b["link"]))
    else:
        img = card(f"{s}-soon.jpg", [(series.upper(), 30, False, "accent"), (b["title"], 78, True, "fg"),
                                      ("COMING SOON", 44, True, "accent"), (f"Book {b['n']} of {total}", 34, False, "muted"),
                                      (f"by {author}", 38, False, "fg")])
        seq.append(add(f"{s}-soon", "soon", img,
            f"Coming soon: {b['title']}, book {b['n']} of {total} in {series} by {author}.\n\nFollow along so you don't miss the release."))
    per_book.append([x for x in seq if x is not None])

# series-level
order = [f"{b['n']}. {b['title']}" + ("" if b["status"] == "published" else " (coming soon)") for b in cfg["books"]]
img = card("series-order.jpg", [(series.upper(), 34, False, "accent"), ("READING ORDER", 56, True, "fg")] +
           [(o, 38, False, "fg") for o in order] + [(f"by {author}", 36, True, "accent")])
add("series-order", "order", img, f"{series} by {author}, in reading order:\n" + "\n".join(order) + "\n\nStart at book 1 and follow it through.", None, True)

for i, q in enumerate(cfg["questions"]):
    img = card(f"question-{i+1}.jpg", [(q, 62, True, "fg"), (f"{author}", 34, True, "accent")])
    add(f"question-{i+1}", "question", img, q + "\n\nTell us in the comments.", None, True)

# Interleave so books and kinds rotate: take round-robin across per-book sequences,
# then drop the series-level posts in between.
series_posts = [p for p in posts if p["id"] == "series-order" or p["id"].startswith("question-")]
book_posts = [p for p in posts if p not in series_posts]
by_book = {}
for p in book_posts:
    by_book.setdefault(p["id"].rsplit("-", 1)[0], []).append(p)
rounds, order_out = max(len(v) for v in by_book.values()), []
for r in range(rounds):
    for v in by_book.values():
        if r < len(v):
            order_out.append(v[r])
final, si = [], 0
for i, p in enumerate(order_out):
    final.append(p)
    if (i + 1) % 3 == 0 and si < len(series_posts):
        final.append(series_posts[si]); si += 1
final += series_posts[si:]

json.dump(final, open(os.path.join(ROOT, "queue", "posts.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(os.path.join(ROOT, "queue", "group_posts.md"), "w", encoding="utf-8").write(
    "# Posts to paste into reader groups by hand\n\nPost these yourself, only where the group's rules allow author promotion "
    "(many have a weekly self-promo thread). One post per group per week at most.\n\n" + "\n".join(groups))
print(f"{len(final)} posts queued, {len(groups)} group drafts")
