# Award Daren

> **An intelligent hotel award search platform powered by a modern data engineering platform.**

---

# Vision

Award Daren helps travelers discover, analyze, and eventually book the best hotel award redemptions.

Rather than repeatedly searching hotel websites for award availability, Award Daren continuously collects, stores, and analyzes hotel award data to provide historical insights, availability trends, and intelligent recommendations.

The long-term vision is to build an AI-powered travel assistant that helps users find, monitor, and eventually book award stays.

Everything begins with a reliable and scalable data platform.

---

# Problem Statement

Finding hotel award availability is often frustrating.

Travelers repeatedly search hotel websites because:

- Award availability changes frequently.
- Hotel websites only show current availability.
- Historical award data is unavailable.
- Travelers don't know whether redeeming points provides good value.
- There is no simple way to monitor availability over time.

Award Daren solves these problems by collecting historical hotel award data and transforming it into useful insights.

---

# Project Goal

Build an intelligent hotel award search platform backed by a production-grade data engineering platform.

The platform should eventually allow users to:

- Search hotel award availability
- Explore historical pricing
- Compare redemption value
- Monitor availability changes
- Receive availability alerts
- Receive AI-powered recommendations
- Eventually receive AI-assisted booking support

---

# Why Hyatt?

Version 1 focuses exclusively on **Hyatt**.

Hyatt was chosen because:

- Award pricing is relatively transparent.
- Hyatt has a strong award travel community.
- The project scope is manageable.
- The architecture can later support additional hotel programs.

Hyatt is the first supported provider—not the only provider.

---

# Target Users

## Award Travelers

Travelers searching for the best Hyatt award redemption opportunities.

## Points Enthusiasts

Users interested in historical pricing, availability trends, and redemption value.

## Future AI Users

Travelers who want personalized recommendations and intelligent booking assistance.

---

# Product Roadmap

## Version 1 — Hyatt Data Platform

The first version focuses on building a reliable data engineering foundation.

### Objectives

- Collect Hyatt award availability
- Store historical observations
- Preserve raw source data
- Validate incoming data
- Build analytics-ready datasets
- Support SQL analytics
- Monitor pipeline health

### Users Can

- Search Hyatt hotels
- View award availability
- View cash prices
- View points prices
- Calculate cents per point (CPP)
- Explore historical pricing
- Explore historical availability

---

## Version 2 — Hyatt Search Platform

Build a complete Hyatt search experience.

Features include:

- Award availability calendar
- Historical availability timeline
- Historical pricing charts
- Search improvements
- Favorite hotels
- Availability alerts

---

## Version 3 — Hyatt AI Assistant

Introduce AI features powered by Award Daren's own data platform.

Examples include:

- Natural-language hotel search
- Award redemption recommendations
- Personalized hotel suggestions
- Trip planning assistance
- Availability monitoring
- AI-assisted booking guidance

The AI will use Award Daren's structured data rather than relying solely on live web searches.

---

## Version 4 — Expand Beyond Hyatt

Support additional hotel programs.

Potential providers:

- Marriott
- Hilton
- IHG

The platform architecture should require minimal changes when adding new providers.

---

# Engineering Goals

Award Daren is powered by a modern data engineering platform.

The engineering objectives are to:

- Build reliable ingestion pipelines
- Preserve raw source data
- Validate incoming data
- Store historical observations
- Transform data into analytics-ready models
- Support SQL analytics
- Build scalable data models
- Monitor pipeline health
- Support future AI capabilities

---

# Engineering Principles

## Reliability

Pipelines should fail gracefully and recover safely.

## Data Quality

Every dataset should be validated before entering the warehouse.

## Idempotency

Running the same pipeline multiple times should never create duplicate records.

## Traceability

Every record should be traceable back to its source.

## Reproducibility

Another developer should be able to run the project locally.

## Scalability

The platform should support additional hotel providers without major redesign.

---

# Success Criteria

Version 1 is successful when:

- Hyatt data is collected consistently.
- Historical observations are preserved.
- Users can search historical availability.
- Users can compare cash prices and award prices.
- SQL analytics provide meaningful insights.
- The architecture supports future expansion.
- The project can be deployed and reproduced by another developer.

---

# Technical Roadmap

## Sprint 0 — Foundation

- Project vision
- Architecture
- Data model
- Local development environment

---

## Sprint 1 — Hyatt Data Ingestion

- Hyatt data collection
- Raw data storage
- PostgreSQL
- Basic validation

---

## Sprint 2 — Data Warehouse

- Staging layer
- Warehouse layer
- SQL transformations
- Data modeling

---

## Sprint 3 — Production Pipeline

- Airflow
- Incremental loading
- Data quality
- Pipeline monitoring

---

## Sprint 4 — Analytics

- SQL analytics
- Dashboard
- Query optimization

---

## Sprint 5 — Hyatt AI Assistant

- Natural-language search
- Recommendation engine
- Tool-calling agent
- AI-assisted booking guidance

---

## Sprint 6 — Multi-Provider Platform

- Marriott
- Hilton
- IHG
- Shared provider architecture

---

# Current Status

**Current Sprint:** Sprint 0 — Foundation & System Design

**Project Status:** 🚧 In Progress
