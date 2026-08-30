# Project Interview Skills

Four Codex skills for structuring project stories, preparing interview answers, reviewing real interviews, and tracing agent errors.

## Skills

- [structure-project-interview](structure-project-interview/) — organize project material into a Why, problem, strategy, validation, and iteration loop.
- [prepare-project-interview-answers](prepare-project-interview-answers/) — produce question-specific memory frameworks, spoken answers, and likely follow-ups.
- [interview-retrospect](interview-retrospect/) — turn an interview transcript into evidence-based analysis, scoring, priorities, and a preparation plan.
- [trace-agent-error](trace-agent-error/) — reconstruct an agent decision path, test causal factors, and propose minimal interventions.

## Installation

Copy the desired skill directory into your Codex skills directory. Keep each directory name unchanged so it matches the skill name in SKILL.md.

## Privacy

The repository contains only skill instructions, templates, validation code, and clearly labeled synthetic evaluation data. Do not commit real resumes, PRDs, internal company material, interview transcripts, generated reports, logs, credentials, or local working directories.

## Validation

Each skill passes the Codex quick_validate.py structural check. The interview retrospective evaluation JSON is valid, and the bundled report validator uses only the Python standard library.
