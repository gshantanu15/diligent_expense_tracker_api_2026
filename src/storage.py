import json
from pathlib import Path

from src.models import Expense, ExpenseCreate


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

    def add_expense(self, expense_data: ExpenseCreate) -> Expense:
        expenses = self.list_expenses()
        next_id = max((expense.id for expense in expenses), default=0) + 1
        expense = Expense(id=next_id, **expense_data.model_dump())
        expenses.append(expense)
        self._write_expenses(expenses)
        return expense

    def _write_expenses(self, expenses: list[Expense]) -> None:
        serializable_expenses = [
            expense.model_dump(mode="json") for expense in expenses
        ]
        self.file_path.write_text(
            json.dumps(serializable_expenses, indent=2),
            encoding="utf-8",
        )
