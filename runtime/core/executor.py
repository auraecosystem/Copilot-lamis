def execute(action, params):
    if action.startswith("wallet_action"):
        return {
            "status": "wallet executed",
            "action": action,
            "params": params
        }

    if action.startswith("transaction_action"):
        return {
            "status": "transaction executed",
            "action": action,
            "params": params
        }

    return {
        "status": "executed",
        "action": action
    }
