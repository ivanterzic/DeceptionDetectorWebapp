# API Credentials Setup

## ⚠️ REQUIRED for Public API

The public API requires environment variables to be set. Credentials are NOT stored in code for security.

## Quick Setup

### Step 1: Generate Credentials
```bash
python generate_secrets.py
```

Follow the prompts to either:
- Enter your own password (recommended for production)
- Generate a random password (good for testing)

### Step 2: Copy the Output

The script will output environment variable commands like:

**Windows (PowerShell):**
```powershell
$env:API_USERNAME="externalapiuser"
$env:API_PASSWORD_HASH="db3d51ecf1d848e50f02d66492608f0398bcf24f00096b8e0fd6476377034989"
$env:JWT_SECRET="<random_secret>"
$env:JWT_EXP_SECONDS="3600"
```

**Linux/Mac:**
```bash
export API_USERNAME="externalapiuser"
export API_PASSWORD_HASH="db3d51ecf1d848e50f02d66492608f0398bcf24f00096b8e0fd6476377034989"
export JWT_SECRET="<random_secret>"
export JWT_EXP_SECONDS="3600"
```

### Step 3: Set Environment Variables

Run the commands from Step 2 in your terminal.

### Step 4: Start Backend
```bash
.\start-backend.bat
```

## Verify Setup

The backend will show a warning if credentials are not configured:
```
⚠️  API_USERNAME and API_PASSWORD_HASH environment variables not set!
   Public API will not work. Run: python generate_secrets.py
```

If you see this warning, repeat Steps 2-4.

## Using the API

Once configured, see `API_USAGE.md` for:
- Complete API documentation
- Testing instructions (cURL, Python, etc.)
- Example code
