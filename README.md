# Award Daren

> A data engineering platform for collecting, transforming, and analyzing hotel award availability.

Award Daren is an end-to-end data engineering project that builds a historical dataset of hotel award availability and pricing.

Version 1 focuses on Hyatt and uses Python, PostgreSQL, SQL, Docker, and automated testing to build a modular ingestion, transformation, storage, and analytics pipeline that can eventually power hotel award search, historical analysis, and AI-assisted travel planning.

---

## Project Goals

Hotel award availability is often difficult to search, compare, and analyze over time.

Award Daren aims to build a structured data platform that can:

* Collect hotel award availability
* Preserve raw source data
* Transform source responses into a consistent data model
* Store historical availability observations
* Compare points and cash pricing
* Track individual pipeline executions
* Analyze award availability trends
* Power future search and AI-assisted travel planning experiences

---

## Features

### Data Platform

* Hyatt award availability ingestion
* Raw JSON source data preservation
* Source-to-database field mapping
* Hyatt award and cash price transformation
* PostgreSQL relational data model
* Historical availability storage
* Pipeline execution tracking
* End-to-end local pipeline command
* Automated pipeline testing
* Sanitized fixture-based testing
* SQL-based data validation and analytics

### Planned Product Features

* Monthly award availability calendar
* Hotel award search
* Points vs. cash price comparison
* Historical pricing trends
* Historical award availability trends
* AI-powered travel assistant

---

## Tech Stack

### Current

* Python
* PostgreSQL
* SQL
* Docker
* pytest
* Git
* GitHub

### Planned

* dbt
* Apache Airflow
* FastAPI
* React
* Cloud data platform integration
* CI/CD
* Monitoring and observability tooling

---

## Data Pipeline

The initial pipeline follows a standard ETL workflow:

```text
Hyatt Source Data
       |
       v
 Raw JSON Files
       |
       v
Python Transformation
       |
       v
 PostgreSQL Load
       |
       v
Pipeline Run Tracking
       |
       v
 SQL Validation
       |
       v
Future Analytics Layer
```

The current pipeline uses captured and sanitized Hyatt source responses so development and testing remain deterministic and do not depend on the live Hyatt website.

The architecture is designed so that automated extraction, orchestration, analytics tooling, and cloud infrastructure can be introduced incrementally as the project grows.

---

## Pipeline Components

The ingestion layer is separated into modular components.

### Configuration

`ingestion/config.py`

Loads and validates required PostgreSQL environment variables.

### Database Connection

`ingestion/database.py`

Provides reusable PostgreSQL database connectivity for pipeline modules.

### Raw Storage

`ingestion/raw_storage.py`

Preserves source responses as raw JSON files before transformation.

### Transformation

`ingestion/transform.py`

Transforms nested Hyatt source responses into normalized hotel, room type, and availability records.

### Loading

`ingestion/load.py`

Loads transformed records into PostgreSQL and connects availability records with their normalized database entities.

### Pipeline Run Tracking

`ingestion/pipeline_runs.py`

Tracks pipeline execution status, timestamps, extracted and loaded record counts, and failures.

### End-to-End Pipeline

`ingestion/run_pipeline.py`

Coordinates the complete local pipeline:

```text
Read Source Files
       |
       v
Start Pipeline Run
       |
       v
Preserve Raw Data
       |
       v
Transform Records
       |
       v
Load PostgreSQL
       |
       v
Complete Pipeline Run
```

If pipeline execution fails, the run is recorded as failed and the command exits with a nonzero status.

---

## Running the Pipeline

The current local pipeline operates on captured Hyatt JSON responses.

Example:

```bash
python -m ingestion.run_pipeline \
  --award-input tests/fixtures/hyatt_award_availability_sample.json \
  --cash-input tests/fixtures/hyatt_cash_availability_sample.json \
  --hotel-input tests/fixtures/hyatt_hotel_sample.json \
  --stay-date 2026-09-22
```

A successful pipeline run:

