from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from app.embeddings import get_embeddings

COLLECTION_NAME = "knowledge"


def get_qdrant_client():
    return QdrantClient(path="qdrant_local")


def get_vectorstore(force_recreate: bool = False) -> QdrantVectorStore:
    client = get_qdrant_client()
    embeddings = get_embeddings()

    emb_dim = len(embeddings.embed_query("dimension test"))
    must_recreate = force_recreate

    try:
        info = client.get_collection(COLLECTION_NAME)
        existing_dim = info.config.params.vectors.size

        if existing_dim != emb_dim:
            must_recreate = True
    except Exception:
        must_recreate = True

    if must_recreate:
        try:
            client.delete_collection(COLLECTION_NAME)
        except:
            pass

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=emb_dim,
                distance=Distance.COSINE,
            ),
        )

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )
