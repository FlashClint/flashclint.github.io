---
name: obsidian-md-convert
description: Convert Obsidian markdown files (.md) from a local knowledge base into Jekyll-compatible blog posts for a GitHub Pages personal website. Handles callout conversion, image embedding, math formula preservation, wikilink cleanup, and reference formatting. Use when the user wants to publish Obsidian notes, protocols, or articles to a beautiful-jekyll based blog.
---

# Obsidian to Jekyll Converter

Converts an Obsidian `.md` file to a Jekyll blog post for a beautiful-jekyll based GitHub Pages site.

## Quick Start

```bash
python scripts/convert_to_jekyll.py <input.md> <image-prefix> [--date YYYY-MM-DD] [--tags tag1,tag2]
```

- `<input.md>`: Path to the Obsidian markdown file
- `<image-prefix>`: Subfolder name under `assets/img/protocols/` for images (e.g., `calcein-leakage`)
- `--date`: Post date (default: today)
- `--tags`: Comma-separated tags (default: `protocols,research-notes`)

Output: Jekyll post file in `_posts/` and images copied to `assets/img/protocols/<prefix>/`.

## Conversion Rules

### 1. Math Formulas (Preserved)
| Obsidian | Jekyll | Example |
|----------|--------|---------|
| `$formula$` | `$formula$` (keep) | `$E = mc^2$` |
| `$$formula$$` | `$$formula$$` (keep) | `$$\sum x_i$$` |

Add `mathjax: true` to post frontmatter (automatic).

### 2. Images
| Obsidian | Jekyll |
|----------|--------|
| `![[file.png]]` | `![file.png](/assets/img/protocols/{prefix}/file.png)` |
| `![[file.png\|400]]` | `<img src="..." width="400" style="max-width:100%;height:auto;">` |

Images are copied from `Images/<topic>/` to `assets/img/protocols/<prefix>/`.

### 3. Callouts
| Obsidian | HTML Output |
|----------|-------------|
| `>[!Note] Title` | `<div class="callout callout-note" markdown="1">...` |
| `>[!Tip] Title` | `<div class="callout callout-tip" markdown="1">...` |
| `>[!Warning] Title` | `<div class="callout callout-warning" markdown="1">...` |

- The `markdown="1"` attribute enables markdown rendering inside the div
- Consecutive callouts are separated (not merged)
- Callout content includes the title and all following indented lines

### 4. Wikilinks & References
| Obsidian | Jekyll |
|----------|--------|
| `[[wikilink\|text]]` | `text` |
| `[[file#^block\|text]]` | `text` |
| `^blockref` | (removed) |

### 5. Reference Badges
After conversion, manually replace citation markers with:
- `Ref.X` → `<sup class="ref-badge" title="Full citation">ref</sup>`
- `(from Author, Source)` → `<sup class="ref-badge" title="Author, Source">ref</sup>`

### 6. Known Fixes
- `<<font color=...>` → `<font color=...>` (double less-than sign)
- Orange highlights: `rgba(240, 107, 5, ...)` → keep (works as-is)

## Output Structure
```
_posts/YYYY-MM-DD-<prefix>.md    # Blog post file
assets/img/protocols/<prefix>/   # Copied images
```

## Frontmatter Generated
```yaml
---
layout: post
title: "..."
date: YYYY-MM-DD
tags: [protocols, research-notes]
mathjax: true
comments: true
---
```
