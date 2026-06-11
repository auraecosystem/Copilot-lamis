# Copilot.nim
# Minimal Nim CLI that sends a prompt to an OpenAI-compatible chat endpoint or to a generic HTTP endpoint.
# Usage examples:
#  COPILOT_API_KEY=... COPILOT_API_URL=https://api.openai.com/v1/chat/completions nim r Copilot.nim "Write a haiku about Nim"
#  COPILOT_PROVIDER=generic COPILOT_API_URL=https://example.com/generate COPILOT_API_KEY=... nim r Copilot.nim "Summarize this"

import os, strutils, httpclient, json, sequtils

const
  defaultModel = "gpt-4o-mini"

proc envOr(name, fallback: string = ""): string =
  let v = getEnv(name)
  if v.len == 0: fallback else: v

proc postJSON(url: string, bodyJson: string, headers: seq[tuple[string,string]] = @[]): string =
  var client = newHttpClient()
  for h in headers:
    client.headers.add(h[0], h[1])
  try:
    let resp = client.request("POST", url, bodyJson)
    result = resp.body
  except HttpRequestError as e:
    quit("HTTP request failed: " & e.msg)

proc sendToOpenAI(apiUrl, apiKey, model, prompt: string): string =
  # Expecting an OpenAI-compatible chat completions endpoint (POST /v1/chat/completions)
  let payload = %*{
    "model": $(model),
    "messages": [ { "role": "user", "content": $(prompt) } ],
    "temperature": 0.7
  }
  let body = $payload
  let hdrs = @[("Authorization", "Bearer " & apiKey), ("Content-Type", "application/json")]
  let respBody = postJSON(apiUrl, body, hdrs)
  # Try parsing response for chat-completions shape
  try:
    let parsed = parseJson(respBody)
    if parsed.hasKey("choices"):
      let ch = parsed["choices"].get(0)
      if ch.hasKey("message") and ch["message"].hasKey("content"):
        return ch["message"]["content"].getStr
      elif ch.hasKey("text"):
        return ch["text"].getStr
    # fallback: return raw body
    return respBody
  except JsonParsingError:
    return respBody

proc sendToGeneric(apiUrl, apiKey, prompt: string): string =
  # Simple generic POST with JSON {"prompt": "..."}; adjust server behaviour as needed.
  let payload = %*{ "prompt": $(prompt) }
  let hdrs = @[("Content-Type", "application/json")]
  if apiKey.len > 0:
    hdrs.add(("Authorization", "Bearer " & apiKey))
  return postJSON(apiUrl, $payload, hdrs)

when isMain:
  let prompt =
    if paramCount() > 0: joinParams(" ")
    else: readLine(stdin) & ""
  if prompt.len == 0:
    echo "Usage: nim r Copilot.nim \"your prompt here\""
    quit(1)

  let provider = envOr("COPILOT_PROVIDER", "openai").toLowerAscii
  let apiKey = envOr("COPILOT_API_KEY", "")
  var apiUrl = envOr("COPILOT_API_URL", "")
  let model = envOr("COPILOT_MODEL", defaultModel)

  if provider == "openai" or provider == "openai-compatible" or provider == "openai-compatible":
    if apiUrl.len == 0:
      # default to OpenAI v1 chat completions if not set
      apiUrl = "https://api.openai.com/v1/chat/completions"
    if apiKey.len == 0:
      quit("COPILOT_API_KEY is required for provider=openai")
    let out = sendToOpenAI(apiUrl, apiKey, model, prompt)
    echo out
  else:
    if apiUrl.len == 0:
      quit("COPILOT_API_URL must be set for generic providers")
    let out = sendToGeneric(apiUrl, apiKey, prompt)
    echo out
