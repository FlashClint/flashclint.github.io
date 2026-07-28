import os, sys, re, yaml, markdown, json, shutil
from datetime import datetime

SITE_DIR = "D:/personal_blog/_preview2"
os.makedirs(SITE_DIR, exist_ok=True)

with open("D:/personal_blog/_config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Load templates
layouts = {}
for f in os.listdir("D:/personal_blog/_layouts"):
    if f.endswith(".html"):
        with open(f"D:/personal_blog/_layouts/{f}", "r", encoding="utf-8") as fh:
            layouts[f.replace(".html","")] = fh.read()

includes = {}
for f in os.listdir("D:/personal_blog/_includes"):
    if f.endswith(".html"):
        with open(f"D:/personal_blog/_includes/{f}", "r", encoding="utf-8") as fh:
            includes[f] = fh.read()

def get_layout_chain(name):
    """Get layout inheritance chain [inner, ..., outer]"""
    chain = []
    while name and name in layouts:
        chain.append(name)
        m = re.search(r"^layout:\s*(\w+)", layouts[name], re.MULTILINE)
        name = m.group(1) if m else None
    return chain  # e.g. ["home", "page", "base"]

def strip_frontmatter(text):
    return re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)

def process_template(template_str, ctx):
    """Process Liquid-style template: includes, variables, for loops, if blocks"""
    result = template_str
    
    # Process includes (recursive)
    def do_include(m):
        fname = m.group(1).strip()
        if fname in includes:
            return process_template(strip_frontmatter(includes[fname]), ctx)
        return ""
    result = re.sub(r"\{%-?\s*include\s+([^\s}]+)\s*-?%\}", do_include, result)
    
    # Remove unsupported Liquid tags
    result = re.sub(r"\{%-?\s*(?:assign|endassign|capture|endcapture|raw|endraw|unless|endunless|comment|endcomment)\b[^%]*?-?%\}", "", result)
    
    # For loops
    def do_for(m):
        item_var = m.group(1)
        collection_raw = m.group(2).strip()
        template = m.group(3)
        items = []
        if collection_raw == "site.posts":
            items = ctx.get("site", {}).get("_posts", [])
        elif collection_raw.startswith("paginator.posts"):
            items = ctx.get("site", {}).get("_posts", [])[:5]
        elif collection_raw == "post.tags":
            items = ctx.get("page", {}).get("tags", [])
        elif collection_raw.startswith("site.navbar-links"):
            links = ctx.get("site", {}).get("navbar-links", {})
            items = list(links.items()) if isinstance(links, dict) else []
            item_var = "link"  # Override for this special case
        results = []
        for item in items:
            ic = dict(ctx)
            if isinstance(item, tuple):
                ic[item_var] = {"key": item[0], "value": item[1]}
                ic["key"] = item[0]
                ic["value"] = item[1]
            elif isinstance(item, dict):
                ic[item_var] = item
                for k, v in item.items():
                    ic[k] = v
            else:
                ic[item_var] = item
            results.append(process_template(template, ic))
        return "\n".join(results)
    result = re.sub(r"\{%-?\s*for\s+(\w+)\s+in\s+([^\}]+)\s*-?%\}(.*?)\{%-?\s*endfor\s*-?%\}", do_for, result, flags=re.DOTALL)
    
    # If blocks (keep content if condition is truthy, otherwise remove)
    def do_if(m):
        condition = m.group(1).strip()
        content = m.group(2)
        false_keys = ["comments", "social-share", "show-social-share", "share-links-active",
                      "google_analytics", "gtag", "gtm", "matomo", "disqus", "fb_comment",
                      "commentbox", "giscus", "utterances", "staticman"]
        # If condition checks a variable we know is disabled
        if any(k in condition for k in false_keys):
            return ""
        # Check variable truthiness
        parts = condition.split(".")
        val = ctx
        for p in parts:
            if isinstance(val, dict):
                val = val.get(p, None)
            else:
                val = None
        return content if val else ""
    result = re.sub(r"\{%-?\s*if\s+([^%}]+?)\s*-?%\}(.*?)\{%-?\s*endif\s*-?%\}", do_if, result, flags=re.DOTALL)
    result = re.sub(r"\{%-?\s*else\s*-?%\}.*?\{%-?\s*endif\s*-?%\}", "", result, flags=re.DOTALL)
    
    # Variables
    def do_var(m):
        expr = m.group(1).strip()
        expr_clean = re.sub(r"\|.*", "", expr).strip()
        parts = expr_clean.split(".")
        val = ctx
        for p in parts:
            if isinstance(val, dict):
                val = val.get(p, "")
            else:
                val = ""
        val_str = str(val) if val else ""
        # Apply filters
        for f in re.findall(r"\|(\w+)", expr):
            if f == "relative_url":
                val_str = "/" + val_str.lstrip("/") if val_str else ""
            elif f == "absolute_url":
                val_str = "https://flashclint.github.io" + ("/" + val_str.lstrip("/")) if val_str else ""
            elif f == "strip_newlines":
                val_str = val_str.replace("\n", " ")
            elif f == "strip_html":
                val_str = re.sub(r"<[^>]+>", "", val_str)
            elif f == "markdownify":
                val_str = markdown.markdown(val_str, extensions=["extra"])
            elif f.startswith("truncatewords"):
                n = 50
                m2 = re.search(r"(\d+)", f)
                if m2: n = int(m2.group(1))
                val_str = " ".join(val_str.split()[:n])
            elif f == "number_of_words":
                val_str = str(len(val_str.split()))
            elif f == "uri_escape":
                from urllib.parse import quote
                val_str = quote(val_str)
        return val_str
    result = re.sub(r"\x7b\x7b\s*(.*?)\s*\x7d\x7d", do_var, result)
    
    # Cleanup remaining Liquid syntax
    result = re.sub(r"\{%[^%]*%\}", "", result)
    result = re.sub(r"\x7b\x7b[^}]*\x7d\x7d", "", result)
    
    return result

