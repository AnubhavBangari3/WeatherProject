from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embeddings():
    """Return a stable and small HF embedding model."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
