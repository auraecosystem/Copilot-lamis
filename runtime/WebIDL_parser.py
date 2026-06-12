import re

def parse_webidl(file_path):
    with open(file_path, "r") as f:
        text = f.read()

    interfaces = re.findall(r"interface\s+(\w+)\s*{([^}]*)}", text)

    parsed = []

    for name, body in interfaces:
        methods = re.findall(r"(\w+)\s+(\w+)\(([^)]*)\);", body)

        for ret, method, params in methods:
            parsed.append({
                "interface": name,
                "method": method,
                "return_type": ret,
                "params": params
            })

    return parsed
