# AI Notes

## 1. What AI generated and what I wrote

I used OpenAI Codex throughout the project as a coding and review partner. The
work was deliberately split into small stages so I could inspect, validate and approve each addition before moving on.

Codex generated the initial versions of:

- The FastAPI application and endpoint implementations. (Scaffolding)
- The Pydantic request and response models.
- The JSON storage class.
- Basic pytest test cases and fixtures.
- The Dockerfile and Docker ignore rules.
- The first draft of `README.md`.

I made the product and implementation decisions, including:

- Python with FastAPI.
- Local JSON persistence instead of memory storage.
- Server-generated sequential integer IDs (instead of random UUIDs, which would add complexity)
- Five fixed expense categories.
- Docker as the single optional bonus.
- A staged workflow with tests, commits, and review checkpoints.

I also directly changed parts of the project:

- I added explanatory comments in code around validation and ID generation and adjusted the blank-title validation message.
- In commit `9e8de85` (`fix: isolate pytest temporary files`), I replaced the
  original pytest temporary-path setup with an isolated
  `TemporaryDirectory`, disabled pytest's cache provider, and documented why
  application data must remain untouched.

## 2. What I validated, tested, or changed

I reviewed the generated work after every stage rather than accepting the
entire project at once.

- Stage 1: verified JSON-file initialization and empty expense listing
  (`2` tests).
- Stage 2: added and checked creation, sequential IDs, persistence, and input
  validation (`9` total tests).
- Stage 3: checked category filtering and overall/category totals
  (`16` total tests).
- Stage 4: checked successful, persisted, missing, and repeated deletion
  (`20` total tests).
- Stage 5: built a dedicated Docker test image and ran all `20` tests on
  Linux with Python `3.12.13`. I also built the separate runtime image,
  confirmed that it does not contain the test suite, and smoke-tested the API
  on port `8000`.

Test Suite uses a new temporary JSON file for each test. Persistence tests create a
second `ExpenseStore` for the same temporary file to prove that changes were
written to disk rather than only held in memory.

The dependency versions are pinned in `requirements.txt`. Both the local
Windows environment and the Linux Docker image installed those dependencies
successfully. The Docker build excludes `src/data/expenses.json` so local
manual-test data cannot be copied into the image.

The final multi-stage Dockerfile keeps the normal API image small while
providing a separate `test` target. This makes the full pytest suite runnable
with the same Docker commands on Windows, macOS, and Linux without requiring a
local Python installation.

One important change to the original AI output was the Windows test-isolation
fix. The initial use of pytest's `tmp_path` was replaced after reviewing how
temporary directories behaved in this environment (due to conflicts with Codex sandbox).

## 3. AI suggestions I did not use

I intentionally rejected or avoided the following suggestions:

- In-memory storage, because the data should survive a local server restart.
- UUID expense IDs, because sequential integers are easier to read and test in
  this small assignment.
- Free-text categories, because fixed categories give clearer validation and
  predictable filtering.
- A database, authentication, pagination, search, and monthly summaries,
  because they were outside the assignment's required scope.
- Additional bonus features, because the instructions requested at most one;
  Docker is the only bonus claimed.
- A larger architecture or concurrency layer, because this is a small local
  JSON-backed REST API.

AI accelerated scaffolding and test generation, but the design choices,
incremental review, corrections, validation, and final submission decisions
remained mine.
