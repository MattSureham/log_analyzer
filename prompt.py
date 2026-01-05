def build_prompt(log_text: str):
    return [
        {
            "role": "system",
            "content": (
                "You are a senior DevOps engineer. "
                "Analyze application logs and identify errors, root causes, "
                "and possible fixes."
            )
        },
        {
            "role": "user",
            "content": f"Here are the logs:\n\n{log_text}"
        }
    ]
