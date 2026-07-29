#!/usr/bin/env python3
"""
Obsidian-to-Jekyll converter: converts an Obsidian markdown file into a Jekyll blog post.

Usage:
    python convert_to_jekyll.py <input.md> <image-prefix> [--date YYYY-MM-DD] [--tags tag1,tag2]

Example:
    python convert_to_jekyll.py "D:/HS-AFM/experiments/protocols/My Protocol.md" my-protocol --tags protocols,biophysics
"""

import re, os, shutil, argparse
from datetime import date

# ── helpers ──────────────────────────────────────────────

def clean_wikilinks(text):
    """Remove Obsidian wikilinks and block references, protect image embeds."""
    text = re.sub(r'!\[\[([^\]]+?)\|(\d+)\]\]', r'!!IMG!!\1||\2', text)
    text = re.sub(r'!\[\[([^\]]+)\]\]', r'!!IMG!!\1||', text)
    text = re.sub(r'\[\[([^\]]+?)#\^([a-z0-9]+)\|(.+?)\]\]', r'\3', text)
    text = re.sub(r'\[\[([^\]]+?)\|(.+?)\]\]', r'\2', text)
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'!!IMG!!([^|]+)\|\|(\d*)', r'!!!IMG/\1|\2!!!', text)
    text = re.sub(r'!!IMG!!([^|]+)\|\|', r'!!!IMG/\1!!!', text)
    text = re.sub(r'\^[a-z0-9]{6}\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\^[a-z0-9]{6}', '', text)
    return text


def convert_images(text, prefix):
    """Convert !!!IMG/ markers to proper markdown images or <img> tags."""
    def repl(m):
        fname = m.group(1)
        w = m.group(2)
        path = f"/assets/img/protocols/{prefix}/{fname}"
        if w:
            return f'<img src="{path}" alt="{fname}" width="{w}" style="max-width:100%;height:auto;">'
        return f'![{fname}]({path})'
    return re.sub(r'!!!IMG/([^!|]+)(?:\|(\d+))?!!!', repl, text)


def convert_callouts(text):
    """Convert Obsidian >[!Note] callouts to HTML divs with markdown=1."""
    styles = {
        "note": ("💡", "#2563eb", "#eff6ff"),
        "tip":  ("💡", "#d97706", "#fffbeb"),
        "warning": ("⚠️", "#dc2626", "#fef2f2"),
        "info": ("ℹ️", "#2563eb", "#eff6ff"),
    }
    lines = text.split("\n")
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r">\s*\[!(\w+)\]\s*(.*)", line)
        if m:
            ctype = m.group(1).lower()
            title = m.group(2).strip() or ctype.capitalize()
            icon, color, bg = styles.get(ctype, ("📝", "#6b7280", "#f9fafb"))
            content_lines = []
            j = i + 1
            while j < len(lines):
                if re.match(r">\s*\[!\w+\]", lines[j]):
                    break
                if not lines[j].startswith(">"):
                    if lines[j].strip() == "":
                        j += 1
                        continue
                    break
                cleaned = re.sub(r"^>\s?", "", lines[j])
                content_lines.append(cleaned)
                j += 1
            inner = "\n".join(content_lines).strip()
            html = (
                f'<div class="callout callout-{ctype}" markdown="1" '
                f'style="background: {bg}; border-left: 4px solid {color}; '
                f'border-radius: 10px; padding: 12px 16px; margin: 16px 0; '
                f'box-shadow: 0 1px 4px rgba(0,0,0,0.06);">\n'
                f'  <p style="margin: 0 0 8px 0; font-weight: 600; color: {color};">'
                f'{icon} {title}</p>\n'
                f'  {inner}\n</div>\n'
            )
            result.append(html)
            i = j
        else:
            result.append(line)
            i += 1
    return "\n".join(result)


# ── reference-badge conversion ───────────────────────────

def convert_references(text):
    """
    Convert citation patterns into unified <sup class="ref-badge"> markup.

    Detected patterns (in priority order):
      1.  (from <span ...styled...>Author, Source</span>)
      2.  (from Author, Source)
      3.  Ref.X
      4.  Standalone orange-highlighted author names
    """
    # Collect all unique citations first
    citations = []
    used_titles = set()

    def add_citation(raw, clean_title):
        """Return a unique ref-badge for this citation."""
        if clean_title not in used_titles:
            used_titles.add(clean_title)
            citations.append(clean_title)
        # Use 1-based index as superscript text
        idx = citations.index(clean_title) + 1
        num = idx if len(citations) <= 20 else "ref"
        idx_text = str(num)
        return f'<sup class="ref-badge" title="{clean_title}">{idx_text}</sup>'

    # Priority 1: (from <span ...styled...>)  – orange-highlighted
    def repl_from_span(m):
        raw = m.group(1)
        clean = re.sub(r'<[^>]+>', '', raw)
        clean = re.sub(r'\s+', ' ', clean).strip()
        clean = clean.replace("~~", "").replace("&amp;", "&")
        return add_citation(raw, clean)

    text = re.sub(
        r'\(from\s*<span[^>]*>([^<]+)</span>(?:\s*&amp;\s*<span[^>]*>([^<]+)</span>)?\s*\)',
        repl_from_span, text
    )

    # Priority 2: (from plain text) – not inside a span
    def repl_from_plain(m):
        clean = m.group(1).strip()
        clean = re.sub(r'\s+', ' ', clean).strip()
        return add_citation(m.group(0), clean)

    text = re.sub(r'\(from\s*([^)]+)\)', repl_from_plain, text)

    # Priority 3: Ref.X (no spaces, e.g. "Ref.1", "Ref. 2")
    def repl_ref(m):
        # Try to infer a meaningful title (the text may be inside a callout)
        return add_citation(m.group(0), f"Reference {m.group(1)}")

    text = re.sub(r'Ref\.\s*(\d+)', repl_ref, text)

    return text


