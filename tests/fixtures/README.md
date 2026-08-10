# Hyatt Test Fixtures

These fixtures contain representative Hyatt availability responses captured
for development and testing.

## Property

- Property: Hyatt Regency Waikiki Beach Resort and Spa
- Property code: `hnlrw`
- Check-in: 2026-09-22
- Check-out: 2026-09-24
- Rooms: 1
- Adults: 2
- Children: 0

## `hyatt_award_availability_sample.json`

Captured from a World of Hyatt award availability search.

The response includes:

- Room types
- Award availability
- Points pricing
- Points + Cash pricing
- Currency information

The request used the Hyatt room-rates endpoint with the World of Hyatt
rate filter.

## `hyatt_cash_availability_sample.json`

Captured from a standard cash availability search.

The response includes:

- Room types
- Member cash rates
- Public cash rates
- Taxes and fees
- Stay totals
- Currency information

The request used the Hyatt room-rates endpoint with:

`rateFilter=standard`

## Capture Method

Responses were captured from the browser developer tools Network tab using
Fetch/XHR requests generated during Hyatt availability searches.

Only JSON response bodies were saved. Request headers, cookies,
authorization information, and browser session data were not included.

## Sanitization

Both fixtures were checked for common sensitive fields including cookies,
authorization headers, tokens, session identifiers, API keys, passwords,
email addresses, and user/account identifiers.

Both fixtures were validated as valid JSON.