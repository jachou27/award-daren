# Local Development Environment

This guide explains how to configure and run the Award Daren project locally.

## Prerequisites

Install the following tools before starting:

* Docker Desktop
* Python 3
* Git
* AWS CLI

Verify the installations:

```bash
docker --version
docker compose version
python3 --version
git --version
aws --version
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

Configure the Amazon S3 settings:

```dotenv
AWS_REGION=us-west-1
S3_BUCKET_NAME=award-daren-data
```

The `.env` file contains local configuration and must not be committed to Git.

AWS credentials should not be stored in `.env`. Local AWS authentication is configured separately through the AWS CLI credential provider chain.

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
python -m pip install "psycopg[binary]" python-dotenv boto3
```

Then save the installed dependencies:

```bash
python -m pip freeze > requirements.txt
```

## 7. Configure Local AWS Authentication

The Award Daren pipeline uses Amazon S3 as durable object storage for raw Hyatt source artifacts.

Configure a local AWS CLI profile:

```bash
aws configure --profile award-daren
```

Enter the AWS Access Key ID and Secret Access Key for an IAM identity with the required Award Daren S3 permissions when prompted.

Do not store AWS credentials in the repository or `.env` file.

Set the AWS profile for the current terminal session:

```bash
export AWS_PROFILE=award-daren
```

Verify the active profile:

```bash
echo $AWS_PROFILE
```

Expected output:

```text
award-daren
```

Verify AWS authentication:

```bash
aws sts get-caller-identity --profile award-daren
```

The returned identity should correspond to the IAM identity configured for local Award Daren development.

## 8. Verify Amazon S3 Access

Verify that the configured AWS identity can access the Award Daren S3 bucket:

```bash
aws s3 ls s3://award-daren-data --profile award-daren
```

The bucket separates raw and synthetic Hyatt data:

```text
award-daren-data/
├── raw/
│   └── hyatt/
└── synthetic/
    └── hyatt/
```

Raw Hyatt artifacts produced by pipeline runs use the following object key structure:

```text
raw/hyatt/<hotel_id>/<pipeline_run_id>/<source_type>_<timestamp>.json
```

For example:

```text
raw/hyatt/HNLRW/10/award_20260930T011142539654Z.json
```

Each pipeline run stores the raw award, cash, and hotel source payloads in S3 before transformation.

The `pipeline_run_id` in the S3 object key makes it possible to associate raw source artifacts with the pipeline run that processed them.

AWS authentication uses the standard AWS credential provider chain. The application does not contain hard-coded AWS credentials.

## 9. Verify the Python Database Connection

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

## AWS Configuration

The S3 integration is configured through the following environment variables:

| Variable         | Description                                    |
| ---------------- | ---------------------------------------------- |
| `AWS_REGION`     | AWS region containing the S3 bucket            |
| `S3_BUCKET_NAME` | S3 bucket used by the Award Daren pipeline     |

The current local configuration is:

```dotenv
AWS_REGION=us-west-1
S3_BUCKET_NAME=award-daren-data
```

AWS credentials are intentionally separate from these application configuration values.

For local development, boto3 obtains credentials through the AWS credential provider chain. Setting:

```bash
export AWS_PROFILE=award-daren
```

allows boto3 to use the locally configured `award-daren` AWS CLI profile without hard-coding credentials in Python.

## Environment File Security

The actual `.env` file must be excluded from Git:

```gitignore
.env
.env.*
!.env.example
```

The `.env.example` file should be committed because it documents the required variables without including real credentials.

AWS Access Key IDs and Secret Access Keys must not be added to `.env`, `.env.example`, Python source files, documentation, or other committed project files.

Never reuse personal passwords in the local development configuration.

## Initial Setup Summary

A developer setting up the project for the first time should run:

```bash
cp .env.example .env

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

aws configure --profile award-daren
export AWS_PROFILE=award-daren
aws sts get-caller-identity --profile award-daren
aws s3 ls s3://award-daren-data --profile award-daren

docker compose up -d
docker compose ps

python ingestion/check_db_connection.py
```

The local environment is ready when:

* Docker Compose starts PostgreSQL successfully.
* The PostgreSQL container reports a healthy status.
* The command-line PostgreSQL query succeeds.
* Python connects to PostgreSQL successfully.
* AWS authentication succeeds.
* The configured AWS identity can access the Award Daren S3 bucket.
* AWS credentials are not stored in the repository.
* The setup steps are documented and reproducible.
