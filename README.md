# Deception Detector Web Application# Deception Detector Web Application# Deception Detector App



> A full-stack AI-powered web application for detecting deception in text using transformer models, featuring both pre-trained models and custom fine-tuning capabilities.



---A full-stack web application for detecting deception in text using AI models, featuring both pre-trained models and custom fine-tuning capabilities.A Vue.js frontend with Flask backend for detecting deception in text using pre-trained Hugging Face models.



## 📋 Table of Contents



- [Features](#-features)## 🌟 Features## Features

- [Project Structure](#-project-structure)

- [Quick Start](#-quick-start)

- [Installation](#-installation)

- [Deployment](#-deployment)### Analysis Features- **Deception Detection**: Get predictions on whether text is deceptive or truthful

  - [Ubuntu/Linux](#ubuntulinux-deployment)

  - [DigitalOcean](#digitalocean-deployment)- **Multi-Model Detection**: Choose from multiple pre-trained BERT and DeBERTa models- **Explainable AI**: 

  - [Windows Server](#windows-server-deployment)

- [Configuration](#-configuration)- **Custom Model Training**: Fine-tune your own models on custom datasets  - LIME explanations showing word-level feature importance

- [API Documentation](#-api-documentation)

- [Usage](#-usage)- **Explainable AI**:   - SHAP explanations for model interpretability

- [Maintenance](#-maintenance)

- [Troubleshooting](#-troubleshooting)  - LIME explanations showing word-level feature importance



---  - SHAP explanations for model interpretability## Project Structure



## 🌟 Features- **Real-time Progress**: Live progress tracking for custom model downloads



### 🔍 Analysis Capabilities```



- **Multi-Model Detection** - Choose from multiple pre-trained BERT and DeBERTa models### Custom Model Featureswebapp/

- **Custom Model Training** - Fine-tune your own models on custom datasets

- **Explainable AI**- **Fine-tuning**: Train models on your own labeled data (CSV format)├── backend/

  - LIME explanations showing word-level feature importance

  - SHAP explanations for model interpretability- **Multiple Base Models**: Choose from BERT, DeBERTa, RoBERTa, ALBERT, or DistilBERT│   ├── app.py              # Flask API server

- **Real-time Progress** - Live progress tracking with percentage and phase updates

- **Model Management**: │   ├── requirements.txt    # Python dependencies

### 🎓 Custom Model Training

  - Models auto-expire after 7 days│   └── models/             # Local model storage

- **Fine-tuning** - Train models on your own labeled data (CSV format)

- **Multiple Base Models** - Choose from:  - Model archives auto-delete after 24 hours├── frontend/

  - `bert-base-uncased` - General-purpose BERT

  - `microsoft/deberta-v3-base` - Enhanced BERT with better performance  - 6-digit model codes for easy access│   ├── src/

  - `roberta-base` - Robustly optimized BERT

  - `albert-base-v2` - Lightweight alternative- **Training Configuration**: Customizable epochs, batch size, learning rate, and validation split|   |   ├── components/       # Vue components

  - `distilbert-base-uncased` - Smaller, faster model

- **Model Management**│   │   ├── public/        # Static assets (images, styles)

  - ⏱️ Models auto-expire after 7 days

  - 🗑️ Model archives auto-delete after 24 hours## 📁 Project Structure│   │   ├── views/         # Application views

  - 🔢 6-digit model codes for easy access

- **Training Configuration** - Customizable:│   │   ├── App.vue        # Main Vue component

  - Epochs

  - Batch size```│   │   └── main.js        # Vue app entry point

  - Learning rate

  - Validation splitwebapp/│   ├── public/



---├── backend/│   │   └── index.html     # HTML template



## 📁 Project Structure│   ├── app.py                    # Flask API server│   ├── package.json       # Node.js dependencies



```│   ├── routes.py                 # Pre-trained model routes│   └── vue.config.js      # Vue CLI configuration

webapp/

├── backend/│   ├── training_routes.py        # Custom training routes├── models.txt             # Available Hugging Face models

│   ├── app.py                    # Flask API server

│   ├── routes.py                 # Pre-trained model routes│   ├── ai_utils.py              # Model loading and inference├── setup.bat              # Complete setup script

│   ├── training_routes.py        # Custom training routes

│   ├── ai_utils.py              # Model loading and inference│   ├── model_trainer.py          # Custom model training logic├── download-models.bat    # Model download script (Windows)

│   ├── model_trainer.py          # Custom model training logic

│   ├── model_utils.py            # Model utility functions│   ├── model_utils.py            # Model utility functions├── download_models.py     # Model download script (Cross-platform)

│   ├── explanations.py           # LIME/SHAP explanation generators

│   ├── config.py                 # Application configuration│   ├── explanations.py           # LIME/SHAP explanation generators├── start-backend.bat      # Backend startup script

│   ├── gpu_utils.py              # GPU device management

│   ├── base_model_cache.py       # Base model caching system│   ├── config.py                 # Application configuration└── start-frontend.bat     # Frontend startup script

│   ├── requirements.txt          # Python dependencies

│   ├── models/                   # Pre-trained models storage│   ├── gpu_utils.py              # GPU device management```

│   ├── base_models/              # Cached base models for training

│   └── custom_models/            # User-trained models storage│   ├── base_model_cache.py       # Base model caching system

│

├── frontend/│   ├── requirements.txt          # Python dependencies## Setup Instructions

│   ├── src/

│   │   ├── components/           # Reusable Vue components│   ├── models/                   # Pre-trained models storage

│   │   ├── views/                # Main application views

│   │   ├── App.vue               # Main Vue component│   ├── base_models/              # Cached base models for training### Quick Setup (Recommended)

│   │   ├── main.js               # Vue app entry point

│   │   └── config.js             # Frontend configuration│   └── custom_models/            # User-trained models storage

│   ├── public/                   # Static assets

│   ├── package.json              # Node.js dependencies├── frontend/Run the complete setup script that handles everything:

│   └── vue.config.js             # Vue CLI configuration

││   ├── src/```bash

├── models.txt                    # Available pre-trained models list

├── setup.bat                     # Windows setup script│   │   ├── components/           # Reusable Vue componentssetup.bat

├── download-models.bat           # Model download (Windows)

├── download_models.py            # Model download (Cross-platform)│   │   ├── views/                # Main application views```

├── start-backend.bat             # Backend startup (Windows)

└── start-frontend.bat            # Frontend startup (Windows)│   │   ├── App.vue               # Main Vue component

```

│   │   ├── main.js               # Vue app entry pointThis will:

---

│   │   └── config.js             # Frontend configuration1. Set up the Python backend environment

## 🚀 Quick Start

│   ├── public/                   # Static assets2. Install frontend dependencies

### Prerequisites

│   ├── package.json              # Node.js dependencies3. Download all required Hugging Face models

| Requirement | Minimum | Recommended |

|------------|---------|-------------|│   └── vue.config.js             # Vue CLI configuration4. Prepare the application for first run

| Python | 3.8+ | 3.9+ |

| Node.js | 14+ | 16+ |├── models.txt                    # Available pre-trained models list

| RAM | 4GB | 8GB+ |

| Storage | 10GB | 20GB+ |├── setup.bat                     # Windows setup script### Manual Setup

| GPU | - | CUDA-compatible |

├── download-models.bat           # Model download (Windows)

### Windows Quick Setup

├── download_models.py            # Model download (Cross-platform)#### Model Download (First Time Only)

**1. Complete Setup** (first time only):

├── start-backend.bat             # Backend startup (Windows)

```bash

setup.bat└── start-frontend.bat            # Frontend startup (Windows)Before running the application for the first time, download the required models:

```

``````bash

This will:

- ✅ Install Python dependencies# Option 1: Using batch script (Windows)

- ✅ Install Node.js dependencies

- ✅ Download all required models## 🚀 Quick Startdownload-models.bat

- ✅ Prepare the application



**2. Start Application**:

### Prerequisites# Option 2: Using Python script (Cross-platform)

```bash

# Terminal 1 - Backend- Python 3.8+ (3.9 recommended)python download_models.py

start-backend.bat

- Node.js 14+ and npm```

# Terminal 2 - Frontend

start-frontend.bat- 4GB+ RAM (8GB+ recommended for training)

```

- GPU recommended but not required**Note**: This step downloads model data based on the models listed in `models.txt` and saves it locally in `backend/models/`. Models are stored locally for faster access and offline usage. The download may take 5-15 minutes depending on your internet connection and the number of models.

**3. Open Browser**:



Navigate to `http://localhost:8080`

### Windows Quick Setup#### Backend Setup

---



## 📦 Installation

1. **Complete Setup** (first time):1. Navigate to the backend directory:

### Backend Setup

   ```bash   ```bash

#### 1. Create Virtual Environment

   setup.bat   cd backend

```bash

cd backend   ```   ```

python -m venv venv

   This downloads models, installs dependencies, and prepares everything.

# Windows

venv\Scripts\activate2. Create a virtual environment (recommended):



# Linux/Mac2. **Start Application**:   ```bash

source venv/bin/activate

```   ```bash   python -m venv venv



#### 2. Install Dependencies   # Terminal 1 - Backend   venv\Scripts\activate  # On Windows



```bash   start-backend.bat   ```

pip install -r requirements.txt

```   



#### 3. Download Pre-trained Models   # Terminal 2 - Frontend3. Install Python dependencies:



```bash   start-frontend.bat   ```bash

cd ..

python download_models.py   ```   pip install -r requirements.txt

```

   ```

> ⏱️ **Note**: First-time model download may take 5-15 minutes depending on your internet connection.

3. Open `http://localhost:8080` in your browser

### Frontend Setup

4. Run the Flask server:

#### 1. Install Dependencies

## 📦 Installation   ```bash

```bash

cd frontend   python app.py

npm install

```### Backend Setup   ```



#### 2. Configure API URL (Optional)



Edit `frontend/src/config.js` for custom deployment:1. **Create Virtual Environment**:The backend will be available at `http://localhost:5000`



```javascript   ```bash

export default {

  apiBaseUrl: 'http://your-server:5000/api'   cd backend### Frontend Setup

}

```   python -m venv venv



#### 3. Start Development Server   1. Navigate to the frontend directory:



```bash   # Windows   ```bash

npm run serve

```   venv\Scripts\activate   cd frontend



Frontend will be available at `http://localhost:8080`      ```



---   # Linux/Mac



## 🌐 Deployment   source venv/bin/activate2. Install Node.js dependencies:



### Ubuntu/Linux Deployment   ```   ```bash



#### Step 1: System Prerequisites   npm install



```bash2. **Install Dependencies**:   ```

# Update system

sudo apt update && sudo apt upgrade -y   ```bash



# Install Python and Node.js   pip install -r requirements.txt3. Start the development server:

sudo apt install python3-pip python3-venv nginx -y

curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -   ```   ```bash

sudo apt install nodejs -y

```   npm run serve



#### Step 2: Clone and Setup3. **Download Pre-trained Models** (first time):   ```



```bash   ```bash

cd /var/www

sudo git clone your-repo deception-detector   cd ..The frontend will be available at `http://localhost:8080`

cd deception-detector

   python download_models.py

# Backend setup

cd backend   ```## Quick Start

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

### Frontend SetupFor first-time users, simply run:

# Download models

cd ..```bash

python3 download_models.py

1. **Install Dependencies**:setup.bat

# Frontend setup

cd frontend   ```bash```

npm install

npm run build   cd frontend

```

   npm installThen start the application:

#### Step 3: Create systemd Service

   ``````bash

Create `/etc/systemd/system/deception-detector-backend.service`:

# Terminal 1

```ini

[Unit]2. **Configure API URL** (optional):start-backend.bat

Description=Deception Detector Backend API

After=network.target   Edit `frontend/src/config.js` if deploying to a different host:



[Service]   ```javascript# Terminal 2  

Type=simple

User=www-data   export default {start-frontend.bat

WorkingDirectory=/var/www/deception-detector/backend

Environment="PATH=/var/www/deception-detector/backend/venv/bin"     apiBaseUrl: 'http://your-server:5000/api'```

ExecStart=/var/www/deception-detector/backend/venv/bin/python app.py

Restart=always   }

RestartSec=10

   ```Open `http://localhost:8080` in your browser.

[Install]

WantedBy=multi-user.target

```

## 🌐 Deployment## Available Models

#### Step 4: Configure Nginx



Create `/etc/nginx/sites-available/deception-detector`:

### Ubuntu/Linux DeploymentThe application supports models discovered from `models.txt`. Models are downloaded from Hugging Face and stored locally. Example models include:

```nginx

server {

    listen 80;

    server_name your-domain.com;#### Using systemd Services1. neurips-user/neurips-bert-covid-1



    # Frontend2. neurips-user/neurips-bert-climate-change-1

    location / {

        root /var/www/deception-detector/frontend/dist;1. **Backend Service** (`/etc/systemd/system/deception-detector-backend.service`):3. neurips-user/neurips-bert-combined-1

        try_files $uri $uri/ /index.html;

    }   ```ini



    # Backend API   [Unit]## API Endpoints

    location /api/ {

        proxy_pass http://localhost:5000/api/;   Description=Deception Detector Backend API

        proxy_http_version 1.1;

        proxy_set_header Upgrade $http_upgrade;   After=network.target### GET /api/models

        proxy_set_header Connection 'upgrade';

        proxy_set_header Host $host;Returns available models for selection (dynamically discovered from local storage).

        proxy_cache_bypass $http_upgrade;

        proxy_set_header X-Real-IP $remote_addr;   [Service]

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

           Type=simple### POST /api/predict

        # Increase timeouts for long-running operations

        proxy_connect_timeout 600;   User=www-dataAnalyzes text for deception detection.

        proxy_send_timeout 600;

        proxy_read_timeout 600;   WorkingDirectory=/var/www/deception-detector/backend

    }

   Environment="PATH=/var/www/deception-detector/backend/venv/bin"**Request Body:**

    client_max_body_size 100M;

}   ExecStart=/var/www/deception-detector/backend/venv/bin/python app.py```json

```

   Restart=always{

#### Step 5: Enable Services

   RestartSec=10  "text": "Text to analyze",

```bash

# Enable backend service  "model": "model"

sudo systemctl enable deception-detector-backend

sudo systemctl start deception-detector-backend   [Install]}



# Enable nginx site   WantedBy=multi-user.target```

sudo ln -s /etc/nginx/sites-available/deception-detector /etc/nginx/sites-enabled/

sudo nginx -t   ```

sudo systemctl restart nginx

**Response:**

# Configure firewall

sudo ufw allow 'Nginx Full'2. **Frontend Build**:```json

sudo ufw allow 22

sudo ufw enable   ```bash{

```

   cd frontend  "confidence": 0.85,

#### Step 6: SSL with Let's Encrypt (Optional)

   npm run build  "explanations": {

```bash

sudo apt install certbot python3-certbot-nginx -y   ```    "lime": [["word", 0.123], ...],

sudo certbot --nginx -d your-domain.com

```    "shap": [["word", 0.456], ...],



### DigitalOcean Deployment3. **Nginx Configuration** (`/etc/nginx/sites-available/deception-detector`):  },



#### Droplet Specifications   ```nginx  "model_used": "deberta-climate-change-1",



| Component | Specification |   server {  "original_text": "Text to analyze",

|-----------|--------------|

| OS | Ubuntu 22.04 LTS |       listen 80;  "prediction": "deceptive|truthful"

| RAM | 4GB minimum (8GB recommended) |

| Storage | 80GB+ SSD |       server_name your-domain.com;}

| CPU | 2+ vCPUs |

```

#### Quick Deploy Script

       # Frontend

```bash

#!/bin/bash       location / {## Usage

# Save as deploy-digitalocean.sh

           root /var/www/deception-detector/frontend/dist;

# Install dependencies

sudo apt update && sudo apt upgrade -y           try_files $uri $uri/ /index.html;1. Start both backend and frontend servers

sudo apt install python3-pip python3-venv nginx -y

curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -       }2. Open `http://localhost:8080` in your browser

sudo apt install nodejs -y

3. Enter text you want to analyze

# Clone and setup

cd /var/www       # Backend API4. Select a model from the dropdown (models are automatically discovered)

sudo git clone YOUR_REPO_URL deception-detector

cd deception-detector       location /api/ {5. Click "Analyze Text"



# Backend           proxy_pass http://localhost:5000/api/;6. View results including:

cd backend

python3 -m venv venv           proxy_http_version 1.1;   - Prediction (deceptive/truthful)

source venv/bin/activate

pip install -r requirements.txt           proxy_set_header Upgrade $http_upgrade;   - Confidence score

cd ..

           proxy_set_header Connection 'upgrade';   - LIME and SHAP explanations in separate tabs

# Download models

python3 download_models.py           proxy_set_header Host $host;



# Frontend           proxy_cache_bypass $http_upgrade;## Requirements

cd frontend

npm install           proxy_set_header X-Real-IP $remote_addr;

npm run build

           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;### Backend

echo "✅ Deployment complete! Configure systemd and nginx next."

```           - Python 3.8+



### Windows Server Deployment           # Increase timeouts for long-running operations- PyTorch



#### Prerequisites           proxy_connect_timeout 600;- Transformers



1. Install **IIS** with required modules           proxy_send_timeout 600;- Flask

2. Install **Python 3.9+**

3. Install **Node.js 16+**           proxy_read_timeout 600;- LIME

4. Install **NSSM** (Non-Sucking Service Manager)

       }- SHAP

#### Setup as Windows Service

- NumPy

```powershell

# Install backend as service       client_max_body_size 100M;- scikit-learn

nssm install DeceptionDetectorBackend "C:\path\to\venv\Scripts\python.exe" "C:\path\to\backend\app.py"

nssm set DeceptionDetectorBackend AppDirectory "C:\path\to\backend"   }

nssm start DeceptionDetectorBackend

```   ```### Frontend



#### IIS Configuration- Node.js 14+



1. Create new website in IIS Manager4. **Enable and Start Services**:- Vue.js 3

2. Point to `frontend/dist` folder

3. Install URL Rewrite module   ```bash- Axios

4. Configure reverse proxy to `localhost:5000` for `/api/` paths

   # Enable services- Bootstrap 5

---

   sudo systemctl enable deception-detector-backend

## 🔧 Configuration

   sudo systemctl start deception-detector-backend## Notes

### Environment Variables

   

Create `.env` file in backend directory:

   # Enable nginx- **Local Model Storage**: Models are downloaded and stored in `backend/models/` for faster access and offline usage

```bash

# Flask Configuration   sudo ln -s /etc/nginx/sites-available/deception-detector /etc/nginx/sites-enabled/- **Base Model Caching**: Training base models are cached in `backend/base_models/` to prevent repeated downloads during fine-tuning

FLASK_ENV=production

API_HOST=0.0.0.0   sudo systemctl restart nginx- **Dynamic Model Discovery**: System automatically discovers available models from `models.txt` and existing downloads

API_PORT=5000

   ```- **Model Requirement**: Models must be downloaded before running the application for the first time

# Model Configuration

MODEL_EXPIRY_DAYS=7- **First Run**: The initial setup downloads both pre-trained and base model files to local storage

ZIP_EXPIRY_HOURS=24

MAX_SEQUENCE_LENGTH=512### DigitalOcean Deployment- **Offline Training**: Once base models are cached, training works without internet connection



# GPU Configuration (optional)- **GPU Support**: GPU support is automatically detected and used if available

CUDA_VISIBLE_DEVICES=0

```1. **Create Droplet**:- **Network**: Internet connection only required for initial model downloads



### GPU Configuration   - Ubuntu 22.04 LTS- CORS is enabled for cross-origin requests from the frontend



The application automatically manages GPU resources via `gpu_utils.py`:   - 4GB+ RAM minimum (8GB recommended for training)- The application includes error handling and loading states



| Feature | Description |   - 80GB+ SSD (for models)

|---------|-------------|

| **Multi-GPU Support** | Automatically selects GPU with most free memory |### Base Model Management

| **CPU Fallback** | Works without GPU if CUDA unavailable |

| **Memory Monitoring** | Logs GPU memory usage during operations |2. **Install Dependencies**:

| **Automatic Selection** | No manual configuration needed |

   ```bashThe system includes automated caching for base models used in training:

To check GPU availability:

   # Update system

```bash

python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'Device Count: {torch.cuda.device_count()}')"   sudo apt update && sudo apt upgrade -y```bash

```

   # Check cache status

---

   # Install Python and Node.jspython backend/manage_base_models.py status

## 📊 API Documentation

   sudo apt install python3-pip python3-venv nginx -y

### Pre-trained Models API

   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -# Download all recommended models

#### **GET** `/api/models`

   sudo apt install nodejs -ypython backend/manage_base_models.py download --all

Get list of available pre-trained models.

   ```

**Response:**

```json# Download specific model

{

  "models": [3. **Clone and Setup**:python backend/manage_base_models.py download bert-base-uncased

    {"key": "bert-covid-1", "name": "BERT COVID-19"},

    {"key": "deberta-climate-change-1", "name": "DeBERTa Climate"}   ```bash

  ]

}   cd /var/www# List available models

```

   git clone your-repo deception-detectorpython backend/manage_base_models.py list

#### **POST** `/api/predict`

   cd deception-detector

Analyze text for deception.

   # Remove cached model

**Request:**

```json   # Backend setuppython backend/manage_base_models.py remove bert-base-uncased

{

  "text": "Text to analyze",   cd backend

  "model": "bert-covid-1"

}   python3 -m venv venv# Validate cache integrity

```

   source venv/bin/activatepython backend/manage_base_models.py validate --fix

**Response:**

```json   pip install -r requirements.txt```

{

  "prediction": "truthful",   

  "confidence": 0.85,

  "original_text": "Text to analyze",   # Download models**Recommended Base Models** (auto-downloaded):

  "model_used": "bert-covid-1"

}   cd ..- `bert-base-uncased` - General-purpose BERT, good for most tasks

```

   python3 download_models.py- `microsoft/deberta-v3-base` - Enhanced BERT with better performance  

#### **POST** `/api/lime`

   - `roberta-base` - Robustly optimized BERT for text classification

Get LIME explanation for prediction.

   # Frontend setup- `albert-base-v2` - Lightweight alternative, faster training

**Request:**

```json   cd frontend- `distilbert-base-uncased` - Smaller, faster model with 95% performance

{

  "text": "Text to analyze",   npm install

  "model": "bert-covid-1"

}   npm run build### Adding New Pre-trained Models

```

   ```

**Response:**

```jsonTo add new models to the application:

{

  "lime_explanation": [4. **Configure Firewall**:

    ["word1", 0.45],

    ["word2", -0.32],   ```bash1. **Add model names to models.txt**: Add the full HuggingFace model names (one per line) to the `models.txt` file in the project root.

    ["word3", 0.18]

  ]   sudo ufw allow 'Nginx Full'

}

```   sudo ufw allow 222. **Download the models**: Run the download script to fetch the new models:



#### **POST** `/api/shap`   sudo ufw enable   ```bash



Get SHAP explanation for prediction.   ```   # Windows



**Request:**   download-models.bat

```json

{5. **SSL with Let's Encrypt** (optional):   

  "text": "Text to analyze",

  "model": "bert-covid-1"   ```bash   # Cross-platform

}

```   sudo apt install certbot python3-certbot-nginx -y   python download_models.py



### Custom Model Training API   sudo certbot --nginx -d your-domain.com   ```



#### **GET** `/api/training/models`   ```



Get available base models for fine-tuning.3. **Restart the application**: The backend will automatically discover the new models on restart.



**Response:**### Windows Server Deployment

```json

{**Example models.txt**:

  "models": [

    {"key": "bert-base-uncased", "name": "BERT Base (Uncased)"},1. **Install IIS and required modules**```

    {"key": "microsoft/deberta-v3-base", "name": "DeBERTa v3 Base"}

  ]2. **Install Python and Node.js**neurips-user/neurips-bert-covid-1

}

```3. **Setup as Windows Service** using NSSM:neurips-user/neurips-bert-climate-change-1



#### **POST** `/api/training/upload-csv`   ```bashneurips-user/neurips-bert-combined-1



Validate CSV training data.   nssm install DeceptionDetectorBackend "C:\path\to\venv\Scripts\python.exe" "C:\path\to\backend\app.py"neurips-user/neurips-deberta-covid-1



**Form Data:**   nssm start DeceptionDetectorBackendneurips-user/neurips-deberta-climate-change-1

- `file` - CSV file with `text` and `label` columns

   ```neurips-user/neurips-deberta-combined-1

**Response:**

```json```

{

  "valid": true,## 🔧 Configuration

  "rows": 1000,

  "columns": ["text", "label"],The system automatically converts model names to local identifiers by removing `neurips-user/` and `neurips-` prefixes.

  "label_distribution": {"0": 500, "1": 500}### Environment Variables

}

```Create `.env` file in backend directory:

```bash

#### **POST** `/api/training/start`# Flask Configuration

FLASK_ENV=production

Start model training.API_HOST=0.0.0.0

API_PORT=5000

**Form Data:**

- `file` - CSV training file# Model Configuration

- `config` - JSON string with configurationMODEL_EXPIRY_DAYS=7

ZIP_EXPIRY_HOURS=24

**Config Format:**MAX_SEQUENCE_LENGTH=512

```json

{# GPU Configuration (optional)

  "base_model": "bert-base-uncased",CUDA_VISIBLE_DEVICES=0

  "name": "My Custom Model",```

  "epochs": 3,

  "batch_size": 16,### GPU Configuration

  "learning_rate": 2e-5,

  "validation_split": 0.2The application automatically detects and uses GPUs via `gpu_utils.py`:

}- **Multi-GPU**: Automatically selects GPU with most free memory

```- **CPU Fallback**: Works without GPU

- **Memory Monitoring**: Logs GPU memory usage during operations

**Response:**

```json## 📊 API Endpoints

{

  "success": true,### Pre-trained Models

  "model_code": "abc123",

  "message": "Training started for model abc123"#### GET `/api/models`

}Get available pre-trained models.

```

**Response:**

#### **GET** `/api/training/status/<model_code>````json

{

Get training status.  "models": [

    {"key": "bert-covid-1", "name": "BERT COVID-19"},

**Response:**    {"key": "deberta-climate-change-1", "name": "DeBERTa Climate"}

```json  ]

{}

  "status": "training",```

  "progress": 65,

  "name": "My Custom Model",#### POST `/api/predict`

  "base_model": "bert-base-uncased",Analyze text for deception.

  "created_at": "2025-10-27T10:30:00",

  "expires_at": "2025-11-03T10:30:00",**Request:**

  "remaining_time": "6 days, 12 hours"```json

}{

```  "text": "Text to analyze",

  "model": "bert-covid-1"

#### **POST** `/api/custom/predict/<model_code>`}

```

Use custom model for prediction.

**Response:**

**Request:**```json

```json{

{  "prediction": "truthful",

  "text": "Text to analyze"  "confidence": 0.85,

}  "original_text": "Text to analyze",

```  "model_used": "bert-covid-1"

}

#### **POST** `/api/custom/download/init/<model_code>````



Initialize model download and get download ID.#### POST `/api/lime`

Get LIME explanation.

**Response:**

```json**Request:**

{```json

  "download_id": "uuid-here",{

  "model_code": "abc123"  "text": "Text to analyze",

}  "model": "bert-covid-1"

```}

```

#### **GET** `/api/custom/download/<model_code>?download_id=<id>`

#### POST `/api/shap`

Download trained model archive.Get SHAP explanation.



**Response:** Binary ZIP file### Custom Model Training



#### **GET** `/api/custom/download-progress/<download_id>`#### GET `/api/training/models`

Get available base models for fine-tuning.

Get real-time download progress.

#### POST `/api/training/upload-csv`

**Response:**Validate CSV training data.

```json

{**Form Data:**

  "status": "creating",- `file`: CSV file with `text` and `label` columns

  "progress": 45,

  "phase": "Compressing: model.safetensors...",#### POST `/api/training/start`

  "elapsed_time": 12.5,Start model training.

  "archive_size_mb": 420.5

}**Form Data:**

```- `file`: CSV training file

- `config`: JSON configuration

---  ```json

  {

## 🎯 Usage    "base_model": "bert-base-uncased",

    "name": "My Custom Model",

### Analyzing Text with Pre-trained Model    "epochs": 3,

    "batch_size": 16,

1. Navigate to **"Text Analysis"** tab    "learning_rate": 2e-5,

2. Enter text (max 1300 words)    "validation_split": 0.2

3. Select a model from dropdown  }

4. Click **"Analyze Text"**  ```

5. View results:

   - Prediction (deceptive/truthful)**Response:**

   - Confidence score```json

   - LIME explanation (word importance){

   - SHAP explanation (feature impact)  "success": true,

  "model_code": "abc123",

### Training a Custom Model  "message": "Training started"

}

1. **Prepare Data**```

   - Create CSV with columns: `text`, `label`

   - Label format: `0` = deceptive, `1` = truthful#### GET `/api/training/status/<model_code>`

   - Minimum 100 rows recommendedGet training status.



2. **Start Training**#### POST `/api/custom/predict/<model_code>`

   - Navigate to **"Model Training"** tabUse custom model for prediction.

   - Upload CSV file

   - Configure parameters:#### POST `/api/custom/download/init/<model_code>`

     - Choose base modelInitialize model download.

     - Set epochs (default: 3)

     - Set batch size (default: 16)#### GET `/api/custom/download/<model_code>`

     - Set learning rate (default: 2e-5)Download trained model archive.

     - Set validation split (default: 0.2)

   - Click **"Start Training"**#### GET `/api/custom/download-progress/<download_id>`

Get download progress (real-time updates).

3. **Save Model Code**

   - Copy your 6-digit model code## 🎯 Usage Examples

   - Training runs in background

   - Check progress anytime with your code### Analyzing Text with Pre-trained Model



4. **Monitor Training**1. Navigate to "Text Analysis" tab

   - Training status updates automatically2. Enter text (max 1300 words)

   - View metrics and progress3. Select a model

   - Training typically takes 5-30 minutes4. Click "Analyze Text"

5. View prediction, confidence, and explanations

### Using Custom Model

### Training a Custom Model

1. Navigate to **"Custom Model"** tab

2. Enter your 6-digit model code1. Navigate to "Model Training" tab

3. Click **"Access Model"**2. Prepare CSV file with columns: `text`, `label` (0=deceptive, 1=truthful)

4. Analyze text with your trained model3. Upload CSV and configure training parameters

5. View LIME/SHAP explanations4. Click "Start Training"

6. Download model archive if needed5. Save your 6-digit model code

6. Monitor training progress

### Downloading Custom Model7. Use model after training completes



1. Access your custom model### Using Custom Model

2. Click **"Download Model"**

3. Watch real-time progress:1. Navigate to "Custom Model" tab

   - Validation2. Enter your 6-digit model code

   - File scanning3. Analyze text with your trained model

   - ZIP creation with file-by-file progress4. Download model archive if needed

   - Download completion

4. Model ZIP downloads automatically## 🛠️ Maintenance



---### Model Cleanup



## 🛠️ MaintenanceModels are automatically cleaned up:

- **Custom Models**: Deleted after 7 days

### Automatic Cleanup- **Model Archives**: Deleted after 24 hours

- **Manual Cleanup**: POST `/api/training/cleanup`

The application automatically manages storage:- **ZIP Cleanup**: Runs hourly via background thread



| Item | Retention | Cleanup |### Base Model Management

|------|-----------|---------|

| **Custom Models** | 7 days | Auto-deleted after expiry |```bash

| **Model Archives** | 24 hours | Hourly cleanup thread |# Check cache status

| **Temp Files** | Session | Deleted on completion |python backend/manage_base_models.py status



### Manual Cleanup# Download all recommended models

python backend/manage_base_models.py download --all

**Cleanup Expired Models:**

```bash# List available models

curl -X POST http://localhost:5000/api/training/cleanuppython backend/manage_base_models.py list

```

# Validate cache

**Cleanup Expired ZIPs:**python backend/manage_base_models.py validate --fix

```bash```

curl -X POST http://localhost:5000/api/training/cleanup-zips

```### Logs



### Base Model Management- **Backend**: Check systemd logs `sudo journalctl -u deception-detector-backend`

- **Nginx**: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`

```bash- **GPU Usage**: Logged in application output

# Check cache status

python backend/manage_base_models.py status## 🔒 Security Considerations



# Download all recommended models1. **File Upload Limits**: Max 100MB (configurable in nginx)

python backend/manage_base_models.py download --all2. **Model Expiration**: Automatic cleanup of old models

3. **CORS**: Configure allowed origins in production

# Download specific model4. **Rate Limiting**: Consider adding rate limiting for API endpoints

python backend/manage_base_models.py download bert-base-uncased5. **SSL**: Use HTTPS in production (Let's Encrypt recommended)



# List available models## 📝 Requirements

python backend/manage_base_models.py list

### Backend Dependencies

# Remove cached model- Flask 2.3.x

python backend/manage_base_models.py remove bert-base-uncased- PyTorch 2.0+

- Transformers 4.30+

# Validate cache integrity- LIME 0.2+

python backend/manage_base_models.py validate --fix- SHAP 0.41+

```- NumPy, pandas, scikit-learn



### Monitoring### Frontend Dependencies

- Vue.js 3.3+

**Check Backend Service:**- Axios 1.4+

```bash- Bootstrap 5.3+

# Linux/systemd- Chart.js 4.3+

sudo systemctl status deception-detector-backend

sudo journalctl -u deception-detector-backend -f## 🐛 Troubleshooting



# Windows### Backend won't start

nssm status DeceptionDetectorBackend- Check Python version: `python --version` (need 3.8+)

```- Verify virtual environment is activated

- Install missing dependencies: `pip install -r requirements.txt`

**Check Nginx:**

```bash### Models not found

# Access logs- Run `python download_models.py` to download models

tail -f /var/log/nginx/access.log- Check `backend/models/` directory exists



# Error logs### GPU not detected

tail -f /var/log/nginx/error.log- Install CUDA toolkit matching PyTorch version

```- Check: `python -c "import torch; print(torch.cuda.is_available())"`



**Check GPU Usage:**### Training fails

```bash- Ensure CSV has `text` and `label` columns

# While application is running- Check sufficient disk space for model storage

watch -n 1 nvidia-smi- Verify GPU memory if using GPU

```

### Frontend connection issues

---- Check `frontend/src/config.js` has correct API URL

- Verify backend is running on correct port

## 🐛 Troubleshooting- Check CORS settings in `backend/app.py`



### Backend Issues## 📄 License



#### Backend Won't Start[Your License Here]



**Symptoms:** Flask server fails to start## 👥 Contributors



**Solutions:**[Your Team/Contributors]

```bash

# Check Python version (need 3.8+)## 📧 Support

python --version

For issues and questions, please open an issue on GitHub or contact [your-email].

# Verify virtual environment
which python  # Should point to venv

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check port availability
netstat -an | grep 5000  # Linux
netstat -an | findstr 5000  # Windows
```

#### Models Not Found

**Symptoms:** "Model not available" errors

**Solutions:**
```bash
# Download models
python download_models.py

# Verify models directory
ls backend/models/  # Should contain model folders

# Check permissions
chmod -R 755 backend/models/  # Linux
```

#### GPU Not Detected

**Symptoms:** Training/inference slow, CPU usage high

**Solutions:**
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Check CUDA version
nvcc --version

# Reinstall PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Frontend Issues

#### Connection Errors

**Symptoms:** "Network Error" or "Cannot connect to backend"

**Solutions:**

1. **Check API URL** in `frontend/src/config.js`:
   ```javascript
   export default {
     apiBaseUrl: 'http://localhost:5000/api'  // Correct URL?
   }
   ```

2. **Verify Backend Running:**
   ```bash
   curl http://localhost:5000/api/models
   ```

3. **Check CORS Settings** in `backend/app.py`

#### Build Failures

**Symptoms:** `npm run build` fails

**Solutions:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 14+
```

### Training Issues

#### Training Fails Immediately

**Symptoms:** Model training stops right after starting

**Solutions:**

1. **Check CSV Format:**
   - Must have `text` and `label` columns
   - Labels must be 0 or 1
   - No missing values

2. **Check Disk Space:**
   ```bash
   df -h  # Linux
   ```

3. **Check GPU Memory:**
   ```bash
   nvidia-smi
   ```
   - Free up GPU memory if needed
   - Try smaller batch size

#### Training Very Slow

**Symptoms:** Training takes hours

**Solutions:**
- Enable GPU if available
- Reduce batch size (try 8 instead of 16)
- Reduce epochs (try 2 instead of 3)
- Use DistilBERT instead of BERT (faster)

### Download Issues

#### Progress Stuck

**Symptoms:** Download progress frozen

**Solutions:**
- Refresh page and try again
- Check backend logs for errors
- Verify model still exists (not expired)

#### Download Fails

**Symptoms:** "Failed to download model" error

**Solutions:**
```bash
# Check model status
curl http://localhost:5000/api/training/status/abc123

# Check disk space
df -h

# Check model directory exists
ls backend/custom_models/abc123/
```

---

## 📝 Requirements

### Backend Dependencies

```
Flask>=2.3.0
torch>=2.0.0
transformers>=4.30.0
lime>=0.2.0
shap>=0.41.0
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
flask-cors>=4.0.0
```

### Frontend Dependencies

```
vue@^3.3.0
axios@^1.4.0
bootstrap@^5.3.0
@fortawesome/fontawesome-free@^6.4.0
chart.js@^4.3.0
```

### System Requirements

| Component | Development | Production |
|-----------|-------------|------------|
| **Python** | 3.8+ | 3.9+ |
| **Node.js** | 14+ | 16+ |
| **RAM** | 4GB | 8GB+ |
| **Storage** | 10GB | 20GB+ |
| **GPU** | Optional | Recommended |
| **CUDA** | 11.7+ | 11.7+ |

---

## 🔒 Security

### Production Checklist

- [ ] Change default Flask secret key
- [ ] Configure CORS for specific domains only
- [ ] Enable SSL/HTTPS with Let's Encrypt
- [ ] Set up firewall rules (UFW/iptables)
- [ ] Implement rate limiting on API endpoints
- [ ] Configure nginx client_max_body_size appropriately
- [ ] Set secure file upload validation
- [ ] Enable nginx access logs for monitoring
- [ ] Configure automatic security updates
- [ ] Set up backup strategy for models
- [ ] Implement API key authentication (optional)
- [ ] Use environment variables for sensitive config

---

## 📄 License

[Your License Here]

---

## 👥 Contributors

[Your Team/Contributors]

---

## 📧 Support

For issues, questions, or feature requests:

- **GitHub Issues**: [your-repo/issues]
- **Email**: [your-email]
- **Documentation**: [your-docs-url]

---

## 🙏 Acknowledgments

- Hugging Face Transformers
- Vue.js Team
- Flask Team
- LIME & SHAP Libraries

---

*Made with ❤️ by [Your Team]*
