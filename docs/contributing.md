# Contributing Guide

This document defines the engineering standards for the Award Daren project. These conventions help keep the codebase consistent, maintainable, and easy for new contributors to understand.

## Git Workflow

Create a separate branch for each ticket or meaningful change.

Before creating a branch, update the local `main` branch:

```bash
git checkout main
git pull
```

Create the new branch from `main`:

```bash
git checkout -b <branch-name>
```

Do not commit directly to `main` unless the change is extremely small and does not affect project behavior.

## Branch Naming Convention

Use the following format:

```text
<type>/<ticket-id>-<short-description>
```

Use lowercase letters and hyphens in the description.

### Allowed branch types

| Type       | Purpose                                 |
| ---------- | --------------------------------------- |
| `feat`     | New functionality                       |
| `fix`      | Bug fix                                 |
| `docs`     | Documentation changes                   |
| `refactor` | Code changes that do not alter behavior |
| `test`     | Test additions or updates               |
| `chore`    | Configuration, tooling, or maintenance  |

### Examples

```text
feat/de-009-create-ingestion-script
fix/de-015-handle-missing-room-price
docs/de-008-engineering-standards
refactor/de-021-simplify-database-connection
test/de-025-add-ingestion-tests
chore/de-007-configure-local-environment
```

A branch should focus on one ticket or one clearly defined change.

## Commit Message Convention

Use the following format:

```text
<type>: <imperative summary>
```

The summary should:

* Begin with a lowercase verb.
* Describe what the commit does.
* Use the imperative form.
* Be concise.
* Avoid ending with a period.

### Allowed commit types

| Type       | Purpose                                        |
| ---------- | ---------------------------------------------- |
| `feat`     | Add new functionality                          |
| `fix`      | Correct a defect                               |
| `docs`     | Update documentation                           |
| `refactor` | Improve code without changing behavior         |
| `test`     | Add or update tests                            |
| `chore`    | Update tooling, dependencies, or configuration |

### Good examples

```text
feat: add Hyatt availability ingestion
fix: handle missing cash prices
docs: add local development instructions
refactor: simplify database connection logic
test: add database connection tests
chore: configure PostgreSQL with Docker
```

### Avoid

```text
updated files
changes
fixed stuff
work in progress
DE-008
```

Each commit should represent one logical change whenever practical.

## Folder and File Naming

Use lowercase names throughout the repository.

### Directories

Use lowercase `snake_case` for directories containing multiple words:

```text
pipeline_metadata/
raw_storage/
data_quality/
```

Existing single-word directories should remain unchanged:

```text
ingestion/
warehouse/
sql/
airflow/
tests/
dashboard/
docs/
docker/
data/
```

Avoid spaces, uppercase letters, and ambiguous abbreviations in directory names.

### Python files

Use lowercase `snake_case`:

```text
check_db_connection.py
load_hotel_data.py
extract_availability.py
```

### SQL files

Use lowercase `snake_case`:

```text
create_tables.sql
load_hotels.sql
daily_availability.sql
```

### Documentation files

Use lowercase `kebab-case`:

```text
local-development.md
data-source.md
product-vision.md
```

The required contribution guide remains:

```text
contributing.md
```

### Configuration files

Use the standard filename expected by the related tool:

```text
compose.yaml
requirements.txt
.env.example
.gitignore
```

## SQL Standards

SQL should prioritize readability and explicit behavior.

### Naming

Use lowercase `snake_case` for:

* Tables
* Columns
* Indexes
* Constraints
* Database objects

Examples:

```sql
daily_availability
pipeline_run_id
observed_at
fk_room_types_hotel
idx_availability_stay_date
```

Use plural nouns for table names:

```text
hotels
room_types
pipeline_runs
daily_availability
```

### Formatting

Use uppercase for SQL keywords:

```sql
SELECT
FROM
WHERE
JOIN
ON
INSERT
UPDATE
DELETE
CREATE TABLE
PRIMARY KEY
FOREIGN KEY
```

Use four spaces for indentation.

Place major clauses on separate lines.

Prefer one selected column per line for longer queries.

End SQL statements with a semicolon.

### Example

```sql
SELECT
    h.hotel_id,
    h.name,
    da.stay_date,
    da.award_available,
    da.points_price
FROM hotels AS h
JOIN room_types AS rt
    ON rt.hotel_id = h.hotel_id
JOIN daily_availability AS da
    ON da.room_type_id = rt.room_type_id
WHERE da.stay_date >= CURRENT_DATE
ORDER BY
    h.name,
    da.stay_date;
```

### Query Guidelines

Use explicit column names instead of:

