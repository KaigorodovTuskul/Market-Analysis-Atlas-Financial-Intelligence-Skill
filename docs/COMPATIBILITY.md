# Agent compatibility

The format aims to follow [Agent Skills](https://agentskills.io/specification) using a single `skills/market-analysis-atlas/SKILL.md`, related Markdown references, data and portable stdlib Python tools. Different hosts vary in auto-discovery and execution permissions.

Project-local installer targets: `codex` and `cursor` → `.agents/skills/`; `opencode` → `.opencode/skills/`; `claude-code` → `.claude/skills/`; `gemini-cli` → `.agents/skills/`; `universal` → `.agents/skills/`.

```bash
python scripts/install.py --project /path/to/project --agent opencode --dry-run
python scripts/install.py --project /path/to/project --agent opencode
```

The installer refuses to overwrite a pre-existing skill directory unless `--force` is explicitly provided, and refuses to replace symlinks. `npx skills add ...` may provide broader installation via its own maintained registry after public GitHub publication.

Host detection and behavior have **not** been live tested against every agent. Running offline Python lookup is independent of host support for the skill-discovery standard.
