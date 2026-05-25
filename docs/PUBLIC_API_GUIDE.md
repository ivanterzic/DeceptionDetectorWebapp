# Deception Detector — Public API Guide

A guide for external users using the Deception Detector API.

---

## Table of Contents

- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [POST /api/auth/token](#post-apiauthtoken)
  - [POST /api/public/checkDeception](#post-apipubliccheckdeception)
  - [GET /api/models](#get-apimodels)
  - [GET /api/health](#get-apihealth)
- [Available Models](#available-models)
- [Rate Limits](#rate-limits)
- [Error Reference](#error-reference)
- [Code Examples](#code-examples)
  - [Python](#python)
  - [JavaScript (Node.js)](#javascript-nodejs)
  - [cURL](#curl)
  - [PowerShell](#powershell)

---

## Overview

The Deception Detector API analyzes text for deceptive content using fine-tuned transformer models (BERT, DeBERTa). Along with a classification result, every response includes **explainability data** — word-level scores from both SHAP and LIME — so you can understand exactly which words drove the model's decision.

---

## Base URL

```
https://api.example.com/api
```

> Replace `https://api.example.com` with the actual host you were given when your account was provisioned.

---

## Authentication

The API uses **JWT (JSON Web Token)** authentication.

### How it works

1. Hash your password with **SHA-256** on the client side before sending it.
2. `POST` your username and hashed password to `/api/auth/token`.
3. You receive a JWT valid for **1 hour**.
4. Include the token in the `Authorization` header of every protected request.
5. When the token expires, request a new one.

> **Security note:** Always hash the password locally before sending. Never transmit plain-text passwords.

### Hashing your password

**Python**
```python
import hashlib
password_hash = hashlib.sha256("your_password_here".encode()).hexdigest()
```

**JavaScript**
```javascript
const crypto = require('crypto');
const passwordHash = crypto.createHash('sha256').update('your_password_here').digest('hex');
```

**Bash**
```bash
echo -n "your_password_here" | sha256sum | cut -d' ' -f1
```

**PowerShell**
```powershell
$hash = [System.BitConverter]::ToString(
    (New-Object System.Security.Cryptography.SHA256Managed).ComputeHash(
        [System.Text.Encoding]::UTF8.GetBytes("your_password_here")
    )
).Replace("-","").ToLower()
```

---

## Endpoints

### POST /api/auth/token

Request a JWT for API access.

**Rate limit:** 10 requests / 60 seconds per IP

**Authentication:** Not required

**Request**

```
POST /api/auth/token
Content-Type: application/json
```

```json
{
  "username": "your_api_username",
  "password_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `username` | string | Yes | Your API username |
| `password_hash` | string | Yes | SHA-256 hex digest of your password |

**Response — 200 OK**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoieW91cl9hcGlfdXNlcm5hbWUiLCJleHAiOjE3MTY2NTQ0MDB9.exampleSignatureHere",
  "expires_in": 3600
}
```

| Field | Type | Description |
|---|---|---|
| `token` | string | JWT to include in subsequent requests |
| `expires_in` | integer | Seconds until the token expires (3600 = 1 hour) |

**Error responses**

| Status | Body | Cause |
|---|---|---|
| 400 | `{"error": "No data provided"}` | Missing request body |
| 401 | `{"error": "Invalid credentials"}` | Wrong username or password |
| 429 | `{"error": "Rate limit exceeded"}` | Too many auth attempts |

---

### POST /api/public/checkDeception

Analyze text for deception. Returns a classification, confidence score, and word-level SHAP and LIME explanations.

**Rate limit:** 20 requests / 60 seconds per IP

**Authentication:** Required — `Authorization: Bearer <token>`

**Request**

```
POST /api/public/checkDeception
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example.token
```

```json
{
  "text": "Scientists have unanimously confirmed that vaccines cause autism.",
  "modelName": "bert-combined-1",
  "params": {
    "top_n_words": 10
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | string | Yes | Text to analyze. Maximum 512 tokens (~400–500 words). |
| `modelName` | string | Yes | Model to use. See [Available Models](#available-models). |
| `params.top_n_words` | integer | No | Limit explanation words returned. Omit for all words. |

**Response — 200 OK**

```json
{
  "is_deceptive": true,
  "confidence": 0.9312,
  "shap_words": [
    ["unanimously", 0.487],
    ["autism", 0.391],
    ["vaccines", 0.204],
    ["cause", 0.178],
    ["scientists", -0.143]
  ],
  "lime_words": [
    ["unanimously", 0.512],
    ["autism", 0.345],
    ["cause", 0.211],
    ["vaccines", 0.189],
    ["confirmed", -0.102]
  ],
  "model_used": "bert-combined-1"
}
```

| Field | Type | Description |
|---|---|---|
| `is_deceptive` | boolean | `true` if the model classifies the text as deceptive, `false` if truthful |
| `confidence` | float | Model confidence (0.0 – 1.0). Higher means more certain. |
| `shap_words` | array | SHAP word importances: `[word, score]` pairs |
| `lime_words` | array | LIME word importances: `[word, score]` pairs |
| `model_used` | string | The model that produced this result |

**Interpreting explanation scores**

| Score | Meaning |
|---|---|
| Positive (e.g. `+0.48`) | This word pushed the prediction toward **deceptive** |
| Negative (e.g. `−0.14`) | This word pushed the prediction toward **truthful** |
| Near zero | This word had little influence on the result |

**Error responses**

| Status | Body | Cause |
|---|---|---|
| 400 | `{"error": "Text is required"}` | Empty or missing `text` field |
| 400 | `{"error": "Text contains 630 tokens, but model limit is 512. Please reduce text length."}` | Input exceeds token limit |
| 400 | `{"error": "Invalid model. Available models: ..."}` | Unknown model name |
| 401 | `{"error": "Invalid or expired token"}` | Missing, malformed, or expired JWT |
| 429 | `{"error": "Rate limit exceeded"}` | Too many requests |
| 500 | `{"error": "Check deception failed"}` | Server-side error |

---

### GET /api/models

Returns the list of model keys currently available for analysis.

**Rate limit:** 60 requests / 60 seconds per IP

**Authentication:** Not required

**Request**

```
GET /api/models
```

**Response — 200 OK**

```json
[
  "bert-climate-change-1",
  "bert-combined-1",
  "bert-covid-1",
  "deberta-climate-change-1",
  "deberta-combined-1",
  "deberta-covid-1"
]
```

Use a value from this list as the `modelName` in `/api/public/checkDeception`.

---

### GET /api/health

Confirms the API is running. Useful for monitoring and connectivity checks.

**Rate limit:** None

**Authentication:** Not required

**Request**

```
GET /api/health
```

**Response — 200 OK**

```json
{
  "status": "healthy",
  "service": "deception-detector-backend"
}
```

---

## Available Models

| Model Key | Base Architecture | Domain |
|---|---|---|
| `bert-combined-1` | BERT | General — works across topics |
| `bert-climate-change-1` | BERT | Climate change claims |
| `bert-covid-1` | BERT | COVID-19 claims |
| `deberta-combined-1` | DeBERTa v3 | General — higher accuracy, slower |
| `deberta-climate-change-1` | DeBERTa v3 | Climate change claims |
| `deberta-covid-1` | DeBERTa v3 | COVID-19 claims |

**Recommendations**

- Use a domain-specific model when your input text clearly falls within that topic — it will typically produce higher confidence and more relevant explanations.
- Use `bert-combined-1` or `deberta-combined-1` for general-purpose or mixed-topic inputs.
- DeBERTa models are more accurate but slower to respond. BERT models are faster and suitable for higher-throughput use cases.

---

## Rate Limits

Rate limits are applied per IP address.

| Endpoint | Limit |
|---|---|
| `POST /api/auth/token` | 10 requests / 60 s |
| `POST /api/public/checkDeception` | 20 requests / 60 s |
| `GET /api/models` | 60 requests / 60 s |
| `GET /api/health` | Unlimited |

When a limit is exceeded, the API returns HTTP `429` with a body of:

```json
{
  "error": "Rate limit exceeded"
}
```

Wait until the window resets (up to 60 seconds) before retrying.

---

## Error Reference

| HTTP Status | Meaning |
|---|---|
| 200 | Success |
| 400 | Bad request — check your input fields |
| 401 | Unauthorized — token missing, expired, or invalid |
| 429 | Rate limit exceeded — slow down and retry |
| 500 | Server error — not caused by your request |

---

## Code Examples

### Python

```python
import hashlib
import requests

BASE_URL = "https://api.example.com/api"
USERNAME  = "your_api_username"
PASSWORD  = "your_api_password"

# 1. Hash the password
password_hash = hashlib.sha256(PASSWORD.encode()).hexdigest()

# 2. Obtain a JWT
auth = requests.post(f"{BASE_URL}/auth/token", json={
    "username": USERNAME,
    "password_hash": password_hash,
})
auth.raise_for_status()
token = auth.json()["token"]

# 3. Analyze text
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/public/checkDeception", headers=headers, json={
    "text": "Scientists have unanimously confirmed that vaccines cause autism.",
    "modelName": "bert-combined-1",
})
response.raise_for_status()
result = response.json()

# 4. Use the result
print(f"Deceptive : {result['is_deceptive']}")
print(f"Confidence: {result['confidence']:.1%}")
print("\nTop words (SHAP):")
for word, score in result["shap_words"][:5]:
    arrow = "→ deceptive" if score > 0 else "→ truthful"
    print(f"  {word:<20} {score:+.3f}  {arrow}")
```

**With automatic token refresh:**

```python
import hashlib
import time
import requests


class DeceptionClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()
        self._token: str | None = None
        self._token_expiry: float = 0

    def _get_token(self) -> str:
        if self._token and time.time() < self._token_expiry:
            return self._token
        r = requests.post(f"{self.base_url}/auth/token", json={
            "username": self.username,
            "password_hash": self._password_hash,
        })
        r.raise_for_status()
        data = r.json()
        self._token = data["token"]
        self._token_expiry = time.time() + data["expires_in"] - 60  # refresh 1 min early
        return self._token

    def check(self, text: str, model: str = "bert-combined-1") -> dict:
        r = requests.post(
            f"{self.base_url}/public/checkDeception",
            headers={"Authorization": f"Bearer {self._get_token()}"},
            json={"text": text, "modelName": model},
        )
        if r.status_code == 401:
            # Force token refresh once
            self._token = None
            r = requests.post(
                f"{self.base_url}/public/checkDeception",
                headers={"Authorization": f"Bearer {self._get_token()}"},
                json={"text": text, "modelName": model},
            )
        r.raise_for_status()
        return r.json()


client = DeceptionClient("https://api.example.com/api", "your_api_username", "your_api_password")
result = client.check("Climate change is a hoax.")
print(result)
```

---

### JavaScript (Node.js)

```javascript
const crypto  = require('crypto');
const axios   = require('axios');

const BASE_URL = 'https://api.example.com/api';
const USERNAME = 'your_api_username';
const PASSWORD = 'your_api_password';

const passwordHash = crypto.createHash('sha256').update(PASSWORD).digest('hex');

(async () => {
  // 1. Get token
  const { data: auth } = await axios.post(`${BASE_URL}/auth/token`, {
    username: USERNAME,
    password_hash: passwordHash,
  });

  const token = auth.token;

  // 2. Analyze text
  const { data: result } = await axios.post(
    `${BASE_URL}/public/checkDeception`,
    {
      text: 'Scientists have unanimously confirmed that vaccines cause autism.',
      modelName: 'bert-combined-1',
    },
    { headers: { Authorization: `Bearer ${token}` } }
  );

  // 3. Use the result
  console.log(`Deceptive : ${result.is_deceptive}`);
  console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
  console.log('\nTop words (SHAP):');
  result.shap_words.slice(0, 5).forEach(([word, score]) => {
    const label = score > 0 ? '→ deceptive' : '→ truthful';
    console.log(`  ${word.padEnd(20)} ${score.toFixed(3).padStart(7)}  ${label}`);
  });
})();
```

---

### cURL

```bash
BASE_URL="https://api.example.com/api"
USERNAME="your_api_username"
PASSWORD="your_api_password"

# 1. Hash the password (Linux/macOS)
PASSWORD_HASH=$(printf '%s' "$PASSWORD" | sha256sum | cut -d' ' -f1)

# 2. Get token
TOKEN=$(curl -s -X POST "$BASE_URL/auth/token" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password_hash\":\"$PASSWORD_HASH\"}" \
  | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# 3. Analyze text
curl -s -X POST "$BASE_URL/public/checkDeception" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Scientists have unanimously confirmed that vaccines cause autism.",
    "modelName": "bert-combined-1"
  }'
```

> If `jq` is installed, pipe the final command to `| jq '.'` for formatted output.

---

### PowerShell

```powershell
$BASE_URL = "https://api.example.com/api"
$USERNAME = "your_api_username"
$PASSWORD = "your_api_password"

# 1. Hash the password
$bytes        = [System.Text.Encoding]::UTF8.GetBytes($PASSWORD)
$sha256       = [System.Security.Cryptography.SHA256]::Create()
$PASSWORD_HASH = [System.BitConverter]::ToString($sha256.ComputeHash($bytes)).Replace("-","").ToLower()

# 2. Get token
$authBody = @{ username = $USERNAME; password_hash = $PASSWORD_HASH } | ConvertTo-Json
$auth     = Invoke-RestMethod -Uri "$BASE_URL/auth/token" -Method POST `
              -ContentType "application/json" -Body $authBody
$TOKEN    = $auth.token

# 3. Analyze text
$body   = @{ text = "Scientists have unanimously confirmed that vaccines cause autism."; modelName = "bert-combined-1" } | ConvertTo-Json
$result = Invoke-RestMethod -Uri "$BASE_URL/public/checkDeception" -Method POST `
            -Headers @{ Authorization = "Bearer $TOKEN" } `
            -ContentType "application/json" -Body $body

# 4. Display results
Write-Host "Deceptive : $($result.is_deceptive)"
Write-Host "Confidence: $([math]::Round($result.confidence * 100, 1))%"
Write-Host "`nTop words (SHAP):"
$result.shap_words[0..4] | ForEach-Object {
    $word, $score = $_
    $label = if ($score -gt 0) { "→ deceptive" } else { "→ truthful" }
    Write-Host ("  {0,-20} {1,+7:F3}  {2}" -f $word, $score, $label)
}
```
