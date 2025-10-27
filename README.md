# Deception Detector Web Application# Deception Detector App



A full-stack web application for detecting deception in text using AI models, featuring both pre-trained models and custom fine-tuning capabilities.A Vue.js frontend with Flask backend for detecting deception in text using pre-trained Hugging Face models.



## 🌟 Features## Features



### Analysis Features- **Deception Detection**: Get predictions on whether text is deceptive or truthful

- **Multi-Model Detection**: Choose from multiple pre-trained BERT and DeBERTa models- **Explainable AI**: 

- **Custom Model Training**: Fine-tune your own models on custom datasets  - LIME explanations showing word-level feature importance

- **Explainable AI**:   - SHAP explanations for model interpretability

  - LIME explanations showing word-level feature importance

  - SHAP explanations for model interpretability## Project Structure

- **Real-time Progress**: Live progress tracking for custom model downloads

```

### Custom Model Featureswebapp/

- **Fine-tuning**: Train models on your own labeled data (CSV format)├── backend/

- **Multiple Base Models**: Choose from BERT, DeBERTa, RoBERTa, ALBERT, or DistilBERT│   ├── app.py              # Flask API server

- **Model Management**: │   ├── requirements.txt    # Python dependencies

  - Models auto-expire after 7 days│   └── models/             # Local model storage

  - Model archives auto-delete after 24 hours├── frontend/

  - 6-digit model codes for easy access│   ├── src/

- **Training Configuration**: Customizable epochs, batch size, learning rate, and validation split|   |   ├── components/       # Vue components

│   │   ├── public/        # Static assets (images, styles)

## 📁 Project Structure│   │   ├── views/         # Application views

│   │   ├── App.vue        # Main Vue component

```│   │   └── main.js        # Vue app entry point

webapp/│   ├── public/

├── backend/│   │   └── index.html     # HTML template

│   ├── app.py                    # Flask API server│   ├── package.json       # Node.js dependencies

│   ├── routes.py                 # Pre-trained model routes│   └── vue.config.js      # Vue CLI configuration

│   ├── training_routes.py        # Custom training routes├── models.txt             # Available Hugging Face models

│   ├── ai_utils.py              # Model loading and inference├── setup.bat              # Complete setup script

│   ├── model_trainer.py          # Custom model training logic├── download-models.bat    # Model download script (Windows)

│   ├── model_utils.py            # Model utility functions├── download_models.py     # Model download script (Cross-platform)

│   ├── explanations.py           # LIME/SHAP explanation generators├── start-backend.bat      # Backend startup script

│   ├── config.py                 # Application configuration└── start-frontend.bat     # Frontend startup script

│   ├── gpu_utils.py              # GPU device management```

│   ├── base_model_cache.py       # Base model caching system

│   ├── requirements.txt          # Python dependencies## Setup Instructions

│   ├── models/                   # Pre-trained models storage

│   ├── base_models/              # Cached base models for training### Quick Setup (Recommended)

│   └── custom_models/            # User-trained models storage

├── frontend/Run the complete setup script that handles everything:

│   ├── src/```bash

│   │   ├── components/           # Reusable Vue componentssetup.bat

│   │   ├── views/                # Main application views```

│   │   ├── App.vue               # Main Vue component

│   │   ├── main.js               # Vue app entry pointThis will:

│   │   └── config.js             # Frontend configuration1. Set up the Python backend environment

│   ├── public/                   # Static assets2. Install frontend dependencies

│   ├── package.json              # Node.js dependencies3. Download all required Hugging Face models

│   └── vue.config.js             # Vue CLI configuration4. Prepare the application for first run

├── models.txt                    # Available pre-trained models list

├── setup.bat                     # Windows setup script### Manual Setup

├── download-models.bat           # Model download (Windows)

├── download_models.py            # Model download (Cross-platform)#### Model Download (First Time Only)

├── start-backend.bat             # Backend startup (Windows)

