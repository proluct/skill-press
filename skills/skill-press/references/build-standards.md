# Build standards: the quality bar for every generated skill

Read this before writing a single line of the new skill. The validator enforces the
mechanical subset; the rest is judgment this file makes explicit.

## Anatomy

```
skill-name/
  SKILL.md            required; the loop or the knowledge, lean
  references/         detail loaded on demand; only if needed
  scripts/            executable helpers for deterministic or repeated work
  assets/             templates, fonts, files used in output
```

Progressive disclosure, three levels: (1) name + description are always in context,
(2) SKILL.md body loads when the skill triggers, (3) references load only when the
body points at them. Budget accordingly: description under 500 characters when
possible (hard max 1024), body under 500 lines, references unlimited but each one
opened only when needed. A reference file over 300 lines gets a table of contents.

Point at references explicitly with WHEN to read them ("Read the absorb reference
before Phase 2"), not a bare link list at the bottom.

## Frontmatter

- `name`: kebab-case, letters/numbers/hyphens only, must equal the directory name.
- `description`: the single highest-leverage string in the skill. It is the ONLY thing
  the agent sees when deciding whether to load the skill. Rules:
  - Third person. State what the skill is in one clause, then when to use it.
  - Be pushy about triggering: list concrete phrases, situations, and symptoms.
    Claude undertriggers skills; a timid description never fires.
  - Include anti-triggers: the adjacent requests this skill must NOT grab.
  - NEVER summarize the internal workflow or phases. A description that says
    "first does X then Y" becomes a shortcut: agents follow the summary and skip
    the body. Triggering conditions only.

## Writing the body

- **Imperative voice.** "Run the sweep", not "the sweep should be run".
- **Explain why, not just what.** Today's models have theory of mind; a rule with its
  reason survives contact with novel situations, a bare MUST gets rationalized away.
  If you catch yourself writing ALWAYS or NEVER in caps, that is a yellow flag: add
  the reason, or the rule needs a deterministic check instead of prose.
- **Generalize.** The skill will run on prompts you never saw. Prefer principles plus
  one worked example over an exhaustive case list tuned to the test prompts.
- **Lock output formats with templates.** When the output has a required shape, show
  the exact template in a code block. Agents copy templates faithfully; they drift on
  prose descriptions of formats.
- **Examples pattern**: show input and output pairs for anything format-sensitive.
- **Bundle scripts for repeated mechanical work.** If every invocation would hand-write
  the same helper (a converter, a validator, a fetch wrapper), write it once into
  `scripts/` and instruct its use. Scripts are also the answer for anything that must
  be deterministic; save prose for judgment calls.
- **State the failure modes.** What goes wrong when agents run this, and the fix.
  Absorbed negative knowledge from the manifest lands here.
- Flowcharts only when a decision is genuinely non-obvious; never put code in them.

## Discipline skills: close the loopholes

A discipline skill (rules the agent must not break) is only as strong as its weakest
rationalization. After drafting:

1. List every excuse an agent could use to skip the rule ("this case is special",
   "the user is in a hurry", "the spirit is satisfied").
2. Answer each one IN the skill, explicitly.
3. Add a red-flags section: thoughts that signal the agent is about to rationalize.
4. Phase 5 pressure tests then try those exact temptations; expect to iterate.

## Hygiene (validator-enforced)

- No em-dash or en-dash characters anywhere. Use a comma, colon, period, or hyphen.
- No emojis.
- No leftover to-do or fix-me markers and no unfilled angle-bracket placeholders in
  shipped files. The validator greps for the usual all-caps marker forms; unfilled
  placeholders are caught by the review subagent in shipcheck leg 2, since legitimate
  templates use angle brackets on purpose.
- Every relative link and every `references/...` or `scripts/...` mention resolves to
  a file that exists.
- No human-time estimates for agent work.

## Anti-patterns

- **Narrative example**: "in session X we did Y" stories. Skills are reference guides,
  not memoirs; extract the technique, drop the story.
- **Workflow-summary description**: see frontmatter rules; the worst failure because
  it silently disables the body.
- **Generic labels**: "helper", "utility", "misc". Name things by what they do.
- **Kitchen-sink body**: 800 lines inline because splitting felt like effort. Split.
- **Untested confidence**: shipping because it reads well. Phase 5 exists because
  this fails constantly.
