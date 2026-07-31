from src.storage import ExpenseStore


def create_expense(client, title: str = "Lunch") -> int:
    response = client.post(
        "/expenses",
        json={
            "title": title,
            "amount": 12.5,
            "category": "food",
            "date": "2026-07-31",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_delete_expense_returns_no_content(client) -> None:
    expense_id = create_expense(client)

    response = client.delete(f"/expenses/{expense_id}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_expense_is_persisted(client, data_file) -> None:
    first_id = create_expense(client, "Lunch")
    second_id = create_expense(client, "Dinner")

    response = client.delete(f"/expenses/{first_id}")
    stored_expenses = ExpenseStore(data_file).list_expenses()

    assert response.status_code == 204
    assert [expense.id for expense in stored_expenses] == [second_id]


def test_delete_unknown_expense_returns_not_found(client) -> None:
    response = client.delete("/expenses/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Expense not found"}


def test_delete_expense_twice_returns_not_found_on_second_attempt(
    client,
) -> None:
    expense_id = create_expense(client)

    first_response = client.delete(f"/expenses/{expense_id}")
    second_response = client.delete(f"/expenses/{expense_id}")

    assert first_response.status_code == 204
    assert second_response.status_code == 404
