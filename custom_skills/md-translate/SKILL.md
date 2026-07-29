---
name: md-translate
description: Translate markdown files from Chinese or Chinese/English mixed content to academic English, with specialized domain knowledge in biophysics, soft matter physics, scanning probe microscopy (AFM, HS-AFM, SICM), membrane biophysics, and liposome assays. Use when the user asks to translate markdown files containing scientific protocols, research notes, or lab documentation involving these domains.
---

# MD Translate

## Overview

Translate markdown files from Chinese or Chinese/English mixed content to academic English. Specialized for scientific and technical domains: scanning probe microscopy (AFM, HS-AFM, SICM, PeakForce Tapping), soft matter physics, biophysics, membrane biophysics, and liposome assays.

## Core Rules

1. **Preserve formula syntax exactly as-is**: Keep $...$ (inline) and ... (display) LaTeX delimiters. Do NOT convert to escaped parens.
2. **Preserve emoji characters exactly as-is**: Do not change or replace any Unicode emoji in the source file.
3. **Preserve original indentation**: Do not add or remove leading whitespace. Match the original file indentation pattern for each line.
4. **Preserve HTML callout structures**: Keep div, sup, font, span, u, sub, img and other inline HTML tags and attributes unchanged.
5. **Preserve image paths and links**: Do not modify URLs, image paths or hyperlinks.
6. **Preserve frontmatter**: Keep YAML frontmatter (title, tags, layout, mathjax, comments, etc.) as-is unless the title itself needs translation.
7. **Keep reference badges**: Keep sup class=ref-badge tags and title attributes unchanged.
8. **No extra markers**: Do not add any end-of-file markers.

## Translation Style

- **Tone**: Concise, precise, academic. Use standard scientific English.
- **Omissions**: If a Chinese sentence is redundant or missing grammatical elements, trim or complete it silently.
- **Terminology**: Refer to references/terminology.md for domain-specific vocabulary conventions.

## Workflow

1. Read the source markdown file.
2. Preserve frontmatter, formula delimiters, emoji, and all HTML tags.
3. Translate all Chinese text sections and mixed-language paragraphs.
4. Retain verbatim any English text that is already correct academic English.
5. Write output to the specified target path (typically original-name_Eng.md).

## Reference File

See references/terminology.md for domain-specific term mappings.