* Reads the source JSON files
* Starts a pipeline execution record
* Preserves raw source responses
* Transforms Hyatt data
* Loads normalized records into PostgreSQL
* Marks the pipeline run as completed
* Prints the pipeline run ID
* Prints extracted and loaded record counts
* Returns exit code `0`

Failures are recorded and return a nonzero exit code.

---

## Data Model

The initial PostgreSQL data model contains four primary tables.

### `hotels`

Stores hotel-level metadata.

Example fields:

* Hotel ID
* Hotel name
* Brand
* Category
* Address
* City
* Country

### `room_types`

Stores hotel room types and source identifiers.

Example fields:

* Room type ID
* Hotel ID
* Source room type ID
* Room name
* Award type

A source room type identifier is unique within a hotel and allows Hyatt source records to be mapped to normalized internal room types.

### `daily_availability`

Stores historical hotel award availability observations.

Example fields:

* Room type ID
* Stay date
* Award availability
* Points price
* Cash price
* Currency
* Observed timestamp
* Pipeline run ID

Each record represents an observed availability state for a room type and stay date.

### `pipeline_runs`

Tracks individual pipeline executions.

Example fields:

* Pipeline run ID
* Source
* Start time
* Completion time
* Status
* Records extracted
* Records loaded
* Error message

The pipeline run ID connects loaded availability observations with the pipeline execution that produced them.

---

## Project Structure

```text
award-daren/

├── ingestion/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── load.py
│   ├── pipeline_runs.py
│   ├── raw_storage.py
│   ├── run_pipeline.py
│   └── transform.py
│
├── tests/
│   ├── fixtures/
│   │   ├── hyatt_award_availability_sample.json
│   │   ├── hyatt_cash_availability_sample.json
│   │   └── hyatt_hotel_sample.json
│   ├── test_config.py
│   ├── test_raw_storage.py
│   └── test_transform.py
│
├── scripts/
│
├── sql/
│   ├── create_tables.sql
│   └── schema.sql
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
├── warehouse/
├── dbt/
├── airflow/
├── dashboard/
├── docker/
│
├── compose.yaml
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Source Data Strategy

The current pipeline uses captured and sanitized Hyatt source responses rather than making requests to the live Hyatt website during development or automated testing.

Three source types are currently used:

* Hotel metadata
* Award availability
* Cash availability

Using captured source data provides several benefits:

* Deterministic development
* Reproducible transformation behavior
* Safe automated testing
* Easier debugging
* Protection against live source changes
* No dependency on external availability during tests

Automated Hyatt extraction can be introduced separately in a future iteration without changing the core transformation and loading architecture.

---

## Raw Data Strategy

Award Daren preserves original Hyatt source responses before transformation.

Raw responses are stored using filenames that identify the hotel, source type, pipeline execution, and observation timestamp:

```text
data/raw/

└── hyatt_<hotel_id>_<source_type>_run<pipeline_run_id>_<timestamp>.json
```

Example:

```text
hyatt_HNLRW_award_run1_20260813T183000000000Z.json
```

Separate raw files can be stored for:

```text
award
cash
hotel
```

Preserving raw source data makes it possible to:

* Reprocess historical responses
* Debug transformation issues
* Validate upstream source changes
* Trace source data to a pipeline execution
* Improve transformation logic without recollecting data

A future production implementation can extend this design by storing raw artifact paths directly with pipeline run metadata for stronger lineage and replayability.

---

## Transformation Layer

Hyatt availability responses contain nested room and rate-plan structures.

The transformation layer converts these source responses into normalized records that match the PostgreSQL data model.

### Hotel Transformation

Hotel metadata is normalized into fields such as:

```text
hotel_id
name
brand
category
address
city
country
```

Required fields are validated while optional fields can safely produce `None`.

### Room Type Transformation

Example source fields:

```text
roomTypeCode
roomType.title
roomCategory
```

are transformed into:

```text
hotel_id
source_room_type_id
name
award_type
```

Required room type fields are validated before normalized records are produced.

### Availability Transformation

Award and cash rate plans are combined to produce normalized availability observations.

Normalized fields include:

```text
source_room_type_id
stay_date
award_available
points_price
cash_price
currency
observed_at
```

Transformation includes:

* Date conversion
* Points price conversion to integer values
* Cash price conversion to `Decimal`
* Currency normalization
* Award availability detection
* Source room type mapping
* Required-field validation

Transformation logic remains independent from PostgreSQL so it can be tested independently.

---

## Loading Strategy

Transformed records are loaded into PostgreSQL through the loading layer.

The loader handles:

* Hotel records
* Room type records
* Availability records
* Pipeline run associations

Hotel and room type records can be matched using stable source identifiers, while daily availability records retain the `pipeline_run_id` responsible for creating them.

This provides a foundation for historical analysis and future pipeline lineage.

---

## Pipeline Run Tracking

Every end-to-end execution creates a pipeline run record.

A pipeline run can move through states such as:

```text
started
   |
   v
