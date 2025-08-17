# Deception Detector App

A Vue.js frontend with Flask backend for detecting deception in text using pre-trained Hugging Face models.

## Features

- **Deception Detection**: Get predictions on whether text is deceptive or truthful
- **Explainable AI**: 
  - LIME explanations showing word-level feature importance
  - SHAP explanations for model interpretability

## Project Structure

```
webapp/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── models/             # Local model storage
├── frontend/
│   ├── src/
|   |   ├── components/       # Vue components
│   │   ├── public/        # Static assets (images, styles)
│   │   ├── views/         # Application views
│   │   ├── App.vue        # Main Vue component
│   │   └── main.js        # Vue app entry point
│   ├── public/
│   │   └── index.html     # HTML template
│   ├── package.json       # Node.js dependencies
│   └── vue.config.js      # Vue CLI configuration
├── models.txt             # Available Hugging Face models
├── setup.bat              # Complete setup script
├── download-models.bat    # Model download script (Windows)
├── download_models.py     # Model download script (Cross-platform)
├── start-backend.bat      # Backend startup script
└── start-frontend.bat     # Frontend startup script
```

## Setup Instructions

### Quick Setup (Recommended)

Run the complete setup script that handles everything:
```bash
setup.bat
```

This will:
1. Set up the Python backend environment
2. Install frontend dependencies
3. Download all required Hugging Face models
4. Prepare the application for first run

### Manual Setup

#### Model Download (First Time Only)

Before running the application for the first time, download the required models:
```bash
# Option 1: Using batch script (Windows)
download-models.bat

# Option 2: Using Python script (Cross-platform)
python download_models.py
```

**Note**: This step downloads model data based on the models listed in `models.txt` and saves it locally in `backend/models/`. Models are stored locally for faster access and offline usage. The download may take 5-15 minutes depending on your internet connection and the number of models.

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run serve
   ```

The frontend will be available at `http://localhost:8080`

## Quick Start

For first-time users, simply run:
```bash
setup.bat
```

Then start the application:
```bash
# Terminal 1
start-backend.bat

# Terminal 2  
start-frontend.bat
```

Open `http://localhost:8080` in your browser.

## Available Models

The application supports models discovered from `models.txt`. Models are downloaded from Hugging Face and stored locally. Example models include:

1. neurips-user/neurips-bert-covid-1
2. neurips-user/neurips-bert-climate-change-1
3. neurips-user/neurips-bert-combined-1

## API Endpoints

### GET /api/models
Returns available models for selection (dynamically discovered from local storage).

### POST /api/predict
Analyzes text for deception detection.

**Request Body:**
```json
{
  "text": "Text to analyze",
  "model": "model"
}
```

**Response:**
```json
{
  "confidence": 0.85,
  "explanations": {
    "lime": [["word", 0.123], ...],
    "shap": [["word", 0.456], ...],
  },
  "model_used": "deberta-climate-change-1",
  "original_text": "Text to analyze",
  "prediction": "deceptive|truthful"
}
```

## Usage

1. Start both backend and frontend servers
2. Open `http://localhost:8080` in your browser
3. Enter text you want to analyze
4. Select a model from the dropdown (models are automatically discovered)
5. Click "Analyze Text"
6. View results including:
   - Prediction (deceptive/truthful)
   - Confidence score
   - LIME and SHAP explanations in separate tabs

## Requirements

### Backend
- Python 3.8+
- PyTorch
- Transformers
- Flask
- LIME
- SHAP
- NumPy
- scikit-learn

### Frontend
- Node.js 14+
- Vue.js 3
- Axios
- Bootstrap 5

## Notes

- **Local Model Storage**: Models are downloaded and stored in `backend/models/` for faster access and offline usage
- **Dynamic Model Discovery**: System automatically discovers available models from `models.txt` and existing downloads
- **Model Requirement**: Models must be downloaded before running the application for the first time
- **First Run**: The initial setup downloads model files to local storage based on `models.txt`
- **Offline Capability**: Once downloaded, models work without internet connection
- **GPU Support**: GPU support is automatically detected and used if available
- **Network**: Internet connection only required for initial model download
- CORS is enabled for cross-origin requests from the frontend
- The application includes error handling and loading states

### Adding New Models

To add new models to the application:

1. **Add model names to models.txt**: Add the full HuggingFace model names (one per line) to the `models.txt` file in the project root.

2. **Download the models**: Run the download script to fetch the new models:
   ```bash
   # Windows
   download-models.bat
   
   # Cross-platform
   python download_models.py
   ```

3. **Restart the application**: The backend will automatically discover the new models on restart.

**Example models.txt**:
```
neurips-user/neurips-bert-covid-1
neurips-user/neurips-bert-climate-change-1
neurips-user/neurips-bert-combined-1
neurips-user/neurips-deberta-covid-1
neurips-user/neurips-deberta-climate-change-1
neurips-user/neurips-deberta-combined-1
```

The system automatically converts model names to local identifiers by removing `neurips-user/` and `neurips-` prefixes.