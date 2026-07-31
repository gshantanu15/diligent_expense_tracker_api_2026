import pytest

from src.storage import ExpenseStore


def valid_expense() -> dict:
    return {
        "title": "Lunch",
        "amount": 12.5,
        "category": "food",
        "date": "2026-07-31",
    }


def test_create_expense_returns_created_expense(client) -> None:
    response = client.post("/expenses", json=valid_expense())

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        **valid_expense(),
    }


def test_create_expense_assigns_sequential_ids(client) -> None:
    first_response = client.post("/expenses", json=valid_expense())
    second_response = client.post(
        "/expenses",
        json={
            **valid_expense(),
            "title": "Bus ticket",
            "category": "transport",
        },
    )

    assert first_response.json()["id"] == 1
    assert second_response.json()["id"] == 2


def test_create_expense_persists_to_json(client, data_file) -> None:
    client.post("/expenses", json=valid_expense())

    stored_expenses = ExpenseStore(data_file).list_expenses()

    assert len(stored_expenses) == 1
    assert stored_expenses[0].title == "Lunch"


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("title", "   "),
        ("amount", 0),
        ("category", "holiday"),
        ("date", "31-07-2026"),
    ],
)
def test_create_expense_rejects_invalid_input(
    client,
    field,
    invalid_value,
) -> None:
    request_body = valid_expense()
    request_body[field] = invalid_value

    response = client.post("/expenses", json=request_body)

    assert response.status_code == 422
