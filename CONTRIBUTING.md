# Contributing to skill-press

The factory improves through evidence from real runs. The best contributions carry that evidence with them.

## Run-log corrections (highest value)

Ran the factory and hit friction, a wrong first attempt, or a gap the instructions should have covered? File an issue titled with the rule you would add, containing: what happened (the evidence), the proposed correction in the run-log format below, and which file it should ultimately amend.

```
## Correction N (YYYY-MM-DD, from <skill-slug> run)
<The rule, imperative, one to three lines. Why: one line.>
```

`/skill-press-retro` drafts these for you; in plugin installs it offers to file the issue directly.

## Validator changes

- **False positive**: the validator flagged fine content. Issue or PR with the flagged text and why it is fine.
- **New check**: a defect class that reached agentic review or dogfood but could have been caught deterministically. PR to `skills/skill-press/scripts/validate_skill.py` with the check, plus a before/after example in the description.

The validator must stay dependency-free (stdlib only) and deterministic.

## Reference improvements

`interview.md`, `absorb.md`, `build-standards.md`, and `shipcheck.md` are the factory's knowledge. Sharper questions, better search patterns, tighter review contracts, and additional dogfood protocols are all welcome, with one line on the run or failure mode that motivated them.

## House rules

- No em-dash or en-dash characters in any file (the validator errors on them); use a comma, colon, period, or hyphen. No emojis.
- Imperative voice in skill bodies; explain why, not just what.
- The factory validates itself: `python skills/skill-press/scripts/validate_skill.py skills/skill-press` (and the other two skill dirs) must pass on every PR.
- No human-time estimates for agent work anywhere in the skills.
