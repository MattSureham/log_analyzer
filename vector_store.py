from sentence_transformers import SentenceTransformer
import chromadb

class VectorStore:
    def __init__(self, persist_dir=".chroma", collection_name="knowledge"):
        self.client = chromadb.Client(
            chromadb.config.Settings(persist_directory=persist_dir)
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add_documents(self, docs):
        embeddings = self.model.encode(docs).tolist()
        ids = [f"doc_{i}" for i in range(len(docs))]

        self.collection.add(
            documents=docs,
            embeddings=embeddings,
            ids=ids
        )

    def query(self, text, top_k=3):
        embedding = self.model.encode([text]).tolist()

        results = self.collection.query(
            query_embeddings=embedding,
            n_results=top_k
        )

        return results["documents"][0]
