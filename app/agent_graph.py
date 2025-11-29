from typing import TypedDict, Literal

from langgraph.graph import StateGraph, END

from langchain_core.prompts import ChatPromptTemplate

from app.llm import llm
from app.weather import get_weather, format_weather_for_llm
from app.rag import answer_with_rag


class AgentState(TypedDict):
    input: str
    route: Literal["weather", "pdf", "unknown"]
    answer: str


def router_node(state: AgentState) -> AgentState:

    user_input = state["input"]

    prompt = ChatPromptTemplate.from_template(
        """You are a router for an AI agent.

Decide if the user is asking about:
- 'weather' (temperature, rain, forecast, city weather, etc.)
- 'pdf' (questions about knowledge, concepts, definitions, document content)
Return ONLY one word: weather or pdf.

User message:
{message}
"""
    )

    decision = (prompt | llm).invoke({"message": user_input})
    decision_text = str(
        getattr(decision, "content", decision)
    ).strip().lower()

    if "weather" in decision_text:
        route: AgentState["route"] = "weather"
    elif "pdf" in decision_text:
        route = "pdf"
    else:
        route = "unknown"

    return {
        **state,
        "route": route,
    }


def weather_node(state: AgentState) -> AgentState:

    user_input = state["input"]

    # Simple approach: assume user mentions city as last word or whole input.
    # For production, you'd parse more robustly.
    city = user_input.strip()

    weather_data = get_weather(city)
    weather_text = format_weather_for_llm(weather_data)

    prompt = ChatPromptTemplate.from_template(
        """You are a helpful weather assistant.

Given this structured weather data, explain it in friendly language
for the user.

Weather info:
{weather}

User question:
{question}
"""
    )
    response = (prompt | llm).invoke(
        {"weather": weather_text, "question": user_input}
    )
    answer_text = (
        response.content if hasattr(response, "content") else str(response)
    )

    return {
        **state,
        "answer": answer_text,
    }


def pdf_node(state: AgentState) -> AgentState:

    user_input = state["input"]
    answer_text = answer_with_rag(user_input)
    return {
        **state,
        "answer": answer_text,
    }


def unknown_node(state: AgentState) -> AgentState:

    answer_text = answer_with_rag(state["input"])
    return {
        **state,
        "answer": answer_text,
    }


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("weather", weather_node)
    graph.add_node("pdf", pdf_node)
    graph.add_node("unknown", unknown_node)

    graph.set_entry_point("router")

    # Conditional edges from router
    def route_selector(state: AgentState) -> str:
        if state["route"] == "weather":
            return "weather"
        elif state["route"] == "pdf":
            return "pdf"
        else:
            return "unknown"

    graph.add_conditional_edges(
        "router",
        route_selector,
        {
            "weather": "weather",
            "pdf": "pdf",
            "unknown": "unknown",
        },
    )

    # Each terminal node goes to END
    graph.add_edge("weather", END)
    graph.add_edge("pdf", END)
    graph.add_edge("unknown", END)

    app = graph.compile()
    return app


# Create a singleton app for reuse
agent_app = build_graph()
