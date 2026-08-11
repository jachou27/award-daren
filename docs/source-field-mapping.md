# Hyatt Source-to-Database Field Mapping

## Purpose

This document defines how fields from the Hyatt room availability response map to the Award Daren PostgreSQL schema.

The mapping is based on the sanitized Hyatt fixtures captured in DE-011:

* `tests/fixtures/hyatt_award_availability_sample.json`
* `tests/fixtures/hyatt_cash_availability_sample.json`

The current implementation focuses on Hyatt award availability and Hyatt Member Rate cash pricing.

---

## Source Structure

Both Hyatt fixtures use the following top-level structure:

```text
roomRates
```

`roomRates` is an object keyed by Hyatt room type code.

Example:

```text
roomRates.VW04
roomRates.VW4Q
roomRates.ADQT
```

Each room object contains room metadata, rate-plan information, points pricing, cash pricing, and currency information.

---

# Hotel Mapping

Hotel metadata is not included in the captured Hyatt room availability response.

## `hotel_id`

**Database table:** `hotels`
**Database column:** `hotel_id`

**Source:** Hyatt request parameter `spiritCode`

Example request value:

```text
spiritCode=hnlrw
```

Example stored value:

```text
HNLRW
```

**Conversion:**

* Convert to string.
* Normalize to uppercase.
* Store as `VARCHAR(50)`.

**Nullable:** No

---

## `name`

**Database table:** `hotels`
**Database column:** `name`

**Source:** Not available in the current room availability response.

**Default:** None

**Database type:** `TEXT NOT NULL`

**Nullable:** No

A separate Hyatt hotel metadata source is required before inserting a new hotel record.

---

## `brand`

**Database table:** `hotels`
**Database column:** `brand`

**Source:** Not available in the current room availability response.

**Default:** None

**Database type:** `TEXT NOT NULL`

**Nullable:** No

A separate Hyatt hotel metadata source is required before inserting a new hotel record.

---

## `category`

**Database table:** `hotels`
**Database column:** `category`

**Source:** Not available in the current room availability response.

**Default:** `NULL`

**Database type:** `SMALLINT`

**Nullable:** Yes

---

## `address`

**Database table:** `hotels`
**Database column:** `address`

**Source:** Not available in the current room availability response.

**Default:** `NULL`

**Database type:** `TEXT`

**Nullable:** Yes

---

## `city`

**Database table:** `hotels`
**Database column:** `city`

**Source:** Not available in the current room availability response.

**Default:** `NULL`

**Database type:** `TEXT`

**Nullable:** Yes

---

## `country`

**Database table:** `hotels`
**Database column:** `country`

**Source:** Not available in the current room availability response.

**Default:** `NULL`

**Database type:** `TEXT`

**Nullable:** Yes

---

# Room Type Mapping

## `source_room_type_id`

**Database table:** `room_types`
**Database column:** `source_room_type_id`

**Source JSON path:**

```text
roomRates.<room_code>.roomTypeCode
```

Example:

```text
roomRates.VW04.roomTypeCode = "VW04"
```

The `roomRates` object key also matches `roomTypeCode` in the observed fixtures.

**Conversion:**

* Store as string.
* Store as `VARCHAR(100)`.

**Nullable:** Yes in the current database schema.

The Hyatt availability response is expected to provide this value, so the ingestion pipeline should populate it whenever available.

---

## `name`

**Database table:** `room_types`
**Database column:** `name`

**Source JSON path:**

```text
roomRates.<room_code>.roomType.title
```

Example:

```text
"1 King Bed, Waikiki City View"
```

**Conversion:**

* Store as text.

**Database type:** `TEXT NOT NULL`

**Nullable:** No

---

## `award_type`

**Database table:** `room_types`
**Database column:** `award_type`

**Source JSON path:**

```text
roomRates.<room_code>.roomCategory
```

Observed values include:

```text
STANDARD
PREMIUM
```

**Conversion:**

* Store the Hyatt value as-is.
* Store as `VARCHAR(50)`.

**Nullable:** Yes

### Limitation

