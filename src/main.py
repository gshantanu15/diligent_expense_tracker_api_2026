from pathlib import Path

from fastapi import FastAPI, Request

from src.models import Category, Expense, ExpenseCreate, TotalResponse
from src.storage import ExpenseStore

DEFAULT_DATA_FILE = Path(__file__).parent / "data" / "expenses.json"


def create_app(data_file: Path = DEFAULT_DATA_FILE) -> FastAPI:
    """Create the API with a configurable data file."""

    app = FastAPI(title="Smart Expense Tracker API")
    app.state.expense_store = ExpenseStore(data_file)

    @app.get("/expenses", response_model=list[Expense])
    def list_expenses(
        request: Request,
        category: Category | None = None,
    ) -> list[Expense]:
        return request.app.state.expense_store.list_expenses(category)

    @app.post("/expenses", response_model=Expense, status_code=201)
    def create_expense(
        expense_data: ExpenseCreate,
        request: Request,
    ) -> Expense:
        return request.app.state.expense_store.add_expense(expense_data)

    @app.get("/expenses/total", response_model=TotalResponse)
    def get_expense_total(
        request: Request,
        category: Category | None = None,
    ) -> TotalResponse:
        total = request.app.state.expense_store.calculate_total(category)
        return TotalResponse(total=total)

    return app


app = create_app()
