# 🕵️ Deception Detector

AI-powered web application for detecting deception in text using state-of-the-art transformer models. Analyze text with pre-trained models or fine-tune your own on custom datasets with full explainability.

**Tech Stack:** Vue.js • Flask • PyTorch • Hugging Face Transformers

---

## ✨ Features

### 🌐 Public API
- **JWT Authentication**: Secure username/password authentication with client-side SHA256 hashing
- **Programmatic Access**: Integrate deception detection into your applications
- **Single Endpoint**: `checkDeception(text, modelName)` returns prediction + SHAP + LIME explanations
- **Rate Limited**: 20 requests/minute for reliable service
- **Secure by Design**: No credentials stored in code - environment variables required
- **Complete Guide**: See `API_USAGE.md` for full documentation

### 🔍 Text Analysis
- **Deception Detection**: Analyze text to determine if it's deceptive or truthful
- **Confidence Scores**: Get probability scores for each prediction
- **Multiple Models**: Choose from BERT and DeBERTa models trained on COVID-19 and climate change datasets
- **Batch Processing**: Analyze multiple texts efficiently

### 🎓 Custom Model Training
- **Fine-tuning**: Train models on your own labeled datasets (CSV format)
- **Multiple Base Models**: Choose from BERT, DeBERTa, RoBERTa, ALBERT, or DistilBERT
- **Configurable Training**: Adjust epochs, batch size, learning rate, and validation split
- **6-Digit Model Codes**: Easy access to your trained models
- **Background Training**: Models train asynchronously while you work
- **Progress Tracking**: Real-time updates on training status

### 🧠 Explainable AI
- **LIME Explanations**: See which words influenced the prediction most
- **SHAP Values**: Understand feature importance with Shaply values
- **Dual Explanations**: Compare LIME and SHAP side-by-side
- **Visual Text Coloring**: Original text displayed with color-coded words
  - **Green words**: Indicate truthfulness (positive contribution)
  - **Red words**: Indicate deception (negative contribution)
  - **Color intensity**: Reflects strength of contribution
- **Flexible Display**: Choose how many top words to show (1, 3, 5, 10, 20, or all)

### 📦 Model Management
- **Download Models**: Export trained models as ZIP archives
- **Real-time Progress**: Live tracking for model downloads with file-by-file progress
- **Auto-cleanup**: Custom models expire after 7 days, downloads after 24 hours
- **Model Codes**: Simple 6-digit codes for easy model access

### ⚡ Performance
- **GPU Support**: Automatic GPU detection and usage for faster training/inference
- **CPU Fallback**: Works without GPU (slower but functional)
- **Memory Optimization**: Efficient memory management for large models
- **Caching**: Base models cached locally to speed up training

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| Python | 3.8+ | 3.9+ |
| Node.js | 14+ | 16+ |
| RAM | 4GB | 8GB+ |
| Storage | 10GB | 20GB+ |
| GPU | - | CUDA 11.7+ |

### Installation

### Quick Start

**Windows:**
```bash
# 1. Complete setup (first time only)
setup.bat

# 2. Start the application
start-backend.bat  # Terminal 1 - Starts Flask API on port 5000
start-frontend.bat # Terminal 2 - Starts Vue dev server on port 8080

# 3. Open browser
# Navigate to http://localhost:8080
```

**Linux/Mac:**
```bash
# 1. Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Download models (first time only - takes 5-15 minutes)
cd ..
python3 download_models.py

# 3. Start backend
python backend/app.py  # Runs on http://localhost:5000

# 4. Frontend setup (new terminal)
cd frontend
npm install
npm run serve  # Runs on http://localhost:8080
```

### Installation

#### Windows (Recommended)

```bash
# One-command setup - installs everything and downloads models
setup.bat

# Start the application (2 terminals)
start-backend.bat   # Terminal 1: Flask API (port 5000)
start-frontend.bat  # Terminal 2: Vue.js app (port 8080)
```

Then open http://localhost:8080 in your browser.

#### Linux/Mac