Hyatt's `roomCategory` should be treated as Hyatt's room classification rather than a strict award classification.

For example, `PREMIUM` may include:

* high-floor rooms
* ocean-view rooms
* junior suites
* full suites
* penthouse suites

This mapping may be revised if additional Hyatt room-category codes or more specific award-type fields are discovered.

---

# Availability Mapping

## `stay_date`

**Database table:** `daily_availability`
**Database column:** `stay_date`

**Source:** Hyatt request parameter `checkinDate`

Example:

```text
checkinDate=2026-09-22
```

**Conversion:**

```text
YYYY-MM-DD → PostgreSQL DATE
```

**Database type:** `DATE NOT NULL`

**Nullable:** No

### Ingestion Rule

The production ingestion pipeline should preferably query Hyatt using one-night intervals.

Example:

```text
checkinDate=2026-09-22
checkoutDate=2026-09-23
```

This ensures that points and cash prices correspond directly to a single `stay_date`.

---

## `award_available`

**Database table:** `daily_availability`
**Database column:** `award_available`

**Source:** Derived from Hyatt rate plans.

A pure points award is considered available when the room contains a qualifying rate plan where:

```text
ratePlanCategory = "POINTS"
```

Source path:

```text
roomRates.<room_code>.ratePlans[].ratePlanCategory
```

Derived value:

```text
Qualifying POINTS rate exists → TRUE
No qualifying POINTS rate → FALSE
```

`POINTS_CASH` does not by itself count as pure points award availability.

The `stexPointAvailable` field is not used for this determination because the captured fixture contains valid `POINTS` availability while `stexPointAvailable` is `false`.

**Conversion:**

* Derived Python boolean.
* Store as PostgreSQL `BOOLEAN`.

**Database type:** `BOOLEAN NOT NULL`

**Nullable:** No

---

## `points_price`

**Database table:** `daily_availability`
**Database column:** `points_price`

**Source JSON path:**

```text
roomRates.<room_code>.ratePlans[].points
```

The selected rate plan must satisfy:

```text
ratePlanCategory = "POINTS"
```

Example:

```text
ratePlanCategory = "POINTS"
points = 20000
```

Hyatt also exposes:

```text
lowestPointValue
lowestPointRatePlanCode
```

These summary fields may be used to identify or validate the selected points rate plan, but `points_price` should come from the actual qualifying `POINTS` rate plan rather than relying only on `lowestPointValue`.

For the observed fixture:

```text
lowestPointRatePlanCode = "LPRM"
```

matches:

```text
ratePlans[].id = "LPRM"
```

**Conversion:**

* Numeric value → integer.
* Store as PostgreSQL `INTEGER`.

**Nullable:** Yes when no qualifying points award is available.

---

## `cash_price`

**Database table:** `daily_availability`
**Database column:** `cash_price`

**Source JSON path:**

```text
roomRates.<room_code>.ratePlans[].totalAfterTax
```

The selected rate plan should be Hyatt's plain Member Rate.

Observed example:

```text
id = "MYHI"
name = "Member Rate"
ratePlanCategory = "CASH"
```

Example values:

```text
rate = 294
totalBeforeTax = 588
totalAfterTax = 828.61
```

For the MVP, Award Daren stores:

```text
cash_price = Member Rate totalAfterTax
```

This represents the total Member Rate cash cost including taxes and fees.

**Conversion:**

* Numeric/decimal value.
* Store as PostgreSQL `NUMERIC(10,2)`.

**Nullable:** Yes if no Member Rate is available.

### Future Consideration

Hyatt also exposes:

```text
rate
totalBeforeTax
rateIncludingFeesBeforeTaxes
```

The MVP uses `totalAfterTax` because the current product use case compares award prices against the total Member Rate cash cost including taxes and fees.

A future product setting may allow users to compare award pricing against cash prices excluding taxes and fees.

---

## `currency`

**Database table:** `daily_availability`
**Database column:** `currency`

**Source JSON path:**

```text
roomRates.<room_code>.ratePlans[].currencyCode
```

Use the same Member Rate plan selected for `cash_price`.

