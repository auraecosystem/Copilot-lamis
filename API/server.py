from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/completions")
def get_completions():
    with open("storage/completion.json", "r") as f:
        return json.load(f)


@app.post("/run")
def run_prompt(prompt: str):
    return {
        "status": "connected",
        "message": f"Received prompt: {prompt}"
    }
