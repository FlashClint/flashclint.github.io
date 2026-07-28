import os, sys, re, yaml, markdown, json, shutil
from datetime import datetime

SITE_DIR = "D:/personal_blog/_preview2"
os.makedirs(SITE_DIR, exist_ok=True)

with open("D:/personal_blog/_config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Load templates with frontmatter preserved
layouts = {}
for f in os.listdir("D:/personal_blog/_layouts"):
    if f.endswith(".html"):
        with open(f"D:/personal_blog/_layouts/{f}", "r", encoding="utf-8") as fh:
            raw = fh.read()
        # Parse frontmatter
        parts = raw.split("---", 2)
        fm = yaml.safe_load(parts[1]) if len(parts) >= 3 and parts[1].strip() else {}
        body = parts[2] if len(parts) >= 3 else raw
        layouts[f.replace(".html","")] = {"fm": fm, "body": body}

includes = {}
for f in os.listdir("D:/personal_blog/_includes"):
    if f.endswith(".html"):
        with open(f"D:/personal_blog/_includes/{f}", "r", encoding="utf-8") as fh:
            includes[f] = fh.read()

def get_layout_chain(name):
    chain = []
    while name and name in layouts:
        chain.append(name)
        name = layouts[name]["fm"].get("layout")
    return chain

def process_template(template_str, ctx):
    """Process Liquid template with proper capture handling"""
    result = template_str
    
    # 1. Process {% capture varname %}...{% endcapture %}
    # Evaluate content and store as variable in context
    def do_capture(m):
        varname = m.group(1).strip()
        content = m.group(2)
        # Recursively process the capture content (variables within)
        content_processed = process_template(content, ctx)
        ctx[varname] = content_processed.strip()
        return ""
    result = re.sub(r"\{%-?\s*capture\s+(\w+)\s*-?%\}(.*?)\{%-?\s*endcapture\s*-?%\}", do_capture, result, flags=re.DOTALL)
    
    # 2. Process {% assign x = y %} - store variable
    def do_assign(m):
        varname = m.group(1).strip()
        value = m.group(2).strip()
        ctx[varname] = process_template(value, ctx).strip()
        return ""
    result = re.sub(r"\{%-?\s*assign\s+(\w+)\s*=\s*(.*?)\s*-?%\}", do_assign, result)
    
    # 3. Remove raw/unless/comment
    result = re.sub(r"\{%-?\s*raw\s*-?%\}.*?\{%-?\s*endraw\s*-?%\}", "", result, flags=re.DOTALL)
    result = re.sub(r"\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}", "", result, flags=re.DOTALL)
    
    # 4. Process includes recursively
    def do_include(m):
        fname = m.group(1).strip()
        if fname in includes:
            return process_template(includes[fname], ctx)
        return ""
    result = re.sub(r"\{%-?\s*include\s+([^\s}]+)\s*-?%\}", do_include, result)
    
    # 5. Process for loops
    def do_for(m):
        item_var = m.group(1)
        collection_raw = m.group(2).strip()
        template = m.group(3)
        items = []
        # Resolve collection value from context
        parts = collection_raw.split(".")
        val = ctx
        for p in parts:
            if isinstance(val, dict):
                val = val.get(p, [])
            elif isinstance(val, list):
                val = val
            else:
                val = []
        items = val if isinstance(val, list) else []
        
        results = []
        for item in items:
            ic = dict(ctx)
            if isinstance(item, dict):
                ic[item_var] = item
                for k, v in item.items():
                    ic[k] = v
            else:
                ic[item_var] = item
            results.append(process_template(template, ic))
        return "\n".join(results)
    result = re.sub(r"\{%-?\s*for\s+(\w+)\s+in\s+([^\}]+)\s*-?%\}(.*?)\{%-?\s*endfor\s*-?%\}", do_for, result, flags=re.DOTALL)
    
    # 6. If blocks
    def resolve_var(name, ctx):
        parts = name.split(".")
        val = ctx
        for p in parts:
            if isinstance(val, dict):
                val = val.get(p, None)
            elif isinstance(val, list):
                try: val = val[int(p)] if p.lstrip("-").isdigit() else None
                except: val = None
            else:
                val = None
            if val is None:
                break
        return val
    
    def eval_condition_simple(cond, ctx):
        negate = cond.strip().startswith("not ")
        check = cond.strip()[4:].strip() if negate else cond.strip()
        val = resolve_var(check, ctx)
        is_truthy = bool(val) if val is not None else False
        return (not is_truthy) if negate else is_truthy

    def eval_condition(cond, ctx):
        cond = cond.strip()
        if " and " in cond:
            parts = [p.strip().strip("()").strip() for p in cond.split(" and ")]
            return all(eval_condition_simple(p, ctx) for p in parts)
        if " or " in cond:
            parts = [p.strip().strip("()").strip() for p in cond.split(" or ")]
            return any(eval_condition_simple(p, ctx) for p in parts)
        return eval_condition_simple(cond, ctx)
    
    def do_if_chain(m):
        full = m.group(0)
        inner_m = re.match(r"\{%-?\s*if\s+([^%}]+?)\s*-?%\}(.*)", full, re.DOTALL)
        if not inner_m:
            return ""
        first_cond = inner_m.group(1).strip()
        rest = inner_m.group(2)
        rest = re.sub(r"\{%-?\s*endif\s*-?%\}$", "", rest.strip(), flags=re.DOTALL)
        
        branches = []
        current_cond = first_cond
        remaining = rest
        
        while remaining:
            parts = re.split(r"\{%-?\s*(elsif|else)\s+([^%}]+?)?\s*-?%\}", remaining, maxsplit=1, flags=re.DOTALL)
            if len(parts) == 1:
                branches.append((current_cond, parts[0].strip()))
                remaining = ""
            else:
                content_before = parts[0].strip()
                keyword = parts[1]
                next_cond = parts[2].strip() if keyword == "elsif" else None
                after = parts[3] if len(parts) > 3 else ""
                branches.append((current_cond, content_before))
                if keyword == "else":
                    branches.append(("__else__", after.strip()))
                    remaining = ""
                else:
                    current_cond = next_cond
                    remaining = after
        
        for cond, branch_content in branches:
            if cond == "__else__":
                return process_template(branch_content, ctx)
            if eval_condition(cond, ctx):
                return process_template(branch_content, ctx)
        return ""
    
    result = re.sub(r"\{%-?\s*if\s+([^%}]+?)\s*-?%\}.*?\{%-?\s*endif\s*-?%\}", do_if_chain, result, flags=re.DOTALL)
    result = re.sub(r"\{%-?\s*else\s*-?%\}", "", result)
from datetime import datetime

SITE_DIR = "D:/personal_blog/_preview2"
os.makedirs(SITE_DIR, exist_ok=True)

with open("D:/personal_blog/_config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Load templates with frontmatter preserved
layouts = {}
for f in os.listdir("D:/personal_blog/_layouts"):
    if f.endswith(".html"):
        with open(f"D:/personal_blog/_layouts/{f}", "r", encoding="utf-8") as fh:
            raw = fh.read()
        # Parse frontmatter
        parts = raw.split("---", 2)
        fm = yaml.safe_load(parts[1]) if len(parts) >= 3 and parts[1].strip() else {}
        body = parts[2] if len(parts) >= 3 else raw
        layouts[f.replace(".html","")] = {"fm": fm, "body": body}

includes = {}
for f in os.listdir("D:/personal_blog/_includes"):
    if f.endswith(".html"):
        with open(f"D:/personal_blog/_includes/{f}", "r", encoding="utf-8") as fh:
            includes[f] = fh.read()

def get_layout_chain(name):
    chain = []
    while name and name in layouts:
        chain.append(name)
        name = layouts[name]["fm"].get("layout")
    return chain

def process_template(template_str, ctx):
    """Process Liquid template with proper capture handling"""
    result = template_str
    
    # 1. Process {% capture varname %}...{% endcapture %}
    # Evaluate content and store as variable in context
    def do_capture(m):
        varname = m.group(1).strip()
        content = m.group(2)
        # Recursively process the capture content (variables within)
        content_processed = process_template(content, ctx)
        ctx[varname] = content_processed.strip()
        return ""
    result = re.sub(r"\{%-?\s*capture\s+(\w+)\s*-?%\}(.*?)\{%-?\s*endcapture\s*-?%\}", do_capture, result, flags=re.DOTALL)
    
    # 2. Process {% assign x = y %} - store variable
    def do_assign(m):
        varname = m.group(1).strip()
        value = m.group(2).strip()
        ctx[varname] = process_template(value, ctx).strip()
        return ""
    result = re.sub(r"\{%-?\s*assign\s+(\w+)\s*=\s*(.*?)\s*-?%\}", do_assign, result)
    
    # 3. Remove raw/unless/comment
    result = re.sub(r"\{%-?\s*raw\s*-?%\}.*?\{%-?\s*endraw\s*-?%\}", "", result, flags=re.DOTALL)
    result = re.sub(r"\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}", "", result, flags=re.DOTALL)
    
    # 4. Process includes recursively
    def do_include(m):
        fname = m.group(1).strip()
        if fname in includes:
            return process_template(includes[fname], ctx)
        return ""
    result = re.sub(r"\{%-?\s*include\s+([^\s}]+)\s*-?%\}", do_include, result)
    
    # 5. Process for loops
    def do_for(m):
        item_var = m.group(1)
        collection_raw = m.group(2).strip()
        template = m.group(3)
        items = []
        # Resolve collection value from context
        parts = collection_raw.split(".")
        val = ctx
        for p in parts:
            if isinstance(val, dict):
                val = val.get(p, [])
            elif isinstance(val, list):
                val = val
            else:
                val = []
        items = val if isinstance(val, list) else []
        
        results = []
        for item in items:
            ic = dict(ctx)
            if isinstance(item, dict):
                ic[item_var] = item
                for k, v in item.items():
                    ic[k] = v
            else:
                ic[item_var] = item
            results.append(process_template(template, ic))
        return "\n".join(results)
    result = re.sub(r"\{%-?\s*for\s+(\w+)\s+in\s+([^\}]+)\s*-?%\}(.*?)\{%-?\s*endfor\s*-?%\}", do_for, result, flags=re.DOTALL)
    
    # 6. If blocks
    def do_if(m):
        condition = m.group(1).strip()
        content = m.group(2)
        false_keys = ["comments", "social-share", "show-social-share", "share-links-active",
                      "google_analytics", "gtag", "gtm", "matomo", "disqus", "fb_comment",
                      "commentbox", "giscus", "utterances", "staticman", "mobile-theme-col",
                      "rss-description"]
        true_keys = ["site.title", "site.keywords", "site.author", "site.avatar", "site.site-css"]
        
        if any(k in condition for k in false_keys):
            return ""
        # Check condition truthiness
        negate = condition.startswith("not ")
        check = condition[4:].strip() if negate else condition
        parts = check.split(".")
        val = ctx
        for p in parts:
            if isinstance(val, dict):
                val = val.get(p, None)
            else:
                val = None
        is_truthy = bool(val) if val is not None else False
        if negate:
            return content if not is_truthy else ""
        return content if is_truthy else ""
    result = re.sub(r"\{%-?\s*if\s+([^%}]+?)\s*-?%\}(.*?)\{%-?\s*endif\s*-?%\}", do_if, result, flags=re.DOTALL)
    result = re.sub(r"\{%-?\s*else\s*-?%\}.*?\{%-?\s*endif\s*-?%\}", "", result, flags=re.DOTALL)
    
    # 7. Variables
    def do_var(m):
        expr = m.group(1).strip()
        expr_clean = re.sub(r"\|.*", "", expr).strip()
        parts = expr_clean.split(".")
        val = ctx
        for p in parts:
            if isinstance(val, dict):
                val = val.get(p, "")
            elif isinstance(val, list):
                try:
                    idx = int(p) if p.lstrip("-").isdigit() else None
                    val = val[idx] if idx is not None else ""
                except:
                    val = ""
            else:
                val = ""
        val_str = str(val) if val else ""
        # Apply filters
        for f in re.findall(r"\|(\w+(?::\d+)?)", expr):
            if f == "relative_url":
                val_str = "/" + val_str.lstrip("/") if val_str else ""
            elif f == "absolute_url":
                val_str = "https://flashclint.github.io" + ("/" + val_str.lstrip("/")) if val_str else ""
            elif f == "strip_newlines":
                val_str = val_str.replace("\n", " ")
            elif f == "strip_html":
                val_str = re.sub(r"<[^>]+>", "", val_str)
            elif f == "xml_escape":
                val_str = val_str.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
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
            elif f == "strip_index":
                val_str = re.sub(r"/index\.html$", "/", val_str)
                val_str = re.sub(r"/index$", "/", val_str)
            elif f.startswith("date:"):
                # Simple date filter skip
                pass
            elif f == "default":
                # default filter - second arg is the default value
                pass
        return val_str
    result = re.sub(r"\x7b\x7b\s*(.*?)\s*\x7d\x7d", do_var, result)
    
    # 8. Cleanup remaining Liquid
    result = re.sub(r"\{%[^%]*%\}", "", result)
    result = re.sub(r"\x7b\x7b.*?\x7d\x7d", "", result)
    
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
                fmt = config.get("date_format", "%B %-d, %Y")
                fm["date_str"] = dt.strftime(fmt.replace("%-d", "%#d"))
                fm["year"] = str(dt.year)
            except:
                fm["date"] = datetime.now()
            posts.append(fm)

site_ctx = dict(config)
site_ctx["_posts"] = posts

def render_with_layout_chain(content_html, page_fm, layout_name):
    """Render through layout chain, preserving layout frontmatter as layout.xxx"""
    chain = get_layout_chain(layout_name)
    current = content_html
    
    for name in chain:
        layout_fm = layouts[name]["fm"]
        layout_body = layouts[name]["body"]
        
        # Build context: site + page + layout + content
        ctx = {
            "site": site_ctx,
            "page": page_fm,
            "layout": layout_fm,
            "content": current,
        }
        # Merge layout vars into ctx for direct access
        for k, v in layout_fm.items():
            if k not in ("layout",):
                ctx[k] = v
        # Merge page vars
        for k, v in page_fm.items():
            if k not in ("layout",):
                ctx.setdefault(k, v)
        
        # Inject current content into layout body and process
        tmpl_with = layout_body.replace("{{ content }}", current)
        current = process_template(tmpl_with, ctx)
    
    return current

# Render pages
for out_name, src_path in [
    ("index.html", "D:/personal_blog/index.html"),
    ("aboutme.html", "D:/personal_blog/aboutme.md"),
    ("research.html", "D:/personal_blog/research.md"),
    ("collections.html", "D:/personal_blog/collections.md"),
    ("404.html", "D:/personal_blog/404.html"),
    ("tags.html", "D:/personal_blog/tags.html"),
]:
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
