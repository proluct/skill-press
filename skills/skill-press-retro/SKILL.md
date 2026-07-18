---
name: skill-press-retro
description: Run a retrospective after a skill-press or skill-press-polish run to improve the factory itself, so the next skill comes out better. Use after any skill-press run, when the user says "retro", "what went wrong with that skill build", "improve the skill factory", "lessons learned", or when a skill-press run ends in a hold verdict. Edits the skill-press skill files, never the skill that was just built (that is polish's job).
version: 1.0.0
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# /skill-press-retro

Mine the session that just built (or failed to build) a skill for systemic lessons,
and apply them to the factory. This is how the factory compounds: every real run makes
the next one better.

## Cardinal rules

- **Retro improves the FACTORY, never the just-built skill.** A flaw in the built
  skill goes to /skill-press-polish. A flaw in how the factory produced it goes here.
- **Systemic only.** A finding must plausibly recur on future runs to earn a change.
  One-off weirdness gets listed under Skip, not patched into the skill.
- **The user approves before any factory file changes.** Show the proposed edits as a
  findings list first.

## Setup

Locate the factory the same way polish does:

```bash
FACTORY_DIR="$(dirname "$(dirname "$(find .claude/skills "$HOME/.claude/skills" "$HOME/.claude/plugins" \
  -type f -path '*/skill-press/scripts/validate_skill.py' 2>/dev/null | head -1)")")"
PRESS_HOME="$HOME/.claude/skill-press"
ls -t "$PRESS_HOME/manuscripts" 2>/dev/null | head -5
```

Resolve which run to retro: default is the most recent manuscripts entry; the user can
name another. Read that run's brief, absorb manifest, shipcheck, and dogfood reports.
The current session transcript is the other evidence source when retro runs in the
same session as the build.

## Upstream mode (plugin installs)

If `FACTORY_DIR` sits under the plugin cache (any path containing `/.claude/plugins/`),
the factory files are managed by the plugin system and local edits will be overwritten
on update. Do not edit them. Run Phases 1 and 2 exactly the same, then in Phase 3 offer
to file each approved finding as an issue on the upstream skill-press repository
instead (`gh issue create`, title = the finding, body = evidence, proposed change, and
a drafted run-log entry). Real-run corrections are this project's main improvement
stream; an issue with evidence is a finished contribution.

## Phase 1: Mine the evidence

Work through these lenses against the run artifacts and session memory:

1. **Friction**: where did the factory's instructions cause hesitation, a wrong first
   attempt, or a retry? What did the agent have to figure out that the skill should
   have said?
2. **Gate quality**: did the Plan Gate showcase give the user what they needed to
   decide? Did any question reach the user that recon or a technical call should have
   absorbed?
3. **Absorb misses**: did dogfood or the user surface prior art or a feature the sweep
   should have found? Which search would have caught it?
4. **Validator accuracy**: false positives (flagged fine content) and false negatives
   (a defect that reached the agentic review or dogfood but a deterministic check
   could have caught earlier and cheaper).
5. **Dogfood honesty**: did the tests actually exercise the skill's distinctive
   features, or did an easy prompt let a weak skill pass?
6. **What went right**: patterns worth reinforcing or making explicit so they are not
   accidental next time.

## Phase 2: Classify and propose

For each finding, classify:

- **skill-fix**: edit `$FACTORY_DIR/SKILL.md` (a phase instruction was wrong/missing)
- **reference-fix**: edit a file under `$FACTORY_DIR/references/`
- **validator-fix**: edit `$FACTORY_DIR/scripts/validate_skill.py` (new check, or
  tune a false positive)
- **correction**: a standing rule for the run-log when the fix is behavioral rather
  than structural
- **skip**: one-off, not systemic; listed for the record

Present the findings to the user as a prose showcase (finding, evidence, proposed
change, one line each), then AskUserQuestion:

1. **Apply all (recommended)** - Make every proposed change
2. **Pick which** - I choose per finding
3. **Skip, just log** - Append to the run-log only, change nothing else

## Phase 3: Apply

Make the approved edits. For every applied change AND every accepted correction,
append a numbered entry to `$FACTORY_DIR/references/run-log.md` in its stated format,
so future runs see the lesson even if they skip the diff history. In upstream mode,
file the approved findings as upstream issues instead, per the section above.

Close with a two-line summary: N findings, M applied, where the run-log now stands.
