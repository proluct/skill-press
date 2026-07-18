---
name: skill-press-polish
description: Diagnose and improve an EXISTING Claude Code skill with a diagnose, fix, re-diagnose pass, whether skill-press built it or not. Use when the user says "polish this skill", "improve my X skill", "this skill keeps misfiring or confusing the agent", "clean up this SKILL.md", or after a skill-press run offers a polish pass. Not for creating new skills (use skill-press) and not for plugin-managed skills, which cannot be edited in place.
version: 1.0.0
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Agent
---

# /skill-press-polish

Second-pass improvement for an existing skill: baseline diagnostics, fixes in priority
order, re-diagnose, report the delta. The skill's job and triggering scope stay what
they are; polish makes the skill better at the job it already has.

```
/skill-press-polish my-pdf-skill
/skill-press-polish ~/.claude/skills/storm
```

## Rules

- **Never widen or change the skill's scope without asking.** Renaming, retargeting,
  or claiming new trigger territory is a design change, not a polish; surface it and
  let the user decide.
- **Plugin-cache skills are read-only.** Anything under `~/.claude/plugins/` is managed
  by the plugin system and edits will be overwritten. Diagnose-only there: report
  findings, do not edit.
- **Fix, do not rewrite.** Surgical edits that preserve the author's structure and
  voice. A full rewrite is a skill-press job with the old skill as prior art.
- Maximum 2 polish loops per invocation.
- No em-dash or en-dash characters in anything you write.

## Setup

Resolve the target from the argument: an absolute path is used as-is; a bare name is
searched in the project's `.claude/skills/`, then `~/.claude/skills/`. No argument:
ask which skill. Confirm `SKILL.md` exists; snapshot the file list and line counts as
the before-state.

Then locate the factory (the installed skill-press skill), which may live in a global
or project skills directory or in the plugin cache:

```bash
VALIDATOR="$(find .claude/skills "$HOME/.claude/skills" "$HOME/.claude/plugins" \
  -type f -path '*/skill-press/scripts/validate_skill.py' 2>/dev/null | head -1)"
FACTORY_DIR="$(dirname "$(dirname "$VALIDATOR")")"
command -v python >/dev/null 2>&1 && PY=python || PY=python3
[ -f "$VALIDATOR" ] || echo "[setup-error] skill-press factory not found; is it installed?"
```

Read `$FACTORY_DIR/references/run-log.md`; its corrections apply to polish runs too.

## Phase 1: Baseline diagnostics

1. **Validator**: `"$PY" "$VALIDATOR" "<skill-dir>"`. Record the output verbatim.
2. **Agentic review**: dispatch one fresh-context subagent with the seven-point
   contract from `$FACTORY_DIR/references/shipcheck.md` (honesty, trigger match,
   clarity, description discipline, dead references, runnability, marketing smell).
3. **Optional behavior probe**: offer via AskUserQuestion when the findings suggest
   the skill misbehaves in use, not just on paper: one fresh subagent runs one
   realistic prompt with the skill (quick-check protocol from shipcheck.md). Skip for
   trivial cosmetic-only findings.

Collate everything into one findings list, each tagged with a priority below.

## Phase 2: Fix in priority order

1. **Validator errors**: dead references, frontmatter faults, banned characters.
2. **Honesty**: promises the instructions cannot deliver; either implement the missing
   instruction or delete the claim.
3. **Clarity**: ambiguous load-bearing steps a fresh agent stalls on.
4. **Description quality**: triggering coverage, anti-triggers, third person, no
   workflow summary. Keep the same territory; sharpen the edges.
5. **Structure**: body over 500 lines gets detail pushed into `references/`; repeated
   mechanical instructions become a bundled script.
6. **Cosmetics**: marketing smell, placeholder markers, stale examples.

Apply `$FACTORY_DIR/references/build-standards.md` as the bar for every edit.

## Phase 3: Re-diagnose and report

Re-run the validator (with `--strict` on the final pass) and re-dispatch the reviewer.
Then report the delta to the user: findings before vs after by priority class, what
was fixed with one line each, what remains and why. State plainly whether another pass
would help (`further polish recommended: yes/no` with one line of reasoning); when the
answer is no, do not offer a "polish again" option.

If anything remains that polish cannot fix without a design change, name it and route:
scope changes to the user, systemic factory lessons to /skill-press-retro.

Remind the user that edits to a skill's description register at session start; a
restart is needed before triggering behavior changes.
