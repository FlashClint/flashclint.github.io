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

def clean_wikilinks(text):
    """Remove Obsidian wikilinks and block references."""
    # Protect image embeds first
    text = re.sub(r'!\[\[([^\]]+?)\|(\d+)\]\]', r'!!IMG!!\1||\2', text)
    text = re.sub(r'!\[\[([^\]]+)\]\]', r'!!IMG!!\1||', text)

    # Convert [[file#^block|text]] -> text
    text = re.sub(r'\[\[([^\]]+?)#\^([a-z0-9]+)\|(.+?)\]\]', r'\3', text)
    text = re.sub(r'\[\[([^\]]+?)\|(.+?)\]\]', r'\2', text)
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)

    # Restore image markers
    text = re.sub(r'!!IMG!!([^|]+)\|\|(\d*)', r'!!!IMG/\1|\2!!!', text)
    text = re.sub(r'!!IMG!!([^|]+)\|\|', r'!!!IMG/\1!!!', text)

    # Remove ^blockref markers
    text = re.sub(r'\^[a-z0-9]{6}\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\^[a-z0-9]{6}', '', text)
    return text


def convert_images(text, prefix):
    """Convert !!!IMG/ markers to proper markdown images."""
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
        "abstract": ("📋", "#9333ea", "#faf5ff"),
        "success": ("✅", "#16a34a", "#f0fdf4"),
        "question": ("❓", "#2563eb", "#f0f9ff"),
        "danger": ("⚡", "#dc2626", "#fef2f2"),
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
                if re.match(r">\s*\[!\w+\]", lines[j]):  # stop at next callout
                    break
                if not lines[j].startswith(">"):          # stop at non-quote line
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
                f'border-radius: 10px; padding: 12px 16px; margin: 16px 0; box-shadow: 0 1px 4px rgba(0,0,0,0.06);">\n'
                f'  <p style="margin: 0 0 8px 0; font-weight: 600; color: {color};">{icon} {title}</p>\n'
                f'  {inner}\n'
                f'</div>\n'
            )
            result.append(html)
            i = j
        else:
            result.append(line)
            i += 1
    return "\n".join(result)


def fix_broken_chars(text):
    """Fix <<font to <font."""
    text = text.replace("<<font", "<font")
    return text


def copy_images(source_dir, img_prefix, proto_name, images_base):
    """Copy images from Obsidian Images/ folder to blog assets."""
    src = os.path.join(source_dir, "Images", proto_name)
    dst = os.path.join(images_base, img_prefix)
    if not os.path.exists(src):
        print(f"  [WARN] Image source not found: {src}")
        return
    os.makedirs(dst, exist_ok=True)
    count = 0
    for fn in os.listdir(src):
        shutil.copy2(os.path.join(src, fn), os.path.join(dst, fn))
        count += 1
    print(f"  Copied {count} images to {dst}")


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
    images_base = os.path.join(blog_dir, "assets", "img", "protocols")
    os.makedirs(posts_dir, exist_ok=True)

    # Read source file
    with open(args.input, "r", encoding="utf-8-sig") as f:
        raw = f.read()

    # Determine title
    title = args.title
    if not title:
        basename = os.path.splitext(os.path.basename(args.input))[0]
        title = basename.replace("-", " ").replace("_", " ").title()

    # Process content
    content = raw
    content = fix_broken_chars(content)
    content = clean_wikilinks(content)
    content = convert_images(content, args.prefix)
    content = convert_callouts(content)

    # Build tags list
    tags = [t.strip() for t in args.tags.split(",")]

    # Write post
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
    print(f"  Created: {out_name}")

    # Copy images
    source_dir = os.path.dirname(os.path.abspath(args.input))
    # Try common Obsidian image locations
    for images_subdir in ["Images", "images", "attachments"]:
        candidate = os.path.join(source_dir, images_subdir)
        if os.path.exists(candidate):
            # Find the right subfolder by matching topic names
            for topic_dir in os.listdir(candidate):
                topic_path = os.path.join(candidate, topic_dir)
                if os.path.isdir(topic_path):
                    # Check if this topic folder has relevant images
                    files = os.listdir(topic_path)
                    if any(args.prefix.replace("-", " ").split()[0].lower() in f.lower() for f in files):
                        copy_images(os.path.dirname(candidate), args.prefix, topic_dir, images_base)
                        break
            break
    else:
        print("  [INFO] No images directory found. Images must be copied manually.")


if __name__ == "__main__":
    main()
