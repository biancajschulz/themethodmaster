#!/usr/bin/env python3
import argparse
import os
import re
from datetime import datetime
from html import unescape

METHODS_DIR = "methods"

def parse_value(body, title):
    # re.escape() sorgt dafür, dass Sonderzeichen wie Klammern keine Regex-Fehler werfen
    pattern = rf"### {re.escape(title)}\n\n(.*?)(?:\n\n---|\n\n###|\Z)"
    match = re.search(pattern, body, re.DOTALL)
    if match:
        return unescape(match.group(1).strip())
    return ""

def create_method_file(body):
    os.makedirs(METHODS_DIR, exist_ok=True)

    # Parse fields from the Issue body
    name = parse_value(body, "Method Name")
    url = parse_value(body, "Method URL")
    purpose = parse_value(body, "Purpose")
    process = parse_value(body, "Process (High-level)")
    experience = parse_value(body, "Experience")
    author = parse_value(body, "Author")
    
    # Optional fields (updated names)
    industry = parse_value(body, "Industry")
    org_size = parse_value(body, "Organization Size")
    teams_count = parse_value(body, "Teams Applied To")
    people_per_team = parse_value(body, "People Per Team")
    roles = parse_value(body, "Roles")
    leadership_levels = parse_value(body, "Leadership or Hierarchy Levels Involved")
    frequency = parse_value(body, "Frequency")
    time_period = parse_value(body, "Time Period")
    layers_to_customer = parse_value(body, "Layers between you and the Customer")
    when_it_breaks = parse_value(body, "When it breaks")
    tips = parse_value(body, "Tips")

    filename = re.sub(r"[^a-z0-9\-]", "-", name.lower().strip())
    filepath = os.path.join(METHODS_DIR, f"{filename}.md")

    # Build optional metadata string
    meta = ""
    if industry: meta += f"\nIndustry: {industry}"
    if org_size: meta += f"\nOrganization Size: {org_size}"
    if teams_count: meta += f"\nTeams Applied To: {teams_count}"
    if people_per_team: meta += f"\nPeople Per Team: {people_per_team}"
    if roles: meta += f"\nRoles: {roles}"
    if leadership_levels: meta += f"\nLeadership or Hierarchy Levels Involved: {leadership_levels}"
    if frequency: meta += f"\nFrequency: {frequency}"
    if time_period: meta += f"\nTime Period: {time_period}"
    if layers_to_customer: meta += f"\nLayers between you and the Customer: {layers_to_customer}"
    if when_it_breaks: meta += f"\nWhen it breaks: {when_it_breaks}"
    if tips: meta += f"\nTips: {tips}"

    content = f"""---
name: "{name}"
url: "{url}"
---

# {name}

## Purpose
{purpose}

## Process (High-level)
{process}
{meta}

## Experience

### By {author} ({datetime.now().strftime("%d.%m.%Y")})
{experience}
"""

    # If file exists, append new experience
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            existing = f.read()
        content = existing + f"""\n\n### By {author} ({datetime.now().strftime("%d.%m.%Y")})\n{experience}\n"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created/Updated: {filepath}")
    return filepath

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Methods Collection")
    parser.append_argument("--body", required=True, help="The full body of the GitHub Issue")
    args = parser.parse_args()

    create_method_file(args.body)