completed
```

or:

```text
started
   |
   v
failed
```

Successful runs record:

* Start time
* Completion time
* Records extracted
* Records loaded

Failed runs preserve an error message so pipeline failures can be inspected and debugged.

This provides the first observability layer for Award Daren.

---

## Testing

Award Daren uses `pytest` for automated pipeline testing.

The current test suite covers:

* Database configuration validation
* Missing required environment variables
* Raw JSON response storage
* Raw filename generation
* Raw file overwrite protection
* Hyatt hotel transformation
* Hyatt room type transformation
* Hyatt availability transformation
* Missing optional fields
* Invalid required fields
* End-to-end transformation using sanitized Hyatt fixtures

Tests use sanitized local fixtures and do not call the live Hyatt website.

Run the complete test suite from the project root:

```bash
pytest
```

Current automated tests validate configuration, raw storage, individual transformation functions, and realistic sanitized Hyatt fixture behavior.

---

## Development Environment

The project uses Docker to provide a reproducible PostgreSQL development environment.

The Python application connects to PostgreSQL using configuration stored in environment variables rather than hard-coded credentials.

Required PostgreSQL configuration includes:

```text
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```

The general local workflow is:

```text
Docker
   |
   v
PostgreSQL 16
   |
   v
Python Pipeline
   |
   v
Raw Storage
   |
   v
Transformation
   |
   v
PostgreSQL Load
```

Environment configuration is validated before database operations are performed.

---

## Sprint 1 Pipeline

Sprint 1 focuses on building the first complete local data engineering workflow.

```text
1. Capture Hyatt Source Responses
                  |
                  v
2. Store Raw JSON Responses
                  |
                  v
3. Transform Source Data
                  |
                  v
4. Load Data into PostgreSQL
                  |
                  v
5. Record Pipeline Execution
                  |
                  v
6. Run Automated Tests
                  |
                  v
