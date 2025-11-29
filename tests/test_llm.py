from app.llm import llm


def test_llm_basic_invoke():

    resp = llm.invoke("Say 'test-ok' in one word.")
    text = resp.content if hasattr(resp, "content") else str(resp)
    assert "test" in text.lower()


def test_llm_responds_with_string():
    resp = llm.invoke("Say the word test.")
    text = resp.content if hasattr(resp, "content") else str(resp)
    assert isinstance(text, str)
    assert "test" in text.lower()


def test_llm_refuses_empty_prompt():
    resp = llm.invoke("")
    text = resp.content if hasattr(resp, "content") else str(resp)
    assert len(text.strip()) > 0