# Copilot-lamis

Lightweight repo combining a Nim CLI (Copilot.nim) and a small Vim plugin (lamis.vim) to demonstrate simple LLM integration and editor bindings.

```bash
>_nim dev
>_general dev
```
Overview
- Copilot.nim — Nim CLI that can send prompts to an OpenAI-compatible or generic HTTP endpoint.
- lamis.vim — Minimal Vim plugin that demonstrates invoking Copilot.nim from the editor.
- CI — Workflow that installs Nim and runs a smoke test.

Quick start (local)
1. Set environment variables:
   - COPILOT_API_KEY — your API key for the provider
   - COPILOT_API_URL — endpoint URL (e.g. https://api.openai.com/v1/chat/completions)
   - Optional: COPILOT_MODEL — model to request (default gpt-4o-mini)

2. Run Copilot.nim:
```bash
# example: prompt from command line
COPILOT_API_KEY=... COPILOT_API_URL=https://api.openai.com/v1/chat/completions nim r Copilot.nim "Write a short poem about Nim"
