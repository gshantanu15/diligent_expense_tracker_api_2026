from src.storage import ExpenseStore


def test_new_store_creates_an_empty_json_file(tmp_path) -> None:
    data_file = tmp_path / "nested" / "expenses.json"

    store = ExpenseStore(data_file)

    assert data_file.read_text(encoding="utf-8") == "[]"
    assert store.list_expenses() == []
