# Smart Expense Tracker API

A small REST API for recording and summarizing personal expenses. It uses
FastAPI, stores data in a local JSON file, and includes an automated pytest
suite.

## Features

- Add an expense with a title, amount, category, and date.
- View all expenses.
- Filter expenses by category.
- Calculate overall or category-specific totals.
- Delete an expense.
- Run locally with Python or in Docker.

## Install, Run, and Test

Choose either local Python or Docker. Click an option to expand or collapse
its instructions.

### Before you start

Download the project and open a terminal in the project root—the folder that
contains `README.md`, `requirements.txt`, `Dockerfile`, `src`, and `tests`.
Do not run the setup commands from inside `src` or `tests`.

To download it with Git:

```bash
git clone https://github.com/gshantanu15/diligent_expense_tracker_api_2026.git
cd diligent_expense_tracker_api_2026
```

If you downloaded a ZIP instead, extract it, open the extracted folder in a
terminal, and confirm that `requirements.txt` is visible before continuing.

**Every command below should be run from this project root unless stated
otherwise.**

<details open>
<summary><strong>Option 1 — Local Python 3.12</strong></summary>

### Requirements

- Python 3.12
- `pip`, included with Python

Check the installed version:

```bash
python --version
```

The output must begin with `Python 3.12`. If `python` is not recognized, install
Python, select the installer's option to add it to `PATH`, and open a new
terminal before trying again.

If needed, download the official
[Python 3.12.10 installer](https://www.python.org/downloads/release/python-31210/).
It is the final Python 3.12 release that provides the standard Windows and
macOS installers.

<details>
<summary><strong>Optional virtual environment</strong></summary>

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

</details>

### Exact review commands

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the server:

```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Wait until the terminal displays `Uvicorn running on http://0.0.0.0:8000`.
Leave this terminal open while using the API. Open a second terminal for the
example requests below. Stop the server at any time by pressing `Ctrl+C`.

Run the tests:

```bash
python -m pytest
```

The API is available at `http://127.0.0.1:8000`. Tests start the application
internally, so the server does not need to be running during the test suite.
Either stop the server first or run the tests from a second terminal opened in
the project root.

</details>

<details>
<summary><strong>Option 2 — Docker</strong></summary>

### Requirements

- Docker Desktop or Docker Engine

No local Python installation is required. On Windows or macOS, open Docker
Desktop and wait until it reports that the engine is running. On Linux, start
Docker Engine using the instructions for your distribution.

If Docker is not installed, use
[Docker Desktop](https://www.docker.com/products/docker-desktop/) on Windows
or macOS, or follow the official
[Docker Engine installation guide](https://docs.docker.com/engine/install/)
on Linux.

Verify Docker before continuing:

```bash
docker version
```

The output must contain both `Client` and `Server` sections. If it reports that
it cannot connect to the Docker daemon or engine, start Docker and run the
command again.

Build the image:

```bash
docker build -t diligent-expense-tracker .
```

Run this from the project root so Docker can find `Dockerfile` and
`requirements.txt`. The first build can take several minutes while Python and
the dependencies download. Wait for the build to finish successfully before
running the next command.

Run the container:

```bash
docker run --rm -p 8000:8000 diligent-expense-tracker
```

The API is available at `http://127.0.0.1:8000`. The image name implicitly
uses Docker's default `latest` tag. Wait for the Uvicorn startup message, keep
this terminal open, and use a second terminal for API requests. Press `Ctrl+C`
to stop the server. Because `--rm` is present, Docker removes the stopped
container automatically; it does not remove the built image.

### Run the tests with Docker

```bash
docker build --target test -t diligent-expense-tracker-test .
docker run --rm diligent-expense-tracker-test
```

The first command builds the dedicated test image. The second starts it, runs
the complete pytest suite, prints the results, and removes the stopped test
container. These commands are the same on Windows, macOS, and Linux and do not
require Python to be installed locally.

The normal `diligent-expense-tracker` image contains only the API. The
`diligent-expense-tracker-test` image additionally contains `pytest.ini` and
the `tests` directory.

</details>

## API

Valid categories are `food`, `transport`, `bills`, `shopping`, and `other`.
Dates use the ISO `YYYY-MM-DD` format, and amounts must be greater than zero.

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| `POST` | `/expenses` | Create an expense | `201` |
| `GET` | `/expenses` | List every expense | `200` |
| `GET` | `/expenses?category=food` | Filter by category | `200` |
| `GET` | `/expenses/total` | Calculate the overall total | `200` |
| `GET` | `/expenses/total?category=food` | Calculate a category total | `200` |
| `DELETE` | `/expenses/{id}` | Delete an expense | `204` |

Invalid request data returns `422`. Deleting an unknown ID returns `404`.

### Example

First start the API using either option above. Keep that terminal running and
enter these commands in a second terminal.

Create an expense:

```bash
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title":"Lunch","amount":12.5,"category":"food","date":"2026-07-31"}'
```

Example response:

```json
{
  "id": 1,
  "title": "Lunch",
  "amount": 12.5,
  "category": "food",
  "date": "2026-07-31"
}
```

List and summarize expenses:

```bash
curl http://127.0.0.1:8000/expenses
curl "http://127.0.0.1:8000/expenses?category=food"
curl http://127.0.0.1:8000/expenses/total
curl "http://127.0.0.1:8000/expenses/total?category=food"
```

Delete expense `1`:

```bash
curl -X DELETE http://127.0.0.1:8000/expenses/1
```

On Windows PowerShell, use `curl.exe` instead of `curl` if `curl` is mapped to
`Invoke-WebRequest`.

## Tests

The project includes 20 pytest cases covering the API and JSON storage layer.
FastAPI's `TestClient` exercises endpoints without requiring a separately
running server.

Major coverage includes:

- Creating expenses with sequential IDs and confirming they persist to JSON.
- Rejecting blank titles, non-positive amounts, unknown categories, and
  invalid dates with `422` responses.
- Listing all expenses and filtering them by category.
- Calculating overall, category-specific, and empty-state totals.
- Deleting expenses, persisting deletions, and returning `404` for missing or
  repeatedly deleted IDs.
- Creating an empty data file when one does not exist.
- Isolating every test in a temporary directory so the real application data
  is never modified.

The suite can be run locally with `python -m pytest` or through the dedicated
Docker test target described above.

## Project Structure

```text
.
|-- README.md
|-- AI_NOTES.md
|-- Dockerfile
|-- requirements.txt
|-- pytest.ini
|-- src/
|   |-- data/expenses.json
|   |-- main.py
|   |-- models.py
|   `-- storage.py
`-- tests/
    |-- conftest.py
    |-- test_create_expense.py
    |-- test_delete_expense.py
    |-- test_expenses.py
    |-- test_filter_and_total.py
    `-- test_storage.py
```
