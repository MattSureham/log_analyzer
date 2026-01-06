from rag import retrieve_context

def build_prompt(log_text: str):
    context = retrieve_context(log_text)

    return [
        {
            "role": "system",
            "content": (
                "You are a senior DevOps engineer. "
                "Use the provided context to analyze logs, "
                "identify root causes, and suggest fixes."
            )
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Logs:\n{log_text}"
            )
        }
    ]