```sql
SELECT *
```

Use explicit `JOIN` syntax instead of placing join conditions in the `WHERE` clause.

Use table aliases when a query includes multiple tables.

Qualify column names when the same column name could exist in multiple tables.

Use `TIMESTAMPTZ` for timestamps representing real moments in time.

Use ISO currency codes such as `USD`, `JPY`, and `EUR`.

Use constraints to protect important data rules when appropriate.

Provide meaningful names for foreign keys, unique constraints, checks, and indexes.

## Python Standards

Python code should follow PEP 8 and remain compatible with automated formatters such as Black and linters such as Ruff.

Automated enforcement may be added in a future ticket.

### Formatting

Use:

* Four spaces for indentation
* A target maximum line length of 88 characters
* Blank lines between top-level functions
* One import per line when practical
* Trailing commas in multiline structures

Do not use tabs for indentation.

### Naming

Use `snake_case` for:

* Variables
* Functions
* Modules

Use `PascalCase` for classes.

Use uppercase `snake_case` for constants.

Examples:

```python
database_name = "award_daren"


def check_database_connection() -> None:
    ...


class HyattAvailabilityClient:
    ...


DEFAULT_BATCH_SIZE = 100
```

### Imports

Group imports in this order:

1. Python standard library
2. Third-party packages
3. Local project imports

Separate each group with one blank line.

Example:

```python
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

from ingestion.config import DatabaseConfig
```

### Type Hints

Use type hints for:

* Function parameters
* Function return values
* Shared data structures
* Public interfaces

Example:

```python
def load_hotel(hotel_id: str) -> dict[str, str]:
    ...
```

### Functions

Functions should:

* Have one clear responsibility
* Use descriptive names
* Avoid unnecessary side effects
* Return values instead of relying only on printed output
* Remain reasonably small and testable

Use the main guard for executable scripts:

```python
if __name__ == "__main__":
    main()
```

### Documentation

Add docstrings to:

* Public functions
* Classes
* Functions with non-obvious behavior
* Data pipeline steps with important assumptions

Example:

```python
def check_database_connection() -> None:
    """Connect to PostgreSQL and run a verification query."""
```

Comments should explain why something is done, not simply repeat what the code says.

### File and Path Handling

Prefer `pathlib.Path` instead of manually combining path strings:

```python
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
```

### Configuration and Secrets

Load environment-specific values from environment variables.

Do not hard-code:

* Passwords
* API keys
* Database credentials
* Private URLs
* Access tokens

Real credentials belong in `.env`, which must not be committed.

Document required variables in `.env.example`.

### Error Handling

Catch specific exceptions instead of using a broad exception unnecessarily.

Preferred:

```python
except psycopg.Error as error:
    ...
```

Avoid:

```python
except Exception:
    ...
```

Error messages should provide enough context to identify what failed without exposing secrets.

## Documentation Standards

Project documentation should be written in Markdown and stored in `docs/` unless it belongs in the root `README.md`.

### Structure

Each document should:

* Begin with one level-one heading
* Use descriptive section headings
* Use sentence case for headings
* Organize information in a logical order
* Include copyable commands when setup steps are involved

Example:

```markdown
# Local Development Environment

## Prerequisites

## Initial Setup

## Start PostgreSQL
```

### Code and Commands

Use fenced code blocks and specify the language when possible:

````markdown
```bash
docker compose up -d
```

```python
print("Database connection successful.")
```

```sql
SELECT current_database();
```
````

Commands should be safe to copy and run from the documented location.

Clearly label destructive commands such as:

```bash
docker compose down -v
```

### Links

Use relative links for files within the repository:

```markdown
[Local development setup](local-development.md)
```

Avoid hard-coded local file paths such as:

```text
/Users/name/Desktop/award-daren/
```

### Documentation Maintenance

Documentation should be updated in the same branch when a change affects:

* Setup instructions
* Environment variables
* Database schemas
* Pipeline behavior
* Commands
* Folder structure
* User-facing functionality

Outdated documentation should be treated as a defect.

### Sensitive Information

Documentation must never contain:

* Real passwords
* API keys
* Private tokens
* Personal access credentials
* Sensitive production data

Use placeholders instead:

```dotenv
POSTGRES_PASSWORD=replace_with_local_password
```

## Definition of Done

Before considering a change complete:

* The code or documentation satisfies the ticket acceptance criteria.
* Relevant commands run successfully.
* New files follow the naming conventions.
* SQL and Python follow the formatting standards.
* Environment secrets are not committed.
* Documentation is updated when behavior or setup changes.
* `git status` has been reviewed before committing.
* The change has a clear commit message.
