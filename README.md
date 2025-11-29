# WeatherProject



# ASCII Architecture Diagram

                         ┌─────────────────────────┐
                         │        User Input        │
                         └─────────────┬───────────┘
                                       │
                                       ▼
                         ┌─────────────────────────┐
                         │      Router Node         │
                         │ (LLM-based decision)     │
                         └───────┬─────────┬───────┘
                                 │         │
                                 │         │
                   ┌─────────────┘         └──────────────┐
                   ▼                                        ▼
    ┌──────────────────────────────┐          ┌──────────────────────────────┐
    │        Weather Node          │          │         PDF RAG Node         │
    │------------------------------│          │------------------------------│
    │ extract_city()               │          │ Retriever: QdrantVectorStore │
    │ get_weather()                │          │ get_relevant_documents()     │
    │ format_weather_for_llm()     │          │ build context                │
    └───────────────┬──────────────┘          │ LLM answer_with_rag()       │
                    │                         └───────────────┬────────────┘
                    │                                         │
                    ▼                                         ▼
        ┌──────────────────────────┐              ┌──────────────────────────┐
        │   Weather API (OpenWeather) │           │   Qdrant Local VectorDB  │
        └──────────────────────────┘              └──────────────────────────┘
                                       │
                                       ▼
                           ┌─────────────────────────┐
                           │        Final Answer     │
                           │      (via Streamlit)    │
                           └─────────────────────────┘



## Mermaid Diagram


flowchart TD

    A[User Input] --> B[Router Node<br>(LLM-based)]
    
    B -->|weather| C[Weather Node]
    B -->|pdf| D[PDF RAG Node]
    B -->|unknown| D

    C --> E[extract_city()]
    E --> F[get_weather()]
    F --> G[format_weather_for_llm()]
    G --> Z[Final Answer]

    D --> H[Retriever<br>Qdrant VectorStore]
    H --> I[Build RAG Context]
    I --> J[LLM answer_with_rag()]
    J --> Z[Final Answer]

    F --> W[OpenWeather API]
    H --> V[Qdrant Local DB]


## Architecture Explanation

1. User Input

User types a question in Streamlit:

“What’s the weather in London?”

“Explain chapter 2 from the PDF”

2. Router Node (LLM-based)

Your router_node uses an LLM prompt to decide:

If the query is about weather → go to weather node

If it’s about a PDF question → go to RAG node

This is the heart of your agentic pipeline.

3. Weather Node

This pipeline runs:

extract_city() → detect city name

get_weather() → call OpenWeather API

format_weather_for_llm() → convert into readable text

LLM generates the final answer

4. PDF RAG Node

This pipeline does:

Uses QdrantVectorStore

Retrieves top k=4 relevant chunks

Builds context string

answer_with_rag()

LLM returns final answer

5. Final Answer

Returned to Streamlit cleanly as the chat response.

