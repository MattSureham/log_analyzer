# RAG
def retrieve_context(log_text: str, kb_path="knowledge.txt", max_chunks=3):
    with open(kb_path, "r") as f:
        kb = f.read().split("\n\n")

    relevant = []
    for chunk in kb:
        for line in log_text.splitlines():
            if line.lower() in chunk.lower():
                relevant.append(chunk)
                break

        if len(relevant) >= max_chunks:
            break

    return "\n\n".join(relevant)
