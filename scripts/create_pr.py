#!/usr/bin/env python3
import argparse
import os
import re
from datetime import datetime

METHODS_DIR = "methods"

FIELD_TITLES = [
    "Method Name", "Method URL", "Purpose", "Underlying Theory / Principles",
    "Process (High-level)", "Experience", "Author", "Industry",
    "Organization Size", "Teams Applied To", "People Per Team", "Roles",
    "Leadership or Hierarchy Levels Involved", "Frequency", "Time Period",
    "Layers between you and the Customer", "When it breaks", "Tips",
]


def parse_value(body, title):
    others = "|".join(re.escape(t) for t in FIELD_TITLES if t != title)
    pattern = rf"### {re.escape(title)}\s*\n+(.*?)(?=\n### (?:{others})\s*\n|\Z)"
    match = re.search(pattern, body, re.DOTALL)
    if not match:
        return ""
    value = match.group(1).strip()
    return "" if value == "_No response_" else value


def yaml_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def create_method_file(body):
    os.makedirs(METHODS_DIR, exist_ok=True)

    name = parse_value(body, "Method Name")
    url = parse_value(body, "Method URL")
    purpose = parse_value(body, "Purpose")
    theory = parse_value(body, "Underlying Theory / Principles")
    process = parse_value(body, "Process (High-level)")
    experience = parse_value(body, "Experience")
    author = parse_value(body, "Author")

    optional = [
        ("Industry", parse_value(body, "Industry")),
        ("Organization Size", parse_value(body, "Organization Size")),
        ("Teams Applied To", parse_value(body, "Teams Applied To")),
        ("People Per Team", parse_value(body, "People Per Team")),
        ("Roles", parse_value(body, "Roles")),
        ("Leadership or Hierarchy Levels Involved",
         parse_value(body, "Leadership or Hierarchy Levels Involved")),
        ("Frequency", parse_value(body, "Frequency")),
        ("Time Period", parse_value(body, "Time Period")),
        ("Layers between you and the Customer",
         parse_value(body, "Layers between you and the Customer")),
        ("When it breaks", parse_value(body, "When it breaks")),
        ("Tips", parse_value(body, "Tips")),
    ]
    meta = "".join(f"\n{label}: {value}" for label, value in optional if value)

    filename = re.sub(r"[^a-z0-9\-]+", "-", name.lower().strip()).strip("-")
    if not filename:
        filename = f"method-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    filepath = os.path.join(METHODS_DIR, f"{filename}.md")

    date = datetime.now().strftime("%d.%m.%Y")

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            existing = f.read()
        content = existing + f"\n\n### By {author} ({date})\n{experience}\n"
    else:
        content = f"""---
name: "{yaml_escape(name)}"
url: "{yaml_escape(url)}"
---

# {name}

## Purpose
{purpose}

## Underlying Theory / Principles
{theory}

## Process (High-level)
{process}
{meta}

## Experience

### By {author} ({date})
{experience}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created/Updated: {filepath}")
    return filepath


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Methods Collection")
    parser.add_argument("--body", required=True, help="The full body of the GitHub Issue")
    args = parser.parse_args()

    create_method_file(args.body)