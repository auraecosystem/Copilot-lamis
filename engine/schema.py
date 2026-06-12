from datetime import datetime
import uuid

def create_completion(model, prompt, response):
    return {
        "id": str(uuid.uuid4()),
        "model": model,
        "prompt": prompt,
        "response": response,
        "created_at": datetime.utcnow().isoformat()
    }
