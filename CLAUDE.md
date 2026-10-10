# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Agent Instructions
You're working inside the **WAT framework** (Workflows, Agents, Tools). This architecture separates concerns so that probabilistic AI handles reasoning while deterministic code handles execution. That separation is what makes this system reliable.

## The WAT Architecture
**Layer 1: Workflows (The Instructions)**
- Markdown SOPs stored in `workflows/`
- Each workflow defines the objective, required inputs, which tools to use, expected outputs, and how to handle edge cases
- Written in plain language, the same way you'd brief someone on your team

**Layer 2: Agents (The Decision-Maker)**
- This is your role. You're responsible for intelligent coordination.
- Read the relevant workflow, run tools in the correct sequence, handle failures gracefully, and ask clarifying questions when needed
- You connect intent to execution without trying to do everything yourself
- Example (illustrative only; these files don't exist yet): If you need to pull data from a website, don't attempt it directly. Read `workflows/scrape_website.md`, figure out the required inputs, then execute `tools/scrape_single_site.py`

**Layer 3: Tools (The Execution)**
- Python & powershell scripts in `tools/` that do the work
- API calls, data transformations, file operations, database queries
- Credentials and API keys are stored in `.env`
- These scripts are consistent, testable, and fast

## How to Operate
- Try to reuse exsting tools in the `tools/` folder.
- After every chagnge run the unit tests. They must all pass before proceeding.
- If you make some changes that involve more than 1 line, display a summary of the changes to me in the termainal and ask me to approve. Ask clarifying questions or give me alternatives to choose from if there is ambiguity.
- Once I have approved the changes, stage & commit the code changes. 
-When you start the project, if there is no data, seed the sample data from 
`src\seeds\seed_StudentEnrolements.py`
-For unit testing, Use the moto library to simulate a dynamo db in memory.
- Run every command from the project root. The `src.` module imports depend on it.
- Format code with `.\tools\FormatPythonFile.ps1`, which runs `ruff format src tests` (Ruff is installed in `.venv`). Don't run `ruff format *`, which also reaches other directories.
- New routers: create the module in `src/api/` with an `APIRouter(prefix=...)` and register it in `src/main.py` with `app.include_router(...)`.
- Use `httpx2`, not `httpx`, for FastAPI's `TestClient`. With `httpx` this Starlette version prints a deprecation warning.
- PUT replaces the whole record. Send every field, or the omitted optional fields become null.

## Steps
- Start the server from the project root: `.\tools\StartServer.ps1`
   Interactive docs Url: http://127.0.0.1:8000/docs
- When you start the project, if there is no data in teh StudentEntrolements table, seed the data with this script `.\tools\SeedData.ps1`
- Run the unit tests with tihs script `.\tools\RunUnitTests.ps1`

## Folder structure
.github/    * Git files
.tmp/		# Temporary files (scraped data, intermediate exports). Regenerated as needed.
tools/		# Python scripts for deterministic execution
workflows/	# Markdown SOPs defining what to do and how
.env		# API keys and environment variables
out/		# Local final outputs, only when a deliverable can't go to a cloud service

## Context Boundaries (STRICT)
ALLOWED directories (you may read, write, and list):
- `src/*`
- `tests/`
- `tools/`
- `workflows/`
- `config/` (if present)
- `.tmp/` (for generated data only)
- `out/` (for final outputs)
- `.venv/` (project-local virtualenv; install packages here only)
- Root-level files only: `.env`, `pyproject.toml`, `.gitignore`, `CLAUDE.md`

## Language Type
- Never make assumptions when important information is missing.
- Keep outputs concise and relevant.
- Do not add filler content to increase length.
- Stay within requested word counts and formats.
- Use practical examples whenever possible.
- When multiple approaches exist, explain the tradeoffs.
- If uncertain, ask before proceeding.
- Review outputs before final delivery.

## Git commits
Every time I ask for a series of instructions to be carried out, finish with a git commit:
1. Run `.\tools\PreCommitCheck.ps1` (formats with Ruff, then runs the tests). Don't commit if a test fails; fix it or report it first.
2. Commit only project files (`src/`, `tests/`, `tools/`, `workflows/`, `pyproject.toml`, `.gitignore`, `CLAUDE.md`). Never commit `.env`, `credentials.json`, `token.json` or `.venv/`; `.gitignore` already excludes them.
3. Make one commit per logical change, with a message that says what changed and why.
