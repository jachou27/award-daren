# Award Daren

> **An intelligent hotel award search platform powered by a modern data engineering platform.**

---

# Problem Statement

Finding hotel award availability is often time-consuming and frustrating.

Travelers frequently revisit hotel websites because award availability changes constantly, historical pricing is unavailable, and it is difficult to determine whether redeeming points provides good value.

Award Daren aims to solve this problem by collecting, storing, and analyzing historical hotel award data, enabling travelers to make smarter redemption decisions.

---

# Project Goal

Build an intelligent hotel award search platform backed by a production-grade data engineering platform.

The initial goal is to provide reliable Hyatt award availability and pricing data through a scalable data pipeline. Over time, Award Daren will evolve into an AI-powered travel assistant that helps users discover, monitor, and eventually book award stays.

---

# Target Users

### Award Travelers

Travelers searching for the best Hyatt award redemption opportunities.

### Points Enthusiasts

Users interested in historical pricing, award availability trends, and redemption value.

### Future AI Users

Travelers who want personalized recommendations and intelligent booking assistance.

---

# MVP Scope (Version 1)

Version 1 focuses exclusively on **Hyatt**.

### Users can:

- Search Hyatt hotels
- View award availability
- Compare cash prices and points prices
- Calculate cents per point (CPP)
- Explore historical pricing trends
- Explore historical award availability

### Engineering Objectives

- Build a reliable Hyatt data ingestion pipeline
- Preserve historical observations
- Store data in PostgreSQL
- Validate incoming data
- Support SQL analytics
- Build a scalable architecture for future expansion

---

# Future Roadmap

## Version 2 — Hyatt Search Experience

- Award availability calendar
- Favorite hotels
- Availability alerts
- Improved search experience

## Version 3 — Hyatt AI Assistant

- Natural-language search
- Personalized recommendations
- Trip planning assistance
- AI-assisted booking guidance

## Version 4 — Multi-Provider Platform

Expand Award Daren to support additional hotel programs, including:

- Marriott
- Hilton
- IHG

The platform architecture will be designed so new providers can be added with minimal changes.

---

> **Guiding Principle**

Award Daren starts with Hyatt, but it is designed to become a scalable platform for intelligent hotel award travel.
