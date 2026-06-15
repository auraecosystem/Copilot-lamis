This PR adds a simple integration for Copilot-lamis:

- Copilot.nim (already on main) — Nim CLI that can call OpenAI-compatible or generic HTTP endpoints
- lamis.vim — minimal Vim plugin with a mapping to invoke Copilot.nim and show results
- README.md — usage and setup instructions
- THIRD_PARTY_SOURCES.md — referenced/credited repositories and language composition metadata
- .github/workflows/nim.yml — CI: install Nim, build Copilot.nim, smoke-run
- .gitignore

Notes:
- CI does not call real external APIs and uses a smoke run only.
- Do not commit API keys. Use repository secrets for any legitimate CI runs that require secrets.
- Confirm license and attribution requirements for referenced third-party projects.

Reviewer checklist:
- [ ] No secrets in commits
- [ ] README instructions are clear and reproduce the example locally
- [ ] CI is non-destructive and does not expose secrets
- [ ] Licensing/attribution reviewed for included references
- [ ] Try the lamis.vim mapping on a Nim file: open a Nim file, press <Leader>lc, enter a prompt, and verify output appears in a scratch buffer
