# Award Daren

> A data engineering platform for collecting, transforming, and analyzing hotel award availability.

Award Daren is an end-to-end data engineering project that builds a historical dataset of hotel award availability and pricing.

Version 1 focuses on Hyatt and uses Python, PostgreSQL, SQL, and Docker to build the ingestion, transformation, storage, and analytics pipeline that will eventually power hotel award search, historical analysis, and AI-assisted travel planning.

---

## Project Goals

Award availability is often difficult to search, compare, and analyze over time.

Award Daren aims to build a structured data platform that can:

* Collect hotel award availability
* Preserve raw source data
* Transform source responses into a consistent data model
* Store historical availability observations
* Compare points and cash pricing
* Analyze award availability trends
* Power future search and AI-assisted travel planning experiences

---

## Features

### Data Platform

* Hyatt award availability ingestion
* Raw JSON source data preservation
* Source-to-database field mapping
* Award availability transformation
* PostgreSQL relational data model
* Historical availability storage
* Pipeline execution tracking
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
* Git
* GitHub

### Planned

* dbt
* Apache Airflow
* FastAPI
* React
* Cloud data platform integration

---

## Data Pipeline

The initial pipeline follows a standard ETL workflow:

```text
Hyatt Availability Source
          |
          v
   Raw JSON Response
          |
          v
   Python Transformation
          |
          v
      PostgreSQL
          |
          v
    SQL Analytics
```

The pipeline is designed so that additional orchestration, transformation, and analytics tools can be introduced as the project grows.

---

## Data Model

The initial PostgreSQL data model contains four primary tables.

### `hotels`

Stores hotel-level metadata.

Examples:

* Hotel ID
* Hotel name
* Brand
* Category
* Address
* City
* Country

### `room_types`

Stores hotel room types and source identifiers.

Examples:

* Room type ID
* Hotel ID
* Source room type ID
* Room name
* Award type

### `daily_availability`

Stores historical hotel award availability observations.

Examples:

* Room type ID
* Stay date
* Award availability
* Points price
* Cash price
* Currency
* Observed timestamp
* Pipeline run ID

### `pipeline_runs`

Tracks individual pipeline executions.

Examples:

* Pipeline run ID
* Source
* Start time
* Completion time
* Status
* Records extracted
* Records loaded
* Error message

---

## Project Structure

```text
award-daren/
├── ingestion/
│   ├── config.py
│   └── database.py
│
├── warehouse/
│
├── sql/
│   └── create_tables.sql
│
├── dbt/
├── airflow/
├── tests/
│   └── fixtures/
│
├── dashboard/
├── docs/
├── docker/
│
├── data/
│   ├── raw/
│   └── processed/
│
└── README.md
```

---

## Project Status

### Current Sprint

**Sprint 1 — First End-to-End Data Pipeline**

The goal of Sprint 1 is to build the first working version of the Hyatt data pipeline from source response through PostgreSQL.

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
* ✅ Source-to-database field mapping
* ✅ Raw Hyatt response storage
* ✅ Hyatt award availability transformation
* ✅ Room type transformation
* ✅ Points price extraction
* ✅ Cash price mapping prototype

### In Progress

* 🚧 Load transformed records into PostgreSQL
* 🚧 Pipeline execution tracking
* 🚧 SQL verification and data validation

### Next

* ⏳ Complete the first end-to-end pipeline
* ⏳ Automate Hyatt availability extraction
* ⏳ Add automated tests and data quality checks
* ⏳ Expand historical data collection
* ⏳ Introduce dbt
* ⏳ Introduce workflow orchestration
* ⏳ Build analytics and search layers

---

## Sprint 1 Pipeline

Sprint 1 focuses on implementing the core data engineering workflow.

```text
1. Capture Hyatt Availability Response
                  |
                  v
2. Store Raw JSON Response
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
6. Validate Data with SQL
```

---

## Current Transformation Flow

Hyatt availability responses contain nested room and rate-plan structures.

The transformation layer converts the source response into normalized records used by the PostgreSQL data model.

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

### Availability Transformation

Award rate plans are identified from Hyatt rate-plan data and transformed into fields such as:

```text
stay_date
award_available
points_price
cash_price
currency
observed_at
```

The source room type identifier is used during transformation to map availability records to the corresponding internal PostgreSQL `room_type_id`.

---

## Raw Data Strategy

Award Daren preserves original Hyatt responses before transformation.

Raw responses are stored using timestamped filenames:

```text
data/raw/
└── hyatt_<hotel_id>_<timestamp>.json
```

Example:

```text
hyatt_HNLRW_20260813T181226690239Z.json
```

Preserving raw source data makes it possible to:

* Reprocess historical responses
* Debug transformation issues
* Validate source changes
* Improve transformation logic without recollecting data

---

## Development Environment

The project uses Docker to provide a reproducible PostgreSQL development environment.

The Python application connects to PostgreSQL using configuration stored in environment variables rather than hard-coded credentials.

Example workflow:

```text
Docker
   |
   v
PostgreSQL 16
   |
   v
Python ingestion modules
   |
   v
Transformation + Loading
```

---

## Roadmap

### Version 1 — Hyatt Data Foundation

Build the core Hyatt data pipeline.

* Hyatt source research
* Raw data ingestion
* Data transformation
* PostgreSQL storage
* Pipeline tracking
* Historical availability collection
* SQL validation

### Version 2 — Hyatt Analytics & Search

Build the analytical and search layer.

* Historical availability analysis
* Award pricing trends
* Monthly availability calendar
* Points vs. cash comparisons
* Hotel search APIs

### Version 3 — Hyatt AI Assistant

Add AI-assisted travel planning capabilities.

Potential capabilities include:

* Natural-language award searches
* Redemption recommendations
* Historical pricing insights
* Flexible-date suggestions
* Award availability summaries

### Version 4 — Multi-Provider Platform

Expand beyond Hyatt.

Potential hotel programs include:

* Marriott Bonvoy
* Hilton Honors
* IHG One Rewards
* Other hotel loyalty programs

---

## Future Data Engineering Improvements

As the pipeline becomes more mature, the project will gradually introduce additional industry tooling and production-style architecture.

Potential improvements include:

* dbt transformation models
* Apache Airflow orchestration
* Automated data quality checks
* Incremental data pipelines
* Cloud data warehouse integration
* CI/CD pipeline testing
* Monitoring and observability
* REST APIs
* Analytics dashboards

---

## Documentation

Additional project documentation is available in the `docs/` directory.

Topics include:

* Product Vision
* MVP Scope
* Hyatt Data Source Research
* High-Level Architecture
* PostgreSQL Data Model
* Source-to-Database Field Mapping
* Local Development Setup
* Engineering Standards

---

## Project Philosophy

Award Daren is being built incrementally using production-oriented data engineering practices.

The project prioritizes:

* Clear separation between raw and transformed data
* Reproducible development environments
* Relational data modeling
* Modular Python components
* Historical data preservation
* Testable pipeline stages
* Data quality and observability
* Incremental adoption of industry-standard tools

The goal is not only to build a hotel award search product, but also to demonstrate how a real-world data platform can evolve from a simple Python and PostgreSQL pipeline into a more scalable data engineering system.
