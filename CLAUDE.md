# skill-press repo conventions

Public repository. Everything committed here ships to the world.

- No em-dash or en-dash characters anywhere (the validator errors on them); use a comma, colon, period, or hyphen. No emojis.
- The factory validates itself: before committing changes to any skill here, run `python skills/skill-press/scripts/validate_skill.py <skill-dir>` on all three skill directories; errors are blockers.
- The validator stays stdlib-only and deterministic. Judgment calls belong in the references, not the script.
- Surgical edits over rewrites; the references carry the factory's voice.
- Never commit personal data, absolute local paths, machine-specific configuration, or private run manuscripts. Run artifacts belong in the user's `~/.claude/skill-press/manuscripts/`, never in this repo.
- Lessons from real runs enter through run-log corrections or upstream issues (see CONTRIBUTING.md), each with its evidence.