Example:

```text
USD
```

**Conversion:**

* Normalize to uppercase.
* Store as three-character currency code.

**Database type:** `CHAR(3)`

**Nullable:** Yes if no cash rate is available.

---

## `observed_at`

**Database table:** `daily_availability`
**Database column:** `observed_at`

**Source:** Generated by the Award Daren ingestion pipeline.

This value represents when Award Daren observed the Hyatt availability data rather than a timestamp supplied by Hyatt.

Example:

```text
2026-08-11T21:00:00Z
```

**Conversion:**

* Generate the current UTC timestamp during ingestion.
* Store as PostgreSQL `TIMESTAMPTZ`.

**Database type:** `TIMESTAMPTZ NOT NULL`

**Nullable:** No

---

# Pricing Selection Rules

## Points

For each room:

1. Inspect `ratePlans`.
2. Find a qualifying rate plan where:

```text
ratePlanCategory = "POINTS"
```

3. Extract:

```text
points
```

4. Use `lowestPointRatePlanCode` as supporting validation when applicable.
5. Do not treat `POINTS_CASH` as equivalent to a pure points award.

---

## Cash

For each room:

1. Inspect `ratePlans`.
2. Select the plain Hyatt Member Rate.
3. Confirm:

```text
ratePlanCategory = "CASH"
```

4. Extract:

```text
totalAfterTax
currencyCode
```

The MVP uses the Hyatt Member Rate because users evaluating World of Hyatt award redemptions are expected to be World of Hyatt members.

---

# Type Conversion Summary

| Database Column       | Source Type              | Database Type / Conversion |
| --------------------- | ------------------------ | -------------------------- |
| `hotel_id`            | String request parameter | `VARCHAR(50)`, uppercase   |
| `source_room_type_id` | String                   | `VARCHAR(100)`             |
| `name`                | String                   | `TEXT`                     |
| `award_type`          | String                   | `VARCHAR(50)`              |
| `stay_date`           | Request date string      | `DATE`                     |
| `award_available`     | Derived                  | `BOOLEAN`                  |
| `points_price`        | Number                   | `INTEGER`                  |
| `cash_price`          | Number / decimal         | `NUMERIC(10,2)`            |
| `currency`            | String                   | `CHAR(3)`, uppercase       |
| `observed_at`         | Generated timestamp      | `TIMESTAMPTZ`              |

---

# Missing and Unavailable Fields

The current Hyatt room availability response does not contain:

* hotel name
* hotel brand
* Hyatt hotel category
* hotel address
* city
* country
* requested stay dates
* observation timestamp

Hotel metadata will require a separate Hyatt metadata source.

Because `hotels.name` and `hotels.brand` are `NOT NULL`, the room availability response alone is not sufficient to create a complete new hotel record.

The hotel record must either:

* already exist in the database, or
* be populated from a separate Hyatt hotel metadata source.

Stay dates come from the Hyatt request parameters.

`observed_at` is generated by the Award Daren ingestion pipeline.

---

# Known Limitations

1. The current fixtures were captured using a multi-night search. Production ingestion should preferably query one night at a time to align pricing with the `daily_availability` table grain.

2. Hyatt's `roomCategory` currently contains values such as `STANDARD` and `PREMIUM`. Additional values may exist and should be reviewed as more hotels are tested.

3. `PREMIUM` is a broad Hyatt room category and should not be interpreted as meaning only suite inventory.

4. The current cash pricing rule uses the Hyatt Member Rate and includes taxes and fees through `totalAfterTax`.

5. Future product requirements may support cash-price comparisons excluding taxes and fees.

6. Hyatt rate-plan codes and names should be tested across additional properties before assuming identifiers such as `MYHI` are universal.

7. The current points-price mapping uses the qualifying `POINTS` rate plan rather than relying only on `lowestPointValue`.

8. Hotel metadata requires a separate source because the current room availability endpoint does not provide enough information to populate all required fields in the `hotels` table.

9. This mapping should be updated as additional Hyatt properties, room categories, rate plans, and response variations are collected.
