from pathlib import Path

from src.storage import ExpenseStore


# Leave data/expenses.json untouched and verify that a new store starts empty.
def test_new_store_creates_an_empty_json_file(test_directory: Path) -> None:
    data_file = test_directory / "nested" / "expenses.json"

    store = ExpenseStore(data_file)

    assert data_file.read_text(encoding="utf-8") == "[]"
    assert store.list_expenses() == []
