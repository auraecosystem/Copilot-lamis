def generate_fastapi(parsed):
    code = []
    code.append("from fastapi import FastAPI\n")
    code.append("app = FastAPI()\n\n")

    for interface, methods in parsed.items():
        for return_type, name, params in methods:

            param_list = params.replace("string", "str").replace("float", "float").replace("boolean", "bool")

            endpoint = f"""
@app.post("/{interface.lower()}/{name}")
def {name}({param_list}):
    return {{
        "status": "ok",
        "interface": "{interface}",
        "method": "{name}"
    }}

"""
            code.append(endpoint)

    return "\n".join(code)
