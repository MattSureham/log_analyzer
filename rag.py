# RAG

from vector_store import VectorStore

_store = None

def init_vector_store(kb_path="knowledge.txt"):
    global _store
    if _store is not None:
        return _store

    store = VectorStore()

    with open(kb_path, "r") as f:
        chunks = f.read().split("\n\n")

    store.add_documents(chunks)
    _store = store
    return store

def retrieve_context(log_text: str, top_k=3):
    store = init_vector_store()
    docs = store.query(log_text, top_k=top_k)
    return "\n\n".join(docs)

'''
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
'''
