from app import agent_graph as ag
from app.agent_graph import AgentState
from langchain_core.runnables import RunnableLambda


def make_fake_llm(output_text: str):
    """Return a Runnable LLM that always outputs the given text."""

    def fake_invoke(_):
        class Resp:
            def __init__(self, content):
                self.content = content
        return Resp(output_text)

    # RunnableLambda makes it compatible with (prompt | llm)
    return RunnableLambda(lambda x: fake_invoke(x))


def test_router_weather(monkeypatch):
    monkeypatch.setattr(ag, "llm", make_fake_llm("weather"))

    state: AgentState = {
        "input": "weather in delhi",
        "route": "unknown",
        "answer": ""
    }

    new_state = ag.router_node(state)
    assert new_state["route"] == "weather"


def test_router_pdf(monkeypatch):
    monkeypatch.setattr(ag, "llm", make_fake_llm("pdf"))

    state: AgentState = {
        "input": "explain chapter 2",
        "route": "unknown",
        "answer": ""
    }

    new_state = ag.router_node(state)
    assert new_state["route"] == "pdf"
