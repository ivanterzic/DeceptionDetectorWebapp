# Deception Detector

Full-stack web application for detecting deception in text using AI. Features pre-trained transformer models (BERT, DeBERTa) for COVID-19 and climate change datasets, plus custom model fine-tuning capabilities with explainable AI (LIME/SHAP).

**Tech Stack:** Vue.js frontend, Flask backend, PyTorch, Hugging Face Transformers

## Features

- **Text Analysis**: Detect deception in text with confidence scores
- **Multiple Models**: Choose from pre-trained BERT/DeBERTa models
- **Custom Training**: Fine-tune models on your own CSV data (text + label columns)
- **Explainable AI**: LIME and SHAP visualizations showing word importance
- **Real-time Progress**: Live tracking for model training and downloads
- **Auto-cleanup**: Models expire after 7 days, downloads after 24 hours

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- 4GB+ RAM (8GB recommended for training)
- Optional: CUDA-compatible GPU for faster training

### Quick Start

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

### What the Scripts Do

- **setup.bat**: Installs Python dependencies, Node.js dependencies, and downloads all pre-trained models
- **start-backend.bat**: Activates Python environment and starts Flask API server
- **start-frontend.bat**: Starts Vue.js development server with hot-reload
- **download_models.py**: Downloads pre-trained BERT/DeBERTa models from Hugging Face to `backend/models/`

### Usage

1. **Analyze Text** (Pre-trained Models):
   - Go to "Text Analysis" tab
   - Enter text (max 1300 words)
   - Select model (e.g., BERT COVID-19, DeBERTa Climate Change)
   - Click "Analyze Text"
   - View prediction, confidence score, and LIME/SHAP explanations

2. **Train Custom Model**:
   - Prepare CSV with `text` and `label` columns (0=deceptive, 1=truthful)
   - Go to "Model Training" tab
   - Upload CSV, configure settings (epochs, batch size, learning rate)
   - Click "Start Training" and save your 6-digit code
   - Training runs in background (5-30 minutes depending on data size)

3. **Use Custom Model**:
   - Go to "Custom Model" tab
   - Enter your 6-digit code
   - Analyze text or download model archive

## Project Structure

```
webapp/
├── backend/
│   ├── app.py              # Flask API server
│   ├── routes.py           # Pre-trained model endpoints
│   ├── training_routes.py  # Custom training endpoints
│   ├── ai_utils.py         # Model inference logic
│   ├── model_trainer.py    # Training logic with progress tracking
│   ├── explanations.py     # LIME/SHAP generators
│   ├── gpu_utils.py        # GPU device management
│   ├── config.py           # App configuration
│   ├── models/             # Downloaded pre-trained models
│   └── custom_models/      # User-trained models
├── frontend/
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Main views (Analysis, Training, Custom)
│   │   ├── App.vue         # Root component
│   │   └── config.js       # API endpoint configuration
│   └── public/
├── setup.bat               # Windows setup script
├── start-backend.bat       # Backend startup
├── start-frontend.bat      # Frontend startup
├── download_models.py      # Model download script
└── models.txt              # List of Hugging Face models to download
```

## Deployment (Ubuntu)

```bash
# Install
sudo apt update && apt install python3-pip python3-venv nginx nodejs npm -y

# Setup
cd /var/www && git clone repo deception-detector && cd deception-detector
cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cd .. && python3 download_models.py
cd frontend && npm install && npm run build
```

**Systemd** (`/etc/systemd/system/deception-detector.service`):
```ini
[Unit]
Description=Deception Detector
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/deception-detector/backend
Environment="PATH=/var/www/deception-detector/backend/venv/bin"
ExecStart=/var/www/deception-detector/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Nginx** (`/etc/nginx/sites-available/deception-detector`):
```nginx
server {
    listen 80;
    server_name your-domain.com;
    client_max_body_size 100M;

    location / {
        root /var/www/deception-detector/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_set_header Host $host;
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
    }
}
```

**Enable:**
```bash
sudo systemctl enable deception-detector && sudo systemctl start deception-detector
sudo ln -s /etc/nginx/sites-available/deception-detector /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
```

## API

| Endpoint | Method |
|----------|--------|
| `/api/models` | GET |
| `/api/predict` | POST |
| `/api/lime` | POST |
| `/api/shap` | POST |
| `/api/training/start` | POST |
| `/api/training/status/<code>` | GET |
| `/api/custom/predict/<code>` | POST |
| `/api/custom/download/<code>` | GET |

## Config

**Backend** `.env`:
```
API_PORT=5000
MODEL_EXPIRY_DAYS=7
ZIP_EXPIRY_HOURS=24
```

**Frontend** `src/config.js`:
```javascript
export default { apiBaseUrl: 'http://your-server:5000/api' }
```

## Troubleshooting

- Backend won't start: `pip install -r requirements.txt`
- Models not found: `python download_models.py`
- Training fails: Check CSV has `text` and `label` columns (0/1)