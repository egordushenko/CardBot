from pathlib import Path


def test_payments_file_is_only_robokassa_todo_comment():
    content = Path("payments.py").read_text(encoding="utf-8").strip()

    assert content == "# TODO: Robokassa integration"
