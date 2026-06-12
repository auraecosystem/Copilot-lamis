import re

def parse_webidl(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    interfaces = re.findall(r"interface\s+(\w+)\s*{([^}]*)}", content)

    parsed = {}

    for name, body in interfaces:
        methods = re.findall(r"(\w+)\s+(\w+)\(([^)]*)\);", body)
        parsed[name] = methods

    return parsed
