from pathlib import Path


def test_session_form_exists():
    form_path = Path(__file__).resolve().parents[1] / "web" / "session_form.html"
    assert form_path.exists(), "session_form.html should exist"

    content = form_path.read_text(encoding="utf-8")
    required_fields = [
        '<input type="date"',
        '<input type="number"',
        '<input type="file"',
        '<textarea',
    ]
    for field in required_fields:
        assert field in content, f"Expected {field} in HTML form"

