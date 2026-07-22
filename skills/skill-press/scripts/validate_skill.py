#!/usr/bin/env python3
"""Deterministic skill validator: the mechanical leg of skill-press shipcheck.

Usage:
    python validate_skill.py <skill-dir> [--strict]

Exit codes: 0 = pass (warnings allowed unless --strict), 1 = errors found,
2 = bad invocation.
"""

import difflib
import re
import sys
from pathlib import Path

MAX_DESCRIPTION = 1024
BODY_LINE_WARN = 500
REFERENCE_TOC_WARN = 300

# Characters banned outright in shipped skill files (house style: these read
# as machine-generated filler; use a comma, colon, period, or hyphen).
BANNED_CHARS = {"—": "em-dash", "–": "en-dash"}

PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|TBD|XXX)\b|<placeholder>", re.IGNORECASE)
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Workflow-summary smell in descriptions: sequenced-process wording that tempts
# agents to follow the description instead of reading the body.
WORKFLOW_SMELL_RE = re.compile(r"(->|\bthen\s+I\b|\bstep \d|\bphase \d)", re.IGNORECASE)
MD_LINK_RE = re.compile(r"\]\(([^)#>][^)]*)\)")
BARE_REF_RE = re.compile(r"(?<![\w/(\[])((?:references|scripts|assets)/[\w.\-/]+)")

# Frontmatter keys the loader recognizes. A key outside this set is only an
# error when it is close enough to a known key to be a typo; anything else is a
# warning, so a newly supported key never blocks a ship.
KNOWN_KEYS = ["name", "description", "version", "allowed-tools", "license", "metadata", "model"]
# 0.75 catches real slips ('nmae', 'descrption', 'verison') without matching
# unrelated words ('tools', 'author'), which would produce a misleading hint.
TYPO_CUTOFF = 0.75


def parse_frontmatter(text):
    """Return (dict, errors, warnings). Minimal parser: no yaml dependency guaranteed."""
    if not text.startswith("---"):
        return None, ["SKILL.md does not start with '---' frontmatter"], []
    lines = text.split("\n")
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return None, ["frontmatter never closes with '---'"], []
    fields = {}
    current_key = None
    errors, warnings = [], []
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if m:
            current_key = m.group(1)
            if current_key not in KNOWN_KEYS:
                near = difflib.get_close_matches(current_key, KNOWN_KEYS, n=1, cutoff=TYPO_CUTOFF)
                if near:
                    errors.append(f"frontmatter: unknown top-level key '{current_key}' (did you mean '{near[0]}'?)")
                else:
                    warnings.append(f"frontmatter: unrecognized top-level key '{current_key}'")
            fields[current_key] = m.group(2).strip().strip("\"'")
        elif current_key and (line.startswith("  ") or line.startswith("\t")):
            # continuation (folded scalar or list item); append for length checks
            fields[current_key] = (fields[current_key] + " " + line.strip().lstrip("- ")).strip()
    return fields, errors, warnings


def check_file_hygiene(path, rel, errors, warnings):
    text = path.read_text(encoding="utf-8", errors="replace")
    for ch, label in BANNED_CHARS.items():
        count = text.count(ch)
        if count:
            first_line = next(i for i, l in enumerate(text.split("\n"), 1) if ch in l)
            errors.append(f"{rel}: {count}x {label} (first at line {first_line}); banned everywhere")
    for m in PLACEHOLDER_RE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        warnings.append(f"{rel}:{line}: placeholder marker '{m.group(0)}'")
    return text


def check_references_resolve(text, rel, skill_dir, errors):
    seen = set()
    for regex in (MD_LINK_RE, BARE_REF_RE):
        for m in regex.finditer(text):
            target = m.group(1).strip()
            if target in seen:
                continue
            seen.add(target)
            if re.match(r"^[a-z][a-z0-9+.-]*://", target) or target.startswith("mailto:"):
                continue  # URL
            if re.match(r"^[A-Za-z]:[\\/]|^[/~$]", target):
                continue  # absolute/home/env path: environment-dependent, skip
            if any(c in target for c in "*<>|\"' "):
                continue  # glob/template text, not a real path
            candidate = (skill_dir / target).resolve()
            if not candidate.exists():
                line = text.count("\n", 0, m.start()) + 1
                errors.append(f"{rel}:{line}: referenced path '{target}' does not exist")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    if len(args) != 1:
        print(__doc__)
        return 2
    skill_dir = Path(args[0]).resolve()
    skill_md = skill_dir / "SKILL.md"
    errors, warnings = [], []

    if not skill_md.is_file():
        print(f"ERROR: {skill_dir} has no SKILL.md")
        return 1

    text = check_file_hygiene(skill_md, "SKILL.md", errors, warnings)
    fields, fm_errs, fm_warns = parse_frontmatter(text)
    if fields is None:
        errors.extend(f"SKILL.md: {err}" for err in fm_errs)
    else:
        errors.extend(fm_errs)
        warnings.extend(fm_warns)
        name = fields.get("name", "")
        desc = fields.get("description", "")
        # Reported independently of any key-name finding: a typo'd key and a
        # genuinely absent field are separate defects and both must surface.
        if not name:
            errors.append("frontmatter: missing 'name'")
        elif not NAME_RE.match(name):
            errors.append(f"frontmatter: name '{name}' is not kebab-case")
        elif name != skill_dir.name:
            errors.append(f"frontmatter: name '{name}' != directory '{skill_dir.name}'")
        if not desc:
            errors.append("frontmatter: missing 'description'")
        else:
            if len(desc) > MAX_DESCRIPTION:
                errors.append(f"description: {len(desc)} chars > {MAX_DESCRIPTION} max")
            if WORKFLOW_SMELL_RE.search(desc):
                warnings.append("description: reads like a workflow summary (sequenced steps); keep it to triggering conditions")

    body_lines = len(text.split("\n"))
    if body_lines > BODY_LINE_WARN:
        warnings.append(f"SKILL.md: {body_lines} lines > {BODY_LINE_WARN}; push detail into references/")

    check_references_resolve(text, "SKILL.md", skill_dir, errors)

    for sub in sorted(skill_dir.rglob("*.md")):
        if sub == skill_md:
            continue
        rel = sub.relative_to(skill_dir).as_posix()
        sub_text = check_file_hygiene(sub, rel, errors, warnings)
        check_references_resolve(sub_text, rel, skill_dir, errors)
        n = len(sub_text.split("\n"))
        if n > REFERENCE_TOC_WARN and "## Contents" not in sub_text and "## table of contents" not in sub_text.lower():
            warnings.append(f"{rel}: {n} lines with no table of contents")

    for line in errors:
        print(f"ERROR   {line}")
    for line in warnings:
        print(f"WARNING {line}")
    verdict_fail = bool(errors) or (strict and bool(warnings))
    print(f"\n{skill_dir.name}: {len(errors)} error(s), {len(warnings)} warning(s) -> "
          + ("FAIL" if verdict_fail else "PASS"))
    return 1 if verdict_fail else 0


if __name__ == "__main__":
    sys.exit(main())
