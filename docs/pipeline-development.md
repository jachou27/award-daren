# Pipeline Development Guide

## Overview

This guide explains how to initialize and run the Award Daren Hyatt data pipeline in a local development environment.

The current pipeline uses captured and sanitized Hyatt source responses rather than making requests to the live Hyatt website.

The local workflow is:

```text
Hyatt Fixture Data
        |
        v
Start Pipeline Run
        |
        v
Preserve Raw JSON
        |
        v
Transform Records
        |
        v
Load PostgreSQL
        |
        v
Complete Pipeline Run
        |
        v
SQL Verification
```

The pipeline currently processes three source types:

* Hotel metadata
* Award availability
* Cash availability

---

## Prerequisites

Install the following tools before running the project locally:

* Git
* Python 3
* Docker Desktop
* Docker Compose

The local database runs PostgreSQL 16 through Docker.

Verify the required tools:

```bash
git --version
python3 --version
docker --version
docker compose version
```

Make sure Docker Desktop is running before starting the PostgreSQL container.

---

## 1. Open the Project

From a new terminal, navigate to the Award Daren repository:

```bash
cd award-daren
```

All commands in this guide should be run from the project root unless otherwise noted.

---

## 2. Configure Environment Variables

Award Daren reads PostgreSQL connection settings from environment variables.

Create a `.env` file in the project root.

The following variables are required:

```text
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```

Example structure:

```text
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=<database_name>
POSTGRES_USER=<database_user>
POSTGRES_PASSWORD=<database_password>
```

Use local development credentials that match the PostgreSQL configuration in `compose.yaml`.

Do not commit `.env` or real database credentials to Git.

Application configuration is loaded and validated by:

```text
ingestion/config.py
```

---

## 3. Create and Activate the Python Virtual Environment

Create a virtual environment from the project root:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

After activation, the terminal should display `(.venv)` before the command prompt.

To verify the active Python environment:

```bash
which python
python --version
```

When opening a new terminal later, reactivate the environment with:

```bash
source .venv/bin/activate
```

---

## 4. Install Dependencies

With the virtual environment activated, install the project dependencies:

```bash
pip install -r requirements.txt
```

The project dependencies include the PostgreSQL client library and `pytest` for automated testing.

Optionally verify the test environment:

```bash
pytest
```

The tests use sanitized local fixtures and do not call the live Hyatt website.

---

## 5. Start PostgreSQL with Docker

Start the PostgreSQL service:

```bash
docker compose up -d db
```

Verify that the container is running:

```bash
docker compose ps
```

The `db` service should appear as running or healthy.

To inspect PostgreSQL directly:

```bash
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

Exit PostgreSQL with:

```text
\q
```

---

## 6. Initialize the Database Schema

The PostgreSQL schema is stored under:

```text
sql/
```

The local database tables are initialized using:

```text
sql/create_tables.sql
```

Initialize the local database from the project root:

```bash
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < sql/create_tables.sql
```

The schema creates the primary pipeline tables:

```text
hotels
room_types
daily_availability
pipeline_runs
```

To verify that the tables exist, connect to PostgreSQL:

```bash
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

Then run:

```sql
\dt
```

You should see the four pipeline tables.

---

## 7. Run the End-to-End Pipeline

The end-to-end pipeline is implemented in:

```text
ingestion/run_pipeline.py
```

The current development pipeline uses three sanitized fixtures:

```text
tests/fixtures/hyatt_award_availability_sample.json
tests/fixtures/hyatt_cash_availability_sample.json
tests/fixtures/hyatt_hotel_sample.json
```

Run the pipeline from the project root:

```bash
python -m ingestion.run_pipeline \
  --award-input tests/fixtures/hyatt_award_availability_sample.json \
  --cash-input tests/fixtures/hyatt_cash_availability_sample.json \
  --hotel-input tests/fixtures/hyatt_hotel_sample.json \
  --stay-date 2026-09-22
```

The `--stay-date` argument represents the date associated with the availability observation.

A successful execution will:

