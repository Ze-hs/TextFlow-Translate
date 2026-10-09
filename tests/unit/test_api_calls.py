from openrouter import call_openrouter


def test_openrouter_connection():
    response = call_openrouter("Hi")
    assert(response.ok)