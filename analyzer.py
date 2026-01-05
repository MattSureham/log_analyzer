from prompt import build_prompt

def analyze_logs(log_file: str, llm):
    with open(log_file, "r") as f:
        logs = f.read()

    messages = build_prompt(logs)

    print("Analyzing logs...\n")
    result = llm.chat(messages)

    print("=== Analysis Result ===")
    print(result)
