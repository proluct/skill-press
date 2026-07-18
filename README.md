# skill-press

A factory for Claude Code skills: interview, prior-art absorb, one plan gate, build, deterministic validation, fresh-subagent dogfood. Nothing ships untested.

Most skills are written once, installed, and trusted. A SKILL.md that reads well is not evidence it works: descriptions that never trigger, instructions a fresh agent stalls on, promised capabilities with no implementing step. skill-press exists because the gap between "reads well" and "works" is where skills die.

## The loop

```
/skill-press a skill that turns meeting notes into action lists
```

1. **Interview** until the job has no fuzzy edges; one brief
2. **Absorb**: mandatory prior-art sweep across GitHub, marketplaces, CLIs, and guides; every good idea gets cataloged, then the design adds what none of them do
3. **Plan gate**: you approve the full feature list before anything is built
4. **Build** to an explicit quality bar (progressive disclosure, description discipline, locked output templates)
5. **Shipcheck**: a deterministic Python validator plus a fresh-context agentic review plus a trigger audit
6. **Dogfood**: fresh subagents actually use the skill on realistic prompts, compared against a baseline agent without it; failures are fix-before-ship
7. **Ship**, or an honest `hold` with the broken skill quarantined

## The three skills

| Skill | Job |
|---|---|
| `skill-press` | Build a new skill through the full gated loop |
| `skill-press-polish` | Diagnose, fix, re-diagnose an existing skill without changing its scope |
| `skill-press-retro` | Mine a real run for systemic lessons and improve the factory itself |

## The validator

`skills/skill-press/scripts/validate_skill.py` is the deterministic leg: frontmatter validity, name/directory match, description length and workflow-summary smell, body line budgets, dead reference links, placeholder markers, banned characters. It runs standalone on any skill directory:

```
python skills/skill-press/scripts/validate_skill.py <skill-dir> [--strict]
```

It exists so quality checks the model could rationalize past become exit codes it cannot.

## Testing discipline is the point

- Dogfood compares with-skill against a no-skill baseline; a tie means the skill adds nothing and the design gets revisited.
- Discipline skills (rules an agent must not break) get pressure tests: temptation scenarios run with and without the skill, and every rationalization the baseline produces gets closed inside the skill as an explicit loophole.
- There is no skip option for testing. Refusing tests yields a `hold` verdict, never `ship`.

## Relation to skill-creator

Anthropic's official `skill-creator` plugin helps write skills. skill-press is complementary and opinionated about verification: a hard plan-approval gate, a deterministic validator, baseline-comparison dogfood, `hold` verdicts with quarantine, and a retro loop that feeds lessons from real runs back into the factory.

## Install

As a plugin (recommended):

```
/plugin marketplace add proluct/skill-press
/plugin install skill-press@skill-press
```

Or manually: copy the three directories under `skills/` into `~/.claude/skills/` and restart Claude Code.

Requires Python (for the validator) and a POSIX shell for the small preflight blocks (on Windows, Claude Code's Bash tool covers this).

## The retro flywheel

`/skill-press-retro` mines every real run for systemic lessons. On a manual install it edits the factory files directly and appends numbered corrections to the run log. On a plugin install the factory files are managed, so retro files its approved findings as issues on this repository instead. Every serious user's retro run is a contribution: this is how the factory compounds.

## Related

[skanna](https://github.com/proluct/skanna) is the companion project: a security scanner that vets Claude Code skills and plugins before install. skill-press builds them, skanna vets them.

## License

MIT