# Parse posts
posts = []
for f in sorted(os.listdir("D:/personal_blog/_posts"), reverse=True):
    if f.endswith(".md"):
        with open(f"D:/personal_blog/_posts/{f}", "r", encoding="utf-8") as fh:
            content = fh.read()
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1])
            body = parts[2].strip()
            fm["url"] = "/" + f.replace(".md", ".html")
            fm["id"] = f.replace(".md", "")
            fm["excerpt"] = re.sub(r"\s+", " ", body[:300]).strip()[:200]
            fm["body"] = body
            fm["content"] = markdown.markdown(body, extensions=["extra", "codehilite"])
            try:
                dt = datetime.strptime(f[:10], "%Y-%m-%d")
                fm["date"] = dt
                fm["date_str"] = dt.strftime("%B %-d, %Y")
                fm["year"] = str(dt.year)
            except:
                fm["date"] = datetime.now()
            posts.append(fm)

site_ctx = dict(config)
site_ctx["_posts"] = posts

def render_with_layout_chain(content_html, page_fm, layout_name):
    """Render content through layout chain from inside out"""
    chain = get_layout_chain(layout_name)
    current = content_html
    
    # For each layout (innermost to outermost), wrap the content
    for name in chain:  # ["home", "page", "base"] for home layout
        tmpl = strip_frontmatter(layouts[name])
        # Replace {{ content }} with current rendered content
        tmpl_with = tmpl.replace("{{ content }}", current)
        # Create context for this level
        ctx = {"site": site_ctx, "page": page_fm, "content": current}
        # Process
        current = process_template(tmpl_with, ctx)
    
    return current

# Render pages
pages_list = [
    ("index.html", "D:/personal_blog/index.html"),
    ("aboutme.html", "D:/personal_blog/aboutme.md"),
    ("research.html", "D:/personal_blog/research.md"),
    ("collections.html", "D:/personal_blog/collections.md"),
    ("404.html", "D:/personal_blog/404.html"),
    ("tags.html", "D:/personal_blog/tags.html"),
]

for out_name, src_path in pages_list:
    with open(src_path, "r", encoding="utf-8") as f:
        raw = f.read()
    parts = raw.split("---", 2)
    if len(parts) >= 3:
        fm = yaml.safe_load(parts[1])
        body = parts[2].strip()
        is_md = src_path.endswith(".md")
        body_html = markdown.markdown(body, extensions=["extra"]) if is_md else body
        rendered = render_with_layout_chain(body_html, fm, fm.get("layout", "page"))
        with open(f"{SITE_DIR}/{out_name}", "w", encoding="utf-8") as fh:
            fh.write(rendered)
        print(f"  Page: {out_name}")

# Render posts
for post in posts:
    rendered = render_with_layout_chain(post["content"], post, post.get("layout", "post"))
    fname = post["id"] + ".html"
    with open(f"{SITE_DIR}/{fname}", "w", encoding="utf-8") as fh:
        fh.write(rendered)
    print(f"  Post: {fname}")

# Copy assets
if os.path.exists("D:/personal_blog/assets"):
    dst = f"{SITE_DIR}/assets"
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree("D:/personal_blog/assets", dst)

print(f"\nDone! Preview at: {SITE_DIR}")


