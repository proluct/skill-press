# Absorb: prior-art sweep and manifest

The factory does not "find gaps". It absorbs every good idea from every existing tool
that does this job, then transcends with things none of them do. This phase builds that
manifest. It always runs; an empty result is recorded, never assumed.

## Step 1: Search everything that touches this job

Run these in parallel, substituting the skill's domain terms:

1. WebSearch: `"<job>" Claude skill SKILL.md site:github.com`
2. WebSearch: `"<job>" Claude Code plugin site:github.com`
3. WebSearch: `"<job>" MCP server`
4. WebSearch: `awesome claude skills <domain>` (curated lists)
5. WebSearch: `"<job>" CLI tool OR script site:github.com`
6. WebSearch: `how to <job> workflow best practices` (written guides; a great blog
   post is absorbable prior art too)
7. WebFetch: `github.com/anthropics/skills` (the official skills repo) for an
   official take on the domain
8. Check the local machine: installed skills (Phase 0 already listed them), plugin
   marketplaces in `~/.claude/plugins/`, and any project skills. Local prior art is
   the cheapest to read fully.

Read the top hits for real. For a found SKILL.md, read the actual file, not the repo
README; the file shows the prompt engineering, the README shows the marketing.

Time-box the sweep: when two more searches in a row add nothing new, stop.

## Step 2: Catalog into the absorb manifest

For each tool found, list every feature, device, or trick worth having:

```markdown
## Absorb Manifest

### Absorbed (match or beat everything that exists)
| # | Feature | Best source | Our implementation | Added value |
|---|---------|-------------|--------------------|-------------|
| 1 | Chunked reading for big inputs | pdf-skill (gh:x/y) | Same, plus size probe first | No context blowout |
```

Every row is a commitment: if it is in the manifest at gate time, it ships. If a row
will ship deliberately reduced, mark it `(reduced)` with a one-line reason so the user
approves that explicitly.

Also absorb NEGATIVE knowledge: failure modes and complaints found in issues, reviews,
or the guides ("tool X always mangles tables"). These become tests and warnings in the
built skill.

## Step 3: Transcendence features

Start from the users, not the mechanism. Who runs this job, what are their rituals,
what question can they not answer today? "What could a script do?" is the wrong
question; "what would make a power user say I need this?" is right.

```markdown
### Transcendence (only ours does this)
| # | Feature | Why only we can | Evidence it matters |
|---|---------|-----------------|---------------------|
```

Guidance on count: a workflow skill should find at least 3 real transcendence features;
a small reference skill may honestly have 1 or none. Do not invent filler to hit a
number; the gate showcase must be able to defend every row.

## Step 4: Write the manifest

Write `$RUN_DIR/absorb-manifest.md` with both tables plus a `### Sources` list (name,
URL, what it contributed). If the sweep found nothing, write the queries that came up
empty under `### Searched, found nothing`; the Plan Gate showcase states that plainly.
