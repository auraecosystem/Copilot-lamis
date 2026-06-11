# Copilot agent onboarding — Copilot-lamis

Summary
- Small, educational repo demonstrating a Nim CLI (Copilot.nim) that calls OpenAI‑compatible or generic HTTP LLM endpoints, plus a minimal Vim plugin (lamis.vim) that shows how to invoke the CLI from the editor.
- Purpose for an agent: implement small edits, refactors, or improvements to Copilot.nim and lamis.vim; update docs and CI; produce small demos.

Repository at-a-glance
- Size & type: Very small source tree (single Nim CLI + auxiliary files and a tiny Vim plugin). No heavy dependency graph or tests.
- Languages: Nim (primary), small Vim Script file, and ancillary Markdown. (Languages: Nim ~44%, Python ~39% in metadata — but active source is Nim + Vim Script.)
- Key files/paths (root):
  - Copilot.nim — main CLI (project entrypoint)
  - lamis.vim — minimal Vim plugin
  - README.md — usage and quick-start
  - .github/workflows/nim.yml — CI that installs Nim and runs a smoke build/run
  - .gitignore, THIRD_PARTY_SOURCES.md, HIGHLIGHT.md (may exist), doc/ and Rdoc/ directories

Build & validation (trusted sequence — follow these exactly before opening PRs)
1) Bootstrap environment (Linux / Ubuntu CI-like environment assumed):
   - Install choosenim (Nim toolchain installer) and select stable toolchain:
     - curl https://nim-lang.org/choosenim/init.sh -sSf | sh
     - source ~/.profile || true
     - choosenim stable
   - Always verify with: nim --version
   - Rationale: CI installs choosenim and uses the stable toolchain; matching that minimizes CI mismatch.

2) Clean workspace (recommended before build):
   - Remove Nim cache and previous artifacts: rm -rf nimcache/ *.c *.exe *.out
   - Ensure working tree is clean: git status --porcelain should be empty for CI-like runs.

3) Build and run (local reproduction of CI):
   - Build and run in one step (compiles then runs): nim c -r Copilot.nim --verbosity:0
     - Notes: The repository's CI uses the same command but allows failure (|| true). Locally, expect nim to compile and then run the program.
   - Smoke-run without real credentials (safe test):
     - COPILOT_API_URL="https://example.invalid" echo "test" | nim r Copilot.nim
     - This verifies CLI input path without calling real APIs.

4) Environment variables used by runtime (do NOT commit secrets):
   - COPILOT_API_KEY — API key
   - COPILOT_API_URL — endpoint URL (e.g., https://api.openai.com/v1/chat/completions)
   - Optional: COPILOT_MODEL (default gpt-4o-mini), COPILOT_PROVIDER ("openai" or "generic")
   - When testing real requests, use GitHub Actions secrets or local env, never commit keys into the repo.

5) Tests & lints
   - There are no automated test suites or linter configs present. The CI performs only a smoke build/run. For changes that add behavior, include reproducible manual smoke tests in the PR description.

CI / Checks to expect
- GitHub Actions workflow: .github/workflows/nim.yml
  - Installs choosenim, selects stable, prints nim --version, runs nim c -r Copilot.nim and a smoke run.
  - Keep changes compatible with a fresh choosenim stable install and a default Ubuntu runner.
- Before submitting a PR, verify locally using the Build & run steps above so CI will likely pass.

Project layout and where to make edits
- Entry point: Copilot.nim (root) — edits here change runtime behavior.
- Editor integration: lamis.vim (root) — safe to change UX/mappings; if you run system() from Vim, ensure shellescape and safe quoting are used to avoid command injection.
- Docs and metadata: README.md, THIRD_PARTY_SOURCES.md, .github/*

Non-obvious dependencies / gotchas
- The project depends on the Nim toolchain; the choosenim installer modifies ~/.profile. When scripting in ephemeral shells, ensure profile is sourced before calling choosenim/nim.
- Nim builds generate C files and nimcache/ directory; these are ignored by .gitignore but will appear locally.
- There is no package manager manifest (no .nimble file required for current sources); treat Copilot.nim as a standalone Nim script.
- lamis.vim may attempt to call Copilot.nim — when updating, prefer safe behavior that prints the command or writes to a scratch buffer by default unless explicitly configured.

Rules-of-thumb for agents (follow these to reduce rejected PRs)
- Always replicate CI steps locally (bootstrap choosenim stable then run nim c -r Copilot.nim) and confirm the smoke run succeeds before creating a PR.
- Never add code that requires additional system packages on CI without also updating .github/workflows/nim.yml to install them.
- Do not commit secrets or credentials. Use repo secrets for CI and document required secrets in README (without values).
- For Vim plugin changes that spawn shell commands, use shellescape() and sanitize inputs. Prefer writing output to a scratch buffer instead of opening external windows.
- If adding tests or linters, include CI updates and document how to run them locally.

If something fails
- If choosenim installation fails, retry with a fresh shell and ensure curl succeeds; source ~/.profile then run choosenim stable.
- If nim c fails with C compilation errors, remove nimcache/ and retry. Inspect generated .c file for hints.
- If CI fails with timeouts, split heavy work into separate steps or avoid network calls in CI; the current CI is intentionally light.

Final note to agents
Trust these onboarding instructions for routine exploration and build tasks. Only perform additional repo-wide searches or tool calls when you cannot reproduce an expected result using the steps above or when the change requires locating files not listed here.

(End of instructions)
