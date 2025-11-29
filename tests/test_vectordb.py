from pathlib import Path

from qdrant_client import QdrantClient
from langchain_core.documents import Document

import app.vectorstore as vs_mod


def test_vectorstore_add_and_search(tmp_path, monkeypatch):
    # Use a per-test Qdrant folder to avoid lock conflicts
    qdrant_path = tmp_path / "qdrant_test"

    def fake_get_qdrant_client():
        return QdrantClient(path=str(qdrant_path))

    monkeypatch.setattr(vs_mod, "get_qdrant_client", fake_get_qdrant_client)

    vs = vs_mod.get_vectorstore(force_recreate=True)

    docs = [
        Document(page_content="Hello world"),
        Document(page_content="AI is amazing"),
    ]
    vs.add_documents(docs)

    retriever = vs.as_retriever(search_kwargs={"k": 1})
    results = retriever.invoke("hello")

    assert len(results) >= 1
    assert "hello" in results[0].page_content.lower()