```bash
# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download pre-trained models (5-15 minutes)
cd ..
python3 download_models.py

# Start backend (Terminal 1)
python backend/app.py

# Frontend setup (Terminal 2)
cd frontend
npm install
npm run serve
```

Then open http://localhost:8080 in your browser.

#### Public API Setup (Optional)

To enable the public API, you must configure credentials via environment variables:

```bash
# Generate secure credentials
python generate_secrets.py

# Follow the prompts to set environment variables
# Then restart the backend
```

**⚠️ Important:** API credentials are NOT stored in code for security. See `API_USAGE.md` for details.

---

## 📖 How to Use

### 1️⃣ Analyze Text with Pre-trained Models

1. Click the **"Analysis"** tab
2. Enter or paste your text (up to 1300 words)
3. Select a model from the dropdown:
   - BERT COVID-19
   - BERT Climate Change
   - BERT Combined
   - DeBERTa COVID-19
   - DeBERTa Climate Change
   - DeBERTa Combined
4. Click **"Analyze Text"**
5. View results:
   - **Prediction**: Deceptive or Truthful
   - **Confidence**: Probability score
   - **Visual Explanation**: Color-coded text showing word contributions
     - Green words = support truthfulness
     - Red words = support deception
     - Stronger color = higher importance
   - **LIME Tab**: Word-level importance with ranked list
   - **SHAP Tab**: Feature impact visualization with ranked list
   - **Word Count Selector**: Choose how many top words to display (1, 3, 5, 10, 20, all)

### 2️⃣ Train Your Own Model

1. **Prepare your data**:
   - Create a CSV file with two columns: `text` and `label`
   - Labels: `0` = deceptive, `1` = truthful
   - Minimum 100 rows recommended

2. Click the **"Fine-tuning"** tab

3. **Upload CSV** and review validation:
   - Total rows
   - Label distribution
   - Sample preview

4. **Configure training**:
   - **Base Model**: BERT, DeBERTa, RoBERTa, ALBERT, or DistilBERT
   - **Model Name**: Give it a memorable name
   - **Epochs**: 2-5 (more = better but slower)
   - **Batch Size**: 8-16 (lower if GPU memory limited)
   - **Learning Rate**: 2e-5 (default works well)
   - **Validation Split**: 0.2 (20% for validation)

5. Click **"Start Training"**

6. **Save your 6-digit code** (e.g., `abc123`)

7. Monitor progress:
   - Training phase
   - Current epoch
   - Validation metrics
   - Estimated time remaining

8. Training typically takes 5-30 minutes depending on:
   - Dataset size
   - Base model choice
   - Hardware (GPU vs CPU)
   - Number of epochs

### 3️⃣ Use Your Custom Model

1. Click the **"Model Access"** tab

2. Enter your **6-digit model code**

3. Click **"Access Model"**

4. View model details:
   - Model name
   - Base model used
   - Creation date
   - Expiration date (7 days from creation)

5. **Analyze text** with your model:
   - Enter text
   - Click "Analyze Text"
   - View predictions and explanations

6. **Download model** (optional):
   - Click "Download Model"
   - Watch real-time progress (file-by-file)
   - Archive includes model weights, config, tokenizer
   - Download expires after 24 hours

---

## 🗂️ Project Structure

## 🗂️ Project Structure

