import json
from pathlib import Path

from src.models import Category, Expense, ExpenseCreate


class ExpenseStore:
    """Store expenses in a local JSON file."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._create_file_if_missing()

    def _create_file_if_missing(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def list_expenses(
        self,
        category: Category | None = None,
    ) -> list[Expense]:
        raw_expenses = json.loads(self.file_path.read_text(encoding="utf-8"))
        expenses = [
            Expense.model_validate(expense) for expense in raw_expenses
        ]
        if category is None:
            return expenses
        return [
            expense for expense in expenses if expense.category == category
        ]

    def add_expense(self, expense_data: ExpenseCreate) -> Expense:
        expenses = self.list_expenses()

        # Generate a new ID with a basic auto-increment strategy.
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

    def calculate_total(
        self,
        category: Category | None = None,
    ) -> float:
        return sum(
            expense.amount for expense in self.list_expenses(category)
        )

    def delete_expense(self, expense_id: int) -> bool:
        expenses = self.list_expenses()
        remaining_expenses = [
            expense for expense in expenses if expense.id != expense_id
        ]
        if len(remaining_expenses) == len(expenses):
            return False

        self._write_expenses(remaining_expenses)
        return True
