## Database Initialization

The local PostgreSQL database runs through Docker Compose.

### 1. Start PostgreSQL

From the project root, run:

```bash
docker compose up -d db
```

Verify that the database container is running:

```bash
docker compose ps
```

### 2. Initialize the Schema

Run the schema initialization script:

```bash
docker compose exec -T db psql -U award_daren_user -d award_daren < sql/create_tables.sql
```

This creates the following tables:

* `hotels`
* `room_types`
* `pipeline_runs`
* `daily_availability`

The script uses `CREATE TABLE IF NOT EXISTS`, so it can be safely rerun without recreating existing tables.

### 3. Verify the Schema

Connect to PostgreSQL:

```bash
docker compose exec db psql -U award_daren_user -d award_daren
```

List all tables:

```sql
\dt
```

Inspect an individual table and its constraints:

```sql
\d hotels
\d room_types
\d pipeline_runs
\d daily_availability
```

Exit PostgreSQL:

```sql
\q
```
