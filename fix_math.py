import re

bs = chr(92)  # backslash

for fname in ["2026-07-28-calcein-leakage.md", "2026-07-28-peakforce-tapping.md"]:
    path = "D:/personal_blog/_posts/" + fname
    content = open(path, "r", encoding="utf-8").read()
    
    # Step 1: Protect $$...$$ display math
    display_matches = re.findall(r"\$\$[^$]*\$\$", content)
    for i, dm in enumerate(display_matches):
        content = content.replace(dm, f"!!DM{i}!!", 1)
    
    # Step 2: Convert $...$ (inline) -> \\(...\\)
    # Input has $x$, output needs \\(x\\)
    def convert(m):
        inner = m.group(1).strip()
        # Output: \\(  inner  \\)
        return f"{bs}{bs}({inner}{bs}{bs})"
    
    content = re.sub(r"\$(?!\$)([^$\n]+?)\$(?!\$)", convert, content)
    
    # Step 3: Restore display math
    for i, dm in enumerate(display_matches):
        content = content.replace(f"!!DM{i}!!", dm, 1)
    
    # Count inline math
    inline_count = content.count(f"{bs}{bs}(")
    print(f"{fname}: {inline_count} inline math expressions")
    
    open(path, "w", encoding="utf-8").write(content)

print("Done!")
