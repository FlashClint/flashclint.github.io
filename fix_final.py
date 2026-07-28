import re, sys

# Fix _config.yml
cfg = open("D:/personal_blog/_config.yml", "r", encoding="utf-8").read()
cfg = cfg.replace('Protocols: "tag/protocols"', 'Protocols: "/tags#protocols"')
cfg = cfg.replace('Research Notes: "tag/research-notes"', 'Research Notes: "/tags#research-notes"')
cfg = cfg.replace("  math_engine: mathjax\n  math_engine: mathjax", "  math_engine: mathjax")
open("D:/personal_blog/_config.yml", "w", encoding="utf-8").write(cfg)
print("Config fixed")

# Fix inline math: $x$ -> \(x\)
dollar = chr(36)
bs = chr(92)
for fname in ["2026-07-28-calcein-leakage.md", "2026-07-28-peakforce-tapping.md"]:
    path = "D:/personal_blog/_posts/" + fname
    content = open(path, "r", encoding="utf-8").read()
    
    # Protect $$...$$ display math
    display_maths = re.findall(r"\$\$[^$]*\$\$", content)
    for i, dm in enumerate(display_maths):
        placeholder = f"!!DM{i}!!"
        content = content.replace(dm, placeholder, 1)
    
    # Convert $...$ (inline) -> \(...\)
    def convert(m):
        inner = m.group(1).strip()
        return f"{bs}({inner}{bs})"
    content = re.sub(r"\$(?!\$)([^$\n]+?)\$(?!\$)", convert, content)
    
    # Restore display math
    for i, dm in enumerate(display_maths):
        content = content.replace(f"!!DM{i}!!", dm, 1)
    
    open(path, "w", encoding="utf-8").write(content)
    print(f"Fixed inline math in {fname}")

# Verify
cfg2 = open("D:/personal_blog/_config.yml", "r", encoding="utf-8").read()
print(f"math_engine count: {cfg2.count('math_engine')}")
print(f"Protocols nav correct: {'/tags#protocols' in cfg2}")
