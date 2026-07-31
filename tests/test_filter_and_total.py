import pytest


def create_expense(
    client,
    title: str,
    amount: float,
    category: str,
) -> None:
    response = client.post(
        "/expenses",
        json={
            "title": title,
            "amount": amount,
            "category": category,
            "date": "2026-07-31",
        },
    )
    assert response.status_code == 201


def add_sample_expenses(client) -> None:
    create_expense(client, "Lunch", 12.5, "food")
    create_expense(client, "Bus ticket", 7.25, "transport")
    create_expense(client, "Dinner", 20.0, "food")


def test_list_expenses_without_filter_returns_all_expenses(client) -> None:
    add_sample_expenses(client)

    response = client.get("/expenses")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_list_expenses_filters_by_category(client) -> None:
    add_sample_expenses(client)

    response = client.get("/expenses?category=food")

    assert response.status_code == 200
    assert [expense["title"] for expense in response.json()] == [
        "Lunch",
        "Dinner",
    ]


def test_total_returns_overall_expense_total(client) -> None:
    add_sample_expenses(client)

    response = client.get("/expenses/total")

    assert response.status_code == 200
    assert response.json() == {"total": 39.75}


def test_total_filters_by_category(client) -> None:
    add_sample_expenses(client)

    response = client.get("/expenses/total?category=food")

    assert response.status_code == 200
    assert response.json() == {"total": 32.5}


def test_total_is_zero_when_there_are_no_expenses(client) -> None:
    response = client.get("/expenses/total")

    assert response.status_code == 200
    assert response.json() == {"total": 0.0}


@pytest.mark.parametrize(
    "endpoint",
    [
        "/expenses?category=holiday",
        "/expenses/total?category=holiday",
    ],
)
def test_category_filter_rejects_unknown_category(
    client,
    endpoint,
) -> None:
    response = client.get(endpoint)

    assert response.status_code == 422