└── start-frontend.bat            # Frontend startup (Windows)Before running the application for the first time, download the required models:

``````bash

# Option 1: Using batch script (Windows)

## 🚀 Quick Startdownload-models.bat



### Prerequisites# Option 2: Using Python script (Cross-platform)

- Python 3.8+ (3.9 recommended)python download_models.py

- Node.js 14+ and npm```

- 4GB+ RAM (8GB+ recommended for training)

- GPU recommended but not required**Note**: This step downloads model data based on the models listed in `models.txt` and saves it locally in `backend/models/`. Models are stored locally for faster access and offline usage. The download may take 5-15 minutes depending on your internet connection and the number of models.



### Windows Quick Setup#### Backend Setup



1. **Complete Setup** (first time):1. Navigate to the backend directory:

   ```bash   ```bash

   setup.bat   cd backend

   ```   ```

   This downloads models, installs dependencies, and prepares everything.

2. Create a virtual environment (recommended):

2. **Start Application**:   ```bash

   ```bash   python -m venv venv

   # Terminal 1 - Backend   venv\Scripts\activate  # On Windows

   start-backend.bat   ```

   

   # Terminal 2 - Frontend3. Install Python dependencies:

   start-frontend.bat   ```bash

   ```   pip install -r requirements.txt

   ```

3. Open `http://localhost:8080` in your browser

4. Run the Flask server:

## 📦 Installation   ```bash

   python app.py

### Backend Setup   ```



1. **Create Virtual Environment**:The backend will be available at `http://localhost:5000`

   ```bash

   cd backend### Frontend Setup

   python -m venv venv

   1. Navigate to the frontend directory:

   # Windows   ```bash

   venv\Scripts\activate   cd frontend

      ```

   # Linux/Mac

   source venv/bin/activate2. Install Node.js dependencies:

   ```   ```bash

   npm install

2. **Install Dependencies**:   ```

   ```bash

   pip install -r requirements.txt3. Start the development server:

   ```   ```bash

   npm run serve

3. **Download Pre-trained Models** (first time):   ```

   ```bash

   cd ..The frontend will be available at `http://localhost:8080`

   python download_models.py

   ```## Quick Start



### Frontend SetupFor first-time users, simply run:

```bash

1. **Install Dependencies**:setup.bat

   ```bash```

   cd frontend

   npm installThen start the application:

   ``````bash

# Terminal 1

2. **Configure API URL** (optional):start-backend.bat

   Edit `frontend/src/config.js` if deploying to a different host:

   ```javascript# Terminal 2  

   export default {start-frontend.bat

     apiBaseUrl: 'http://your-server:5000/api'```

   }

   ```Open `http://localhost:8080` in your browser.



## 🌐 Deployment## Available Models



### Ubuntu/Linux DeploymentThe application supports models discovered from `models.txt`. Models are downloaded from Hugging Face and stored locally. Example models include:



#### Using systemd Services1. neurips-user/neurips-bert-covid-1

2. neurips-user/neurips-bert-climate-change-1

1. **Backend Service** (`/etc/systemd/system/deception-detector-backend.service`):3. neurips-user/neurips-bert-combined-1

   ```ini

   [Unit]## API Endpoints

   Description=Deception Detector Backend API

   After=network.target### GET /api/models

Returns available models for selection (dynamically discovered from local storage).

   [Service]

   Type=simple### POST /api/predict

   User=www-dataAnalyzes text for deception detection.

   WorkingDirectory=/var/www/deception-detector/backend

   Environment="PATH=/var/www/deception-detector/backend/venv/bin"**Request Body:**

   ExecStart=/var/www/deception-detector/backend/venv/bin/python app.py```json

   Restart=always{

   RestartSec=10  "text": "Text to analyze",

  "model": "model"

   [Install]}

   WantedBy=multi-user.target```

   ```

**Response:**

