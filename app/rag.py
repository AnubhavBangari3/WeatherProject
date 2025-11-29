from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

from app.config import PDF_PATH
from app.llm import llm
from app.vectorstore import get_vectorstore



def load_pdf_documents():
    loader = PyPDFLoader(PDF_PATH)
    return loader.load()



def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )
    return splitter.split_documents(docs)



def ingest_pdf_into_qdrant(force_rebuild: bool = False):  
    vs = get_vectorstore(force_recreate=force_rebuild)
    docs = load_pdf_documents()
    chunks = chunk_documents(docs)

    # Add chunks to vectorstore
    vs.add_documents(chunks)

    return len(chunks)



def answer_with_rag(query: str) -> str:

    vs = get_vectorstore()  
    retriever = vs.as_retriever(search_kwargs={"k": 4})
    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join(d.page_content for d in docs)

    prompt = ChatPromptTemplate.from_template("""
Use ONLY the context to answer.
If the context does not contain the answer, say "I do not know."

Question:
{q}

Context:
{ctx}

Answer:
""")

    response = (prompt | llm).invoke({"q": query, "ctx": context})
    return response.content
