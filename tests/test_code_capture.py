from code_capture import CodeCapture

def test_code_is_captured():
    with CodeCapture("hello"):
        name = "world"
        print(f"Hello, {name}!")
    assert CodeCapture.store["hello"] == "name = \"world\"\nprint(f\"Hello, {name}!\")\n"

def test_code_is_captured_with_line_processor():
    def trim_if_bool_processor(line: str):
        if line.lstrip() in ("if False:\n", "if True:\n"):
            return None
        return line
    with CodeCapture("hello", line_processor=trim_if_bool_processor):
        if True:
            name = "world"
            print(f"Hello, {name}!")
    assert CodeCapture.store["hello"] == "name = \"world\"\nprint(f\"Hello, {name}!\")\n"
