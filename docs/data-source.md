# Hyatt Data Source Research

## Objective

The goal of this document is to identify the data required by Award Daren and evaluate the best approach for collecting Hyatt award availability data.

---

# Product Requirements

Award Daren aims to provide a monthly award availability calendar similar to MaxMyPoint.

For each Hyatt hotel, users should be able to view:

- Award availability by stay date
- Points price
- Cash price
- Historical availability
- Historical pricing

---

# Required Data

## Hotel

| Field | Description |
|--------|-------------|
| Hotel ID | Unique hotel identifier |
| Name | Hotel name |
| Brand | Hyatt brand |
| Category | Hyatt category |
| Address | Hotel address |
| City | City |
| Country | Country |

---

## Award Availability

| Field | Description |
|--------|-------------|
| Hotel ID | Related hotel |
| Stay Date | Date of stay |
| Room Type | Standard Room, Suite, etc. |
| Award Available | Whether award booking is available |
| Points Price | Required points |
| Cash Price | Cash rate |
| Currency | Currency |
| Observed At | When the data was collected |
| Pipeline Run ID | Pipeline execution reference |

---

## Pipeline Run

| Field | Description |
|--------|-------------|
| Pipeline Run ID | Unique pipeline execution ID |
| Source | Data source |
| Started At | Pipeline start time |
| Completed At | Pipeline completion time |
| Status | Success or failure |
| Records Extracted | Number of records collected |
| Records Loaded | Number of records loaded |
| Error Message | Failure reason if applicable |

---

# Candidate Data Sources

To be researched.

Possible options include:

- Hyatt website
- Hyatt APIs
- Third-party APIs
- Web scraping

---

# Open Questions

- Does Hyatt provide a public API?
- Can we retrieve an entire month's availability efficiently?
- Which room types are returned?
- How frequently should data be collected?
- What are the rate limits?
- What data validation is required?