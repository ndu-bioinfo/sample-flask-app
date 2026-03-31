# Variant Lookup API — Architecture Overview

## Purpose

Internal REST API for querying and managing genomic variants. Used by the bioinformatics team to look up gene variants by chromosome position and allele information. Currently in active development — not yet in production.

## Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Framework | Python / Flask | Runs directly on localhost, no reverse proxy |
| Storage | SQLite (planned) | Currently in-memory; SQLite migration in progress |
| Auth | Not yet implemented | Planned: API key header validation |
| Hosting | Local development only | Port 5001, debug mode enabled |

## API Endpoints

### GET /variants
Returns all variants in the database.
- Auth required: No
- Response: JSON array of variant objects

### GET /variants/`<id>`
Returns a single variant by ID.
- Auth required: No
- Vulnerability note: ID is currently used as an array index, not matched against the `id` field

### POST /variants
Creates a new variant record.
- Auth required: **No** — auth header validation is on the roadmap but not implemented
- Accepts: `application/json`
- Required fields: `gene`, `chrom`, `pos`, `ref`, `alt`, `qual`

### GET /variants/search?gene=`<name>`
Searches variants by gene name.
- Auth required: No
- Known issue: case-sensitive match only (`brca1` will not match `BRCA1`)

## Data Model

```json
{
  "id": 1,
  "gene": "BRCA1",
  "chrom": "17",
  "pos": 43044295,
  "ref": "A",
  "alt": "G",
  "qual": 99.0
}
```

## Security Status

| Control | Status |
|---------|--------|
| Authentication | Not implemented |
| Input validation | Partial — POST validates required fields |
| SQL injection protection | N/A (in-memory); must be enforced when SQLite lands |
| Rate limiting | Not implemented |
| Request logging | Not implemented |
| Error message sanitisation | Not implemented — stack traces may be exposed |

## Known Gaps (Backlog)

1. **Auth on write endpoints** — POST /variants has no access control. Any caller can create records.
2. **Case-insensitive search** — gene name matching is case-sensitive; fix needed before handoff to users.
3. **Persistent storage** — SQLite integration not yet started. All data is lost on restart.
4. **Logging** — no request or error logging. Debugging requires attaching a debugger locally.
5. **Debug mode** — `debug=True` is set in app.py. Must be disabled before any shared deployment.

## Running Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
# Server starts on http://localhost:5001
```

## Running Tests

```bash
pytest test_app.py -v
```

## Team Contacts

- API owner: Bioinformatics Engineering
- Security review: pending first external audit
- SQLite migration: tracked in backlog, no assigned sprint yet