```
webapp/
├── backend/                    # Flask API server
│   ├── app.py                 # Main application entry
│   ├── routes.py              # Pre-trained model API routes
│   ├── training_routes.py     # Custom training API routes
│   ├── ai_utils.py            # Model inference engine
│   ├── model_trainer.py       # Training orchestration
│   ├── explanations.py        # LIME/SHAP generators
│   ├── gpu_utils.py           # GPU management utilities
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── models/                # Pre-trained models storage
│   ├── base_models/           # Cached base models for training
│   └── custom_models/         # User-trained models (auto-expire)
│
├── frontend/                   # Vue.js application
│   ├── src/
│   │   ├── components/        # Reusable Vue components
│   │   │   ├── AnalysisResults.vue
│   │   │   ├── InputForm.vue
│   │   │   ├── LimeExplanation.vue
│   │   │   ├── ShapExplanation.vue
│   │   │   └── LoadingScreen.vue
│   │   ├── views/             # Main application views
│   │   │   ├── AnalysisView.vue    # Pre-trained analysis
│   │   │   ├── TrainingView.vue    # Model fine-tuning
│   │   │   └── CustomModelView.vue # Custom model access
│   │   ├── App.vue            # Root component
│   │   ├── main.js            # Vue app initialization
│   │   └── config.js          # API configuration
│   ├── public/
│   │   ├── index.html         # HTML template
│   │   └── images/
│   │       ├── ddetection/    # App logos (light/dark) and favicons
│   │       └── ngeu/          # NextGenerationEU visibility logos (footer)
│   └── package.json           # Node.js dependencies
│
├── setup.bat                  # Windows one-click setup
├── start-backend.bat          # Backend launcher
├── start-frontend.bat         # Frontend launcher
├── download_models.py         # Model download script
├── models.txt                 # List of models to download
└── README.md                  # This file
```

---

## ⚙️ Configuration

### Backend Settings

Create a `.env` file in the `backend/` directory:

```bash
# Server Configuration
API_HOST=0.0.0.0
API_PORT=5000
FLASK_ENV=development

# Model Management
MODEL_EXPIRY_DAYS=7          # Custom models auto-delete after 7 days
ZIP_EXPIRY_HOURS=24          # Downloaded archives expire after 24 hours
MAX_SEQUENCE_LENGTH=512      # Maximum token length for models

# GPU (optional)
CUDA_VISIBLE_DEVICES=0       # Specify GPU device
```

### Frontend Settings

Edit `frontend/src/config.js`:

```javascript
export default {
  apiBaseUrl: 'http://localhost:5000/api'  // Backend API URL
}
```

---

## 🛠️ Troubleshooting

### Backend Issues

**Backend won't start**
```bash
# Check Python version
python --version  # Need 3.8+

# Reinstall dependencies
cd backend
pip install --upgrade -r requirements.txt
```

**Models not found**
```bash
# Download models manually
python download_models.py

# Verify models directory
ls backend/models/  # Should show model folders
```

**GPU not detected**
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Check GPU memory
nvidia-smi
```

### Frontend Issues

**Connection errors**
- Verify backend is running on port 5000
- Check `frontend/src/config.js` has correct API URL
- Ensure CORS is enabled in `backend/app.py`

**Build failures**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Training Issues

**Training fails immediately**
- Ensure CSV has `text` and `label` columns
- Labels must be 0 (deceptive) or 1 (truthful)
- Check for missing values in your data
- Verify sufficient disk space (5GB+ free)

**Out of memory errors**
- Reduce batch size (try 4 or 8)
- Use a smaller base model (DistilBERT)
- Close other applications using GPU
- Switch to CPU mode (slower but works)

**Training very slow**
- Enable GPU if available
- Reduce number of epochs
- Use a smaller dataset for testing
- Try DistilBERT instead of BERT/DeBERTa

---

## 🔌 API Reference

### 🌐 Public API (JWT Protected)

**Full documentation:** See `API_USAGE.md`

#### Authentication
```bash
POST /api/auth/token
Body: {"username": "externalapiuser", "password_hash": "<sha256_hash>"}
Response: {"token": "...", "expires_in": 3600}

Note: Password must be hashed with SHA256 client-side before sending
```

#### Check Deception
```bash
POST /api/public/checkDeception
Headers: Authorization: Bearer <token>
Body: {"text": "...", "modelName": "bert-combined-1"}
```

**Response:**
```json
{
  "is_deceptive": true,
  "confidence": 0.95,
  "shap_words": [["word1", 0.5], ["word2", -0.3]],
  "lime_words": [["word1", 0.6], ["word2", -0.2]],
  "model_used": "bert-combined-1"
}
```

**Test the API:** See `API_USAGE.md` for testing instructions

**Python Example:**
```python
import requests
import hashlib

# Hash password (SHA256)
password_hash = hashlib.sha256("your_password".encode()).hexdigest()

# Get token
auth = requests.post("http://localhost:5000/api/auth/token",
    json={"username": "externalapiuser", "password_hash": password_hash})
