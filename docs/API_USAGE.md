# Public API Usage Guide

## Authentication

The DeceptionDetector public API uses JWT (JSON Web Token) authentication.

**Security:** Password must be hashed with SHA256 on the client side before sending.

### Get a Token

**Endpoint:** `POST /api/auth/token`

**Request:**
```json
{
  "username": "externalapiuser",
  "password_hash": "db3d51ecf1d848e50f02d66492608f0398bcf24f00096b8e0fd6476377034989"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

Token expires after 1 hour.

**⚠️ Important:** Never send plain-text passwords. Always hash with SHA256 first.

---

## Check Deception

**Endpoint:** `POST /api/public/checkDeception`

**Headers:**
```
Authorization: Bearer <your_token>
Content-Type: application/json
```

**Request:**
```json
{
  "text": "Your text to analyze",
  "modelName": "bert-combined-1"
}
```

**Available Models:**
- `bert-climate-change-1`
- `bert-combined-1`
- `bert-covid-1`
- `deberta-climate-change-1`
- `deberta-combined-1`
- `deberta-covid-1`

**Response:**
```json
{
  "is_deceptive": true,
  "confidence": 0.9547,
  "shap_words": [
    ["word1", 0.423],
    ["word2", -0.312]
  ],
  "lime_words": [
    ["word1", 0.567],
    ["word2", -0.234]
  ],
  "model_used": "bert-combined-1"
}
```

- `is_deceptive`: `true` = deceptive, `false` = truthful
- `confidence`: Model confidence (0.0 - 1.0)
- `shap_words`: SHAP explanation (positive = deceptive, negative = truthful)
- `lime_words`: LIME explanation (positive = deceptive, negative = truthful)

---

## Python Example

```python
import requests
import hashlib

BASE_URL = "http://localhost:5000"

# Hash password with SHA256
password = "your_password"
password_hash = hashlib.sha256(password.encode()).hexdigest()

# 1. Get token
auth_response = requests.post(
    f"{BASE_URL}/api/auth/token",
    json={
        "username": "externalapiuser",
        "password_hash": password_hash
    }
)
token = auth_response.json()["token"]

# 2. Check deception
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/api/public/checkDeception",
    headers=headers,
    json={
        "text": "Climate change is a hoax.",
        "modelName": "bert-climate-change-1"
    }
)

result = response.json()
print(f"Deceptive: {result['is_deceptive']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Top SHAP words: {result['shap_words'][:3]}")
```

---

## Production Setup

### Required Configuration

**⚠️ IMPORTANT:** Credentials are NOT stored in code. You MUST set environment variables.

**Generate secrets:**
```bash
python generate_secrets.py
```

This will generate:
- Password hash (SHA256)
- JWT secret
- Environment variable commands

**Set environment variables:**

**Windows (PowerShell):**
```powershell
$env:API_USERNAME="externalapiuser"
$env:API_PASSWORD_HASH="<generated_hash>"
$env:JWT_SECRET="<generated_secret>"
$env:JWT_EXP_SECONDS="3600"
```

**Linux/Mac:**
```bash
export API_USERNAME="externalapiuser"
export API_PASSWORD_HASH="<generated_hash>"
export JWT_SECRET="<generated_secret>"
export JWT_EXP_SECONDS="3600"
```

**For persistent storage, use:**
- `.env` file (with python-dotenv)
- System environment variables
- Secret management service (AWS Secrets Manager, Azure Key Vault, etc.)

---

## Rate Limits

- **Token endpoint:** 10 requests/minute
- **checkDeception endpoint:** 20 requests/minute

Rate limits are per IP address.

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 401 | Unauthorized (invalid credentials or token) |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

## Testing

### Quick Test with cURL

**Windows (PowerShell):**
```powershell
# 1. Get token
$password_hash = [System.BitConverter]::ToString((New-Object System.Security.Cryptography.SHA256Managed).ComputeHash([System.Text.Encoding]::UTF8.GetBytes("apipassword123"))).Replace("-","").ToLower()

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/auth/token" -Method POST -ContentType "application/json" -Body (@{username="externalapiuser"; password_hash=$password_hash} | ConvertTo-Json)

$token = $response.token

# 2. Check deception
Invoke-RestMethod -Uri "http://localhost:5000/api/public/checkDeception" -Method POST -Headers @{Authorization="Bearer $token"} -ContentType "application/json" -Body (@{text="Climate change is a hoax"; modelName="bert-climate-change-1"} | ConvertTo-Json)
```

**Linux/Mac (bash with curl + jq):**
```bash
# 1. Hash password and get token
PASSWORD_HASH=$(echo -n "apipassword123" | sha256sum | cut -d' ' -f1)
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/token \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"externalapiuser\",\"password_hash\":\"$PASSWORD_HASH\"}" \
  | jq -r '.token')

# 2. Check deception
curl -X POST http://localhost:5000/api/public/checkDeception \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Climate change is a hoax","modelName":"bert-climate-change-1"}'
```

### Test with Python Script

Create a file `test_api.py`:
```python
import requests
import hashlib

# Hash password
password_hash = hashlib.sha256("apipassword123".encode()).hexdigest()

# Get token
auth = requests.post("http://localhost:5000/api/auth/token",
    json={"username": "externalapiuser", "password_hash": password_hash})
print(f"Token: {auth.json()['token'][:20]}...")

# Check deception
token = auth.json()["token"]
response = requests.post("http://localhost:5000/api/public/checkDeception",
    headers={"Authorization": f"Bearer {token}"},
    json={"text": "Climate change is a hoax", "modelName": "bert-climate-change-1"})

result = response.json()
print(f"\nDeceptive: {result['is_deceptive']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Top 3 SHAP words: {result['shap_words'][:3]}")
print(f"Top 3 LIME words: {result['lime_words'][:3]}")
```

Run: `python test_api.py`
