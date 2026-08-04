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

### Hyatt Website Fetch/XHR Feasibility Test

A manual Chrome DevTools Network inspection was performed to evaluate whether Hyatt website responses expose room type and points pricing data for a selected Japanese Hyatt property.

#### Test Scope

- Property: Park Hyatt Niseko Hanazono, Japan
- Property code / spirit code: `ctsph`
- Search type: Points / award availability
- Rooms: `1`
- Adults: `2`
- Kids: `0`
- Test dates: `2026-08-22` to `2026-08-23`

#### Observed Request

A likely room rates endpoint was identified during the points booking search.

- Method: `GET`
- Status: `200 OK`
- Endpoint path: `/en-US/shop/service/rooms/roomrates/ctsph`

Example request URL:

```text
https://www.hyatt.com/en-US/shop/service/rooms/roomrates/ctsph?spiritCode=ctsph&rooms=1&adults=2&checkinDate=2026-08-22&checkoutDate=2026-08-23&kids=0&accessibilityCheck=false&rate=Standard&suiteUpgrade=true
```

Important query parameters:

```text
spiritCode=ctsph
rooms=1
adults=2
checkinDate=2026-08-22
checkoutDate=2026-08-23
kids=0
accessibilityCheck=false
rate=Standard
suiteUpgrade=true
```

#### Observed Response Fields

The JSON response includes room type information and points pricing fields.

Relevant fields observed:

```text
roomTypeCode
roomCategory
roomQuantity
roomType.code
roomType.title
roomType.description
roomType.type
ratePlans[].ratePlanCategory
ratePlans[].points
ratePlans[].avgPoints
ratePlans[].totalPoints
currencyCode
```

Observed example:

```text
roomTypeCode: KGST
roomCategory: STANDARD
roomQuantity: 1
roomType.title: Suite, 1 King Bed
roomType.type: Suites
ratePlans[].ratePlanCategory: POINTS
ratePlans[].points: 45000
ratePlans[].avgPoints: 45000
ratePlans[].totalPoints: 45000
currencyCode: JPY
```

#### Feasibility Finding

The Hyatt website response appears to contain the core data needed for the prototype: room type, room category, availability-related room quantity, and points pricing.

This suggests Hyatt website Network responses may be feasible as an initial prototype data source for award availability research.

#### Limitations and Compliance Notes

This test was performed through manual Chrome DevTools inspection only.

No authentication bypass, CAPTCHA bypass, rate-limit circumvention, automated scraping, or access-control bypass was attempted. Sensitive headers, cookies, session identifiers, and authorization values were not recorded.

Production use would require further review, including Hyatt Terms of Service, legal/compliance considerations, rate-limit behavior, reliability testing, monitoring, and a compliant ingestion strategy.