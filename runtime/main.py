from core.webidl_parser import parse_webidl
from core.agent_engine import decide_action
from core.executor import execute
from core.memory import log_event

def run_system():
    parsed = parse_webidl("idl/aura.idl")

    for item in parsed:
        action = decide_action(item)
        result = execute(action, item)

        log_event({
            "parsed": item,
            "action": action,
            "result": result
        })

        print(result)

if __name__ == "__main__":
    run_system()
