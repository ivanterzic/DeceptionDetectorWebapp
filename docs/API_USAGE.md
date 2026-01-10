# Deception Detector API Usage Guide

Complete guide for using the Deception Detector API with authentication, rate limiting, and explainable AI features.

## 🚀 Quick Start

### Base URLs
- **Local Development:** `http://localhost:5000/api`
- **Docker/Production:** `http://localhost/api` (through nginx)
- **Custom Domain:** `https://yourdomain.com/api`

### Authentication Flow
1. Hash your password with SHA256 (client-side)
2. Request JWT token from `/api/auth/token`
3. Include token in `Authorization: Bearer <token>` header for all requests
4. Token expires after 1 hour - request a new one when needed

---

## 📋 Table of Contents
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Get JWT Token](#get-jwt-token)
  - [Check Deception (Public API)](#check-deception-public-api)
  - [Get Available Models](#get-available-models)
  - [Predict (No Auth)](#predict-no-auth)
  - [Health Check](#health-check)
- [Code Examples](#code-examples)
- [Rate Limits](#rate-limits)
- [Error Handling](#error-handling)
- [Production Setup](#production-setup)

---

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication for secure access.

**⚠️ Security Best Practice:** Always hash passwords with SHA256 on the client side before sending. Never send plain-text passwords over the network.

### Password Hashing

**Python:**
```python
import hashlib
password_hash = hashlib.sha256("your_password".encode()).hexdigest()
```

**JavaScript:**
```javascript
const crypto = require('crypto');
const passwordHash = crypto.createHash('sha256').update('your_password').digest('hex');
```

**PowerShell:**
```powershell
$password_hash = [System.BitConverter]::ToString((New-Object System.Security.Cryptography.SHA256Managed).ComputeHash([System.Text.Encoding]::UTF8.GetBytes("your_password"))).Replace("-","").ToLower()
```

**Bash:**
```bash
PASSWORD_HASH=$(echo -n "your_password" | sha256sum | cut -d' ' -f1)
```

---

## 🔌 Endpoints

### Get JWT Token

Request an authentication token for API access.

**Endpoint:** `POST /api/auth/token`

**Rate Limit:** 10 requests/minute per IP

**Request Body:**
```json
{
  "username": "externalapiuser",
  "password_hash": "db3d51ecf1d848e50f02d66492608f0398bcf24f00096b8e0fd6476377034989"
}
```

**Success Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZXh0ZXJuYWxhcGl1c2VyIiwiZXhwIjoxNjg5MzY3MjAwfQ.abc123...",
  "expires_in": 3600
}
```

**Error Response (401):**
```json
{
  "error": "Invalid credentials"
}
```

---

### Check Deception (Public API)

Analyze text for deception with AI explainability (LIME + SHAP).

**Endpoint:** `POST /api/public/checkDeception`

**Rate Limit:** 20 requests/minute per IP

**Authentication:** Required (JWT Bearer token)

**Headers:**
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "Climate change is a hoax created by scientists.",
  "modelName": "bert-combined-1"
}
```

**Parameters:**
- `text` (string, required): Text to analyze (max 512 tokens)
- `modelName` (string, required): Model to use for analysis

**Available Models:**
- `bert-climate-change-1` - Specialized for climate change claims
- `bert-combined-1` - General deception detection (all topics)
- `bert-covid-1` - Specialized for COVID-19 claims
- `deberta-climate-change-1` - Advanced climate change model
- `deberta-combined-1` - Advanced general deception model
- `deberta-covid-1` - Advanced COVID-19 model

**Success Response (200):**
```json
{
  "is_deceptive": true,
  "confidence": 0.9547,
  "shap_words": [
    ["hoax", 0.423],
    ["scientists", 0.312],
    ["created", 0.187],
    ["climate", -0.156],
    ["change", -0.089]
  ],
  "lime_words": [
    ["hoax", 0.567],
    ["scientists", 0.234],
    ["climate", -0.123]
  ],
  "model_used": "bert-combined-1"
}
```

**Response Fields:**
- `is_deceptive` (boolean): `true` if deceptive, `false` if truthful
- `confidence` (float): Model confidence score (0.0 - 1.0)
- `shap_words` (array): SHAP explanation - [word, importance_score]
  - Positive scores → contribute to deceptive classification
  - Negative scores → contribute to truthful classification
- `lime_words` (array): LIME explanation - [word, importance_score]
  - Same scoring as SHAP
- `model_used` (string): Model that performed the analysis

**Error Responses:**
```json
// 400 Bad Request - Invalid input
{
  "error": "Text is required"
}

// 401 Unauthorized - Invalid/expired token
{
  "error": "Invalid or expired token"
}

// 429 Too Many Requests - Rate limit exceeded
{
  "error": "Rate limit exceeded"
}

// 500 Internal Server Error
{
  "error": "Prediction failed"
}
```

---

### Get Available Models

Retrieve list of all available models for analysis.

**Endpoint:** `GET /api/models`

**Rate Limit:** 60 requests/minute per IP

**Authentication:** None required

**Success Response (200):**
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

---

### Predict (No Auth)

Simple prediction endpoint without authentication (for internal/testing use).

**Endpoint:** `POST /api/predict`

**Rate Limit:** 20 requests/minute per IP

**Authentication:** None required

**Request Body:**
```json
{
  "text": "Your text to analyze",
  "model_name": "bert-combined-1"
}
```

**Success Response (200):**
```json
{
  "prediction": "deceptive",
  "confidence": 0.9547,
  "probabilities": {
    "deceptive": 0.9547,
    "truthful": 0.0453
  },
  "processing_time": 0.234,
  "model_used": "bert-combined-1"
}
```

---

### Health Check

Check API health status.

**Endpoint:** `GET /api/health`

**Rate Limit:** None

**Authentication:** None required

**Success Response (200):**
```json
{
  "status": "healthy",
  "service": "deception-detector-backend"
}
```

---

## 💻 Code Examples

### Python

**Complete Example:**
```python
import requests
import hashlib

# Configuration
BASE_URL = "http://localhost/api"  # Use /api for nginx proxy
USERNAME = "externalapiuser"
PASSWORD = "your_password_here"

# 1. Hash password
password_hash = hashlib.sha256(PASSWORD.encode()).hexdigest()
print(f"Password hash: {password_hash}")

# 2. Get JWT token
auth_response = requests.post(
    f"{BASE_URL}/auth/token",
    json={
        "username": USERNAME,
        "password_hash": password_hash
    }
)

if auth_response.status_code != 200:
    print(f"Auth failed: {auth_response.json()}")
    exit(1)

token = auth_response.json()["token"]
print(f"Token obtained: {token[:20]}...")

# 3. Check deception
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/public/checkDeception",
    headers=headers,
    json={
        "text": "Climate change is a hoax created by scientists.",
        "modelName": "bert-climate-change-1"
    }
)

if response.status_code != 200:
    print(f"Prediction failed: {response.json()}")
    exit(1)

# 4. Display results
result = response.json()
print(f"\n{'='*50}")
print(f"Deceptive: {result['is_deceptive']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"\nTop 5 SHAP explanations:")
for word, score in result['shap_words'][:5]:
    direction = "→ deceptive" if score > 0 else "→ truthful"
    print(f"  {word:15} {score:+.3f} {direction}")
print(f"{'='*50}")
```

**With Error Handling:**
```python
import requests
import hashlib
import time

class DeceptionDetectorAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.token = None
        self.token_expiry = 0
    
    def get_token(self):
        """Get or refresh JWT token"""
        if self.token and time.time() < self.token_expiry:
            return self.token
        
        response = requests.post(
            f"{self.base_url}/auth/token",
            json={
                "username": self.username,
                "password_hash": self.password_hash
            }
        )
        response.raise_for_status()
        
        data = response.json()
        self.token = data["token"]
        self.token_expiry = time.time() + data["expires_in"] - 60  # Refresh 1 min early
        return self.token
    
    def check_deception(self, text, model_name="bert-combined-1", retry=True):
        """Check if text is deceptive"""
        token = self.get_token()
        
        response = requests.post(
            f"{self.base_url}/public/checkDeception",
            headers={"Authorization": f"Bearer {token}"},
            json={"text": text, "modelName": model_name}
        )
        
        if response.status_code == 401 and retry:
            # Token expired, refresh and retry
            self.token = None
            return self.check_deception(text, model_name, retry=False)
        
        response.raise_for_status()
        return response.json()

# Usage
api = DeceptionDetectorAPI(
    base_url="http://localhost/api",
    username="externalapiuser",
    password="your_password"
)

try:
    result = api.check_deception(
        "Climate change is a hoax",
        model_name="bert-climate-change-1"
    )
    print(f"Deceptive: {result['is_deceptive']}")
    print(f"Confidence: {result['confidence']:.2%}")
except requests.exceptions.HTTPError as e:
    print(f"API Error: {e.response.json()}")
```

---

### JavaScript (Node.js)

```javascript
const axios = require('axios');
const crypto = require('crypto');

const BASE_URL = 'http://localhost/api';
const USERNAME = 'externalapiuser';
const PASSWORD = 'your_password';

// Hash password
const passwordHash = crypto.createHash('sha256').update(PASSWORD).digest('hex');

async function checkDeception() {
    try {
        // 1. Get token
        const authResponse = await axios.post(`${BASE_URL}/auth/token`, {
            username: USERNAME,
            password_hash: passwordHash
        });
        
        const token = authResponse.data.token;
        console.log(`Token obtained: ${token.substring(0, 20)}...`);
        
        // 2. Check deception
        const response = await axios.post(
            `${BASE_URL}/public/checkDeception`,
            {
                text: 'Climate change is a hoax created by scientists.',
                modelName: 'bert-climate-change-1'
            },
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
        
        // 3. Display results
        const result = response.data;
        console.log('\n' + '='.repeat(50));
        console.log(`Deceptive: ${result.is_deceptive}`);
        console.log(`Confidence: ${(result.confidence * 100).toFixed(2)}%`);
        console.log('\nTop 5 SHAP explanations:');
        result.shap_words.slice(0, 5).forEach(([word, score]) => {
            const direction = score > 0 ? '→ deceptive' : '→ truthful';
            console.log(`  ${word.padEnd(15)} ${score.toFixed(3).padStart(6)} ${direction}`);
        });
        console.log('='.repeat(50));
        
    } catch (error) {
        if (error.response) {
            console.error(`API Error: ${error.response.status}`, error.response.data);
        } else {
            console.error('Error:', error.message);
        }
    }
}

checkDeception();
```

---

### cURL (Linux/Mac)

```bash
#!/bin/bash

BASE_URL="http://localhost/api"
USERNAME="externalapiuser"
PASSWORD="your_password"

# 1. Hash password
PASSWORD_HASH=$(echo -n "$PASSWORD" | sha256sum | cut -d' ' -f1)

# 2. Get token
TOKEN=$(curl -s -X POST "$BASE_URL/auth/token" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password_hash\":\"$PASSWORD_HASH\"}" \
  | jq -r '.token')

echo "Token: ${TOKEN:0:20}..."

# 3. Check deception
curl -X POST "$BASE_URL/public/checkDeception" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Climate change is a hoax created by scientists.",
    "modelName": "bert-climate-change-1"
  }' | jq '.'
```

---

### PowerShell (Windows)

```powershell
$BASE_URL = "http://localhost/api"
$USERNAME = "externalapiuser"
$PASSWORD = "your_password"

# 1. Hash password
$password_hash = [System.BitConverter]::ToString(
    (New-Object System.Security.Cryptography.SHA256Managed).ComputeHash(
        [System.Text.Encoding]::UTF8.GetBytes($PASSWORD)
    )
).Replace("-","").ToLower()

Write-Host "Password hash: $password_hash"

# 2. Get token
$authBody = @{
    username = $USERNAME
    password_hash = $password_hash
} | ConvertTo-Json

$authResponse = Invoke-RestMethod -Uri "$BASE_URL/auth/token" `
    -Method POST `
    -ContentType "application/json" `
    -Body $authBody

$token = $authResponse.token
Write-Host "Token obtained: $($token.Substring(0,20))..."

# 3. Check deception
$checkBody = @{
    text = "Climate change is a hoax created by scientists."
    modelName = "bert-climate-change-1"
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "$BASE_URL/public/checkDeception" `
    -Method POST `
    -Headers @{Authorization="Bearer $token"} `
    -ContentType "application/json" `
    -Body $checkBody

# 4. Display results
Write-Host "`n$('='*50)"
Write-Host "Deceptive: $($result.is_deceptive)"
Write-Host "Confidence: $([math]::Round($result.confidence * 100, 2))%"
Write-Host "`nTop 5 SHAP explanations:"
$result.shap_words[0..4] | ForEach-Object {
    $word, $score = $_
    $direction = if ($score -gt 0) { "→ deceptive" } else { "→ truthful" }
    Write-Host "  $($word.PadRight(15)) $([math]::Round($score, 3).ToString('+0.000;-0.000')) $direction"
}
Write-Host $('='*50)
```

---

## ⚙️ Rate Limits

Rate limits are enforced per IP address:

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/auth/token` | 10 requests | 60 seconds |
| `/api/public/checkDeception` | 20 requests | 60 seconds |
| `/api/predict` | 20 requests | 60 seconds |
| `/api/training/*` | 5 requests | 60 seconds |
| Other endpoints | 60 requests | 60 seconds |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 20
X-RateLimit-Remaining: 19
X-RateLimit-Reset: 1673524800
```

**Rate Limit Exceeded (429):**
```json
{
  "error": "Rate limit exceeded. Try again in 45 seconds."
}
```

---

## ❌ Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input parameters |
| 401 | Unauthorized - Invalid or expired token |
| 404 | Not Found - Endpoint or resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server-side issue |

### Common Errors

**Invalid Token:**
```json
{
  "error": "Invalid or expired token"
}
```

**Missing Text:**
```json
{
  "error": "Text is required"
}
```

**Text Too Long:**
```json
{
  "error": "Text contains 650 tokens, but model limit is 512. Please reduce text length."
}
```

**Invalid Model:**
```json
{
  "error": "Invalid model. Available models: bert-combined-1, bert-covid-1, ..."
}
```

**Rate Limit:**
```json
{
  "error": "Rate limit exceeded"
}
```

---

## 🔧 Production Setup

### Backend Configuration

**1. Generate Secure Credentials:**
```bash
python generate_secrets.py
```

**2. Set Environment Variables:**

Create `backend/.env` file:
```env
# API Authentication
API_USERNAME=externalapiuser
API_PASSWORD=your_secure_generated_password

# JWT Configuration  
JWT_SECRET=your_secure_jwt_secret_min_32_chars
JWT_ALGORITHM=HS256
JWT_EXP_SECONDS=3600

# Flask Configuration
FLASK_ENV=production
DEBUG_MODE=False

# CORS Origins (comma-separated for production)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**3. Start with Docker:**
```bash
docker-compose up -d
```

### Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use strong passwords** (minimum 20 characters)
3. **Rotate JWT secrets** regularly (every 90 days)
4. **Use HTTPS** in production (configure SSL in nginx)
5. **Update ALLOWED_ORIGINS** to your actual domain
6. **Monitor rate limits** and adjust as needed
7. **Keep dependencies updated** for security patches

### Docker Deployment

**Build and run:**
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Check status
docker-compose ps
```

**GPU Support:**
Ensure NVIDIA Container Toolkit is installed for GPU acceleration.

---

## 📊 Response Times

Typical response times on GPU (RTX 4060):
- Token generation: < 100ms
- Simple prediction: 200-500ms
- Prediction with LIME/SHAP: 1-3 seconds

On CPU:
- Token generation: < 100ms
- Simple prediction: 1-2 seconds
- Prediction with LIME/SHAP: 5-10 seconds

---

## 🆘 Support

For issues, questions, or feature requests:
- Check [API_SETUP.md](API_SETUP.md) for setup instructions
- Review [PRODUCTION_SECURITY.md](PRODUCTION_SECURITY.md) for security guidelines
- See [KORISNICKI_PRIRUCNIK.md](KORISNICKI_PRIRUCNIK.md) for user guide

---

**Last Updated:** January 10, 2026
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