1. Validate the input files.
2. Read the Hyatt JSON fixtures.
3. Start a pipeline run.
4. Preserve the raw source responses.
5. Transform hotel, room type, and availability records.
6. Load normalized records into PostgreSQL.
7. Associate availability records with the pipeline run.
8. Mark the pipeline run as completed.
9. Print the pipeline run ID.
10. Print extracted and loaded record counts.
11. Exit with status code `0`.

If an exception occurs, the pipeline records the execution as failed and returns a nonzero exit code.

---

## 8. Inspect Pipeline Run Records

Every end-to-end execution creates a row in:

```text
pipeline_runs
```

Connect to PostgreSQL:

```bash
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

View recent pipeline runs:

```sql
SELECT
    pipeline_run_id,
    source,
    started_at,
    completed_at,
    status,
    records_extracted,
    records_loaded,
    error_message
FROM pipeline_runs
ORDER BY pipeline_run_id DESC;
```

A successful pipeline run should have:

```text
status = completed
completed_at = populated
records_extracted >= 0
records_loaded >= 0
error_message = NULL
```

To inspect one specific pipeline run, use the ID printed by the pipeline:

```sql
SELECT *
FROM pipeline_runs
WHERE pipeline_run_id = <pipeline_run_id>;
```

For example:

```sql
SELECT *
FROM pipeline_runs
WHERE pipeline_run_id = 7;
```

Failed executions can be inspected with:

```sql
SELECT
    pipeline_run_id,
    started_at,
    completed_at,
    status,
    error_message
FROM pipeline_runs
WHERE status = 'failed'
ORDER BY pipeline_run_id DESC;
```

---

## 9. Verify Loaded Data

After a successful run, use SQL to confirm that normalized data was loaded.

### Hotels

```sql
SELECT *
FROM hotels;
```

The current Hyatt fixture should produce a hotel record for:

```text
HNLRW
```

To inspect that hotel directly:

```sql
SELECT *
FROM hotels
WHERE hotel_id = 'HNLRW';
```

### Room Types

```sql
SELECT
    room_type_id,
    hotel_id,
    source_room_type_id,
    name,
    award_type
FROM room_types
WHERE hotel_id = 'HNLRW'
ORDER BY room_type_id;
```

### Daily Availability

```sql
SELECT
    room_type_id,
    stay_date,
    award_available,
    points_price,
    cash_price,
    currency,
    observed_at,
    pipeline_run_id
FROM daily_availability
WHERE stay_date = '2026-09-22'
ORDER BY room_type_id;
```

### Verify Data from a Specific Pipeline Run

Use the pipeline run ID printed by the command:

```sql
SELECT *
FROM daily_availability
WHERE pipeline_run_id = <pipeline_run_id>;
```

This allows availability observations to be traced back to the pipeline execution that produced them.

### Join Availability with Room and Hotel Data

For a more complete verification:

```sql
SELECT
    h.hotel_id,
    h.name AS hotel_name,
    rt.source_room_type_id,
    rt.name AS room_name,
    da.stay_date,
    da.award_available,
    da.points_price,
    da.cash_price,
    da.currency,
    da.observed_at,
    da.pipeline_run_id
FROM daily_availability da
JOIN room_types rt
    ON da.room_type_id = rt.room_type_id
JOIN hotels h
    ON rt.hotel_id = h.hotel_id
ORDER BY
    da.stay_date,
    rt.room_type_id;
```

This verifies the normalized relationship between hotel, room type, availability, and pipeline-run data.

---

## 10. Raw Response Storage

Award Daren preserves source responses before transformation.

Raw files are stored in:

```text
data/raw/
```

The current filename format identifies:

* Hotel
* Source type
* Pipeline run
* Observation timestamp

Format:

```text
hyatt_<hotel_id>_<source_type>_run<pipeline_run_id>_<timestamp>.json
```

Example:

```text
hyatt_HNLRW_award_run7_20260826T230000000000Z.json
```

A pipeline execution can preserve separate files for:

```text
award
cash
hotel
```

Raw source preservation allows developers to:

* Debug transformation problems.
* Reprocess historical responses.
* Validate upstream changes.
* Compare transformed data against its original input.
* Improve transformation logic without recollecting data.

The current filename includes the pipeline run ID for traceability. A future production implementation may also store raw artifact paths directly in pipeline metadata for stronger lineage and replayability.

---

## 11. Common Errors and Fixes

### PostgreSQL Connection Refused

Example:

```text
connection refused
```

Cause:

The PostgreSQL Docker container is not running.

Fix:

```bash
docker compose up -d db
docker compose ps
```

Confirm that the `db` service is running before retrying the pipeline.

---

### `role "root" does not exist`

Cause:

`psql` was started inside the Docker container without specifying the configured PostgreSQL user.

Do not use:

```bash
docker compose exec db psql
```

Instead use:

```bash
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

