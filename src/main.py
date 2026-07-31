from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response, status

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

    @app.delete(
        "/expenses/{expense_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def delete_expense(expense_id: int, request: Request) -> Response:
        deleted = request.app.state.expense_store.delete_expense(expense_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found",
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app


app = create_app()
