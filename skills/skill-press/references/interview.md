# Interview: from idea to brief

The interview exists to remove every fuzzy edge before research starts. It is the same
move as a good feature grill: recon first, then questions the recon could not answer.

## Order of operations

1. Strike from your question list everything Phase 0 recon already answered (files
   read, session history, USER_BRIEFING_CONTEXT).
2. Ask the load-bearing questions first, in batches of max 4 via AskUserQuestion.
3. Stress-test with invented edge scenarios.
4. Classify the skill type.
5. Write the brief.

## Question bank

Product questions (these reach the user):

- **Job**: What should this skill enable that does not happen well today? What does the
  user say or do right before they need it?
- **Triggers**: What phrases or situations should invoke it? What nearby requests should
  NOT invoke it? (Anti-triggers matter as much as triggers.)
- **Output**: What does the finished output look like? A file, an answer in chat, an
  edit, a report? Is there a format to lock (template, sections, naming)?
- **Done-criteria**: How would the user check the output is right? Push for something
  objective. "Until it looks good" is not a criterion; "every claim has a source link"
  is.
- **Scope**: One job done well, or a router over several related jobs? What is
  explicitly out of scope?
- **Audience**: Who invokes it, in which projects? Global or project-local install?
- **Frequency**: Used daily or occasionally? Daily skills earn more bundled tooling.

Technical calls (decide yourself, one-line reasoning, record in the brief):

- file layout, reference split, script language
- data formats and intermediate artifacts
- which tools the skill instructs the agent to use
- naming, unless the user volunteered a name

## Edge stress-tests

Invent scenarios and ask what should happen. Pick the ones that fit the job:

- The input is empty, huge, malformed, or in the wrong language.
- The external tool or API the skill depends on is down or not installed.
- Two plausible interpretations of the same trigger phrase exist.
- The skill is invoked mid-task with partial context instead of fresh.
- The user asks for the one thing the skill explicitly must not do.

A fuzzy answer means more grilling, not an assumption.

## Skill types

Classify into exactly one primary type; it drives testing in Phase 5.

| Type | What it is | Example | Phase 5 test |
|---|---|---|---|
| Technique | Concrete method with steps | condition-based waiting | Task-based dogfood |
| Pattern | A way of thinking about problems | flatten-with-flags | Task-based dogfood |
| Reference | Docs, syntax, tool knowledge | API cheat-sheet | Retrieval questions |
| Discipline | Rules the agent must not break | TDD enforcement | Pressure tests |
| Workflow | Multi-phase guided process | a factory like this one | Dry-run walkthrough + task dogfood |

Hybrid skills exist: still pick ONE primary type for the brief, note the secondary
components, and Phase 5 tests each component with its own protocol.

## Brief template

Write `$RUN_DIR/brief.md`:

```markdown
# Skill Brief: <name>

## Job
What it enables, in two sentences. Who invokes it and when.

## Triggers
- Should fire on: <phrases and situations>
- Must NOT fire on: <anti-triggers>

## Output
Shape of the finished result. Locked formats if any.

## Done-criteria
Checkable statements. These become the dogfood grading rubric verbatim.

## Type
<technique|pattern|reference|discipline|workflow> and why.

## Dependencies
Tools, files, credentials, other skills. Note anything untestable in-session.

## Install target
<global|project> path.

## User vision
Verbatim context the user volunteered (USER_BRIEFING_CONTEXT and interview answers
in their framing).

## Technical calls
Your decisions with one-line reasoning each.

## Out of scope
What was explicitly deferred.
```

Keep it dense. If a section is hard to fill, that is a missing decision: go back and
ask, do not pad.