# ── image copy & path check ──────────────────────────────

def copy_and_check_images(source_dir, prefix, blog_dir):
    """
    Copy images from Obsidian's Images/ folder and report any missing ones.
    Returns list of (status, path) tuples.
    """
    blog_assets = os.path.join(blog_dir, "assets", "img", "protocols", prefix)
    os.makedirs(blog_assets, exist_ok=True)

    # Search for image source folders
    image_roots = []
    for candidate in ["Images", "images", "attachments", "img"]:
        p = os.path.join(source_dir, candidate)
        if os.path.isdir(p):
            image_roots.append(p)
            # Check subdirectories
            for sub in os.listdir(p):
                sp = os.path.join(p, sub)
                if os.path.isdir(sp):
                    image_roots.append(sp)

    # Extract referenced filenames from the original markdown
    with open(args.input, "r", encoding="utf-8-sig") as f:
        raw = f.read()

    referenced = set(re.findall(r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|svg))', raw, re.IGNORECASE))
    results = []

    for fname in sorted(referenced):
        found = False
        src_path = None
        for root in image_roots:
            candidate = os.path.join(root, fname)
            if os.path.exists(candidate):
                src_path = candidate
                found = True
                break

        if found and src_path:
            dst = os.path.join(blog_assets, fname)
            shutil.copy2(src_path, dst)
            results.append(("OK", fname))
        else:
            results.append(("MISSING", fname))

    return results


# ── orphan span fix ──────────────────────────────────────

def fix_orphan_spans(text):
    """Replace remaining orange-highlight spans with hl-orange class."""
    text = re.sub(
        r'<span style="background:rgba\(240,\s*107,\s*5,\s*[^)]+\)">(.*?)</span>',
        r'<span class="hl-orange">\1</span>', text
    )
    text = text.replace("<<font", "<font")
    return text


# ── main ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Convert Obsidian .md to Jekyll blog post")
    parser.add_argument("input", help="Path to the Obsidian markdown file")
    parser.add_argument("prefix", help="Image prefix (subfolder under assets/img/protocols/)")
    parser.add_argument("--date", default=str(date.today()), help="Post date (YYYY-MM-DD)")
    parser.add_argument("--tags", default="protocols,research-notes", help="Comma-separated tags")
    parser.add_argument("--title", default=None, help="Post title (default: derived from filename)")
    parser.add_argument("--blog-dir", default=".", help="Blog root directory (default: current dir)")
    args = parser.parse_args()

    blog_dir = os.path.abspath(args.blog_dir)
    posts_dir = os.path.join(blog_dir, "_posts")
    os.makedirs(posts_dir, exist_ok=True)

    # Read source
    with open(args.input, "r", encoding="utf-8-sig") as f:
        raw = f.read()

    # Derive title
    title = args.title
    if not title:
        basename = os.path.splitext(os.path.basename(args.input))[0]
        title = basename.replace("-", " ").replace("_", " ").title()

    # ── pipeline ──
    content = raw
    content = fix_orphan_spans(content)
    content = clean_wikilinks(content)
    content = convert_images(content, args.prefix)
    content = convert_callouts(content)
    content = convert_references(content)

    # Build frontmatter
    tags = [t.strip() for t in args.tags.split(",")]
    post = f"""---
layout: post
title: "{title}"
date: {args.date}
tags: [{', '.join(tags)}]
mathjax: true
comments: true
---

"""
    post += content

    out_name = f"{args.date}-{args.prefix}.md"
    out_path = os.path.join(posts_dir, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(post)
    print(f"[OK] Post written: {out_name}")

    # ── image copy ──
    source_dir = os.path.dirname(os.path.abspath(args.input))
    image_results = copy_and_check_images(source_dir, args.prefix, blog_dir)

    ok = [r for r in image_results if r[0] == "OK"]
    missing = [r for r in image_results if r[0] == "MISSING"]
    if ok:
        print(f"[OK] Images copied to assets/img/protocols/{args.prefix}/ ({len(ok)} files)")
    if missing:
        for _, fname in missing:
            print(f"[WARN] Image not found: {fname}  – copy manually")

    # ── reference summary ──
    print(f"[INFO] Citations converted to ref-badge markers.")
    print(f"[INFO] After posting, verify by visiting the site and hovering over each superscript.")


if __name__ == "__main__":
    main()
