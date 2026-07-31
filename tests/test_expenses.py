def test_list_expenses_is_empty_initially(client) -> None:
    response = client.get("/expenses")

    assert response.status_code == 200
    assert response.json() == []
