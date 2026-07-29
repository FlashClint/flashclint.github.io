---
name: obsidian-md-convert
description: Convert Obsidian markdown files (.md) from a local knowledge base into Jekyll-compatible blog posts for a GitHub Pages personal website. Handles callout conversion, image embedding with path checking, math formula preservation, wikilink cleanup, and automatic reference-to-badge conversion. Use when the user wants to publish Obsidian notes, protocols, or articles to a beautiful-jekyll based blog.
---

# Obsidian to Jekyll Converter

Converts an Obsidian `.md` file to a Jekyll blog post for a beautiful-jekyll based GitHub Pages site.

## Quick Start

```bash
python scripts/convert_to_jekyll.py <input.md> <image-prefix> [options]
```

**Example:**
```bash
cd D:\personal_blog
python custom_skills/obsidian-md-convert/scripts/convert_to_jekyll.py \
  "D:\HS-AFM\experiments\protocols\Peakforce Tapping.md" \
  peakforce-tapping \
  --tags protocols,biophysics
```

### Options
| Flag | Default | Description |
|------|---------|-------------|
| `--date` | today | Post date (YYYY-MM-DD) |
| `--tags` | protocols,research-notes | Comma-separated tags |
| `--title` | derived from filename | Post title |
| `--blog-dir` | `.` | Blog root directory |

## Pipeline (automatic)

The script runs these steps in order:

```
Input(.md) → fix chars → clean wikilinks → convert images
           → convert callouts → convert references → Output(.md)
```

### 1. Wikilinks & Block Refs
| Obsidian | Output |
|----------|--------|
| `[[wikilink\|text]]` | `text` (wikilink removed) |
| `[[file#^block\|text]]` | `text` |
| `^abcdef` | removed |

### 2. Images
| Obsidian | Output | Notes |
|----------|--------|-------|
| `![[img.png]]` | `![img.png](/assets/img/protocols/{prefix}/img.png)` | Auto-copied |
| `![[img.png\|400]]` | `<img src=... width="400">` | Sized variant |

The script searches `Images/`, `images/`, `attachments/`, `img/` and subdirectories.
Missing images are reported as warnings.

### 3. Callouts
| Obsidian | Output |
|----------|--------|
| `>[!Note] Title` | `<div class="callout callout-note" markdown="1">...` |
| `>[!Tip] Title` | `<div class="callout callout-tip" markdown="1">...` |
| `>[!Warning] Title` | `<div class="callout callout-warning" markdown="1">...` |

The `markdown="1"` attribute enables markdown processing inside the div (bold, links, code, etc.).

### 4. Math
`$formula$` and `$$display$$` are preserved as-is. Frontmatter includes `mathjax: true`.

### 5. References → Badges (NEW)

The script automatically detects three patterns and converts them into unified `ref-badge` superscripts:

| Source pattern | Badge text | Tooltip |
|---------------|------------|---------|
| `(from <span...>Author</span>)` | sequential number | cleaned author text |
| `(from Plain Author)` | sequential number | plain author text |
| `Ref.1` / `Ref. 2` | sequential number | "Reference X" |

Badges with the **same citation text** get the **same number**.

### 6. Known Fixes
- `<<font` → `<font`
- Orange spans `rgba(240,107,5,...)` → `hl-orange` CSS class

## Output Structure
```
_posts/YYYY-MM-DD-<prefix>.md          # Blog post
assets/img/protocols/<prefix>/         # Copied images
```

## Verification Checklist
After running, check:
1. Post file exists in `_posts/`
2. Images are in `assets/img/protocols/<prefix>/` (warnings shown for missing)
3. Run `git status` to confirm new files
4. Push to GitHub with: `git add -A && git commit -m "..." && git push`

## Manual Edits Still Needed After Conversion
- **Review references**: Open the page after deploying and hover over each `ref` badge to verify tooltips
- **Post title**: Adjust `title` in frontmatter if the auto-derived name is not ideal
- **Tags**: Add or remove tags via the `--tags` parameter
