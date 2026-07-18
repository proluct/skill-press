# Run log: corrections from real runs

Numbered standing corrections that override the main SKILL.md and references where
they conflict. Written by /skill-press-retro after real runs; read at the start of
every /skill-press and /skill-press-polish run.

Format: one numbered entry per correction, newest last, with the date, the run that
exposed it, and the rule.

```
## Correction N (YYYY-MM-DD, from <skill-slug> run)
<The rule, imperative, one to three lines. Why: one line.>
```

The corrections below are seed entries from the author's pre-release runs, kept
because they encode lessons every install benefits from. Your own retro runs append
after them (or, on plugin installs, file them as issues upstream; see retro's
upstream mode).

## Correction 1 (2026-07-14, from vm-librarian run)
When the built skill's task edits shared state, run the dogfood baseline in
propose-only mode and sequence the real with-skill run after all read-only agents
(now also in shipcheck.md). Why: concurrent same-turn agents mutating the same files
corrupt the comparison.

## Correction 2 (2026-07-14, from vm-librarian run)
Grade dogfood finding-sets both ways: whatever the baseline caught that the with-skill
run missed is a candidate missing instruction, fix before ship (now also in
shipcheck.md). Why: the baseline's unique finds produced this run's only real skill
improvement.

## Correction 3 (2026-07-14, from vm-librarian run)
When the skill operates on existing state (a repo, a dataset, live configs), harvest
real defects during Phase 0 recon and encode them in the brief's done-criteria as
named regression fixtures. Why: they gave dogfood objective pass/fail regressions
instead of invented scenarios.

## Correction 4 (2026-07-14, from vm-librarian run)
In dogfood.md, name every branch of a conditional rule that no test exercised (a
commit policy with clean/dirty branches where only dirty ran, say so). Why: an
unexercised branch is an honest gap the ship verdict must carry visibly.
