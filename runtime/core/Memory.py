import json
import os
from datetime import datetime

FILE = "storage/completion.json"

def log_event(event):
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump([], f)

    with open(FILE, "r") as f:
        data = json.load(f)

    data.append({
        "timestamp": datetime.utcnow().isoformat(),
        "event": event
    })

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)