7. Validate Data with SQL
```

The Sprint 1 end-to-end pipeline is complete and operational locally using sanitized Hyatt source data. The workflow now includes raw data preservation, transformation, PostgreSQL loading, pipeline run tracking, automated testing, SQL verification, and developer documentation.

---

## Project Status

### Current Status

**Sprint 1 — First End-to-End Data Pipeline: Complete**

Sprint 1 established the first working Hyatt data pipeline from captured source responses through normalized PostgreSQL storage, including pipeline run tracking, automated testing, SQL verification, and developer documentation.

### Completed

* ✅ Project vision and MVP scope
* ✅ Hyatt data source research
* ✅ High-level system architecture
* ✅ PostgreSQL data model
* ✅ Engineering standards
* ✅ Local Docker/PostgreSQL development environment
* ✅ PostgreSQL schema initialization
* ✅ Reusable Python database connection module
* ✅ Hyatt award availability sample capture
* ✅ Hyatt cash availability sample capture
* ✅ Hyatt hotel metadata fixture
* ✅ Source-to-database field mapping
* ✅ Raw Hyatt response storage
* ✅ Hyatt hotel transformation
* ✅ Hyatt room type transformation
* ✅ Hyatt award availability transformation
* ✅ Points price extraction
* ✅ Cash price transformation
* ✅ Load transformed records into PostgreSQL
* ✅ Pipeline execution tracking
* ✅ End-to-end local pipeline command
* ✅ Raw source preservation during pipeline execution
* ✅ Automated pipeline tests
* ✅ Sanitized Hyatt fixture testing
* ✅ Required-field validation
* ✅ Missing optional-field handling
* ✅ SQL verification and data validation
* ✅ Pipeline development documentation
* ✅ Sprint 1 pipeline workflow documentation

### Next

Sprint 2 will focus on expanding the pipeline beyond the initial local workflow and introducing additional production-oriented data engineering capabilities.

Potential next steps include:

* ⏳ Expand historical availability collection
* ⏳ Automate Hyatt availability extraction
* ⏳ Add additional data quality checks
* ⏳ Introduce dbt
* ⏳ Introduce workflow orchestration
* ⏳ Build analytics and search layers
* ⏳ Introduce monitoring and observability
* ⏳ Explore cloud deployment

---

## Roadmap

### Version 1 — Hyatt Data Foundation

Build the core Hyatt data platform.

* Hyatt source research
* Raw data ingestion
* Data transformation
* PostgreSQL storage
* Pipeline execution tracking
* Automated testing
* Historical availability collection
* SQL validation
* Data quality checks

### Version 2 — Hyatt Analytics & Search

Build the analytical and application-facing layers.

* Historical availability analysis
* Award pricing trends
* Monthly availability calendar
* Points vs. cash comparisons
* Hotel search APIs
* Analytics models
* Search-oriented datasets

### Version 3 — Hyatt AI Assistant

Add AI-assisted travel planning capabilities.

Potential capabilities include:

* Natural-language award searches
* Redemption recommendations
* Historical pricing insights
* Flexible-date suggestions
* Award availability summaries
* Historical availability reasoning

### Version 4 — Multi-Provider Platform

Expand beyond Hyatt.

Potential hotel programs include:

* Marriott Bonvoy
* Hilton Honors
* IHG One Rewards
* Other hotel loyalty programs

The data platform is intended to evolve toward a provider-independent architecture as additional sources are introduced.

---

## Future Data Engineering Improvements

As the pipeline becomes more mature, the project will gradually introduce additional industry tooling and production-style architecture.

Potential improvements include:

* dbt transformation models
* Apache Airflow orchestration
* Automated Hyatt extraction
* Automated data quality checks
* Incremental data pipelines
* Raw data lineage and replay
* Cloud object storage
* Cloud data warehouse integration
* CI/CD pipeline testing
* Monitoring and observability
* Pipeline alerting
* REST APIs
* Analytics dashboards
* Historical data backfills

These tools will be introduced when they solve a concrete scaling, reliability, orchestration, analytics, or operational problem rather than being added only for technology coverage.

---

## Documentation

Additional project documentation is available in the `docs/` directory.

* [Product Vision](docs/product-vision.md)
* [Data Source Research](docs/data-source.md)
* [Source-to-Database Field Mapping](docs/source-field-mapping.md)
* [Database Design](docs/database.md)
* [Local Development Setup](docs/local-development.md)
* [Pipeline Development Guide](docs/pipeline-development.md)
* [Contributing Guide](docs/contributing.md)

Documentation will continue to evolve alongside the pipeline architecture.

---

## Project Philosophy

Award Daren is being built incrementally using production-oriented data engineering practices.

The project prioritizes:

* Clear separation between raw and transformed data
* Reproducible development environments
* Relational data modeling
* Modular Python components
* Historical data preservation
* Deterministic transformation behavior
* Testable pipeline stages
* Explicit failure handling
* Pipeline execution tracking
* Data quality and observability
* Incremental adoption of industry-standard tools

The goal is not only to build a hotel award search product, but also to demonstrate how a real-world data platform can evolve from a local Python and PostgreSQL pipeline into a more scalable, observable, and production-oriented data engineering system.
