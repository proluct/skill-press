---
name: skill-press
description: The Skill Printing Press. A guided factory that turns an idea into a ship-ready Claude Code skill, with prior-art research, one plan-approval gate, and subagent-tested verification before anything counts as done. Use when the user wants to create, build, or make a new skill, says "turn this into a skill", "skill for X", "capture this workflow", or types /skill-press. Not for editing an existing skill (use skill-press-polish), not for hooks or settings (those live in settings.json), not for subagent definitions.
version: 1.0.0
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - AskUserQuestion
  - Agent
---

# /skill-press

Print the best useful skill for a job without burning an hour on phase theater.

```
/skill-press
/skill-press a skill that turns meeting notes into action lists
/skill-press turn what we just did into a skill
/skill-press capture our deploy checklist as a skill
```

One lean loop:

1. Interview until the job has no fuzzy edges, write one brief
2. Absorb: research every existing skill and tool that does this job
3. Plan gate: the user approves the design before anything is built
4. Build the skill
5. Shipcheck: deterministic validation + agentic review
6. Dogfood: fresh-context subagents actually use the skill
7. Ship menu

Artifacts are written, but only the ones that materially help the next step.

## Rules

- **Do not ship a skill that has not been behaviorally tested.** A SKILL.md that reads
  well is not evidence it works. A fresh-context subagent must follow it on a realistic
  task before the verdict can be `ship`. Quick Check is the floor; Full Dogfood is the
  default recommendation.
- **Bugs found during dogfood are fix-before-ship, not "note for later".** Context is
  freshest in-session. Fix, then rerun the failed test.
- **The Plan Gate approval is shipping scope.** Do not silently drop an approved feature
  mid-build. If something turns out infeasible, return to the gate with a revised plan.
- **The absorb phase always runs.** Designing a skill without checking prior art
  reinvents worse versions of things that already exist. Finding nothing is a valid
  result; skipping the search is not.
- **Validator errors are blockers.** `scripts/validate_skill.py` is deterministic on
  purpose. Do not rationalize past a red check; fix the file.
- **No em-dash or en-dash characters in any generated file.** House rule of this
  factory; the validator enforces it as an error.
- **No human-time estimates for agent work.** Describe scope (files, lines, number of
  test runs), not minutes. The one carve-out: telling the user up front that a full
  factory run is a longer session, not a one-liner.
- **Prose showcase before every AskUserQuestion.** Print the context as a normal reply
  first, then ask with short one-line options. Never cram the explanation into option
  descriptions.
- Maximum 2 fix loops per verification stage unless the user asks for more.
- Durable run artifacts go under the manuscripts directory (see Preflight). The built
  skill goes to the target skills directory and nowhere else.

## Preflight

`FACTORY_DIR` is the directory this SKILL.md lives in. You just read this file from
disk, so substitute its parent directory as an absolute path in the block below, then
run it before any user-facing prompt:

```bash
PRESS_HOME="$HOME/.claude/skill-press"
FACTORY_DIR="<absolute path of the directory containing this SKILL.md>"
VALIDATOR="$FACTORY_DIR/scripts/validate_skill.py"
mkdir -p "$PRESS_HOME/manuscripts"

# Python is required for the mechanical shipcheck leg.
if command -v python >/dev/null 2>&1; then PY=python
elif command -v python3 >/dev/null 2>&1; then PY=python3
else
  echo "[setup-error] Python not found. The shipcheck validator needs it."
  echo "Install Python, then re-run /skill-press."
fi
[ -f "$VALIDATOR" ] || echo "[setup-error] validator missing at $VALIDATOR"
echo "PRESS_HOME=$PRESS_HOME"
echo "VALIDATOR=$VALIDATOR"
echo "PY=$PY"
```

On `[setup-error]`, stop and surface the fix. Otherwise capture the three values and
continue. Read [references/run-log.md](references/run-log.md) for corrections from past
runs; they override anything else in this skill that they contradict.

## Orientation & Briefing

### No arguments

Print an orientation:

> The Skill Press turns an idea into a working Claude Code skill. You describe the job;
> I research every existing skill and tool that does it, absorb their best ideas, add
> ideas of my own, and show you a plan. You approve the plan, I build the skill, then I
> prove it works by having fresh subagents actually use it before calling it done.
>
> This is a full factory run, not a quick file write. Simple reference skills are fast;
> workflow skills with real testing take a while.

Then ask via `AskUserQuestion`:

- **question:** "What should the new skill do?"
- **options:**
  1. **"Describe it (recommended)"** - "Tell me the job in your own words via Other."
  2. **"Improve an existing skill instead"** - "Route to /skill-press-polish."

If they pick polish, invoke the `skill-press-polish` skill and end this run.

### With arguments

Print a briefing in prose:

