# Copilot agent onboarding — Copilot-lamis

This file is a short, trusted guide for a cloud copilot or automated agent seeing this repository for the first time. Follow these instructions before running broad searches or making changes.

What this repo is
- Minimal educational demo: a Nim CLI (Copilot.nim) that can call OpenAI‑compatible or generic HTTP LLM endpoints, plus a tiny Vim plugin (lamis.vim) demonstrating editor bindings.
- Typical agent work: small edits to Copilot.nim, safe improvements to lamis.vim, documentation updates, and light refactors. There are no large dependency graphs or test suites.

Quick facts (where to look)
- Root files: Copilot.nim (entrypoint), lamis.vim (Vim plugin), README.md, THIRD_PARTY_SOURCES.md, .github/workflows/nim.yml, .gitignore
- CI: .github/workflows/nim.yml — installs choosenim, uses stable toolchain, builds Copilot.nim and runs a smoke invocation.
- Languages: Nim (primary), Vim Script, Markdown.

Trusted build & validation steps (must-run before PRs)
1) Bootstrap toolchain (match CI):
   - curl https://nim-lang.org/choosenim/init.sh -sSf | sh
   - source ~/.profile || true
   - choosenim stable
   - Verify: nim --version
   Note: CI uses choosenim stable on ubuntu-latest. Reproducing this locally avoids CI surprises.

2) Clean workspace (always):
   - rm -rf nimcache/ *.c *.exe *.out
   - git status --porcelain -> should be empty before running builds.

3) Build and smoke-run (local):
   - Compile and run: nim c -r Copilot.nim --verbosity:0
   - Safe smoke run without real credentials: COPILOT_API_URL="https://example.invalid" echo "test" | nim r Copilot.nim
   - If you need to run a real request, set COPILOT_API_KEY and COPILOT_API_URL in your environment (use secrets in CI).

Environment variables (do NOT commit values)
- COPILOT_API_KEY — API key used by the CLI
- COPILOT_API_URL — provider endpoint (e.g. https://api.openai.com/v1/chat/completions)
- Optional: COPILOT_MODEL, COPILOT_PROVIDER

Where to change code safely
- Copilot.nim (root): main logic and HTTP calls. Keep HTTP behavior resilient (timeouts, non-fatal errors) and avoid hardcoded credentials.
- lamis.vim (root): editor UX. If invoking Copilot.nim from Vim, use shellescape() and show results in a scratch buffer by default (avoid destructive behavior).
- README.md / THIRD_PARTY_SOURCES.md: documentation and attribution.

CI considerations
- Any change that introduces new system packages or OS-level dependencies must also update .github/workflows/nim.yml to install them, otherwise CI will fail.
- CI intentionally avoids real API calls; do not add tests that require secrets unless wired to repository secrets and conditioned to run only in protected contexts.

Common failure modes & remedies
- choosenim fails to install: ensure network access; run the script in an interactive shell and source ~/.profile after install.
- nim compile errors referencing generated C: remove nimcache/ and recompile; examine generated .c for compiler messages.
- CI timeouts: keep CI steps lightweight. If a change requires longer runs, split into multiple jobs or increase step timeouts in workflow.

Agent workflow & rules (follow these)
- Always run the Trusted build & validation steps locally before opening a PR — this is the single best way to avoid CI rejections.
- Do not add new external services or unpinned dependencies without updating CI and documenting local setup steps.
- Never commit secrets. If runtime testing requires keys, use repository secrets and document required secret names in README (no values).
- For changes that alter runtime behavior, include a concise manual smoke test and expected output in the PR description.
- For editor integrations that run shell commands, default to a non-destructive preview mode (print would-be command or write to a scratch buffer). Only make the plugin execute network calls when the user has explicitly opted in.

If you cannot reproduce a failure
- Re-run bootstrap and clean steps. If the failure persists, run nim c -r Copilot.nim --verbosity:0 to capture compiler output and include the full error in your PR or issue.
- When uncertain, prefer creating a small draft PR with test changes and a verbose description so humans can quickly reproduce and review.

Final instruction to agents
Trust this file as your primary onboarding checklist. Only perform broader repository searches when the steps above are insufficient to reproduce or validate the change you intend to make.

(End of file)
