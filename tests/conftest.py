from collections.abc import Iterator
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from fastapi.testclient import TestClient

from src.main import create_app

# Set up a unique temporary directory for each test. Unlike pytest's built-in
# tmp_path fixture, this does not reuse a shared folder tied to a Windows user.
@pytest.fixture
def test_directory() -> Iterator[Path]:
    with TemporaryDirectory(prefix="diligent-expense-tests-") as directory:
        yield Path(directory)


# Set up the API without a real server and keep its data out of expenses.json.
@pytest.fixture
def data_file(test_directory: Path) -> Path:
    return test_directory / "expenses.json"


@pytest.fixture
def client(data_file: Path) -> Iterator[TestClient]:
    app = create_app(data_file)
    with TestClient(app) as test_client:
        yield test_client
