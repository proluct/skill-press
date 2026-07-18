# Shipcheck and dogfood: verification contracts

Three shipcheck legs (mechanical, agentic review, trigger audit), then dogfood.
Fix order within any leg: blockers first, then honesty findings, then clarity, then
polish. Maximum 2 loops per stage; after that the verdict is `hold`, not a third loop.

## Leg 1: Mechanical validator

```bash
"$PY" "$VALIDATOR" "<target-skill-dir>"
```

Exit 0 with warnings is passable if each warning is either fixed or consciously
accepted and noted in the shipcheck report. Exit 1 (errors) is a blocker, always.
`--strict` treats warnings as errors; use it for the final confirmation pass.

## Leg 2: Agentic review (fresh-context subagent)

Dispatch ONE subagent (general-purpose) with this contract, substituting real paths:

> Review the skill at `<target-skill-dir>` as a skeptical fresh reader. You have never
> seen this conversation. Read SKILL.md and every file it references. Report findings
> under 50 words each, tagged error or warning:
>
> 1. **Honesty**: does the skill promise anything its instructions cannot deliver?
>    Claimed capabilities with no implementing instruction are errors.
> 2. **Trigger-capability match**: does every trigger phrase in the description
>    correspond to something the body actually handles?
> 3. **Clarity**: where would a fresh agent be confused, have two readings, or need
>    information the skill does not provide? Ambiguity in a load-bearing step is an
>    error; elsewhere a warning.
> 4. **Description discipline**: does the description stay on triggering conditions,
>    third person, with anti-triggers, and avoid summarizing the workflow?
> 5. **Dead references**: does every mentioned file, tool, command, and skill exist?
>    Check files on disk; flag tools you cannot verify.
> 6. **Runnability**: could you actually execute these instructions top to bottom?
>    Name the first step where you would stall.
> 7. **Marketing smell**: "comprehensive", "seamless", "powerful" and friends instead
>    of concrete capability statements.
>
> Return the findings list, or "PASS, no findings".

Error findings: fix before proceeding. Warnings: surface to the user in the shipcheck
report and proceed if they accept.

## Leg 3: Trigger audit

1. Draft 4 to 6 should-trigger phrases (varied phrasings, some casual, some that never
   name the skill) and 4 to 6 should-not-trigger near-misses (adjacent jobs, shared
   keywords with different intent). Obvious negatives test nothing; make them tricky.
2. For each phrase, judge honestly: given only the installed-skills list plus the new
   description, which skill would an agent pick? Collisions with an installed skill's
   territory are findings.
3. Fix by sharpening the description or adding anti-triggers; do not fix by claiming
   territory an existing skill owns better.
4. Record the phrase table and verdicts in the shipcheck report. Note for the user
   that real triggering can only be confirmed after a session restart.

## Dogfood protocols

Grading rubric: the brief's Done-criteria section, verbatim, plus "did the skill's
distinctive features (transcendence rows) actually show up in the output?".

### Full dogfood (default recommendation)

1. Write 2 or 3 realistic test prompts. Realistic means concrete: file paths, names,
   sloppy phrasing, a little backstory. Not "summarize a PDF" but "ok i have this
   report in downloads called q3-final-v2.pdf, need the key numbers as bullets for my
   boss by standup". Prepare fixtures FIRST: every file or input a prompt references
   must actually exist (find a real one or create one); a prompt pointing at a
   nonexistent file invalidates the whole comparison.
2. For each prompt, in the SAME turn spawn two subagents:
   - with-skill: "Read `<target-skill-dir>/SKILL.md` and follow it to accomplish:
     `<prompt>`. Save outputs under `<run-dir>/dogfood/<n>/with/`."
   - baseline: the same prompt, no mention of the skill, outputs under `.../without/`.

   Mutation exception: when the skill's task EDITS shared state (repo files, configs,
   a database), two agents doing it concurrently corrupt the test. Run the baseline in
   propose-only mode (instruct it: describe the exact edits you would make, touch
   nothing) and sequence the real with-skill run after every read-only agent has
   finished. Detection quality still compares; note the mode in dogfood.md.
3. Grade both against the rubric. The skill must beat baseline; a tie means the skill
   adds nothing and the design needs revisiting, not a wording tweak. Compare the
   finding-sets BOTH ways: anything the baseline surfaced that the with-skill run
   missed is a candidate missing instruction in the skill, diagnose and fix before
   ship. The baseline is a discovery tool, not just a bar to clear.
4. On failure: diagnose whether the skill misled the agent (fix wording), lacked a
   needed instruction (add it), or the design is wrong (back to the Plan Gate).
   Rerun only the failed prompt after the fix.

### Quick check

One fresh subagent, one test prompt, with-skill only. Grade against the rubric.
Catches broken instructions and stalls; misses subtle quality gaps. Say so in the
report.

### Pressure tests (discipline skills)

1. Write 2 or 3 temptation scenarios: situations where violating the rule is easy,
   locally attractive, and superficially justifiable (time pressure, sunk cost, "just
   this once", an authority figure asking).
2. Baseline first: a subagent gets the scenario WITHOUT the skill. Document the exact
   rationalization it uses; that wording is gold.
3. With-skill run: same scenario, skill loaded. Compliance = pass.
4. If the with-skill agent still rationalizes past the rule, quote its rationalization
   INSIDE the skill as an explicitly closed loophole and rerun. This loop is the whole
   point of pressure testing.

### Reference skills

Ask the subagent 3 to 5 retrieval questions whose answers live in the skill. Wrong or
not-found answers mean the structure buries the content; restructure and rerun.

### Workflow skills

One dry-run walkthrough: a subagent reads the skill and narrates each phase for a toy
request, without executing side effects. Check phase order, gate stops, and that no
step references context it will not have. Then at least one real task run if the
workflow's effects are safe to execute in-session.

## Reports

`$RUN_DIR/shipcheck.md`: validator output summary, review findings and their fixes,
trigger table, remaining accepted warnings.

`$RUN_DIR/dogfood.md`: per-prompt verdicts with evidence (what the output was, which
rubric lines passed or failed), fixes applied, final verdict `ship` or `hold` with one
line of reasoning.
