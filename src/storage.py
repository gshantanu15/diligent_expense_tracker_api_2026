import json
from pathlib import Path

from src.models import Expense


class ExpenseStore:
    """Store expenses in a local JSON file."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._create_file_if_missing()

    def _create_file_if_missing(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def list_expenses(self) -> list[Expense]:
        raw_expenses = json.loads(self.file_path.read_text(encoding="utf-8"))
        return [Expense.model_validate(expense) for expense in raw_expenses]