token = auth.json()["token"]

# Check deception
response = requests.post("http://localhost:5000/api/public/checkDeception",
    headers={"Authorization": f"Bearer {token}"},
    json={"text": "Your text", "modelName": "bert-combined-1"})
print(response.json())
```

### Pre-trained Models (Internal Web App)

**GET** `/api/models` - List available models

**POST** `/api/predict` - Analyze text
```json
{
  "text": "Your text here",
  "model": "bert-covid-1"
}
```

**POST** `/api/explain/lime` - Get LIME explanation

**POST** `/api/explain/shap` - Get SHAP explanation

### Custom Training

**GET** `/api/training/models` - List base models for fine-tuning

**POST** `/api/training/upload-csv` - Validate training data

**POST** `/api/training/start` - Start model training

**GET** `/api/training/status/<code>` - Check training progress

**POST** `/api/training/cleanup` - Manually cleanup expired models

### Custom Models

**POST** `/api/custom/predict/<code>` - Predict with custom model

**POST** `/api/custom/download/init/<code>` - Initialize download

**GET** `/api/custom/download/<code>` - Download model archive

**GET** `/api/custom/download-progress/<id>` - Track download progress

---

## � Production Deployment

### For Traditional Servers (VPS, Dedicated, Cloud VM)

We provide complete automated deployment for Linux servers with terminal access:

#### Quick Deploy (Recommended)

```bash
# On your local machine
cd webapp

# Upload to server
scp -r . user@your-server:/tmp/webapp/

# SSH to server and run deployment
ssh user@your-server
cd /tmp/webapp/deployment
chmod +x deploy.sh
sudo ./deploy.sh
```

**The script automatically:**
- ✅ Installs dependencies (Python, Node.js, Nginx, SSL)
- ✅ Sets up systemd services for auto-start
- ✅ Configures Nginx reverse proxy
- ✅ Obtains SSL certificate (Let's Encrypt)
- ✅ Sets up firewall rules
- ✅ Downloads AI models (optional)

**Time:** 15-45 minutes depending on model download

#### What You Need

- Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- 4GB+ RAM (8GB+ recommended)
- 20GB+ storage
- Root/sudo access
- Domain name with DNS configured (optional but recommended)

#### Complete Documentation

- **[deployment/DEPLOYMENT_GUIDE.md](deployment/DEPLOYMENT_GUIDE.md)** - Full step-by-step guide
- **[deployment/QUICK_REFERENCE.md](deployment/QUICK_REFERENCE.md)** - Essential commands & troubleshooting
- **[docs/PRODUCTION_SECURITY.md](docs/PRODUCTION_SECURITY.md)** - Security checklist
- **[deployment/README.md](deployment/README.md)** - Deployment files overview

#### Architecture

```
Internet → Nginx (:443 HTTPS) → Frontend (:8080) or Backend (:5000)
                                      ↓                    ↓
                                 Express serves       Flask API with
                                 built Vue.js         Gunicorn WSGI
```

#### After Deployment

The application will be available at `https://yourdomain.com`

**Essential commands:**
```bash
# Restart services
sudo systemctl restart deception-detector-backend
sudo systemctl restart deception-detector-frontend

# View logs
sudo journalctl -u deception-detector-backend -f

# Health check
sudo /opt/deception-detector/deployment/health-check.sh

# Update application
sudo /opt/deception-detector/deployment/update.sh
```

For detailed instructions and troubleshooting, see the deployment documentation above.

---

## �📝 Data Format

### Training CSV Format

```csv
text,label
"This is a truthful statement about climate.",1
"This is a deceptive claim about vaccines.",0
"Another truthful text example here.",1
```

**Requirements:**
- Two columns: `text` and `label`
- Labels: `0` = deceptive, `1` = truthful
- Minimum 100 rows recommended
- No missing values
- UTF-8 encoding

---

## 🎨 Color Scheme

- **Primary Red**: `#FE483E` - Buttons, accents, active states
- **Dark Navy**: `#213544` - Text, headings, navbar
- **Light Background**: `#f8f9fa` - Page background

---