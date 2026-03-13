# API Reference — Donation for Shifa

Base URL: `http://localhost:8000`

All responses are wrapped in a standard envelope:

```json
{ "message": "Success", "data": { ... } }
```

Errors follow:

```json
{ "success": false, "message": "...", "status_code": 4xx }
```

Paginated responses include:

```json
{
  "message": "Success",
  "total": 10,
  "page": 1,
  "size": 10,
  "data": [ ... ],
  "nextPage": 2,
  "prevPage": null,
  "pageChunks": [1, 2]
}
```

---

## Authentication

JWT token via `Authorization: Bearer <token>` header.

Admin endpoints additionally require `is_admin = true` on the user account.

---

## User

### POST `/api/v1/user/signup`

Register a new user.

**Request body:**

```json
{
  "email": "user@example.com",
  "name": "Ali Hassan",
  "password": "securepassword"
}
```

**Response `200`:**

```json
{
  "message": "Success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

---

### POST `/api/v1/user/token`

Obtain a JWT access token.

**Request body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response `200`:**

```json
{
  "message": "Success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

**Response `401`** — invalid credentials:

```json
{ "success": false, "message": "Invalid email or password" }
```

---

### GET `/api/v1/user/me`

Get the currently authenticated user's profile.

**Headers:** `Authorization: Bearer <token>`

**Response `200`:**

```json
{
  "id": 1,
  "username": "alihassan",
  "email": "user@example.com",
  "name": "Ali Hassan",
  "joined_at": "2026-03-01T10:00:00Z",
  "updated_at": "2026-03-01T10:00:00Z"
}
```

**Response `401`** — missing or invalid token.

---

## Donations

### GET `/api/v1/donations`

Public list of received donations. No authentication required.

**Query params:**

| Param  | Type | Default | Description        |
|--------|------|---------|--------------------|
| `page` | int  | `1`     | Page number        |
| `size` | int  | `10`    | Items per page     |

**Response `200`:**

```json
{
  "message": "Success",
  "total": 2,
  "page": 1,
  "size": 10,
  "data": [
    {
      "id": 1,
      "donor_name": "Ahmed Raza",
      "transaction_number": "TXN-2024-001",
      "amount": "50000.00",
      "date_received": "2024-06-01"
    },
    {
      "id": 2,
      "donor_name": "Sara Khan",
      "transaction_number": "TXN-2024-002",
      "amount": "25000.00",
      "date_received": "2024-07-15"
    }
  ],
  "nextPage": null,
  "prevPage": null,
  "pageChunks": [1]
}
```

---

### GET `/api/v1/admin/donations`

Admin list of donations with search and date filters.

**Headers:** `Authorization: Bearer <admin-token>`

**Query params:**

| Param       | Type   | Description                                  |
|-------------|--------|----------------------------------------------|
| `page`      | int    | Page number (default: 1)                     |
| `size`      | int    | Items per page (default: 10)                 |
| `search`    | string | Search by donor name or transaction number   |
| `date_from` | date   | Filter: date received ≥ this date (YYYY-MM-DD) |
| `date_to`   | date   | Filter: date received ≤ this date (YYYY-MM-DD) |

**Example:** `GET /api/v1/admin/donations?search=Ahmed&date_from=2024-01-01&date_to=2024-12-31`

**Response `200`:**

```json
{
  "message": "Success",
  "total": 1,
  "page": 1,
  "size": 10,
  "data": [
    {
      "id": 1,
      "donor_name": "Ahmed Raza",
      "transaction_number": "TXN-2024-001",
      "amount": "50000.00",
      "date_received": "2024-06-01",
      "notes": "Zakat donation",
      "created_at": "2026-03-01T10:00:00Z",
      "updated_at": "2026-03-01T10:00:00Z",
      "created_by_id": 1
    }
  ],
  "nextPage": null,
  "prevPage": null,
  "pageChunks": [1]
}
```

**Response `401`** — missing/invalid token. **Response `403`** — not an admin.

---

### POST `/api/v1/admin/donations`

Create a donation record.

**Headers:** `Authorization: Bearer <admin-token>`

**Request body:**

```json
{
  "donor_name": "Ahmed Raza",
  "transaction_number": "TXN-2024-001",
  "amount": "50000.00",
  "date_received": "2024-06-01",
  "notes": "Zakat donation"
}
```

| Field                | Type    | Required | Constraints          |
|----------------------|---------|----------|----------------------|
| `donor_name`         | string  | yes      | max 255 chars        |
| `transaction_number` | string  | yes      | max 100 chars, unique |
| `amount`             | decimal | yes      | > 0                  |
| `date_received`      | date    | yes      | YYYY-MM-DD           |
| `notes`              | string  | no       |                      |

**Response `200`:**

```json
{
  "message": "Donation created",
  "data": {
    "id": 1,
    "donor_name": "Ahmed Raza",
    "transaction_number": "TXN-2024-001",
    "amount": "50000.00",
    "date_received": "2024-06-01",
    "notes": "Zakat donation",
    "created_at": "2026-03-01T10:00:00Z",
    "updated_at": "2026-03-01T10:00:00Z",
    "created_by_id": 1
  }
}
```

**Response `409`** — transaction number already exists.

---

### GET `/api/v1/admin/donations/{donation_id}`

Get a single donation by ID.

**Headers:** `Authorization: Bearer <admin-token>`

**Response `200`:**

```json
{
  "message": "Success",
  "data": {
    "id": 1,
    "donor_name": "Ahmed Raza",
    "transaction_number": "TXN-2024-001",
    "amount": "50000.00",
    "date_received": "2024-06-01",
    "notes": "Zakat donation",
    "created_at": "2026-03-01T10:00:00Z",
    "updated_at": "2026-03-01T10:00:00Z",
    "created_by_id": 1
  }
}
```

**Response `404`** — donation not found.

---

### PUT `/api/v1/admin/donations/{donation_id}`

Update a donation record. All fields are optional (partial update).

**Headers:** `Authorization: Bearer <admin-token>`

**Request body:**

```json
{
  "amount": "55000.00",
  "notes": "Updated: includes sadqa"
}
```

**Response `200`:**

```json
{
  "message": "Donation updated",
  "data": {
    "id": 1,
    "donor_name": "Ahmed Raza",
    "transaction_number": "TXN-2024-001",
    "amount": "55000.00",
    "date_received": "2024-06-01",
    "notes": "Updated: includes sadqa",
    "created_at": "2026-03-01T10:00:00Z",
    "updated_at": "2026-03-14T09:00:00Z",
    "created_by_id": 1
  }
}
```

**Response `404`** — not found. **Response `409`** — duplicate transaction number.

---

### DELETE `/api/v1/admin/donations/{donation_id}`

Delete a donation record.

**Headers:** `Authorization: Bearer <admin-token>`

**Response `200`:**

```json
{ "message": "Donation deleted", "data": {} }
```

**Response `404`** — not found.

---

## Distributions

### GET `/api/v1/distributions`

Public list of distributions to recipients. No authentication required.

**Query params:** `page`, `size` (same as donations)

**Response `200`:**

```json
{
  "message": "Success",
  "total": 1,
  "page": 1,
  "size": 10,
  "data": [
    {
      "id": 1,
      "recipient_name": "Zainab Bibi",
      "address": "Village Kot Addu, Punjab",
      "problem_description": "Lost crops in flood, family of 6 needs immediate aid.",
      "amount_received": "20000.00",
      "date_distributed": "2024-08-20"
    }
  ],
  "nextPage": null,
  "prevPage": null,
  "pageChunks": [1]
}
```

---

### GET `/api/v1/admin/distributions`

Admin list of distributions with search and date filters.

**Headers:** `Authorization: Bearer <admin-token>`

**Query params:**

| Param       | Type   | Description                                      |
|-------------|--------|--------------------------------------------------|
| `page`      | int    | Page number (default: 1)                         |
| `size`      | int    | Items per page (default: 10)                     |
| `search`    | string | Search by recipient name or address              |
| `date_from` | date   | Filter: date distributed ≥ this date (YYYY-MM-DD) |
| `date_to`   | date   | Filter: date distributed ≤ this date (YYYY-MM-DD) |

**Example:** `GET /api/v1/admin/distributions?search=Zainab&date_from=2024-08-01`

**Response `200`:**

```json
{
  "message": "Success",
  "total": 1,
  "page": 1,
  "size": 10,
  "data": [
    {
      "id": 1,
      "recipient_name": "Zainab Bibi",
      "address": "Village Kot Addu, Punjab",
      "problem_description": "Lost crops in flood, family of 6 needs immediate aid.",
      "amount_received": "20000.00",
      "date_distributed": "2024-08-20",
      "notes": null,
      "created_at": "2026-03-01T10:00:00Z",
      "updated_at": "2026-03-01T10:00:00Z",
      "created_by_id": 1
    }
  ],
  "nextPage": null,
  "prevPage": null,
  "pageChunks": [1]
}
```

---

### POST `/api/v1/admin/distributions`

Create a distribution record.

**Headers:** `Authorization: Bearer <admin-token>`

**Request body:**

```json
{
  "recipient_name": "Zainab Bibi",
  "address": "Village Kot Addu, Punjab",
  "problem_description": "Lost crops in flood, family of 6 needs immediate aid.",
  "amount_received": "20000.00",
  "date_distributed": "2024-08-20",
  "notes": "First instalment"
}
```

| Field                 | Type    | Required | Constraints       |
|-----------------------|---------|----------|-------------------|
| `recipient_name`      | string  | yes      | max 255 chars     |
| `address`             | string  | yes      | min 5 chars       |
| `problem_description` | string  | yes      | min 10 chars      |
| `amount_received`     | decimal | yes      | > 0               |
| `date_distributed`    | date    | yes      | YYYY-MM-DD        |
| `notes`               | string  | no       |                   |

**Response `200`:**

```json
{
  "message": "Distribution created",
  "data": {
    "id": 1,
    "recipient_name": "Zainab Bibi",
    "address": "Village Kot Addu, Punjab",
    "problem_description": "Lost crops in flood, family of 6 needs immediate aid.",
    "amount_received": "20000.00",
    "date_distributed": "2024-08-20",
    "notes": "First instalment",
    "created_at": "2026-03-01T10:00:00Z",
    "updated_at": "2026-03-01T10:00:00Z",
    "created_by_id": 1
  }
}
```

---

### GET `/api/v1/admin/distributions/{distribution_id}`

Get a single distribution by ID.

**Headers:** `Authorization: Bearer <admin-token>`

**Response `200`:** same shape as the create response. **Response `404`** — not found.

---

### PUT `/api/v1/admin/distributions/{distribution_id}`

Update a distribution record. All fields optional (partial update).

**Headers:** `Authorization: Bearer <admin-token>`

**Request body:**

```json
{
  "amount_received": "25000.00",
  "notes": "Second instalment added"
}
```

**Response `200`:**

```json
{
  "message": "Distribution updated",
  "data": {
    "id": 1,
    "recipient_name": "Zainab Bibi",
    "address": "Village Kot Addu, Punjab",
    "problem_description": "Lost crops in flood, family of 6 needs immediate aid.",
    "amount_received": "25000.00",
    "date_distributed": "2024-08-20",
    "notes": "Second instalment added",
    "created_at": "2026-03-01T10:00:00Z",
    "updated_at": "2026-03-14T09:00:00Z",
    "created_by_id": 1
  }
}
```

**Response `404`** — not found.

---

### DELETE `/api/v1/admin/distributions/{distribution_id}`

Delete a distribution record.

**Headers:** `Authorization: Bearer <admin-token>`

**Response `200`:**

```json
{ "message": "Distribution deleted", "data": {} }
```

**Response `404`** — not found.

---

## Applications

### POST `/api/v1/applications`

Submit a financial assistance application. No authentication required.

Rate limited to **5 submissions per IP per 24 hours** (when Redis is available).

**Request body:**

```json
{
  "applicant_name": "Fatima Malik",
  "applicant_phone": "0300-1234567",
  "applicant_address": "456 Street Karachi",
  "problem_description": "Need financial help for my child's medical treatment",
  "amount_requested": "50000.00"
}
```

| Field                 | Type    | Required | Constraints       |
|-----------------------|---------|----------|-------------------|
| `applicant_name`      | string  | yes      |                   |
| `applicant_phone`     | string  | no       |                   |
| `applicant_address`   | string  | yes      | min 5 chars       |
| `problem_description` | string  | yes      | min 20 chars      |
| `amount_requested`    | decimal | no       | > 0               |

**Response `200`** — returns only `id` and `submitted_at` (no sensitive data echoed back):

```json
{
  "message": "Application submitted",
  "data": {
    "id": 1,
    "submitted_at": "2026-03-14T10:00:00Z"
  }
}
```

**Response `422`** — validation error (e.g. `problem_description` too short):

```json
{
  "success": false,
  "message": "Validation Error! 'problem_description' String should have at least 20 characters !"
}
```

**Response `429`** — too many submissions from this IP:

```json
{ "success": false, "message": "Too many submissions. Try again tomorrow." }
```

---

### GET `/api/v1/admin/applications`

Admin list of applications with search and status filters.

**Headers:** `Authorization: Bearer <admin-token>`

**Query params:**

| Param    | Type   | Description                                           |
|----------|--------|-------------------------------------------------------|
| `page`   | int    | Page number (default: 1)                              |
| `size`   | int    | Items per page (default: 10)                          |
| `search` | string | Search by applicant name or address                   |
| `status` | string | Filter by status: `pending`, `reviewed`, `approved`, `rejected` |

**Example:** `GET /api/v1/admin/applications?status=pending&search=Fatima`

**Response `200`:**

```json
{
  "message": "Success",
  "total": 1,
  "page": 1,
  "size": 10,
  "data": [
    {
      "id": 1,
      "applicant_name": "Fatima Malik",
      "applicant_phone": "0300-1234567",
      "applicant_address": "456 Street Karachi",
      "problem_description": "Need financial help for my child's medical treatment",
      "amount_requested": "50000.00",
      "status": "pending",
      "admin_notes": null,
      "submitted_at": "2026-03-14T10:00:00Z",
      "updated_at": "2026-03-14T10:00:00Z",
      "reviewed_by_id": null
    }
  ],
  "nextPage": null,
  "prevPage": null,
  "pageChunks": [1]
}
```

---

### GET `/api/v1/admin/applications/{application_id}`

Get a single application by ID.

**Headers:** `Authorization: Bearer <admin-token>`

**Response `200`:**

```json
{
  "message": "Success",
  "data": {
    "id": 1,
    "applicant_name": "Fatima Malik",
    "applicant_phone": "0300-1234567",
    "applicant_address": "456 Street Karachi",
    "problem_description": "Need financial help for my child's medical treatment",
    "amount_requested": "50000.00",
    "status": "pending",
    "admin_notes": null,
    "submitted_at": "2026-03-14T10:00:00Z",
    "updated_at": "2026-03-14T10:00:00Z",
    "reviewed_by_id": null
  }
}
```

**Response `404`** — not found.

---

### PATCH `/api/v1/admin/applications/{application_id}/status`

Update the status of an application. Sets `reviewed_by_id` to the current admin's ID.

**Headers:** `Authorization: Bearer <admin-token>`

**Request body:**

```json
{
  "status": "approved",
  "admin_notes": "Verified. Approved for PKR 50,000 assistance."
}
```

| Field        | Type   | Required | Allowed values                          |
|--------------|--------|----------|-----------------------------------------|
| `status`     | string | yes      | `reviewed`, `approved`, `rejected`      |
| `admin_notes`| string | no       |                                         |

**Response `200`:**

```json
{
  "message": "Application status updated",
  "data": {
    "id": 1,
    "applicant_name": "Fatima Malik",
    "applicant_phone": "0300-1234567",
    "applicant_address": "456 Street Karachi",
    "problem_description": "Need financial help for my child's medical treatment",
    "amount_requested": "50000.00",
    "status": "approved",
    "admin_notes": "Verified. Approved for PKR 50,000 assistance.",
    "submitted_at": "2026-03-14T10:00:00Z",
    "updated_at": "2026-03-14T11:00:00Z",
    "reviewed_by_id": 1
  }
}
```

**Response `404`** — not found.

---

## Stats

### GET `/api/v1/stats/summary`

Aggregated donation and distribution totals. No authentication required.

Cached in Redis for 60 seconds when Redis is available.

**Response `200`:**

```json
{
  "message": "Success",
  "data": {
    "total_collected": "125002.00",
    "total_distributed": "35000.00",
    "donation_count": 3,
    "distribution_count": 2
  }
}
```

| Field                | Description                              |
|----------------------|------------------------------------------|
| `total_collected`    | Sum of all `amount` across donations     |
| `total_distributed`  | Sum of all `amount_received` across distributions |
| `donation_count`     | Total number of donation records         |
| `distribution_count` | Total number of distribution records     |

---

## Error Reference

| Status | Meaning                                     |
|--------|---------------------------------------------|
| `400`  | Bad request                                 |
| `401`  | Missing or invalid JWT token                |
| `403`  | Authenticated but not an admin              |
| `404`  | Resource not found                          |
| `409`  | Conflict — duplicate unique field           |
| `422`  | Validation error — invalid request body     |
| `429`  | Rate limit exceeded                         |
| `500`  | Internal server error                       |

---

## Quick Start with curl

```bash
# 1. Sign up
curl -s -X POST http://localhost:8000/api/v1/user/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","name":"Admin User","password":"mypassword"}'

# 2. Get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/user/token \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"mypassword"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])")

# 3. Check stats (public)
curl -s http://localhost:8000/api/v1/stats/summary

# 4. Create a donation (admin)
curl -s -X POST http://localhost:8000/api/v1/admin/donations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"donor_name":"Ahmed Raza","transaction_number":"TXN-001","amount":"50000","date_received":"2026-03-14"}'

# 5. Create a distribution (admin)
curl -s -X POST http://localhost:8000/api/v1/admin/distributions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"recipient_name":"Zainab Bibi","address":"Village Kot Addu, Punjab","problem_description":"Flood affected family","amount_received":"20000","date_distributed":"2026-03-14"}'

# 6. Submit a public application
curl -s -X POST http://localhost:8000/api/v1/applications \
  -H "Content-Type: application/json" \
  -d '{"applicant_name":"Fatima Malik","applicant_address":"456 Street Karachi","problem_description":"Need financial help for medical treatment","amount_requested":"50000"}'

# 7. Review the application (admin)
curl -s -X PATCH http://localhost:8000/api/v1/admin/applications/1/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"approved","admin_notes":"Approved after verification"}'
```
