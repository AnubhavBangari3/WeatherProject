from langchain_core.documents import Document
from app.rag import chunk_documents, answer_with_rag

def test_chunk_documents_basic():
    docs = [Document(page_content="Hello " * 300)]
    chunks = chunk_documents(docs)
    assert len(chunks) > 1
    assert all(len(c.page_content) > 0 for c in chunks)


def test_chunk_documents_respects_chunk_size():
    text = "Hello world " * 1000
    chunks = chunk_documents([Document(page_content=text)])
    assert len(chunks) > 3


def test_answer_with_rag_empty_context(monkeypatch):
    # Fake vectorstore with no results
    class FakeRetriever:
        def get_relevant_documents(self, q):
            return []

    class FakeVS:
        def as_retriever(self, search_kwargs=None):
            return FakeRetriever()

    monkeypatch.setattr("app.rag.get_vectorstore", lambda: FakeVS())

    answer = answer_with_rag("What is quantum physics?")
    assert "I do not know" in answer
