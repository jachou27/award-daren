# Local Development Environment

This guide explains how to configure and run the Award Daren project locally.

## Prerequisites

Install the following tools before starting:

* Docker Desktop
* Python 3
* Git

Verify the installations:

```bash
docker --version
docker compose version
python3 --version
git --version
```

## 1. Clone the Repository

```bash
git clone <repository-url>
cd award-daren
```

Replace `<repository-url>` with the project’s GitHub repository URL.

## 2. Configure Environment Variables

Create a local `.env` file from the provided example:

```bash
cp .env.example .env
```

Open `.env` and configure the local PostgreSQL settings:

```dotenv
POSTGRES_DB=award_daren
POSTGRES_USER=award_daren_user
POSTGRES_PASSWORD=replace_with_local_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

The `.env` file contains local credentials and must not be committed to Git.

## 3. Start PostgreSQL

Make sure Docker Desktop is running.

Start the PostgreSQL container:

```bash
docker compose up -d
```

The `-d` option runs the container in the background.

Check the container status:

```bash
docker compose ps
```

The database service should eventually show a status similar to:

```text
Up (healthy)
```

View the PostgreSQL logs:

```bash
docker compose logs db
```

Follow the logs in real time:

```bash
docker compose logs -f db
```

Press `Control + C` to stop following the logs. This does not stop the database.

## 4. Verify PostgreSQL

Run a query inside the PostgreSQL container:

```bash
docker compose exec db psql \
  -U award_daren_user \
  -d award_daren \
  -c "SELECT current_database(), current_user;"
```

Expected output:

```text
 current_database |    current_user
------------------+----------------------
 award_daren      | award_daren_user
```

## 5. Create a Python Virtual Environment

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

After activation, the terminal prompt should begin with:

```text
(.venv)
```

Verify that the virtual environment’s Python interpreter is active:

```bash
which python
```

The path should point to:

```text
award-daren/.venv/bin/python
```

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

## 6. Install Python Dependencies

Install the dependencies listed in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

If `requirements.txt` has not been created yet, install the required packages:

```bash
python -m pip install "psycopg[binary]" python-dotenv
```

Then save the installed dependencies:

```bash
python -m pip freeze > requirements.txt
```

## 7. Verify the Python Database Connection

Make sure PostgreSQL is running:

```bash
docker compose ps
```

Run the connection test:

```bash
python ingestion/check_db_connection.py
```

Expected output:

```text
Database connection successful.
Database: award_daren
User: award_daren_user
PostgreSQL: PostgreSQL 16...
```

## Common Docker Commands

### Start PostgreSQL

```bash
docker compose up -d
```

### Check Container Status

```bash
docker compose ps
```

### View Database Logs

```bash
docker compose logs db
```

### Stop PostgreSQL

```bash
docker compose stop
```

This stops the container without removing it.

### Stop and Remove the Container

```bash
docker compose down
```

This removes the container and Docker network but preserves the PostgreSQL data volume.

### Restart PostgreSQL

```bash
docker compose restart db
```

### Reset the Local Database

Warning: this command deletes all data stored in the local PostgreSQL volume.

```bash
docker compose down -v
docker compose up -d
```

Only use this when a completely fresh local database is needed.

## Database Configuration

The local database is configured through the following environment variables:

| Variable            | Description                                |
| ------------------- | ------------------------------------------ |
| `POSTGRES_DB`       | Name of the PostgreSQL database            |
| `POSTGRES_USER`     | PostgreSQL username                        |
| `POSTGRES_PASSWORD` | PostgreSQL user password                   |
| `POSTGRES_HOST`     | Database host used by Python               |
| `POSTGRES_PORT`     | Database port exposed on the local machine |

Because Python currently runs directly on the local computer, the host should be:

```dotenv
POSTGRES_HOST=localhost
```

If Python is later moved into a Docker Compose service, it will connect through the Compose service name:

```dotenv
POSTGRES_HOST=db
```

## Port Conflict

PostgreSQL uses port `5432` by default.

Check whether another application is already using it:

```bash
lsof -i :5432
```

If port `5432` is unavailable, update `.env`:

```dotenv
POSTGRES_PORT=5433
```

The Docker Compose configuration will then map:

```text
Local port 5433 → PostgreSQL container port 5432
```

The Python connection script will also use port `5433` because it reads the same `.env` file.

## Environment File Security

The actual `.env` file must be excluded from Git:

```gitignore
.env
.env.*
!.env.example
```

The `.env.example` file should be committed because it documents the required variables without including real credentials.

Never reuse personal passwords in the local development configuration.

## Initial Setup Summary

A developer setting up the project for the first time should run:

```bash
cp .env.example .env

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

docker compose up -d
docker compose ps

python ingestion/check_db_connection.py
```

The local environment is ready when:

* Docker Compose starts PostgreSQL successfully.
* The PostgreSQL container reports a healthy status.
* The command-line PostgreSQL query succeeds.
* Python connects to PostgreSQL successfully.
* The setup steps are documented and reproducible.
