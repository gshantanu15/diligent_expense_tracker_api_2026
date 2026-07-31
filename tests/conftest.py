from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from src.main import create_app


@pytest.fixture
def client(tmp_path) -> Iterator[TestClient]:
    app = create_app(tmp_path / "expenses.json")
    with TestClient(app) as test_client:
        yield test_client
