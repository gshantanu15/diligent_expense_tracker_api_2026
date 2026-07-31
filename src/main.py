from pathlib import Path

from fastapi import FastAPI, Request

from src.models import Expense
from src.storage import ExpenseStore

DEFAULT_DATA_FILE = Path(__file__).parent / "data" / "expenses.json"


def create_app(data_file: Path = DEFAULT_DATA_FILE) -> FastAPI:
    """Create the API with a configurable data file."""

    app = FastAPI(title="Smart Expense Tracker API")
    app.state.expense_store = ExpenseStore(data_file)

    @app.get("/expenses", response_model=list[Expense])
    def list_expenses(request: Request) -> list[Expense]:
        return request.app.state.expense_store.list_expenses()

    return app


app = create_app()
