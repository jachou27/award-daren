# Hyatt Test Fixtures

## `hyatt_availability_sample.json`

Representative Hyatt award availability response captured for development
and testing.

### Source

- Property: Hyatt Regency Waikiki Beach Resort and Spa
- Property code: `hnlrw`
- Check-in: 2026-09-22
- Check-out: 2026-09-24
- Rooms: 1
- Adults: 2
- Children: 0
- Search type: World of Hyatt points
- Captured from: Hyatt.com booking flow
- Endpoint: `/en-US/shop/service/rooms/roomrates/hnlrw`

### Capture Method

The response was captured from the browser developer tools Network tab
using a Fetch/XHR request generated during an award availability search.

Only the JSON response body was saved. Request headers, cookies,
authorization information, and browser session data were not included.

### Sanitization

The fixture was checked for common sensitive fields including cookies,
authorization headers, tokens, session identifiers, API keys, passwords,
email addresses, and user/account identifiers.

The sanitized fixture remains valid JSON.