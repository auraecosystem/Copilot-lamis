def decide_action(parsed_item):
    interface = parsed_item["interface"]
    method = parsed_item["method"]

    # Simple rule engine (upgrade later to LLM)
    if interface.lower() == "wallet":
        return f"wallet_action:{method}"

    if interface.lower() == "transaction":
        return f"transaction_action:{method}"

    return f"generic_action:{method}"
