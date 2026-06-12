from engine.generator import generate_completion
from engine.logger import save_completion

def run(prompt):
    completion = generate_completion("aura-model-v1", prompt)
    save_completion(completion)

    return completion

if __name__ == "__main__":
    result = run("Create wallet for user AUR001")
    print(result)
