from code_capture import CodeCapture

def test_code_is_captured():
    with CodeCapture("hello") as cc:
        name = "world"
        print(f"Hello, {name}!")
    assert CodeCapture.store["hello"] == "name = \"world\"\nprint(f\"Hello, {name}!\")\n"

