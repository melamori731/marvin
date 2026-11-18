# Requirement Analyst Skill

Strict synthesis and verification gate for product requirements.

## Recognition in Cursor

This is a **project skill** located at `.cursor/skills/requirement-analyst/SKILL.md`.

Cursor recognizes it automatically when you open this repository because project skills live under `.cursor/skills/`.

The skill can be auto-applied when the user asks to analyze requirements, verify scope, surface gaps, or decide readiness for planning.

## Invoke Explicitly

You can also invoke it from the slash menu as:

```text
/requirement-analyst
```

Then provide the source details in the same message, for example:

```text
/requirement-analyst @input.md
```

You can add more sources in the same message:

```text
/requirement-analyst @input.md @docs/architecture.md PROJ-123
```

The work item ID becomes the output folder name under `requirements/<ticket-id>/`.

## Install Globally (Optional)

If you want the same skill in other repositories, copy this skill directory into `~/.cursor/skills/`:

```bash
mkdir -p ~/.cursor/skills
rm -rf ~/.cursor/skills/requirement-analyst
cp -R "$PWD/.cursor/skills/requirement-analyst" ~/.cursor/skills/requirement-analyst
```

After updates in this repo, re-run the copy command to refresh the global skill.

## Outputs

Seven markdown files plus a machine-readable handoff under `requirements/<ticket-id>/`, structured per templates in `.cursor/skills/requirement-analyst/templates/`:

| File | Content |
|------|---------|
| `requirements/<ticket-id>/assumptions.md` | **Start here**: readiness, assumptions, architecture assumptions, open questions |
| `requirements/<ticket-id>/constraints.md` | Technical, architectural, and operational constraints |
| `requirements/<ticket-id>/functional.md` | Functional requirements |
| `requirements/<ticket-id>/quality.md` | Quality / non-functional requirements |
| `requirements/<ticket-id>/invariants.md` | System invariants |
| `requirements/<ticket-id>/policies.md` | Software architecture policies: business or operational rules the system chooses to apply |
| `requirements/<ticket-id>/conflicts-and-ambiguities.md` | Conflicts and ambiguities in one traceable table format |
| `requirements/<ticket-id>/handoff.json` | Autonomous handoff contract for the planner |

## Behavior summary

The analyst:

- clarifies blocking and high-impact ambiguities with the human in short prioritized rounds
- reduces candidates to a minimal, non-overlapping canonical requirement set
- highlights a small `critical | high | normal` set of canonical items that must anchor planning
- writes priority anchors and `minimumAcceptedScope` to `handoff.json` for the planner

`SKILL.md` defines the detailed operating rules; this README is an invocation and output reference.

## Reference

- Skill: [`SKILL.md`](./SKILL.md)
- Templates: [`templates/`](./templates/)
- Spec: [`specs/requirement_analyst_agent_spec.md`](../../../specs/requirement_analyst_agent_spec.md)
- Sequenced run: [`marvin`](../marvin/README.md) runs this analyst first and still stops for human resolution when the handoff requires it