---

### Missing Environment Variable

Example:

```text
Missing required environment variable
```

Cause:

The `.env` file is missing, incomplete, or contains an incorrect variable name.

Verify that `.env` contains:

```text
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```

Do not store credentials directly in Python files.

---

### Module or Dependency Not Found

Example:

```text
ModuleNotFoundError
```

Cause:

The virtual environment may not be active or dependencies may not be installed.

Fix:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Then rerun the command from the project root.

---

### Input File Does Not Exist

Cause:

One of the fixture paths passed to the pipeline is incorrect.

Verify that these files exist:

```bash
ls tests/fixtures/
```

Expected fixtures include:

```text
hyatt_award_availability_sample.json
hyatt_cash_availability_sample.json
hyatt_hotel_sample.json
```

Run the pipeline from the project root so relative file paths resolve correctly.

---

### PostgreSQL Relation Does Not Exist

Example:

```text
relation "pipeline_runs" does not exist
```

Cause:

The database schema has not been initialized.

Fix:

```bash
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < sql/create_tables.sql
```

Then verify:

```bash
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

Inside PostgreSQL:

```sql
\dt
```

---

### Pipeline Run Fails

The pipeline should record failed executions in `pipeline_runs`.

Inspect the latest failures:

```sql
SELECT
    pipeline_run_id,
    status,
    error_message
FROM pipeline_runs
WHERE status = 'failed'
ORDER BY pipeline_run_id DESC;
```

Use `error_message` to identify whether the failure occurred while reading, transforming, or loading data.

Failed loads should not leave partially committed availability records.

---

## 12. Stopping the Local Environment

To stop the running Docker services without deleting PostgreSQL data:

```bash
docker compose down
```

The database volume is preserved and can be started again with:

```bash
docker compose up -d db
```

---

## 13. Resetting the Local Database

> ⚠️ **DESTRUCTIVE COMMAND**
>
> The following command deletes Docker volumes associated with the project and removes the local PostgreSQL data stored in them.
>
> Do not run this command if the local database contains data that must be preserved.

```bash
docker compose down -v
```

After intentionally resetting the database, restart PostgreSQL:

```bash
docker compose up -d db
```

Then initialize the schema again:

```bash
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < sql/create_tables.sql
```

---

## Clean-Terminal Startup Checklist

When returning to the project from a new terminal, the normal development startup sequence is:

```bash
cd award-daren

source .venv/bin/activate

docker compose up -d db

docker compose ps

python -m ingestion.run_pipeline \
  --award-input tests/fixtures/hyatt_award_availability_sample.json \
  --cash-input tests/fixtures/hyatt_cash_availability_sample.json \
  --hotel-input tests/fixtures/hyatt_hotel_sample.json \
  --stay-date 2026-09-22
```

After the pipeline completes, connect to PostgreSQL:

```bash
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

Then verify the latest pipeline run:

```sql
SELECT
    pipeline_run_id,
    source,
    started_at,
    completed_at,
    status,
    records_extracted,
    records_loaded,
    error_message
FROM pipeline_runs
ORDER BY pipeline_run_id DESC
LIMIT 5;
```

The environment is ready when:

* PostgreSQL is running.
* The virtual environment is active.
* Required environment variables are configured.
* The database schema exists.
* The pipeline completes successfully.
* A completed `pipeline_runs` record exists.
* Normalized records exist in PostgreSQL.
* Raw source files exist under `data/raw/`.
