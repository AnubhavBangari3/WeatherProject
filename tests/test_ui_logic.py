from app.agent_graph import agent_app
from app import agent_graph as ag


def test_agent_weather(monkeypatch):
    def fake_weather(city):
        return {
            "city": city,
            "temperature": 30,
            "feels_like": 29,
            "humidity": 40,
            "description": "clear sky",
        }

    # Patch weather only – router + LLM can behave normally
    monkeypatch.setattr("app.weather.get_weather", fake_weather)

    out = agent_app.invoke({"input": "weather in delhi"})
    assert "delhi" in out["answer"].lower()


def test_agent_pdf(monkeypatch):
    # Patch the answer_with_rag used *inside agent_graph*
    monkeypatch.setattr(ag, "answer_with_rag", lambda q: "PDF says hello")

    out = agent_app.invoke({"input": "explain chapter 2"})
    assert "hello" in out["answer"].lower()
