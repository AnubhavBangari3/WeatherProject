import types
from app import weather as weather_module


def test_format_weather_for_llm():
    fake_weather = {
        "city": "TestCity",
        "temperature": 25,
        "feels_like": 26,
        "humidity": 40,
        "description": "clear sky",
    }
    text = weather_module.format_weather_for_llm(fake_weather)
    assert "TestCity" in text
    assert "25" in text
    assert "clear sky" in text


def test_get_weather_monkeypatch(monkeypatch):
    """
    Do not hit real API here; mock requests.get.
    """

    class FakeResp:
        status_code = 200   # <-- ADD THIS LINE

        def raise_for_status(self):
            pass

        def json(self):
            return {
                "name": "MockCity",
                "main": {
                    "temp": 20,
                    "feels_like": 21,
                    "humidity": 50,
                },
                "weather": [{"description": "mock clear"}],
            }

    def fake_get(url, params=None, timeout=10):
        return FakeResp()

    monkeypatch.setattr(weather_module.requests, "get", fake_get)

    data = weather_module.get_weather("Whatever")
    assert data["city"] == "MockCity"
    assert data["temperature"] == 20