2. **Frontend Build**:```json

   ```bash{

   cd frontend  "confidence": 0.85,

   npm run build  "explanations": {

   ```    "lime": [["word", 0.123], ...],

    "shap": [["word", 0.456], ...],

3. **Nginx Configuration** (`/etc/nginx/sites-available/deception-detector`):  },

   ```nginx  "model_used": "deberta-climate-change-1",

   server {  "original_text": "Text to analyze",

       listen 80;  "prediction": "deceptive|truthful"

       server_name your-domain.com;}

```

       # Frontend

       location / {## Usage

           root /var/www/deception-detector/frontend/dist;

           try_files $uri $uri/ /index.html;1. Start both backend and frontend servers

       }2. Open `http://localhost:8080` in your browser

3. Enter text you want to analyze

       # Backend API4. Select a model from the dropdown (models are automatically discovered)

       location /api/ {5. Click "Analyze Text"

           proxy_pass http://localhost:5000/api/;6. View results including:

           proxy_http_version 1.1;   - Prediction (deceptive/truthful)

           proxy_set_header Upgrade $http_upgrade;   - Confidence score

           proxy_set_header Connection 'upgrade';   - LIME and SHAP explanations in separate tabs

           proxy_set_header Host $host;

           proxy_cache_bypass $http_upgrade;## Requirements

           proxy_set_header X-Real-IP $remote_addr;

           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;### Backend

           - Python 3.8+

           # Increase timeouts for long-running operations- PyTorch

           proxy_connect_timeout 600;- Transformers

           proxy_send_timeout 600;- Flask

           proxy_read_timeout 600;- LIME

       }- SHAP

- NumPy

       client_max_body_size 100M;- scikit-learn

   }

   ```### Frontend

- Node.js 14+

4. **Enable and Start Services**:- Vue.js 3

   ```bash- Axios

   # Enable services- Bootstrap 5

   sudo systemctl enable deception-detector-backend

   sudo systemctl start deception-detector-backend## Notes

   

   # Enable nginx- **Local Model Storage**: Models are downloaded and stored in `backend/models/` for faster access and offline usage

   sudo ln -s /etc/nginx/sites-available/deception-detector /etc/nginx/sites-enabled/- **Base Model Caching**: Training base models are cached in `backend/base_models/` to prevent repeated downloads during fine-tuning

   sudo systemctl restart nginx- **Dynamic Model Discovery**: System automatically discovers available models from `models.txt` and existing downloads

   ```- **Model Requirement**: Models must be downloaded before running the application for the first time

- **First Run**: The initial setup downloads both pre-trained and base model files to local storage

### DigitalOcean Deployment- **Offline Training**: Once base models are cached, training works without internet connection

- **GPU Support**: GPU support is automatically detected and used if available

1. **Create Droplet**:- **Network**: Internet connection only required for initial model downloads

   - Ubuntu 22.04 LTS- CORS is enabled for cross-origin requests from the frontend

   - 4GB+ RAM minimum (8GB recommended for training)- The application includes error handling and loading states

   - 80GB+ SSD (for models)

### Base Model Management

2. **Install Dependencies**:

   ```bashThe system includes automated caching for base models used in training:

   # Update system

   sudo apt update && sudo apt upgrade -y```bash

   # Check cache status

   # Install Python and Node.jspython backend/manage_base_models.py status

   sudo apt install python3-pip python3-venv nginx -y

   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -# Download all recommended models

   sudo apt install nodejs -ypython backend/manage_base_models.py download --all

   ```

# Download specific model

3. **Clone and Setup**:python backend/manage_base_models.py download bert-base-uncased

   ```bash

   cd /var/www# List available models

   git clone your-repo deception-detectorpython backend/manage_base_models.py list

   cd deception-detector

   # Remove cached model

   # Backend setuppython backend/manage_base_models.py remove bert-base-uncased

   cd backend

   python3 -m venv venv# Validate cache integrity

   source venv/bin/activatepython backend/manage_base_models.py validate --fix

   pip install -r requirements.txt```

   

   # Download models**Recommended Base Models** (auto-downloaded):

   cd ..- `bert-base-uncased` - General-purpose BERT, good for most tasks

   python3 download_models.py- `microsoft/deberta-v3-base` - Enhanced BERT with better performance  

   - `roberta-base` - Robustly optimized BERT for text classification

   # Frontend setup- `albert-base-v2` - Lightweight alternative, faster training

   cd frontend- `distilbert-base-uncased` - Smaller, faster model with 95% performance

   npm install

   npm run build### Adding New Pre-trained Models

   ```

To add new models to the application:

4. **Configure Firewall**:

   ```bash1. **Add model names to models.txt**: Add the full HuggingFace model names (one per line) to the `models.txt` file in the project root.

   sudo ufw allow 'Nginx Full'

   sudo ufw allow 222. **Download the models**: Run the download script to fetch the new models:

   sudo ufw enable   ```bash

   ```   # Windows

   download-models.bat

5. **SSL with Let's Encrypt** (optional):   

   ```bash   # Cross-platform

   sudo apt install certbot python3-certbot-nginx -y   python download_models.py

   sudo certbot --nginx -d your-domain.com   ```

   ```

3. **Restart the application**: The backend will automatically discover the new models on restart.

### Windows Server Deployment

**Example models.txt**:

1. **Install IIS and required modules**```

2. **Install Python and Node.js**neurips-user/neurips-bert-covid-1

3. **Setup as Windows Service** using NSSM:neurips-user/neurips-bert-climate-change-1

   ```bashneurips-user/neurips-bert-combined-1

   nssm install DeceptionDetectorBackend "C:\path\to\venv\Scripts\python.exe" "C:\path\to\backend\app.py"neurips-user/neurips-deberta-covid-1

   nssm start DeceptionDetectorBackendneurips-user/neurips-deberta-climate-change-1

   ```neurips-user/neurips-deberta-combined-1

```

## 🔧 Configuration

The system automatically converts model names to local identifiers by removing `neurips-user/` and `neurips-` prefixes.
### Environment Variables

Create `.env` file in backend directory:
```bash
# Flask Configuration
FLASK_ENV=production
API_HOST=0.0.0.0
API_PORT=5000

# Model Configuration
MODEL_EXPIRY_DAYS=7
ZIP_EXPIRY_HOURS=24
MAX_SEQUENCE_LENGTH=512

# GPU Configuration (optional)
CUDA_VISIBLE_DEVICES=0
```

### GPU Configuration

The application automatically detects and uses GPUs via `gpu_utils.py`:
- **Multi-GPU**: Automatically selects GPU with most free memory
- **CPU Fallback**: Works without GPU
- **Memory Monitoring**: Logs GPU memory usage during operations

## 📊 API Endpoints

### Pre-trained Models

#### GET `/api/models`
Get available pre-trained models.

**Response:**
```json
{
  "models": [
    {"key": "bert-covid-1", "name": "BERT COVID-19"},
    {"key": "deberta-climate-change-1", "name": "DeBERTa Climate"}
  ]
}
```

#### POST `/api/predict`
Analyze text for deception.

**Request:**
```json
{
  "text": "Text to analyze",
  "model": "bert-covid-1"
}
```

**Response:**
```json
{
  "prediction": "truthful",
  "confidence": 0.85,
  "original_text": "Text to analyze",
  "model_used": "bert-covid-1"
}
```

#### POST `/api/lime`
Get LIME explanation.

**Request:**
```json
{
  "text": "Text to analyze",
  "model": "bert-covid-1"
}
```

#### POST `/api/shap`
Get SHAP explanation.

### Custom Model Training

#### GET `/api/training/models`
Get available base models for fine-tuning.

#### POST `/api/training/upload-csv`
Validate CSV training data.

**Form Data:**
- `file`: CSV file with `text` and `label` columns

#### POST `/api/training/start`
Start model training.

**Form Data:**
- `file`: CSV training file
- `config`: JSON configuration
  ```json
  {
    "base_model": "bert-base-uncased",
    "name": "My Custom Model",
    "epochs": 3,
    "batch_size": 16,
    "learning_rate": 2e-5,
    "validation_split": 0.2
  }
  ```

**Response:**
```json
{
  "success": true,
  "model_code": "abc123",
  "message": "Training started"
}
```

#### GET `/api/training/status/<model_code>`
Get training status.

#### POST `/api/custom/predict/<model_code>`
Use custom model for prediction.

#### POST `/api/custom/download/init/<model_code>`
Initialize model download.

#### GET `/api/custom/download/<model_code>`
Download trained model archive.

#### GET `/api/custom/download-progress/<download_id>`
Get download progress (real-time updates).

## 🎯 Usage Examples

### Analyzing Text with Pre-trained Model

1. Navigate to "Text Analysis" tab
2. Enter text (max 1300 words)
3. Select a model
4. Click "Analyze Text"
5. View prediction, confidence, and explanations

### Training a Custom Model

1. Navigate to "Model Training" tab
2. Prepare CSV file with columns: `text`, `label` (0=deceptive, 1=truthful)
3. Upload CSV and configure training parameters
4. Click "Start Training"
5. Save your 6-digit model code
6. Monitor training progress
7. Use model after training completes

### Using Custom Model

1. Navigate to "Custom Model" tab
2. Enter your 6-digit model code
3. Analyze text with your trained model
4. Download model archive if needed

## 🛠️ Maintenance

### Model Cleanup

Models are automatically cleaned up:
- **Custom Models**: Deleted after 7 days
- **Model Archives**: Deleted after 24 hours
- **Manual Cleanup**: POST `/api/training/cleanup`
- **ZIP Cleanup**: Runs hourly via background thread

### Base Model Management

```bash
# Check cache status
python backend/manage_base_models.py status

# Download all recommended models
python backend/manage_base_models.py download --all

# List available models
python backend/manage_base_models.py list

# Validate cache
python backend/manage_base_models.py validate --fix
```

### Logs

- **Backend**: Check systemd logs `sudo journalctl -u deception-detector-backend`
- **Nginx**: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`
- **GPU Usage**: Logged in application output

## 🔒 Security Considerations

1. **File Upload Limits**: Max 100MB (configurable in nginx)
2. **Model Expiration**: Automatic cleanup of old models
3. **CORS**: Configure allowed origins in production
4. **Rate Limiting**: Consider adding rate limiting for API endpoints
5. **SSL**: Use HTTPS in production (Let's Encrypt recommended)

## 📝 Requirements

### Backend Dependencies
- Flask 2.3.x
- PyTorch 2.0+
- Transformers 4.30+
- LIME 0.2+
- SHAP 0.41+
- NumPy, pandas, scikit-learn

### Frontend Dependencies
- Vue.js 3.3+
- Axios 1.4+
- Bootstrap 5.3+
- Chart.js 4.3+

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.8+)
- Verify virtual environment is activated
- Install missing dependencies: `pip install -r requirements.txt`

### Models not found
- Run `python download_models.py` to download models
- Check `backend/models/` directory exists

### GPU not detected
- Install CUDA toolkit matching PyTorch version
- Check: `python -c "import torch; print(torch.cuda.is_available())"`

### Training fails
- Ensure CSV has `text` and `label` columns
- Check sufficient disk space for model storage
- Verify GPU memory if using GPU

### Frontend connection issues
- Check `frontend/src/config.js` has correct API URL
- Verify backend is running on correct port
- Check CORS settings in `backend/app.py`

## 📄 License

[Your License Here]

## 👥 Contributors

[Your Team/Contributors]

## 📧 Support

For issues and questions, please open an issue on GitHub or contact [your-email].