> Setting the type for `<skill idea>`. Here is how this will proceed: I interview you
> about the job, research prior art across GitHub and the skill marketplaces, present a
> plan with every absorbed and novel feature, and wait for your approval. Then I build
> it, run a deterministic validator plus an agentic review, and test it with
> fresh-context subagents. At the end you have an installed skill that has actually
> been used successfully at least once.

Then ask via `AskUserQuestion`:

- **question:** "Anything I should know before I begin? Specific behaviors you want,
  workflows this should capture, or examples of it done right?"
- **options:**
  1. **"Let's go (recommended)"** - "Start now; I'll ask when I need something."
  2. **"I have context to share"** - "Capture free-text as USER_BRIEFING_CONTEXT."

`USER_BRIEFING_CONTEXT` feeds the interview and gets its own section in the brief.

## Phase 0: Recon and Reuse

Before any interview question:

1. **Skill-shaped check.** If the request is really a hook or automation ("every time X
   happens do Y"), a settings change, or a subagent definition, say so and route: hooks
   and settings belong in `settings.json` (see the Claude Code hooks docs), subagent
   definitions in `.claude/agents/`. Do not build a skill that cannot work as a skill.
2. **Overlap check.** Scan installed skills for the same job: the available-skills list
   in context, `~/.claude/skills/`, and the project's `.claude/skills/`. On real overlap,
   stop and present it: polish the existing skill instead (recommended when it is
   user-owned), build anyway, or fold the existing skill's ideas into the new one.
   Plugin-cache skills cannot be polished (managed files); note that when relevant.
3. **Prior manuscripts.** Check `$PRESS_HOME/manuscripts/<skill-slug>/` for earlier runs
   of the same idea. Reuse a prior brief or absorb manifest when it is still good.
4. **Local recon.** If the skill captures a workflow from this session or wraps files in
   this repo, read those files now. Never ask the user a question recon could answer.

Then initialize the run:

```bash
SKILL_SLUG="<kebab-case-name>"        # provisional; interview may rename
RUN_ID="$(date +%Y%m%d-%H%M%S)"
RUN_DIR="$PRESS_HOME/manuscripts/$SKILL_SLUG/$RUN_ID"
mkdir -p "$RUN_DIR"
```

If the interview settles on a different name, rename the manuscripts directory to the
final slug so future runs find this one under Prior manuscripts. Run all preflight and
run-init bash in a POSIX shell (on Windows that is the Bash tool, not PowerShell).

## Phase 1: Interview and Brief

Read [references/interview.md](references/interview.md) and run the interview.

Ground rules: product questions (behavior, triggers, scope, output shape) reach the
user; technical calls (file layout, script language, reference structure) are yours,
decided with one line of reasoning and recorded in the brief. Batch questions with
`AskUserQuestion`, max 4 per round, most load-bearing first. Stress-test with invented
edge scenarios. Stop when a new question would only re-ask something settled.

Classify the skill type (technique, pattern, reference, discipline, workflow); the type
drives how Phase 5 tests it.

Write `$RUN_DIR/brief.md` using the template in the reference. The brief must answer:
what the skill enables, when it should trigger (and when NOT), the expected output, what
"done and correct" looks like as a checkable statement, the skill type, and what tools,
files, or credentials it depends on. Also ask (or infer) the install target: global
`~/.claude/skills/` (default) or the project's `.claude/skills/`.

## Phase 2: Absorb

MANDATORY. Read [references/absorb.md](references/absorb.md) and run the prior-art
sweep: existing skills on GitHub and in marketplaces, plugins, CLI tools, and written
guides for the same job. Catalog every feature worth having into the absorb manifest,
then derive transcendence features: things ours can do that none of the found tools do,
grounded in who actually uses this and what they cannot answer today.

Write `$RUN_DIR/absorb-manifest.md`. If the sweep finds nothing, the manifest records
the searches that came up empty; that honesty is part of the gate showcase.

## Phase Gate: Plan Approval

**STOP. Do not build until this gate is approved.**

Part 1, prose showcase. Cover:

1. **Identity**: name, one-line description draft, skill type, install target.
2. **Structure**: the file tree (SKILL.md, references, scripts) with one line on what
   each file carries.
3. **Feature readout**: every absorbed feature with its source, every novel feature
   with why it earns its place. Never hide features behind "plus N more".
4. **Test plan**: the dogfood prompts you intend to run and what passing looks like.
5. **Worries**: anything the user should weigh (external dependencies, overlap with an
   installed skill, low-confidence ideas, parts that cannot be tested in-session).

Part 2, `AskUserQuestion`:

> "Ready to build with this plan? Or do you have ideas to add?"

1. **Approve, build now** - Start the build with this plan
2. **I have ideas to add** - Tell me from your experience, then we regate
3. **Trim scope** - Too ambitious, focus on a subset
4. **Show the full manifest** - Read everything, then this gate is re-presented

On "ideas to add", ask what workflows they use that research missed, what frustrates
them about existing tools, and what their killer feature would be; fold answers in and
return to this gate. WAIT for approval.

## Phase 3: Build

Read [references/build-standards.md](references/build-standards.md) BEFORE writing,
then build the skill at the target directory exactly as approved.

Baseline shape: a lean SKILL.md under 500 lines, detail pushed into `references/`,
deterministic or repeated work pushed into `scripts/`. The description follows the
discovery rules in the standards file (triggering conditions, pushy, anti-triggers, no
workflow summary). Every rule in the standards file applies to the generated skill.

## Phase 4: Shipcheck

One combined verification block. Read [references/shipcheck.md](references/shipcheck.md)
for the full contracts. The three legs, in order:

1. **Mechanical**: run the validator; errors are blockers.

```bash
"$PY" "$VALIDATOR" "<target-skill-dir>"
```

2. **Agentic review**: dispatch one fresh-context subagent with the seven-point review
   contract from the reference (honesty, trigger-capability match, clarity, description
   discipline, dead references, runnability, marketing smell). Error findings are
   fix-before-proceed; warnings are surfaced to the user.
3. **Trigger audit**: draft should-trigger and should-not-trigger phrases, check the
   description against them and against the installed skills' descriptions for
   collisions. Sharpen the description or add anti-triggers as needed.

Maximum 2 shipcheck loops. Write `$RUN_DIR/shipcheck.md` with findings, fixes, and the
before/after validator state. Warnings that survive the fixes are listed in the prose
showcase printed right before the Phase 5 depth question; the user proceeding past that
question is their acceptance.

## Phase 5: Dogfood

**MANDATORY. This is the phase that separates a skill that reads well from one that
works.** Ask the user for depth via `AskUserQuestion`:

> "Shipcheck passed. How thoroughly should I test the skill with fresh subagents?"

1. **Full dogfood (recommended)** - 2 to 3 realistic test prompts, each run by a fresh
   subagent with the skill and a baseline subagent without it, results compared against
   the brief's done-criteria.
2. **Quick check** - One fresh subagent runs one test prompt with the skill.

Recommend Full by default. Recommend Quick only when the user asks for speed or when
testing would cause real side effects (paid API calls, outbound messages). There is no
skip option: if the user insists on skipping testing entirely, the verdict is `hold`,
never `ship`; Quick Check is the floor for a ship verdict. For
discipline skills, Full dogfood means pressure tests: scenarios that tempt an agent to
violate the rule, run with and without the skill. Protocols and grading rubric are in
[references/shipcheck.md](references/shipcheck.md).

Failures are fix-before-ship: fix the skill, rerun the failed prompt. Maximum 2 fix
loops, then the verdict is `hold`. Write `$RUN_DIR/dogfood.md`.

## Phase 6: Ship

Verdict from Phase 5: `ship` (all tests pass, no known broken instructions) or `hold`.

**On ship**, print a summary: what was built, where it lives, what was tested, one
example invocation. Then the restart note, always:

> The skill is installed but registers at session start. Restart Claude Code (or start
> a new session) and it will trigger naturally. Test it with: `<example prompt>`.

Then `AskUserQuestion`:

1. **Done (recommended)** - End the run
2. **Run retro** - Mine this session for factory improvements via /skill-press-retro
3. **Polish pass** - One more /skill-press-polish pass over the new skill

**On hold**, first quarantine: move the built skill out of the live skills directory to
`$RUN_DIR/working/<skill-slug>/` so a known-broken skill does not register at the next
session start; say where it went. Then report what blocked ship. Menu: run retro
(recommended; hold runs are the highest-value retro signal), keep fixing (move the copy
back when it reaches ship), or done.

Retro is one AskUserQuestion option, never auto-run.

## Fast Guidance

### When to stop researching

Stop when you can answer: what the skill must do first, what existing tools already do,
and what ours does that they cannot. If the next search does not change those answers,
stop and gate.

### What not to do

Do not:

- write multiple mandatory research documents; one brief, one manifest
- skip dogfood because the SKILL.md "looks right"
- let the generated SKILL.md bloat past 500 lines instead of using references
- write a description that summarizes the workflow (agents follow it and skip the body)
- ship a discipline skill that was never pressure-tested
- build before the Plan Gate is approved
- quietly drop an approved feature mid-build
- ship with a red validator

### What counts as success

- a built skill that passed the validator and the agentic review
- at least one fresh-context subagent that used the skill successfully on a real prompt
- one or two fix loops, not a maze of re-entry phases
- a user who saw the plan before the build and the evidence before the ship
