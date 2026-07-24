import json
import os
import re
import sys
from datetime import date
from pathlib import Path

data = json.loads(os.environ["JSON"])

method_name = data["method_name"].strip()
slug = re.sub(r"[^a-z0-9]+", "-", method_name.lower()).strip("-")

file = Path("methods") / f"{slug}.md"

if not file.exists():
    print(f"::error::Method not found: {file}")
    sys.exit(1)

author = data.get("author") or "Anonymous"
entry = f"\n### Experience by {author} — {date.today().isoformat()}\n\n{data['experience'].strip()}\n"

md = file.read_text(encoding="utf-8")

if "## Experience" not in md:
    print("::error::No '## Experience' section in method file")
    sys.exit(1)

md = md.replace("## Experience\n", "## Experience\n" + entry, 1)
file.write_text(md, encoding="utf-8")
