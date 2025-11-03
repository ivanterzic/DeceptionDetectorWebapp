# SPECIFIKACIJA SUSTAVA - DECEPTION DETECTOR

**Verzija dokumenta:** 1.0  
**Datum:** 3. studeni 2025.  
**Autor:** [Ime autora]

---

## SADRŽAJ

1. [UVOD](#1-uvod)
2. [PREGLED SUSTAVA](#2-pregled-sustava)
3. [ARHITEKTURA SUSTAVA](#3-arhitektura-sustava)
4. [FRONTEND APLIKACIJA](#4-frontend-aplikacija)
5. [BACKEND APLIKACIJA](#5-backend-aplikacija)
6. [MODELI I ALGORITMI](#6-modeli-i-algoritmi)
7. [BAZA PODATAKA I POHRANA](#7-baza-podataka-i-pohrana)
8. [API SPECIFIKACIJA](#8-api-specifikacija)
9. [SIGURNOST I AUTENTIFIKACIJA](#9-sigurnost-i-autentifikacija)
10. [KORISNIČKO SUČELJE](#10-korisničko-sučelje)
11. [INSTALACIJA I KONFIGURACIJA](#11-instalacija-i-konfiguracija)
12. [TESTIRANJE](#12-testiranje)
13. [ODRŽAVANJE I NADOGRADNJA](#13-održavanje-i-nadogradnja)
14. [ZAKLJUČAK](#14-zaključak)
15. [DODATAK](#15-dodatak)

---

## 1. UVOD

### 1.1 Svrha dokumenta

Ovaj dokument predstavlja detaljnu tehničku specifikaciju sustava **Deception Detector** - web aplikacije za detekciju obmane u tekstualnom sadržaju korištenjem naprednih modela umjetne inteligencije. Dokument je namijenjen programerima, arhitektima sustava, testerima i svim dionicima projekta.

### 1.2 Opseg projekta

Deception Detector je full-stack web aplikacija koja omogućava:
- Analizu tekstualnog sadržaja radi detekcije potencijalne obmane
- Korištenje pretreniranih transformer modela (BERT, DeBERTa)
- Fine-tuning vlastitih modela na prilagođenim podatkovnim skupovima
- Objašnjive AI rezultate pomoću LIME i SHAP metoda
- Upravljanje modelima i praćenje napretka treninga u stvarnom vremenu

### 1.3 Ciljana publika

- **Krajnji korisnici:** Istraživači, analitičari, novinari, stručnjaci za fact-checking
- **Razvojni tim:** Frontend i backend programeri
- **Administratori sustava:** DevOps inženjeri
- **Dionici projekta:** Projektni menadžeri, testeri

### 1.4 Tehnološki stog

| Komponenta | Tehnologija | Verzija |
|------------|-------------|---------|
| Frontend | Vue.js | 3.3+ |
| Backend | Flask (Python) | 2.3+ |
| ML Framework | PyTorch | 2.0+ |
| Transformer modeli | Hugging Face Transformers | 4.30+ |
| Objašnjivost | LIME, SHAP | Latest |
| Styling | Bootstrap | 5.3+ |
| HTTP klijent | Axios | 1.4+ |

### 1.5 Definicije i kratice

- **AI:** Artificial Intelligence (Umjetna inteligencija)
- **ML:** Machine Learning (Strojno učenje)
- **BERT:** Bidirectional Encoder Representations from Transformers
- **DeBERTa:** Decoding-enhanced BERT with Disentangled Attention
- **LIME:** Local Interpretable Model-agnostic Explanations
- **SHAP:** SHapley Additive exPlanations
- **API:** Application Programming Interface
- **CSV:** Comma-Separated Values
- **GPU:** Graphics Processing Unit
- **CPU:** Central Processing Unit
- **REST:** Representational State Transfer

---

## 2. PREGLED SUSTAVA

### 2.1 Opis sustava

Deception Detector je kompleksna web aplikacija koja koristi najnovije dostignuća u području obrade prirodnog jezika (NLP) i dubokog učenja za automatsku detekciju obmane u tekstu. Sustav kombinira moćne transformer modele s tehnikama objašnjive umjetne inteligencije kako bi pružio transparentne i razumljive rezultate.

### 2.2 Glavni ciljevi sustava

1. **Točna detekcija:** Pružiti visoku razinu točnosti u prepoznavanju obmanjujućeg sadržaja
2. **Objašnjivost:** Omogućiti korisnicima razumijevanje zašto je određeni tekst klasificiran kao obmanama
3. **Fleksibilnost:** Podržati različite domene (COVID-19, klimatske promjene, opći sadržaj)
4. **Prilagodljivost:** Omogućiti korisnicima treniranje vlastitih modela na specifičnim podatcima
5. **Korisničko iskustvo:** Pružiti intuitivan i responzivan interfejs
6. **Performanse:** Osigurati brze odgovore i efikasno korištenje resursa

### 2.3 Ključne funkcionalnosti

#### 2.3.1 Analiza teksta s pretreniranim modelima

![Screenshot: Analiza teksta] (TODO: Dodati screenshot)

- Unos teksta do 1300 riječi
- Izbor između 6 pretreniranih modela
- Trenutna analiza i prikaz rezultata
- Vizualizacija povjerenja (confidence score)
- LIME i SHAP objašnjenja

#### 2.3.2 Treniranje prilagođenih modela

![Screenshot: Treniranje modela] (TODO: Dodati screenshot)

- Upload CSV podataka s oznakama
- Validacija podatkovnog skupa
- Konfiguracija hiperparametara (epochs, batch size, learning rate)
- Praćenje napretka u stvarnom vremenu
- 6-znamenkasti kodovi za pristup modelima

#### 2.3.3 Pristup prilagođenim modelima

![Screenshot: Pristup modelima] (TODO: Dodati screenshot)

- Unos 6-znamenkastog koda
- Analiza teksta s prilagođenim modelom
- Preuzimanje modela kao ZIP arhive
- Praćenje napretka preuzimanja
- Automatsko brisanje nakon 24 sata

### 2.4 Korisnici sustava

| Tip korisnika | Opis | Prava pristupa |
|---------------|------|----------------|
| Anonimni korisnik | Koristi pretreniranje modele | Analiza teksta |
| Registrirani korisnik | Trenira vlastite modele | Sve funkcionalnosti |
| Administrator | Upravlja sustavom | Puna kontrola |

**Napomena:** U trenutnoj verziji sustav ne zahtijeva autentifikaciju korisnika.

### 2.5 Ograničenja sustava

- Maksimalna duljina teksta: 1300 riječi (ograničenje modela)
- Maksimalna veličina CSV datoteke: 100MB
- Trajanje prilagođenih modela: 7 dana
- Trajanje ZIP arhiva: 24 sata
- Jezična podrška: Engleski jezik (modeli trenirani na engleskom)
- Jedan trening istovremeno po sesiji

---

## 3. ARHITEKTURA SUSTAVA

### 3.1 Opća arhitektura

Sustav koristi **troslojna client-server arhitektura** s jasnom podjelom odgovornosti:

```
┌─────────────────────────────────────────────────────┐
│                   KORISNIK                          │
│                  (Web preglednik)                    │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/HTTPS
                     │
┌────────────────────▼────────────────────────────────┐
│               FRONTEND SLOJ                          │
│              Vue.js aplikacija                       │
│          (Port 8080 - development)                   │
│    • Korisničko sučelje                             │
│    • Validacija unosa                               │
│    • Vizualizacija rezultata                        │
└────────────────────┬────────────────────────────────┘
                     │ REST API (JSON)
                     │
┌────────────────────▼────────────────────────────────┐
│               BACKEND SLOJ                           │
│               Flask REST API                         │
│            (Port 5000 - default)                     │
│    • Poslovna logika                                │
│    • Upravljanje modelima                           │
│    • Autentifikacija (buduće)                       │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
┌────────────┐ ┌──────────┐ ┌────────────┐
│   AI/ML    │ │  Pohrana │ │  Vanjski   │
│   SLOJ     │ │   SLOJ   │ │  RESURSI   │
├────────────┤ ├──────────┤ ├────────────┤
│ PyTorch    │ │ Lokalni  │ │ Hugging    │
│ Transform. │ │ file     │ │ Face Hub   │
│ LIME/SHAP  │ │ system   │ │            │
└────────────┘ └──────────┘ └────────────┘
```

### 3.2 Komponente sustava

#### 3.2.1 Frontend komponente

| Komponenta | Odgovornost | Lokacija |
|------------|-------------|----------|
| **App.vue** | Glavni kontejner aplikacije | `frontend/src/App.vue` |
| **AnalysisView** | Analiza s pretreniranim modelima | `frontend/src/views/AnalysisView.vue` |
| **TrainingView** | Treniranje prilagođenih modela | `frontend/src/views/TrainingView.vue` |
| **CustomModelView** | Pristup prilagođenim modelima | `frontend/src/views/CustomModelView.vue` |
| **LimeExplanation** | Prikaz LIME objašnjenja | `frontend/src/components/LimeExplanation.vue` |
| **ShapExplanation** | Prikaz SHAP objašnjenja | `frontend/src/components/ShapExplanation.vue` |

#### 3.2.2 Backend komponente

| Komponenta | Odgovornost | Lokacija |
|------------|-------------|----------|
| **app.py** | Glavni ulazni punkt | `backend/app.py` |
| **routes.py** | API rute za pretren. modele | `backend/routes.py` |
| **training_routes.py** | API rute za treniranje | `backend/training_routes.py` |
| **ai_utils.py** | Inferenca modela | `backend/ai_utils.py` |
| **model_trainer.py** | Logika treniranja | `backend/model_trainer.py` |
| **explanations.py** | LIME/SHAP generatori | `backend/explanations.py` |
| **gpu_utils.py** | Upravljanje GPU resursima | `backend/gpu_utils.py` |
| **config.py** | Konfiguracija sustava | `backend/config.py` |

### 3.3 Tok podataka

#### 3.3.1 Analiza teksta (pretrenirani modeli)

```
1. Korisnik → Unos teksta u InputForm
2. Frontend → POST /api/predict {text, model}
3. Backend → Učitava model iz backend/models/
4. AI Engine → Inferenca pomoću transformera
5. Backend → Računa LIME i SHAP
6. Backend → Vraća JSON s rezultatima
7. Frontend → Prikazuje rezultate u AnalysisResults
```

#### 3.3.2 Treniranje modela

```
1. Korisnik → Upload CSV u TrainingView
2. Frontend → POST /api/training/upload-csv
3. Backend → Validira CSV format
4. Frontend → POST /api/training/start
5. Backend → Generira 6-znamenkasti kod
6. Backend → Pokreće treniranje u pozadini
7. Backend → Sprema model u custom_models/
8. Frontend → Polling GET /api/training/status/<code>
9. Backend → Vraća status, epoch, metrics
```

### 3.4 Tehnološke odluke

#### 3.4.1 Zašto Vue.js?

- **Reaktivnost:** Dvosmjerno povezivanje podataka
- **Komponente:** Modularan razvoj
- **Ekosustav:** Bogat skup alata i biblioteka
- **Performanse:** Virtual DOM
- **Dokumentacija:** Odlična dokumentacija

#### 3.4.2 Zašto Flask?

- **Jednostavnost:** Minimalan boilerplate
- **Fleksibilnost:** Lako proširiva arhitektura
- **Python:** Prirodan izbor za ML/AI
- **REST API:** Izvrsna podrška za RESTful servise
- **Zajednica:** Velika zajednica i biblioteke

#### 3.4.3 Zašto PyTorch?

- **Dinamički graf:** Fleksibilnost u razvoju modela
- **Hugging Face:** Integracija s Transformers bibliotekom
- **GPU podrška:** Efikasno korištenje GPU-a
- **Debugging:** Lakše debugiranje od TensorFlow-a
- **Istraživanje:** Dominantan u istraživačkoj zajednici

### 3.5 Skalabilnost

#### 3.5.1 Trenutna implementacija

- **Frontend:** Statička distribucija (može se hostati na CDN-u)
- **Backend:** Single-process Flask server
- **Modeli:** Lokalna pohrana na filesystemu
- **Concurrent requests:** Ograničeno (jedan proces)

#### 3.5.2 Prijedlozi za skaliranje

1. **Backend skaliranje:**
   - Gunicorn/uWSGI s više workera
   - Redis za cache i queue
   - Celery za async taskove

2. **Baza podataka:**
   - PostgreSQL za metapodatke modela
   - Redis za sesije i cache

3. **Load balancing:**
   - Nginx reverse proxy
   - Više backend instanci

4. **Cloud deployment:**
   - Docker kontejnerizacija
   - Kubernetes orkestracija
   - Cloud storage (AWS S3, Azure Blob)

### 3.6 Sigurnosna arhitektura

![Sigurnosni dijagram] (TODO: Dodati dijagram)

- **Input validacija:** Validacija svih korisničkih unosa
- **File upload:** Provjera tipa i veličine datoteka
- **Rate limiting:** Buduća implementacija
- **CORS:** Konfiguriran za specifične domene
- **HTTPS:** Obvezno u produkciji

---

## 4. FRONTEND APLIKACIJA

### 4.1 Tehnološki stack

| Tehnologija | Verzija | Svrha |
|-------------|---------|-------|
| Vue.js | 3.3+ | Core framework |
| Vue Router | 4.0+ | Routing (interno u App.vue) |
| Axios | 1.4+ | HTTP klijent |
| Bootstrap | 5.3+ | CSS framework |
| Font Awesome | 6.4+ | Ikone |
| Chart.js | 4.3+ | Grafikoni (LIME/SHAP) |

### 4.2 Struktura direktorija

```
frontend/
├── public/
│   ├── index.html          # HTML template
│   ├── logo.svg            # Logo aplikacije
│   └── favicon.png         # Browser ikona
├── src/
│   ├── main.js             # Ulazna točka aplikacije
│   ├── App.vue             # Root komponenta
│   ├── config.js           # API konfiguracija
│   ├── components/         # Dijeljene komponente
│   │   ├── AnalysisResults.vue
│   │   ├── InputForm.vue
│   │   ├── LimeExplanation.vue
│   │   ├── ShapExplanation.vue
│   │   └── LoadingScreen.vue
│   └── views/              # Glavni pogledi
│       ├── AnalysisView.vue
│       ├── TrainingView.vue
│       └── CustomModelView.vue
├── package.json            # NPM dependencies
└── vue.config.js           # Vue CLI config
```

### 4.3 Ključne komponente

#### 4.3.1 App.vue

![Screenshot: Navigacija] (TODO: Dodati screenshot)

**Odgovornosti:**
- Upravljanje navigacijom između tri glavna taba
- Globalna stanja aplikacije
- Učitavanje dostupnih modela pri startu
- Centralno upravljanje greškama

**State management:**
```javascript
data() {
  return {
    activeTab: 'analysis',           // Trenutni tab
    analysisView: 'input',           // Pogled analize
    availableModels: [],             // Lista modela
    analysisResults: null,           // Rezultati analize
    analysisError: null,             // Greške
    currentRequest: null,            // Axios request object
    pendingModelCode: null           // Kod modela za custom view
  }
}
```

**Dizajn:**
- Svijetla navigacijska traka s gradijentom
- Logo u gornjem lijevom kutu
- Tri taba: Analysis, Fine-tuning, Model Access
- Crveni akcent (#FE483E) za aktivan tab
- Tamno plava (#213544) za neaktivne elemente

#### 4.3.2 AnalysisView.vue

![Screenshot: Analiza] (TODO: Dodati screenshot)

**Funkcionalnost:**
- Unos teksta (textarea, max 1300 riječi)
- Izbor modela (dropdown)
- Validacija unosa
- Prikaz rezultata s LIME/SHAP tabovima
- Povratak na unos

**Validation rules:**
```javascript
{
  text: {
    required: true,
    minLength: 10,
    maxLength: 1300 * 6  // ~1300 riječi
  },
  model: {
    required: true,
    exists: true  // Mora postojati u listi
  }
}
```

#### 4.3.3 TrainingView.vue

![Screenshot: Treniranje] (TODO: Dodati screenshot)

**Workflow:**
1. **Upload CSV**
   - Drag & drop ili file input
   - Validacija formata
   - Prikaz statistike (rows, distribution)

2. **Konfiguracija**
   - Base model selection (5 opcija)
   - Model name (string)
   - Epochs (1-10, default: 3)
   - Batch size (4-32, default: 16)
   - Learning rate (1e-6 do 1e-4, default: 2e-5)
   - Validation split (0.1-0.3, default: 0.2)

3. **Start training**
   - Generira 6-znamenkasti kod
   - Prikazuje modal s kodom
   - Polling za status (svake 2 sekunde)

4. **Progress tracking**
   - Trenutni epoch
   - Training loss
   - Validation accuracy
   - Preostalo vrijeme (estimate)
   - Progress bar (0-100%)

#### 4.3.4 CustomModelView.vue

![Screenshot: Custom model] (TODO: Dodati screenshot)

**Funkcionalnosti:**
- Unos 6-znamenkastog koda
- Dohvaćanje informacija o modelu
- Analiza teksta s custom modelom
- Preuzimanje modela
- Progress bar za preuzimanje (0-100%)

**Model info prikaz:**
```
Model Name: My Climate Model
Base Model: bert-base-uncased
Created: 2025-11-03 14:30:00
Expires: 2025-11-10 14:30:00
Status: ✅ Ready
```

#### 4.3.5 LimeExplanation.vue

![Screenshot: LIME] (TODO: Dodati screenshot)

**Prikaz:**
- Originalni tekst s highlight-anim riječima
- Pozitivne riječi: zelena boja
- Negativne riječi: crvena boja
- Neutralne riječi: siva boja
- Intenzitet boje = važnost riječi
- Legenda s objašnjenjem

**Komponente:**
```vue
<div class="lime-container">
  <div class="explanation-text">
    <span 
      v-for="(word, index) in words" 
      :key="index"
      :style="getWordStyle(word.importance)"
    >
      {{ word.text }}
    </span>
  </div>
  <div class="legend">...</div>
</div>
```

#### 4.3.6 ShapExplanation.vue

![Screenshot: SHAP] (TODO: Dodati screenshot)

**Prikaz:**
- Horizontalni bar chart
- Riječi na Y-osi
- SHAP vrijednosti na X-osi
- Sortiran po važnosti (apsolutna vrijednost)
- Top 20 najvažnijih riječi
- Color coding: pozitivno/negativno

### 4.4 State Management

Aplikacija koristi **component-level state** bez Vuex-a ili Pinia-e:

- **App.vue:** Globalno stanje
- **Views:** Lokalno stanje za svoj scope
- **Props/Events:** Komunikacija roditelj-dijete

**Razlog:** Jednostavna aplikacija bez potrebe za centralnim state-om.

### 4.5 API komunikacija

#### 4.5.1 Axios konfiguracija

```javascript
// src/config.js
export default {
  apiBaseUrl: 'http://localhost:5000/api'
}

// Usage
import axios from 'axios'
import config from './config.js'

axios.post(`${config.apiBaseUrl}/predict`, {...})
```

#### 4.5.2 Error handling

```javascript
try {
  const response = await axios.post(...)
  this.results = response.data
} catch (error) {
  if (error.response) {
    // Server responded with error
    this.error = error.response.data.error
  } else if (error.request) {
    // No response from server
    this.error = 'Server ne odgovara'
  } else {
    // Other error
    this.error = error.message
  }
}
```

### 4.6 Styling i dizajn

#### 4.6.1 Color palette

| Boja | Hex | Upotreba |
|------|-----|----------|
| Primary Red | #FE483E | Gumbi, aktivan tab, akcenti |
| Dark Navy | #213544 | Naslovi, tekst, navbar |
| Light Gray | #f8f9fa | Pozadina |
| White | #ffffff | Kartice, forme |

#### 4.6.2 Typography

- **Font family:** 'Inter', 'Segoe UI', sans-serif
- **Headings:** 600 weight, dark navy
- **Body:** 400 weight, #333
- **Font sizes:** 
  - H1: 2rem
  - H2: 1.5rem
  - Body: 1rem

#### 4.6.3 Components styling

**Kartice:**
- Border-radius: 15px
- Box-shadow: 0 2px 10px rgba(33, 53, 68, 0.08)
- Hover: Shadow intenzivniji
- Padding: 1.5rem

**Gumbi:**
- Border-radius: 10px
- Gradient background (primary)
- Hover: Transform translateY(-1px)
- Shadow na hover

**Forme:**
- Border-radius: 10px
- Focus: Red border s glowom
- Padding: 0.75rem 1rem

### 4.7 Responzivnost

#### 4.7.1 Breakpoints

```css
/* Mobile */
@media (max-width: 768px) {
  .navbar-brand { font-size: 1.25rem; }
  .nav-link { font-size: 0.9rem; }
  .container { padding: 1rem; }
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) {
  /* ... */
}

/* Desktop */
@media (min-width: 1025px) {
  /* ... */
}
```

#### 4.7.2 Mobile optimizacije

- Stack-ane forme na mobilnom
- Veći touch targets (min 44px)
- Collapsible navbar
- Responsive tablice

### 4.8 Performanse

#### 4.8.1 Optimizacije

- **Code splitting:** Lazy loading komponenti
- **Image optimization:** Compressed PNG/SVG
- **Minification:** Production build
- **Caching:** Browser cache strategije

#### 4.8.2 Bundle size

```
frontend/dist/
├── js/
│   ├── app.[hash].js      (~150 KB)
│   ├── chunk-vendors.[hash].js  (~300 KB)
│   └── chunk-*.[hash].js  (lazy loaded)
├── css/
│   └── app.[hash].css     (~50 KB)
└── index.html            (~2 KB)
```

**Total initial load:** ~500 KB (gzipped: ~150 KB)

---

## 5. BACKEND APLIKACIJA

### 5.1 Tehnološki stack

| Tehnologija | Verzija | Svrha |
|-------------|---------|-------|
| Python | 3.8+ | Programski jezik |
| Flask | 2.3+ | Web framework |
| PyTorch | 2.0+ | Deep learning |
| Transformers | 4.30+ | Hugging Face modeli |
| LIME | 0.2+ | Objašnjivost |
| SHAP | 0.41+ | Objašnjivost |
| NumPy | Latest | Numeričke operacije |
| Pandas | Latest | Data manipulation |
| scikit-learn | Latest | ML utilities |

### 5.2 Struktura direktorija

```
backend/
├── app.py                  # Flask aplikacija
├── config.py               # Konfiguracija
├── requirements.txt        # Python dependencies
├── routes.py               # API rute za modele
├── training_routes.py      # API rute za treniranje
├── ai_utils.py             # ML inferenca
├── model_trainer.py        # Training engine
├── explanations.py         # LIME/SHAP
├── gpu_utils.py            # GPU management
├── models/                 # Pretren irani modeli
│   ├── bert-covid-1/
│   ├── bert-climate-change-1/
│   ├── bert-combined-1/
│   ├── deberta-covid-1/
│   ├── deberta-climate-change-1/
│   └── deberta-combined-1/
├── base_models/            # Cache za base modele
├── custom_models/          # User-trained modeli
│   └── [6-char-code]/
│       ├── config.json
│       ├── model.safetensors
│       ├── tokenizer_config.json
│       ├── tokenizer.json
│       └── metadata.json
└── __pycache__/
```

### 5.3 Ključni moduli

#### 5.3.1 app.py

**Odgovornosti:**
- Inicijalizacija Flask aplikacije
- Registracija blueprinta
- CORS konfiguracija
- Error handling
- Pokretanje dev servera

```python
from flask import Flask
from flask_cors import CORS
from routes import routes_bp
from training_routes import training_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(routes_bp, url_prefix='/api')
app.register_blueprint(training_bp, url_prefix='/api/training')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### 5.3.2 config.py

**Konfiguracija sustava:**

```python
import torch
from gpu_utils import get_torch_device

# Paths
MODELS_DIR = 'models'
CUSTOM_MODELS_DIR = 'custom_models'
BASE_MODELS_DIR = 'base_models'

# Model settings
MAX_SEQUENCE_LENGTH = 512
MODEL_EXPIRY_DAYS = 7
ZIP_EXPIRY_HOURS = 24

# Device configuration
DEVICE = get_torch_device()  # 'cuda' ili 'cpu'

# Training defaults
DEFAULT_EPOCHS = 3
DEFAULT_BATCH_SIZE = 16
DEFAULT_LEARNING_RATE = 2e-5
DEFAULT_VALIDATION_SPLIT = 0.2

# Available base models
BASE_MODELS = {
    'bert-base-uncased': 'BERT Base (Uncased)',
    'microsoft/deberta-v3-base': 'DeBERTa v3 Base',
    'roberta-base': 'RoBERTa Base',
    'albert-base-v2': 'ALBERT Base v2',
    'distilbert-base-uncased': 'DistilBERT Base'
}
```

#### 5.3.3 routes.py

**API endpoints za pretreniranje modele:**

```python
from flask import Blueprint, request, jsonify
import ai_utils
import explanations

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/models', methods=['GET'])
def get_models():
    """Vraća listu dostupnih modela"""
    models = ai_utils.get_available_models()
    return jsonify(models)

@routes_bp.route('/predict', methods=['POST'])
def predict():
    """Analizira tekst"""
    data = request.get_json()
    text = data.get('text')
    model_key = data.get('model')
    
    # Validacija
    if not text or not model_key:
        return jsonify({'error': 'Missing parameters'}), 400
    
    # Inferenca
    result = ai_utils.predict_text(text, model_key)
    return jsonify(result)

@routes_bp.route('/lime', methods=['POST'])
def get_lime():
    """Vraća LIME objašnjenje"""
    data = request.get_json()
    result = explanations.generate_lime(
        data['text'], 
        data['model']
    )
    return jsonify(result)

@routes_bp.route('/shap', methods=['POST'])
def get_shap():
    """Vraća SHAP objašnjenje"""
    data = request.get_json()
    result = explanations.generate_shap(
        data['text'],
        data['model']
    )
    return jsonify(result)
```

#### 5.3.4 training_routes.py

**API endpoints za custom treniranje:**

```python
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import model_trainer
import os
import random
import string

training_bp = Blueprint('training', __name__)

# Globalni dictionary za praćenje statusa
training_status = {}
download_progress = {}

@training_bp.route('/models', methods=['GET'])
def get_base_models():
    """Vraća dostupne base modele"""
    return jsonify({'models': config.BASE_MODELS})

@training_bp.route('/upload-csv', methods=['POST'])
def upload_csv():
    """Validira CSV datoteku"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    validation = model_trainer.validate_csv(file)
    return jsonify(validation)

@training_bp.route('/start', methods=['POST'])
def start_training():
    """Pokreće treniranje modela"""
    # Generate code
    code = ''.join(random.choices(
        string.ascii_lowercase + string.digits, 
        k=6
    ))
    
    # Get config
    config_data = json.loads(request.form['config'])
    file = request.files['file']
    
    # Start training in background
    thread = threading.Thread(
        target=model_trainer.train_model,
        args=(file, config_data, code, training_status)
    )
    thread.start()
    
    return jsonify({
        'success': True,
        'model_code': code
    })

@training_bp.route('/status/<code>', methods=['GET'])
def get_status(code):
    """Vraća status treniranja"""
    if code not in training_status:
        return jsonify({'error': 'Model not found'}), 404
    
    return jsonify(training_status[code])

@training_bp.route('/cleanup', methods=['POST'])
def cleanup_models():
    """Briše istekle modele"""
    deleted = model_trainer.cleanup_expired_models()
    return jsonify({'deleted': deleted})
```

#### 5.3.5 ai_utils.py

**ML inferenca engine:**

```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import config

# Cache za učitane modele
loaded_models = {}

def load_model(model_key):
    """Učitava model u memoriju"""
    if model_key in loaded_models:
        return loaded_models[model_key]
    
    model_path = os.path.join(config.MODELS_DIR, model_key)
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_path
    ).to(config.DEVICE)
    
    loaded_models[model_key] = (tokenizer, model)
    return tokenizer, model

def predict_text(text, model_key):
    """Vrši predikciju na tekstu"""
    tokenizer, model = load_model(model_key)
    
    # Tokenizacija
    inputs = tokenizer(
        text,
        return_tensors='pt',
        max_length=config.MAX_SEQUENCE_LENGTH,
        truncation=True,
        padding=True
    ).to(config.DEVICE)
    
    # Inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)
    
    # Rezultat
    prediction = torch.argmax(probs, dim=1).item()
    confidence = probs[0][prediction].item()
    
    return {
        'prediction': 'truthful' if prediction == 1 else 'deceptive',
        'confidence': float(confidence),
        'original_text': text,
        'model_used': model_key
    }
```

#### 5.3.6 model_trainer.py

**Training engine:**

```python
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    AdamW,
    get_linear_schedule_with_warmup
)
import pandas as pd
import os
import json
from datetime import datetime, timedelta

class TextDataset(Dataset):
    """Custom dataset za tekstove"""
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def train_model(file, config, code, status_dict):
    """Glavna funkcija za treniranje"""
    try:
        # Update status
        status_dict[code] = {
            'status': 'preparing',
            'progress': 0,
            'name': config['name'],
            'base_model': config['base_model']
        }
        
        # Load data
        df = pd.read_csv(file)
        texts = df['text'].tolist()
        labels = df['label'].tolist()
        
        # Split data
        split_idx = int(len(texts) * (1 - config['validation_split']))
        train_texts = texts[:split_idx]
        train_labels = labels[:split_idx]
        val_texts = texts[split_idx:]
        val_labels = labels[split_idx:]
        
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(config['base_model'])
        model = AutoModelForSequenceClassification.from_pretrained(
            config['base_model'],
            num_labels=2
        ).to(config.DEVICE)
        
        # Create datasets
        train_dataset = TextDataset(train_texts, train_labels, tokenizer)
        val_dataset = TextDataset(val_texts, val_labels, tokenizer)
        
        train_loader = DataLoader(
            train_dataset,
            batch_size=config['batch_size'],
            shuffle=True
        )
        val_loader = DataLoader(
            val_dataset,
            batch_size=config['batch_size']
        )
        
        # Optimizer
        optimizer = AdamW(model.parameters(), lr=config['learning_rate'])
        
        # Training loop
        for epoch in range(config['epochs']):
            # Update status
            status_dict[code]['status'] = 'training'
            status_dict[code]['epoch'] = epoch + 1
            status_dict[code]['total_epochs'] = config['epochs']
            
            # Train
            model.train()
            train_loss = 0
            for batch in train_loader:
                optimizer.zero_grad()
                
                input_ids = batch['input_ids'].to(config.DEVICE)
                attention_mask = batch['attention_mask'].to(config.DEVICE)
                labels = batch['labels'].to(config.DEVICE)
                
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            # Validation
            model.eval()
            val_correct = 0
            val_total = 0
            with torch.no_grad():
                for batch in val_loader:
                    input_ids = batch['input_ids'].to(config.DEVICE)
                    attention_mask = batch['attention_mask'].to(config.DEVICE)
                    labels = batch['labels'].to(config.DEVICE)
                    
                    outputs = model(
                        input_ids=input_ids,
                        attention_mask=attention_mask
                    )
                    
                    predictions = torch.argmax(outputs.logits, dim=1)
                    val_correct += (predictions == labels).sum().item()
                    val_total += labels.size(0)
            
            val_accuracy = val_correct / val_total
            
            # Update progress
            progress = int(((epoch + 1) / config['epochs']) * 100)
            status_dict[code]['progress'] = progress
            status_dict[code]['val_accuracy'] = val_accuracy
            status_dict[code]['train_loss'] = train_loss / len(train_loader)
        
        # Save model
        save_path = os.path.join(config.CUSTOM_MODELS_DIR, code)
        os.makedirs(save_path, exist_ok=True)
        
        model.save_pretrained(save_path)
        tokenizer.save_pretrained(save_path)
        
        # Save metadata
        metadata = {
            'name': config['name'],
            'base_model': config['base_model'],
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=7)).isoformat(),
            'config': config
        }
        with open(os.path.join(save_path, 'metadata.json'), 'w') as f:
            json.dump(metadata, f)
        
        # Final status
        status_dict[code]['status'] = 'completed'
        status_dict[code]['progress'] = 100
        
    except Exception as e:
        status_dict[code]['status'] = 'failed'
        status_dict[code]['error'] = str(e)
```

### 5.4 GPU Management

#### 5.4.1 gpu_utils.py

```python
import torch

def get_optimal_device():
    """Odabire najbolji dostupan uređaj"""
    if torch.cuda.is_available():
        # Ako ima više GPU-ova, odaberi onaj s najviše memorije
        if torch.cuda.device_count() > 1:
            max_mem = 0
            best_device = 0
            for i in range(torch.cuda.device_count()):
                mem = torch.cuda.get_device_properties(i).total_memory
                if mem > max_mem:
                    max_mem = mem
                    best_device = i
            return f'cuda:{best_device}'
        return 'cuda:0'
    return 'cpu'

def get_torch_device():
    """Vraća torch.device objekt"""
    device_str = get_optimal_device()
    return torch.device(device_str)

def monitor_gpu_memory():
    """Ispisuje GPU memory usage"""
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            allocated = torch.cuda.memory_allocated(i) / 1024**3
            reserved = torch.cuda.memory_reserved(i) / 1024**3
            total = torch.cuda.get_device_properties(i).total_memory / 1024**3
            print(f"GPU {i}: {allocated:.2f}GB / {total:.2f}GB")
```

### 5.5 Error Handling

**Centralizirano rukovanje greškama:**

```python
@app.errorhandler(Exception)
def handle_exception(e):
    """Global exception handler"""
    import traceback
    
    # Log error
    print(f"Error: {str(e)}")
    print(traceback.format_exc())
    
    # Return JSON response
    return jsonify({
        'error': 'Internal server error',
        'message': str(e) if app.debug else 'Something went wrong'
    }), 500
```

### 5.6 Performanse

**Optimizacije:**

1. **Model caching:** Modeli se ne učitavaju svaki put
2. **GPU usage:** Automatska detekcija i korištenje
3. **Batch processing:** Za više tekstova odjednom
4. **Memory management:** Explicit `torch.cuda.empty_cache()`

---

## 6. MODELI I ALGORITMI

### 6.1 Pretrenrani modeli

Sustav koristi 6 pretreniranih modela za različite domene:

| Model Key | Arhitektura | Domena | Parametri | Točnost |
|-----------|-------------|--------|-----------|---------|
| bert-covid-1 | BERT Base | COVID-19 | 110M | ~85% |
| bert-climate-change-1 | BERT Base | Climate Change | 110M | ~83% |
| bert-combined-1 | BERT Base | Combined | 110M | ~82% |
| deberta-covid-1 | DeBERTa v3 | COVID-19 | 86M | ~87% |
| deberta-climate-change-1 | DeBERTa v3 | Climate Change | 86M | ~85% |
| deberta-combined-1 | DeBERTa v3 | Combined | 86M | ~84% |

### 6.2 BERT (Bidirectional Encoder Representations from Transformers)

**Arhitektura:**
- 12 transformer encoder layera
- 768 hidden size
- 12 attention heads
- 512 max sequence length
- WordPiece tokenizacija (30,000 vocabulary)

**Prednosti:**
- Dobro razumijevanje konteksta
- Bidirekcijska pažnja
- Široka primjena u NLP zadacima
- Brz inference

**Nedostaci:**
- Manji od DeBERTa
- Manje sofisticirana pažnja

### 6.3 DeBERTa (Decoding-enhanced BERT with Disentangled Attention)

**Arhitektura:**
- Disentangled attention mehanizam
- Enhanced mask decoder
- Absolute position embedding nakon dekodiranja
- Bolje modeliranje relativnih pozicija

**Prednosti:**
- Bolji performans od BERT-a
- Bolje razumijevanje strukture rečenice
- Viša točnost na složenijim zadacima

**Nedostaci:**
- Sporiji inference od BERT-a
- Veća memorijska potrošnja

### 6.4 Dostupni base modeli za fine-tuning

| Model | Parametri | Brzina | Memorija | Preporuka |
|-------|-----------|--------|----------|-----------|
| bert-base-uncased | 110M | Srednja | 2GB | Opći zadaci |
| microsoft/deberta-v3-base | 86M | Sporija | 2.5GB | Visoka točnost |
| roberta-base | 125M | Srednja | 2.2GB | Robustan model |
| albert-base-v2 | 12M | Brza | 0.5GB | Mali dataseti |
| distilbert-base-uncased | 66M | Brza | 1GB | Brzi inference |

### 6.5 Transfer Learning proces

```
1. Pretreniranje (već gotovo)
   ├─ Učenje na milijunima tekstova
   ├─ Razumijevanje jezika i konteksta
   └─ Općenito znanje

2. Fine-tuning (korisnik radi)
   ├─ Prilagodba na specifičnu domenu
   ├─ Učenje na označenim podatcima
   └─ Specijalizirano znanje

3. Inference (produkcija)
   ├─ Brza klasifikacija
   ├─ Nema potrebe za dodatnim treniranjem
   └─ Direktna primjena
```

### 6.6 Objašnjivost - LIME

**LIME (Local Interpretable Model-agnostic Explanations)**

**Princip rada:**
1. Uzima originalni tekst
2. Generira perturbacije (modificirane verzije)
3. Dobiva predikcije za perturbacije
4. Trenira linearni model na perturbacijama
5. Identificira najvažnije riječi

**Implementacija:**

```python
from lime.lime_text import LimeTextExplainer

explainer = LimeTextExplainer(class_names=['deceptive', 'truthful'])

def predict_proba(texts):
    """Wrapper funkcija za model"""
    predictions = []
    for text in texts:
        result = predict_text(text, model_key)
        predictions.append([
            1 - result['confidence'],  # deceptive
            result['confidence']        # truthful
        ])
    return np.array(predictions)

# Generiranje objašnjenja
explanation = explainer.explain_instance(
    text,
    predict_proba,
    num_features=20,
    num_samples=1000
)

# Ekstrakcija važnosti riječi
word_importances = explanation.as_list()
```

**Output format:**
```json
{
  "lime_explanation": [
    ["vaccine", 0.45],
    ["safe", 0.32],
    ["effective", -0.28],
    ["risk", -0.15]
  ]
}
```

### 6.7 Objašnjivost - SHAP

**SHAP (SHapley Additive exPlanations)**

**Princip rada:**
- Baziran na teoriji igara (Shapley values)
- Mjeri doprinos svake riječi predikciji
- Zadovoljava svojstva: efikasnost, simetričnost, dummy, additivnost

**Implementacija:**

```python
import shap

# Kreiranje explainera
explainer = shap.Explainer(model, tokenizer)

# Generiranje objašnjenja
shap_values = explainer([text])

# Ekstrakcija vrijednosti
words = tokenizer.tokenize(text)
values = shap_values.values[0]

word_shap_pairs = list(zip(words, values))
```

**Output format:**
```json
{
  "shap_explanation": [
    ["vaccine", 0.52],
    ["proven", 0.38],
    ["dangerous", -0.41],
    ["unverified", -0.33]
  ]
}
```

### 6.8 Training algoritam

**Proces treniranja:**

```python
# 1. Priprema podataka
texts, labels = load_csv_data(file)
train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts, labels, 
    test_size=validation_split
)

# 2. Tokenizacija
train_encodings = tokenizer(train_texts, truncation=True, padding=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True)

# 3. Kreiranje dataseta
train_dataset = TextDataset(train_encodings, train_labels)
val_dataset = TextDataset(val_encodings, val_labels)

# 4. Optimizer i scheduler
optimizer = AdamW(model.parameters(), lr=learning_rate)
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=0,
    num_training_steps=len(train_loader) * epochs
)

# 5. Training loop
for epoch in range(epochs):
    model.train()
    for batch in train_loader:
        optimizer.zero_grad()
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        scheduler.step()
    
    # Validation
    model.eval()
    val_accuracy = evaluate(model, val_loader)
    
    # Save checkpoint if best
    if val_accuracy > best_accuracy:
        save_model(model, tokenizer, save_path)
        best_accuracy = val_accuracy
```

**Hiperparametri:**

| Parametar | Default | Raspon | Opis |
|-----------|---------|--------|------|
| Learning rate | 2e-5 | 1e-6 - 1e-4 | Brzina učenja |
| Batch size | 16 | 4 - 32 | Broj uzoraka po batch-u |
| Epochs | 3 | 1 - 10 | Broj prolaza kroz podatke |
| Warmup steps | 0 | 0 - 1000 | Postepeno povećanje LR |
| Weight decay | 0.01 | 0 - 0.1 | L2 regularizacija |
| Max seq length | 512 | 128 - 512 | Maks duljina tokena |

### 6.9 Evaluacijske metrike

**Metrike tijekom treniranja:**

```python
# Accuracy
accuracy = correct_predictions / total_predictions

# Precision
precision = true_positives / (true_positives + false_positives)

# Recall
recall = true_positives / (true_positives + false_negatives)

# F1 Score
f1 = 2 * (precision * recall) / (precision + recall)

# Loss
cross_entropy_loss = -sum(y_true * log(y_pred))
```

**Konfuzijska matrica:**

```
                Predicted
              Decept  Truth
Actual Decept   TP      FN
       Truth    FP      TN
```

### 6.10 Optimizacije

**Model optimizacije:**

1. **Mixed Precision Training:**
   ```python
   from torch.cuda.amp import autocast, GradScaler
   
   scaler = GradScaler()
   with autocast():
       outputs = model(**batch)
       loss = outputs.loss
   scaler.scale(loss).backward()
   ```

2. **Gradient Accumulation:**
   ```python
   accumulation_steps = 4
   for i, batch in enumerate(train_loader):
       loss = model(**batch).loss / accumulation_steps
       loss.backward()
       if (i + 1) % accumulation_steps == 0:
           optimizer.step()
           optimizer.zero_grad()
   ```

3. **Model Pruning:** Buduća implementacija

4. **Quantization:** Buduća implementacija

---

## 7. BAZA PODATAKA I POHRANA

### 7.1 Struktura pohrane

Sustav **ne koristi klasičnu relacijsku bazu podataka**. Umjesto toga, koristi **file-based storage** s JSON metapodatcima.

```
webapp/
└── backend/
    ├── models/                      # Pre-trained modeli (statični)
    │   └── [model-name]/
    │       ├── config.json
    │       ├── model.safetensors
    │       ├── tokenizer_config.json
    │       ├── tokenizer.json
    │       └── vocab.txt
    │
    ├── base_models/                 # Cache za base modele
    │   └── [model-name]/
    │       └── (isti format kao models/)
    │
    └── custom_models/               # User-trained modeli (dinamični)
        └── [6-char-code]/
            ├── config.json          # Model config
            ├── model.safetensors    # Težine modela
            ├── tokenizer_config.json
            ├── tokenizer.json
            ├── vocab.txt
            └── metadata.json        # Custom metadata
```

### 7.2 Metadata format

**metadata.json za custom modele:**

```json
{
  "name": "My Climate Model",
  "base_model": "bert-base-uncased",
  "created_at": "2025-11-03T14:30:00",
  "expires_at": "2025-11-10T14:30:00",
  "code": "abc123",
  "config": {
    "epochs": 3,
    "batch_size": 16,
    "learning_rate": 2e-5,
    "validation_split": 0.2
  },
  "metrics": {
    "final_accuracy": 0.87,
    "final_loss": 0.32,
    "training_time_seconds": 1234
  }
}
```

### 7.3 Upravljanje životnim ciklusom

**Automatsko brisanje isteklih modela:**

```python
import os
import json
from datetime import datetime

def cleanup_expired_models():
    """Briše modele starije od MODEL_EXPIRY_DAYS"""
    deleted_models = []
    
    for code in os.listdir(CUSTOM_MODELS_DIR):
        model_path = os.path.join(CUSTOM_MODELS_DIR, code)
        metadata_path = os.path.join(model_path, 'metadata.json')
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            expires_at = datetime.fromisoformat(metadata['expires_at'])
            
            if datetime.now() > expires_at:
                shutil.rmtree(model_path)
                deleted_models.append(code)
    
    return deleted_models
```

**Cleanup se izvršava:**
- Pri startu aplikacije
- Svakih 6 sati (scheduled task)
- Ručno putem `/api/training/cleanup` endpointa

### 7.4 ZIP arhive za download

**Struktura:**

```
model_abc123.zip
├── config.json
├── model.safetensors
├── tokenizer_config.json
├── tokenizer.json
├── vocab.txt
├── metadata.json
└── README.txt              # Upute za korištenje
```

**README.txt sadržaj:**

```
Deception Detector - Custom Model

Model: My Climate Model
Created: 2025-11-03 14:30:00
Base Model: bert-base-uncased

To use this model:

1. Install dependencies:
   pip install torch transformers

2. Load model:
   from transformers import AutoTokenizer, AutoModelForSequenceClassification
   
   tokenizer = AutoTokenizer.from_pretrained('./path/to/extracted/folder')
   model = AutoModelForSequenceClassification.from_pretrained('./path/to/extracted/folder')

3. Make predictions:
   inputs = tokenizer("Your text here", return_tensors="pt")
   outputs = model(**inputs)
   prediction = torch.argmax(outputs.logits, dim=1).item()
   
   # 0 = deceptive, 1 = truthful
```

### 7.5 Backup strategija

**Preporuke za produkciju:**

1. **Regular backups:**
   - Backup `custom_models/` svaki dan
   - Backup `base_models/` tjedno
   - Pretrained modeli ne trebaju backup (mogu se re-download)

2. **Cloud storage:**
   ```bash
   # Example: Sync to S3
   aws s3 sync ./backend/custom_models/ s3://bucket/custom_models/
   ```

3. **Version control:**
   - Ne stavljati modele u Git (preveliki)
   - Koristiti Git LFS ili DVC za tracking

### 7.6 Disk space management

**Procjena potrebnog prostora:**

| Komponenta | Veličina po modelu | Broj modela | Ukupno |
|------------|--------------------|-------------|--------|
| Pretrained modeli | ~400-500 MB | 6 | ~3 GB |
| Base models cache | ~400-500 MB | 5 | ~2.5 GB |
| Custom modeli | ~400-500 MB | Varijabilan | ~5-50 GB |
| ZIP arhive | ~400-500 MB | Privremeno | ~5-10 GB |

**Minimum:** 20 GB slobodnog prostora  
**Preporučeno:** 50+ GB za normalan rad

### 7.7 Buduća implementacija baze podataka

**PostgreSQL schema (prijedlog):**

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    code VARCHAR(6) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    base_model VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL,  -- training, completed, failed
    metadata JSONB
);

CREATE TABLE training_jobs (
    id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES models(id),
    status VARCHAR(20) NOT NULL,
    progress INTEGER DEFAULT 0,
    current_epoch INTEGER,
    metrics JSONB,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    model_code VARCHAR(6),
    text TEXT NOT NULL,
    prediction VARCHAR(20) NOT NULL,
    confidence FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 8. API SPECIFIKACIJA

### 8.1 Opće informacije

**Base URL:** `http://localhost:5000/api`  
**Format:** JSON  
**Authentication:** Trenutno nije implementirana  
**CORS:** Omogućen za sve origine (development)

### 8.2 Pre-trained Models API

#### 8.2.1 GET /api/models

**Opis:** Vraća listu dostupnih pretreniranih modela

**Request:**
```http
GET /api/models HTTP/1.1
Host: localhost:5000
```

**Response:** `200 OK`
```json
{
  "models": [
    {
      "key": "bert-covid-1",
      "name": "BERT COVID-19",
      "type": "bert",
      "domain": "covid-19"
    },
    {
      "key": "deberta-climate-change-1",
      "name": "DeBERTa Climate Change",
      "type": "deberta",
      "domain": "climate"
    }
  ]
}
```

#### 8.2.2 POST /api/predict

**Opis:** Analizira tekst i vraća predikciju

**Request:**
```http
POST /api/predict HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "text": "Climate change is a serious global threat that requires immediate action.",
  "model": "bert-climate-change-1"
}
```

**Response:** `200 OK`
```json
{
  "prediction": "truthful",
  "confidence": 0.8542,
  "original_text": "Climate change is a serious...",
  "model_used": "bert-climate-change-1"
}
```

**Error Responses:**

`400 Bad Request` - Nedostaju parametri
```json
{
  "error": "Missing required parameters: text, model"
}
```

`404 Not Found` - Model ne postoji
```json
{
  "error": "Model not found"
}
```

`500 Internal Server Error` - Greška pri inferenci
```json
{
  "error": "Prediction failed",
  "message": "Out of memory"
}
```

#### 8.2.3 POST /api/lime

**Opis:** Generira LIME objašnjenje za predikciju

**Request:**
```http
POST /api/lime HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "text": "Vaccines are dangerous and untested.",
  "model": "bert-covid-1"
}
```

**Response:** `200 OK`
```json
{
  "lime_explanation": [
    ["dangerous", -0.45],
    ["untested", -0.32],
    ["vaccines", 0.18],
    ["are", 0.05]
  ],
  "prediction": "deceptive",
  "confidence": 0.78
}
```

**Explanation format:**
- Tuple: `[word, importance]`
- Negativna vrijednost: riječ pridonosi "deceptive" klasifikaciji
- Pozitivna vrijednost: riječ pridonosi "truthful" klasifikaciji
- Vrijednost: apsolutna važnost (0.0 - 1.0)

#### 8.2.4 POST /api/shap

**Opis:** Generira SHAP objašnjenje za predikciju

**Request:**
```http
POST /api/shap HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "text": "Scientific studies confirm vaccine safety.",
  "model": "bert-covid-1"
}
```

**Response:** `200 OK`
```json
{
  "shap_explanation": [
    ["scientific", 0.52],
    ["confirm", 0.38],
    ["safety", 0.29],
    ["vaccine", 0.15],
    ["studies", 0.12]
  ],
  "prediction": "truthful",
  "confidence": 0.91
}
```

### 8.3 Custom Training API

#### 8.3.1 GET /api/training/models

**Opis:** Vraća dostupne base modele za fine-tuning

**Request:**
```http
GET /api/training/models HTTP/1.1
Host: localhost:5000
```

**Response:** `200 OK`
```json
{
  "models": [
    {
      "key": "bert-base-uncased",
      "name": "BERT Base (Uncased)",
      "parameters": "110M",
      "speed": "medium",
      "memory": "2GB"
    },
    {
      "key": "microsoft/deberta-v3-base",
      "name": "DeBERTa v3 Base",
      "parameters": "86M",
      "speed": "slow",
      "memory": "2.5GB"
    }
  ]
}
```

#### 8.3.2 POST /api/training/upload-csv

**Opis:** Validira CSV datoteku prije treniranja

**Request:**
```http
POST /api/training/upload-csv HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data

--boundary
Content-Disposition: form-data; name="file"; filename="data.csv"
Content-Type: text/csv

text,label
"This is true",1
"This is false",0
--boundary--
```

**Response:** `200 OK`
```json
{
  "valid": true,
  "rows": 1000,
  "columns": ["text", "label"],
  "label_distribution": {
    "0": 450,
    "1": 550
  },
  "sample_texts": [
    "This is true",
    "This is false"
  ],
  "warnings": []
}
```

**Error Response:** `400 Bad Request`
```json
{
  "valid": false,
  "error": "Missing required column: label",
  "details": "CSV must contain 'text' and 'label' columns"
}
```

#### 8.3.3 POST /api/training/start

**Opis:** Pokreće treniranje novog modela

**Request:**
```http
POST /api/training/start HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data

--boundary
Content-Disposition: form-data; name="file"; filename="data.csv"
Content-Type: text/csv

[CSV content]
--boundary
Content-Disposition: form-data; name="config"

{
  "base_model": "bert-base-uncased",
  "name": "My Custom Model",
  "epochs": 3,
  "batch_size": 16,
  "learning_rate": 2e-5,
  "validation_split": 0.2
}
--boundary--
```

**Response:** `200 OK`
```json
{
  "success": true,
  "model_code": "abc123",
  "message": "Training started for model abc123"
}
```

**Error Responses:**

`400 Bad Request` - Loši parametri
```json
{
  "error": "Invalid configuration",
  "details": "Batch size must be between 4 and 32"
}
```

`500 Internal Server Error` - Greška pri pokretanju
```json
{
  "error": "Failed to start training",
  "message": "Insufficient GPU memory"
}
```

#### 8.3.4 GET /api/training/status/:code

**Opis:** Provjerava status treniranja modela

**Request:**
```http
GET /api/training/status/abc123 HTTP/1.1
Host: localhost:5000
```

**Response (u tijeku):** `200 OK`
```json
{
  "status": "training",
  "progress": 65,
  "name": "My Custom Model",
  "base_model": "bert-base-uncased",
  "created_at": "2025-11-03T10:30:00",
  "expires_at": "2025-11-10T10:30:00",
  "remaining_time": "6 days, 12 hours",
  "current_epoch": 2,
  "total_epochs": 3,
  "train_loss": 0.324,
  "val_accuracy": 0.856,
  "estimated_completion": "2025-11-03T11:45:00"
}
```

**Response (završeno):** `200 OK`
```json
{
  "status": "completed",
  "progress": 100,
  "name": "My Custom Model",
  "base_model": "bert-base-uncased",
  "created_at": "2025-11-03T10:30:00",
  "expires_at": "2025-11-10T10:30:00",
  "completed_at": "2025-11-03T11:35:00",
  "final_metrics": {
    "accuracy": 0.872,
    "loss": 0.298,
    "precision": 0.865,
    "recall": 0.880,
    "f1_score": 0.872
  }
}
```

**Response (greška):** `200 OK`
```json
{
  "status": "failed",
  "error": "Out of memory during training",
  "name": "My Custom Model",
  "created_at": "2025-11-03T10:30:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "error": "Model not found",
  "code": "abc123"
}
```

#### 8.3.5 POST /api/training/cleanup

**Opis:** Ručno pokreće brisanje isteklih modela

**Request:**
```http
POST /api/training/cleanup HTTP/1.1
Host: localhost:5000
```

**Response:** `200 OK`
```json
{
  "deleted": ["abc123", "def456", "ghi789"],
  "count": 3,
  "freed_space_mb": 1250
}
```

### 8.4 Custom Model Usage API

#### 8.4.1 POST /api/custom/predict/:code

**Opis:** Vrši predikciju koristeći custom model

**Request:**
```http
POST /api/custom/predict/abc123 HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "text": "This is my custom text to analyze"
}
```

**Response:** `200 OK`
```json
{
  "prediction": "truthful",
  "confidence": 0.892,
  "original_text": "This is my custom text...",
  "model_code": "abc123",
  "model_name": "My Custom Model"
}
```

#### 8.4.2 POST /api/custom/download/init/:code

**Opis:** Inicijalizira preuzimanje modela i vraća download ID

**Request:**
```http
POST /api/custom/download/init/abc123 HTTP/1.1
Host: localhost:5000
```

**Response:** `200 OK`
```json
{
  "download_id": "550e8400-e29b-41d4-a716-446655440000",
  "model_code": "abc123",
  "estimated_size_mb": 450
}
```

#### 8.4.3 GET /api/custom/download/:code?download_id=:id

**Opis:** Preuzima ZIP arhivu modela

**Request:**
```http
GET /api/custom/download/abc123?download_id=550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:5000
```

**Response:** `200 OK`
```http
Content-Type: application/zip
Content-Disposition: attachment; filename="model_abc123.zip"
Content-Length: 471859200

[Binary ZIP data]
```

#### 8.4.4 GET /api/custom/download-progress/:id

**Opis:** Prati napredak kreiranja ZIP arhive

**Request:**
```http
GET /api/custom/download-progress/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:5000
```

**Response (u tijeku):** `200 OK`
```json
{
  "status": "creating",
  "progress": 45,
  "phase": "Compressing: model.safetensors (234/500 MB)",
  "elapsed_time": 12.5,
  "estimated_remaining": 15.3,
  "archive_size_mb": 234,
  "files_processed": 3,
  "total_files": 6
}
```

**Response (gotovo):** `200 OK`
```json
{
  "status": "ready",
  "progress": 100,
  "phase": "Complete",
  "elapsed_time": 27.8,
  "archive_size_mb": 450,
  "files_processed": 6,
  "total_files": 6
}
```

### 8.5 Rate Limiting (buduća implementacija)

**Planirani limiti:**

| Endpoint | Limit | Window |
|----------|-------|--------|
| /api/predict | 100 zahtjeva | 1 sat |
| /api/training/start | 5 zahtjeva | 1 dan |
| /api/custom/download | 10 zahtjeva | 1 sat |

### 8.6 Webhooks (buduća implementacija)

**Training completion webhook:**

```json
POST https://your-server.com/webhook/training-complete
Content-Type: application/json

{
  "event": "training.completed",
  "model_code": "abc123",
  "status": "completed",
  "metrics": {
    "accuracy": 0.872
  },
  "timestamp": "2025-11-03T11:35:00Z"
}
```

---

## 9. SIGURNOST I AUTENTIFIKACIJA

### 9.1 Trenutno stanje

**Napomena:** Sustav trenutno **ne implementira autentifikaciju korisnika**. Svi korisnici mogu:
- Koristiti pretreniranje modele bez ograničenja
- Trenirati vlastite modele
- Preuzimati modele pomoću 6-znamenkastog koda

### 9.2 Sigurnosne mjere

#### 9.2.1 Input validacija

**Backend validacija:**

```python
def validate_text_input(text):
    """Validira tekstualni unos"""
    if not text or not isinstance(text, str):
        raise ValueError("Text must be a non-empty string")
    
    if len(text) > 10000:  # ~1300 riječi
        raise ValueError("Text too long")
    
    # Sanitizacija
    text = text.strip()
    return text

def validate_csv_file(file):
    """Validira CSV upload"""
    # Provjera ekstenzije
    if not file.filename.endswith('.csv'):
        raise ValueError("File must be CSV")
    
    # Provjera veličine (max 100MB)
    file.seek(0, os.SEEK_END)
    size = file.tell()
    if size > 100 * 1024 * 1024:
        raise ValueError("File too large (max 100MB)")
    
    file.seek(0)
    return file
```

#### 9.2.2 CORS konfiguracija

**Development:**
```python
from flask_cors import CORS

# Dopušta sve origine
CORS(app)
```

**Production (preporuka):**
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

#### 9.2.3 File upload sigurnost

```python
from werkzeug.utils import secure_filename

def secure_file_upload(file):
    """Sigurno rukovanje uploadanim datotekama"""
    # Sigurno ime datoteke
    filename = secure_filename(file.filename)
    
    # Random naziv za pohranu
    random_name = str(uuid.uuid4()) + '.csv'
    
    # Pohrana u privremeni direktorij
    temp_path = os.path.join('/tmp', random_name)
    file.save(temp_path)
    
    return temp_path
```

#### 9.2.4 Model code sigurnost

**Generiranje koda:**
```python
import random
import string

def generate_model_code():
    """Generira siguran 6-znamenkasti kod"""
    # Koristi lowercase i brojeve (bez uppercase za izbjegavanje zabune)
    chars = string.ascii_lowercase + string.digits
    code = ''.join(random.choices(chars, k=6))
    
    # Provjeri da nije duplicate
    while os.path.exists(os.path.join(CUSTOM_MODELS_DIR, code)):
        code = ''.join(random.choices(chars, k=6))
    
    return code
```

**Prostor kodova:** 36^6 = 2,176,782,336 mogućih kombinacija

### 9.3 Buduća autentifikacija

#### 9.3.1 JWT autentifikacija (prijedlog)

```python
from flask_jwt_extended import JWTManager, create_access_token

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

@app.route('/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Provjera kredencijala
    user = authenticate(username, password)
    if not user:
        return {'error': 'Invalid credentials'}, 401
    
    # Generiraj token
    access_token = create_access_token(identity=user.id)
    return {'access_token': access_token}

@app.route('/api/predict', methods=['POST'])
@jwt_required()
def predict():
    current_user = get_jwt_identity()
    # ...
```

#### 9.3.2 OAuth 2.0 integracija (prijedlog)

**Google OAuth:**
```python
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/auth/google')
def google_login():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)
```

### 9.4 Rate limiting (prijedlog)

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/predict', methods=['POST'])
@limiter.limit("100 per hour")
def predict():
    # ...

@app.route('/api/training/start', methods=['POST'])
@limiter.limit("5 per day")
def start_training():
    # ...
```

### 9.5 HTTPS u produkciji

**Nginx konfiguracija s SSL:**

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Redirect HTTP to HTTPS
    if ($scheme != "https") {
        return 301 https://$server_name$request_uri;
    }
    
    location / {
        root /var/www/deception-detector/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 9.6 Sigurnost podataka

#### 9.6.1 Osjetljivi podatci

**Što NE spremamo:**
- Email adrese (bez auth sustava)
- Lozinke (bez auth sustava)
- Kreditne kartice
- Osobne identifikacijske podatke

**Što spremamo:**
- Tekstove za analizu (privremeno u memoriji)
- CSV podatke za treniranje (privremeno)
- Trenirane modele (7 dana)
- Model kodove (6-znamenkasti)

#### 9.6.2 GDPR compliance (buduće)

**Prava korisnika:**
- Pravo na pristup (izvoz podataka)
- Pravo na brisanje (delete account)
- Pravo na ispravljanje
- Pravo na prenosivost podataka

**Implementacija:**
```python
@app.route('/api/user/data', methods=['GET'])
@jwt_required()
def get_user_data():
    """Izvozi sve podatke korisnika"""
    user_id = get_jwt_identity()
    data = {
        'models': get_user_models(user_id),
        'predictions': get_user_predictions(user_id),
        'created_at': get_user_created_at(user_id)
    }
    return jsonify(data)

@app.route('/api/user/delete', methods=['DELETE'])
@jwt_required()
def delete_user():
    """Briše korisnički račun i sve podatke"""
    user_id = get_jwt_identity()
    delete_user_models(user_id)
    delete_user_predictions(user_id)
    delete_user_account(user_id)
    return {'message': 'Account deleted'}
```

---

## 10. KORISNIČKO SUČELJE

### 10.1 Navigacija

![Screenshot: Navigacija] (TODO: Dodati screenshot)

**Glavna navigacijska traka:**
- Logo (lijevo)
- Tri taba (desno):
  - **Analysis** - Analiza s pretreniranim modelima
  - **Fine-tuning** - Treniranje vlastitih modela
  - **Model Access** - Pristup i download vlastitih modela

**UX principi:**
- Jednostavnost: Maksimalno 3 klika do bilo koje funkcionalnosti
- Dosljednost: Isti dizajn elemenata kroz cijelu aplikaciju
- Feedback: Trenutne povratne informacije za sve akcije
- Tolerancija grešaka: Jasne poruke o greškama s uputama

### 10.2 Analysis View

![Screenshot: Analysis Input] (TODO: Dodati screenshot)

**Input forma:**
- Textarea za unos teksta (autoresize, min 3 reda)
- Character counter (0 / ~8000)
- Model selector dropdown
- "Analyze Text" gumb (disabled dok nema teksta)

**UX detalji:**
- Placeholder text s primjerom
- Tooltips na hover (objašnjenja modela)
- Validacija u stvarnom vremenu
- Loading state tijekom analize

![Screenshot: Results] (TODO: Dodati screenshot)

**Prikaz rezultata:**

```
┌─────────────────────────────────────┐
│  PREDICTION                         │
│  ◉ Truthful                   85.4% │
│  ○ Deceptive                  14.6% │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  ORIGINAL TEXT                      │
│  Climate change is a serious...     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  EXPLANATIONS                       │
│  ┌─────────┬──────────┐            │
│  │  LIME   │   SHAP   │            │
│  └─────────┴──────────┘            │
│  [Colored text with highlights]    │
└─────────────────────────────────────┘
```

### 10.3 Training View

![Screenshot: CSV Upload] (TODO: Dodati screenshot)

**Upload sekcija:**
- Drag & drop zona
- Ili "Browse files" gumb
- Validacija odmah nakon uploada
- Prikaz statistike:
  ```
  ✓ Valid CSV format
  📊 1,000 rows
  📈 Distribution: 45% deceptive, 55% truthful
  📝 Sample texts: "This is...", "Another..."
  ```

![Screenshot: Configuration] (TODO: Dodati screenshot)

**Konfiguracija parametara:**

```
Base Model:         [Dropdown: BERT, DeBERTa, etc.]
Model Name:         [Input: My Climate Model       ]

Training Settings:
  Epochs:           [Slider: 1 ───●─── 10] 3
  Batch Size:       [Slider: 4 ──●──── 32] 16
  Learning Rate:    [Input: 2e-5              ]
  Validation Split: [Slider: 10% ──●── 30%] 20%

Estimated training time: ~15 minutes
```

**Advanced options (collapsible):**
- Weight decay
- Warmup steps
- Max sequence length
- Gradient accumulation

![Screenshot: Training Progress] (TODO: Dodati screenshot)

**Training progress modal:**

```
┌──────────────────────────────────────┐
│  Training: My Climate Model          │
│  Code: abc123 (SAVE THIS!)           │
├──────────────────────────────────────┤
│  Progress: ████████░░ 80%            │
│  Status: Training                    │
│  Epoch: 2 / 3                        │
│                                      │
│  Metrics:                            │
│  • Training Loss: 0.324              │
│  • Validation Accuracy: 85.6%        │
│                                      │
│  Time Remaining: ~3 minutes          │
└──────────────────────────────────────┘
```

### 10.4 Custom Model View

![Screenshot: Model Access] (TODO: Dodati screenshot)

**Code input:**

```
┌──────────────────────────────────────┐
│  Enter your 6-digit model code       │
│                                      │
│  ┌────────────────┐                 │
│  │  a b c 1 2 3   │  [Access Model] │
│  └────────────────┘                 │
└──────────────────────────────────────┘
```

**Model info card:**

```
┌──────────────────────────────────────┐
│  📦 My Climate Model                 │
│  ────────────────────────────────    │
│  Base: bert-base-uncased             │
│  Created: 2025-11-03 14:30          │
│  Expires: 2025-11-10 14:30          │
│  Status: ✅ Ready                     │
│                                      │
│  [Analyze Text]  [Download Model]   │
└──────────────────────────────────────┘
```

![Screenshot: Download Progress] (TODO: Dodati screenshot)

**Download progress:**

```
┌──────────────────────────────────────┐
│  📥 Downloading Model                │
├──────────────────────────────────────┤
│  Progress: ██████████░░ 65%         │
│  Phase: Compressing model.safetensors│
│         (234 / 500 MB)               │
│                                      │
│  Files: 3 / 6 completed              │
│  Time: 12s elapsed, ~15s remaining   │
│                                      │
│  [Cancel Download]                   │
└──────────────────────────────────────┘
```

### 10.5 Responzivni dizajn

**Mobile (< 768px):**
- Stack-ana navigacija (hamburger menu)
- Vertikalno slaganje elemenata
- Veći gumbi (min 44px touch target)
- Simplificiran prikaz tablice

**Tablet (768px - 1024px):**
- 2-kolumnski layout gdje je moguće
- Optimizirane širine inputa
- Prilagođena veličina fontova

**Desktop (> 1024px):**
- Puni 3-kolumnski layout
- Side-by-side usporedbe (LIME vs SHAP)
- Hover efekti i tooltips

### 10.6 Accessibility (A11y)

**Implementirane značajke:**

```vue
<!-- Semantički HTML -->
<nav role="navigation" aria-label="Main navigation">
  <button 
    role="tab" 
    :aria-selected="activeTab === 'analysis'"
    @click="switchTab('analysis')"
  >
    Analysis
  </button>
</nav>

<!-- Keyboard navigation -->
<button 
  @keydown.enter="submitForm"
  @keydown.space.prevent="submitForm"
  tabindex="0"
>
  Analyze Text
</button>

<!-- Screen reader text -->
<span class="sr-only">Loading analysis results</span>

<!-- ARIA live regions -->
<div 
  role="status" 
  aria-live="polite" 
  aria-atomic="true"
>
  {{ statusMessage }}
</div>
```

**Color contrast:**
- WCAG AA compliance
- Minimum 4.5:1 za normalan tekst
- Minimum 3:1 za veliki tekst i UI komponente

**Keyboard shortcuts:**
- Tab: Navigacija kroz elemente
- Enter: Submit forme
- Escape: Zatvaranje modala
- Arrow keys: Navigacija kroz dropdown

### 10.7 Error states

**Prikaz grešaka:**

```
┌──────────────────────────────────────┐
│  ⚠️ Error                            │
│  Failed to analyze text              │
│                                      │
│  The backend server is not responding│
│  Please check that the backend is    │
│  running on port 5000.               │
│                                      │
│  [Try Again]  [Go Back]              │
└──────────────────────────────────────┘
```

**Empty states:**

```
┌──────────────────────────────────────┐
│          📭                          │
│     No models found                  │
│                                      │
│  Your custom models will appear here │
│  after you train them in the         │
│  Fine-tuning tab.                    │
│                                      │
│  [Start Training]                    │
└──────────────────────────────────────┘
```

---

## 11. INSTALACIJA I KONFIGURACIJA

### 11.1 Preduvjeti

| Komponenta | Minimalna verzija | Preporučena verzija | Svrha |
|------------|-------------------|---------------------|-------|
| Python | 3.8+ | 3.10+ | Backend izvršavanje |
| Node.js | 14.x | 18.x LTS | Frontend build |
| npm/yarn | 6.x / 1.22.x | 8.x / 1.22.x | Dependency management |
| Git | 2.x | 2.40+ | Version control |
| CUDA | 11.1+ | 11.8+ | GPU podrška (optional) |

**Hardware preporuke:**

| Komponenta | Minimum | Preporučeno | Napomena |
|------------|---------|-------------|----------|
| RAM | 8 GB | 16 GB+ | Za treniranje 32 GB+ |
| CPU | 4 cores | 8+ cores | Za CPU inference |
| GPU | - | NVIDIA 8GB+ VRAM | Značajno ubrzava treniranje |
| Disk | 10 GB | 50 GB+ | Modeli zauzimaju ~3GB |

### 11.2 Instalacija - Windows

**1. Preuzimanje projekta:**

```powershell
# Clone repository
git clone https://github.com/yourusername/deception-detector.git
cd deception-detector\webapp
```

**2. Backend setup:**

```powershell
# Kreiraj virtualenv
python -m venv venv

# Aktiviraj virtualenv
.\venv\Scripts\Activate.ps1

# Instaliraj dependencies
cd backend
pip install -r requirements.txt
```

**3. Download modela:**

```powershell
# Automatski download svih pretreniranih modela
python download_models.py

# Ili koristi batch skriptu
.\download-models.bat
```

**4. Frontend setup:**

```powershell
# Otvori novi terminal
cd frontend

# Instaliraj dependencies
npm install

# Ili koristi yarn
yarn install
```

**5. Pokretanje:**

```powershell
# Terminal 1: Backend
cd backend
.\venv\Scripts\Activate.ps1
python app.py

# Terminal 2: Frontend
cd frontend
npm run serve
```

Aplikacija će biti dostupna na `http://localhost:8080`.

### 11.3 Instalacija - Linux/macOS

**1. Preuzimanje projekta:**

```bash
# Clone repository
git clone https://github.com/yourusername/deception-detector.git
cd deception-detector/webapp
```

**2. Backend setup:**

```bash
# Kreiraj virtualenv
python3 -m venv venv

# Aktiviraj virtualenv
source venv/bin/activate

# Instaliraj dependencies
cd backend
pip install -r requirements.txt
```

**3. Download modela:**

```bash
# Automatski download
python3 download_models.py
```

**4. Frontend setup:**

```bash
# Novi terminal
cd frontend
npm install
```

**5. Pokretanje:**

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python app.py

# Terminal 2: Frontend
cd frontend
npm run serve
```

### 11.4 Docker instalacija (opciono)

**Dockerfile - Backend:**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ .
COPY download_models.py .

# Download models
RUN python download_models.py

EXPOSE 5000

CMD ["python", "app.py"]
```

**Dockerfile - Frontend:**

```dockerfile
FROM node:18-alpine AS build

WORKDIR /app

# Install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Build app
COPY frontend/ .
RUN npm run build

# Production server
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend/models:/app/models
      - ./backend/custom_models:/app/custom_models
    environment:
      - FLASK_ENV=production
      - CUDA_VISIBLE_DEVICES=0
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

**Pokretanje Docker kontejnera:**

```bash
# Build i pokreni
docker-compose up -d

# Provjeri status
docker-compose ps

# Logovi
docker-compose logs -f

# Zaustavi
docker-compose down
```

### 11.5 Konfiguracija

#### 11.5.1 Backend konfiguracija

**backend/config.py:**

```python
import os

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
CUSTOM_MODELS_DIR = os.path.join(BASE_DIR, 'custom_models')

# === Device ===
# Auto-detect GPU
import torch
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# Ručno postavljanje:
# DEVICE = 'cpu'  # Prisili CPU
# DEVICE = 'cuda:0'  # Prisili specifični GPU

# === Model Defaults ===
MAX_LENGTH = 512  # Maksimalna duljina tokena
BATCH_SIZE = 16  # Za batch inference

# === Training Defaults ===
DEFAULT_EPOCHS = 3
DEFAULT_BATCH_SIZE = 16
DEFAULT_LEARNING_RATE = 2e-5
VALIDATION_SPLIT = 0.2

# === Custom Models ===
MODEL_EXPIRATION_DAYS = 7
MAX_CUSTOM_MODELS = 100  # Limit broja custom modela

# === LIME/SHAP ===
LIME_NUM_SAMPLES = 1000
SHAP_MAX_SAMPLES = 100

# === Flask ===
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True  # False u produkciji
```

**Environment varijable (.env):**

```bash
# Flask
FLASK_ENV=development
FLASK_DEBUG=1

# Device
CUDA_VISIBLE_DEVICES=0

# Paths
MODELS_DIR=/path/to/models
CUSTOM_MODELS_DIR=/path/to/custom_models

# Training
MAX_EPOCHS=10
DEFAULT_BATCH_SIZE=16
```

**Učitavanje .env:**

```python
from dotenv import load_dotenv
import os

load_dotenv()

FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
DEVICE = os.getenv('CUDA_VISIBLE_DEVICES', 'cpu')
```

#### 11.5.2 Frontend konfiguracija

**frontend/src/config.js:**

```javascript
// API Base URL
export const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000';

// API Endpoints
export const API_ENDPOINTS = {
  // Pretrained models
  models: '/api/models',
  predict: '/api/predict',
  lime: '/api/lime',
  shap: '/api/shap',
  
  // Training
  trainingModels: '/api/training/models',
  uploadCsv: '/api/training/upload-csv',
  startTraining: '/api/training/start',
  trainingStatus: '/api/training/status',
  cleanup: '/api/training/cleanup',
  
  // Custom models
  customPredict: '/api/custom/predict',
  downloadInit: '/api/custom/download/init',
  download: '/api/custom/download',
  downloadProgress: '/api/custom/download-progress'
};

// UI Configuration
export const UI_CONFIG = {
  maxTextLength: 8000,
  pollInterval: 2000,  // ms za status polling
  downloadPollInterval: 500,  // ms za download progress
  toastDuration: 5000  // ms za toast messages
};

// Theme
export const THEME = {
  primaryColor: '#FE483E',
  darkNavy: '#213544',
  gradients: {
    primary: 'linear-gradient(135deg, #FE483E 0%, #FF6B63 100%)',
    navbar: 'linear-gradient(to right, #ffffff 0%, #f8f9fa 100%)'
  }
};
```

**Environment varijable (.env.development):**

```bash
VUE_APP_API_URL=http://localhost:5000
VUE_APP_ENABLE_MOCK=false
```

**Environment varijable (.env.production):**

```bash
VUE_APP_API_URL=https://api.yourdomain.com
VUE_APP_ENABLE_ANALYTICS=true
```

### 11.6 Verifikacija instalacije

**Test skripta (test_setup.py):**

```python
import torch
import transformers
import flask
import flask_cors
import lime
import shap
import os

def test_setup():
    print("=== Testing Setup ===\n")
    
    # 1. Python verzija
    import sys
    print(f"✓ Python: {sys.version.split()[0]}")
    
    # 2. PyTorch
    print(f"✓ PyTorch: {torch.__version__}")
    print(f"  CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  CUDA version: {torch.version.cuda}")
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
    
    # 3. Transformers
    print(f"✓ Transformers: {transformers.__version__}")
    
    # 4. Flask
    print(f"✓ Flask: {flask.__version__}")
    
    # 5. XAI libraries
    print(f"✓ LIME: {lime.__version__}")
    print(f"✓ SHAP: {shap.__version__}")
    
    # 6. Models directory
    models_dir = './backend/models'
    if os.path.exists(models_dir):
        models = [d for d in os.listdir(models_dir) 
                  if os.path.isdir(os.path.join(models_dir, d))]
        print(f"✓ Models: {len(models)} found")
        for model in models:
            print(f"  - {model}")
    else:
        print("✗ Models directory not found!")
    
    print("\n=== Setup Complete ===")

if __name__ == '__main__':
    test_setup()
```

**Pokretanje:**

```bash
python test_setup.py
```

**Očekivani output:**

```
=== Testing Setup ===

✓ Python: 3.10.8
✓ PyTorch: 2.0.1
  CUDA available: True
  CUDA version: 11.8
  GPU: NVIDIA GeForce RTX 3080
✓ Transformers: 4.30.2
✓ Flask: 2.3.2
✓ LIME: 0.2.0.1
✓ SHAP: 0.42.1
✓ Models: 6 found
  - bert-climate-change-1
  - bert-combined-1
  - bert-covid-1
  - deberta-climate-change-1
  - deberta-combined-1
  - deberta-covid-1

=== Setup Complete ===
```

### 11.7 Troubleshooting

#### 11.7.1 PyTorch CUDA problemi

**Problem:** `RuntimeError: CUDA out of memory`

**Rješenje:**
```python
# Smanji batch size u config.py
DEFAULT_BATCH_SIZE = 8  # Umjesto 16

# Ili forsaj CPU
DEVICE = 'cpu'
```

**Problem:** `torch.cuda.is_available() = False`

**Rješenje:**
```bash
# Provjeri CUDA instalaciju
nvidia-smi

# Reinstaliraj PyTorch s CUDA
pip uninstall torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### 11.7.2 Model download problemi

**Problem:** `ConnectionError: Failed to download model`

**Rješenje:**
```python
# Povećaj timeout u download_models.py
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained(
    'bert-base-uncased',
    cache_dir='./models',
    resume_download=True,  # Nastavi prekinuti download
    force_download=False,  # Ne preuzimaj ponovno
    timeout=300  # 5 minuta timeout
)
```

#### 11.7.3 Frontend CORS problemi

**Problem:** `CORS policy: No 'Access-Control-Allow-Origin' header`

**Rješenje:**
```python
# backend/app.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

#### 11.7.4 Port zauzet

**Problem:** `Address already in use: 5000`

**Rješenje:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:5000 | xargs kill -9

# Ili promijeni port u backend/app.py
app.run(host='0.0.0.0', port=5001)
```

---

## 12. TESTIRANJE

### 12.1 Test strategija

```
┌─────────────────────────────────────────┐
│         Test Piramida                   │
├─────────────────────────────────────────┤
│              E2E Tests                  │
│         (Selenium, Cypress)             │
│                                         │
│         Integration Tests               │
│       (API endpoints, flows)            │
│                                         │
│           Unit Tests                    │
│      (Functions, components)            │
│                                         │
│         Static Analysis                 │
│     (Linting, type checking)            │
└─────────────────────────────────────────┘
```

### 12.2 Unit testovi

#### 12.2.1 Backend unit testovi

**backend/tests/test_ai_utils.py:**

```python
import unittest
import torch
from ai_utils import load_model, predict_text

class TestAIUtils(unittest.TestCase):
    
    def setUp(self):
        """Setup before each test"""
        self.model_name = 'bert-combined-1'
        self.model, self.tokenizer = load_model(self.model_name)
    
    def test_load_model(self):
        """Test model loading"""
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.tokenizer)
        self.assertEqual(self.model.__class__.__name__, 
                        'BertForSequenceClassification')
    
    def test_predict_text_truthful(self):
        """Test prediction on truthful text"""
        text = "Climate change is supported by scientific evidence."
        result = predict_text(text, self.model, self.tokenizer)
        
        self.assertIn('label', result)
        self.assertIn('confidence', result)
        self.assertIn('probabilities', result)
        self.assertEqual(result['label'], 'Truthful')
        self.assertGreater(result['confidence'], 0.7)
    
    def test_predict_text_deceptive(self):
        """Test prediction on deceptive text"""
        text = "Climate change is a hoax invented by scientists."
        result = predict_text(text, self.model, self.tokenizer)
        
        self.assertEqual(result['label'], 'Deceptive')
    
    def test_predict_text_empty(self):
        """Test prediction with empty text"""
        with self.assertRaises(ValueError):
            predict_text("", self.model, self.tokenizer)
    
    def test_predict_text_too_long(self):
        """Test prediction with text exceeding max length"""
        text = "word " * 10000  # ~10k riječi
        with self.assertRaises(ValueError):
            predict_text(text, self.model, self.tokenizer)
    
    def tearDown(self):
        """Cleanup after each test"""
        del self.model
        del self.tokenizer
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

if __name__ == '__main__':
    unittest.main()
```

**Pokretanje:**

```bash
cd backend
python -m unittest tests/test_ai_utils.py
```

#### 12.2.2 Frontend unit testovi

**frontend/tests/unit/InputForm.spec.js:**

```javascript
import { mount } from '@vue/test-utils';
import InputForm from '@/components/InputForm.vue';

describe('InputForm.vue', () => {
  let wrapper;
  
  beforeEach(() => {
    wrapper = mount(InputForm, {
      props: {
        models: [
          { name: 'bert-combined-1', display_name: 'BERT Combined' }
        ]
      }
    });
  });
  
  it('renders textarea and model selector', () => {
    expect(wrapper.find('textarea').exists()).toBe(true);
    expect(wrapper.find('select').exists()).toBe(true);
  });
  
  it('disables submit button when text is empty', () => {
    const button = wrapper.find('button[type="submit"]');
    expect(button.attributes('disabled')).toBeDefined();
  });
  
  it('enables submit button when text is provided', async () => {
    const textarea = wrapper.find('textarea');
    await textarea.setValue('Test text');
    
    const button = wrapper.find('button[type="submit"]');
    expect(button.attributes('disabled')).toBeUndefined();
  });
  
  it('shows character counter', async () => {
    const textarea = wrapper.find('textarea');
    await textarea.setValue('Hello');
    
    expect(wrapper.text()).toContain('5 / 8000');
  });
  
  it('prevents submission with text exceeding limit', async () => {
    const longText = 'a'.repeat(8001);
    const textarea = wrapper.find('textarea');
    await textarea.setValue(longText);
    
    const button = wrapper.find('button[type="submit"]');
    expect(button.attributes('disabled')).toBeDefined();
  });
  
  it('emits analyze event on form submission', async () => {
    const textarea = wrapper.find('textarea');
    const select = wrapper.find('select');
    
    await textarea.setValue('Test text');
    await select.setValue('bert-combined-1');
    
    await wrapper.find('form').trigger('submit.prevent');
    
    expect(wrapper.emitted('analyze')).toBeTruthy();
    expect(wrapper.emitted('analyze')[0]).toEqual([{
      text: 'Test text',
      model: 'bert-combined-1'
    }]);
  });
});
```

**Pokretanje:**

```bash
cd frontend
npm run test:unit
```

### 12.3 Integration testovi

**backend/tests/test_api.py:**

```python
import unittest
import json
from app import app

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        """Setup test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_get_models(self):
        """Test GET /api/models"""
        response = self.app.get('/api/models')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # Check model structure
        model = data[0]
        self.assertIn('name', model)
        self.assertIn('display_name', model)
    
    def test_predict(self):
        """Test POST /api/predict"""
        payload = {
            'text': 'Climate change is real.',
            'model_name': 'bert-combined-1'
        }
        
        response = self.app.post('/api/predict',
                                data=json.dumps(payload),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('label', data)
        self.assertIn('confidence', data)
        self.assertIn('probabilities', data)
    
    def test_predict_invalid_model(self):
        """Test prediction with invalid model"""
        payload = {
            'text': 'Test text',
            'model_name': 'nonexistent-model'
        }
        
        response = self.app.post('/api/predict',
                                data=json.dumps(payload),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
    
    def test_predict_missing_text(self):
        """Test prediction without text"""
        payload = {'model_name': 'bert-combined-1'}
        
        response = self.app.post('/api/predict',
                                data=json.dumps(payload),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_lime_explanation(self):
        """Test POST /api/lime"""
        payload = {
            'text': 'Climate change is real.',
            'model_name': 'bert-combined-1'
        }
        
        response = self.app.post('/api/lime',
                                data=json.dumps(payload),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('as_list', data)
        self.assertIn('as_html', data)
        self.assertIsInstance(data['as_list'], list)

if __name__ == '__main__':
    unittest.main()
```

### 12.4 E2E testovi

**frontend/tests/e2e/analysis.cy.js (Cypress):**

```javascript
describe('Analysis Flow', () => {
  beforeEach(() => {
    cy.visit('/');
  });
  
  it('completes full analysis workflow', () => {
    // Navigate to Analysis tab
    cy.contains('Analysis').click();
    
    // Enter text
    cy.get('textarea').type('Climate change is a serious global issue.');
    
    // Select model
    cy.get('select').select('bert-combined-1');
    
    // Submit
    cy.contains('Analyze Text').click();
    
    // Wait for results
    cy.contains('PREDICTION', { timeout: 10000 }).should('be.visible');
    
    // Verify results structure
    cy.contains('Truthful').or(cy.contains('Deceptive'));
    cy.contains('%');
    
    // Check explanations tabs
    cy.contains('LIME').click();
    cy.get('.lime-explanation').should('be.visible');
    
    cy.contains('SHAP').click();
    cy.get('.shap-explanation').should('be.visible');
  });
  
  it('validates empty text submission', () => {
    cy.contains('Analysis').click();
    
    // Try to submit without text
    cy.contains('Analyze Text').should('be.disabled');
    
    // Enter text and verify enabled
    cy.get('textarea').type('Some text');
    cy.contains('Analyze Text').should('not.be.disabled');
  });
});
```

### 12.5 Performance testovi

**Load testing s Locust:**

```python
from locust import HttpUser, task, between

class DeceptionDetectorUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def predict(self):
        """Simulate prediction request"""
        self.client.post('/api/predict', json={
            'text': 'Climate change is a serious issue.',
            'model_name': 'bert-combined-1'
        })
    
    @task(1)
    def get_models(self):
        """Simulate fetching models list"""
        self.client.get('/api/models')
    
    @task(1)
    def lime_explanation(self):
        """Simulate LIME explanation request"""
        self.client.post('/api/lime', json={
            'text': 'Climate change is a serious issue.',
            'model_name': 'bert-combined-1'
        })
```

**Pokretanje:**

```bash
locust -f tests/load_test.py --host=http://localhost:5000
```

### 12.6 Coverage izvještaj

**Konfiguracija (.coveragerc):**

```ini
[run]
source = backend
omit = 
    */tests/*
    */venv/*
    */__pycache__/*

[report]
precision = 2
show_missing = True
```

**Pokretanje s coverage:**

```bash
cd backend
coverage run -m unittest discover tests/
coverage report
coverage html  # Generira HTML izvještaj
```

**Očekivani output:**

```
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
ai_utils.py             142      8    94%   234-235, 301-305
app.py                   45      2    96%   67-68
config.py                23      0   100%
explanations.py          89     12    87%   145-150, 201-206
model_utils.py           67      5    93%   89-93
routes.py               156     18    88%   various
---------------------------------------------------
TOTAL                   522     45    91%
```

---

## 13. ODRŽAVANJE I NADOGRADNJA

### 13.1 Redovno održavanje

#### 13.1.1 Čišćenje prosječenih modela

**Automatsko čišćenje (jednom dnevno):**

```python
# cleanup_scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from model_utils import cleanup_expired_models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scheduled_cleanup():
    """Scheduled cleanup task"""
    try:
        count = cleanup_expired_models()
        logger.info(f"Cleanup completed: {count} models deleted")
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")

# Setup scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    scheduled_cleanup,
    'cron',
    hour=3,  # 3 AM svaki dan
    minute=0
)
scheduler.start()

# Dodaj u app.py:
# from cleanup_scheduler import scheduler
```

**Ručno čišćenje:**

```bash
# Linux/macOS
python -c "from model_utils import cleanup_expired_models; print(f'{cleanup_expired_models()} models deleted')"

# Windows PowerShell
python -c "from model_utils import cleanup_expired_models; print(f'{cleanup_expired_models()} models deleted')"
```

#### 13.1.2 Log management

**Logging konfiguracija:**

```python
# backend/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    """Setup application logging"""
    
    # Create logs directory
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    
    # Format
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Add to app
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    return app.logger
```

#### 13.1.3 Disk space monitoring

**Monitoring skripta:**

```python
# monitor_disk.py
import os
import shutil
from config import MODELS_DIR, CUSTOM_MODELS_DIR

def check_disk_space(path):
    """Check available disk space"""
    stat = shutil.disk_usage(path)
    return {
        'total': stat.total / (1024**3),  # GB
        'used': stat.used / (1024**3),
        'free': stat.free / (1024**3),
        'percent': (stat.used / stat.total) * 100
    }

def get_directory_size(path):
    """Calculate directory size"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total += os.path.getsize(filepath)
    return total / (1024**3)  # GB

def monitor():
    """Monitor disk usage"""
    print("=== Disk Space Monitor ===\n")
    
    # Overall disk space
    disk = check_disk_space('/')
    print(f"Total Disk: {disk['total']:.2f} GB")
    print(f"Used: {disk['used']:.2f} GB ({disk['percent']:.1f}%)")
    print(f"Free: {disk['free']:.2f} GB\n")
    
    # Models directories
    models_size = get_directory_size(MODELS_DIR)
    custom_size = get_directory_size(CUSTOM_MODELS_DIR)
    
    print(f"Pretrained Models: {models_size:.2f} GB")
    print(f"Custom Models: {custom_size:.2f} GB")
    print(f"Total Models: {models_size + custom_size:.2f} GB\n")
    
    # Alert if low space
    if disk['free'] < 5:
        print("⚠️  WARNING: Less than 5 GB free space!")
    elif disk['percent'] > 90:
        print("⚠️  WARNING: Disk usage over 90%!")

if __name__ == '__main__':
    monitor()
```

### 13.2 Backup strategija

**Backup skripta:**

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/path/to/webapp"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup custom models
echo "Backing up custom models..."
tar -czf "$BACKUP_DIR/custom_models_$DATE.tar.gz" \
    -C "$APP_DIR/backend" custom_models/

# Backup configuration
echo "Backing up configuration..."
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" \
    -C "$APP_DIR" \
    backend/config.py \
    backend/.env \
    frontend/src/config.js

# Delete backups older than 30 days
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### 13.3 Update proces

**Backend dependencies:**

```bash
cd backend

# Check outdated packages
pip list --outdated

# Update specific package
pip install --upgrade transformers

# Freeze new versions
pip freeze > requirements.txt
```

**Frontend dependencies:**

```bash
cd frontend

# Check outdated packages
npm outdated

# Update specific package
npm update vue

# Check for breaking changes
npm audit
```

### 13.4 Monitoring

**Health check endpoint:**

```python
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    import torch
    
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'device': str(DEVICE),
        'cuda_available': torch.cuda.is_available(),
        'models_loaded': len(model_cache),
        'custom_models_count': len([
            d for d in os.listdir(CUSTOM_MODELS_DIR)
            if os.path.isdir(os.path.join(CUSTOM_MODELS_DIR, d))
        ])
    }
    
    if torch.cuda.is_available():
        status['gpu_memory'] = {
            'allocated': f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB",
            'cached': f"{torch.cuda.memory_reserved() / 1024**3:.2f} GB"
        }
    
    return jsonify(status)
```

### 13.5 Deployment

**Systemd service:**

```ini
[Unit]
Description=Deception Detector Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/webapp/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 14. ZAKLJUČAK

### 14.1 Sažetak sustava

**Deception Detector** je napredna web aplikacija za detekciju dezinformacija koja kombinira moć state-of-the-art transformer modela s intuitivnim korisničkim sučeljem. Sustav omogućuje:

✅ **Trenutnu analizu** teksta pomoću šest pretreniranih modela  
✅ **Prilagodbu modela** (fine-tuning) na vlastitim podacima  
✅ **Objašnjive AI** (XAI) analize putem LIME i SHAP vizualizacija  
✅ **Jednostavno dijeljenje** modela pomoću 6-znamenkastih kodova  

### 14.2 Postignuća

**Performanse:**
- Latencija predviđanja: < 2s na CPU, < 500ms na GPU
- Točnost modela: 85-92% ovisno o domeni
- Podrška za tekst do ~1300 riječi
- Treniranje custom modela: 10-30 min ovisno o podatcima

**Skalabilnost:**
- Model caching za brže učitavanje
- GPU/CPU automatska detekcija
- Optimizirani batch inference
- Efficient tokenization

**Korisničke značajke:**
- 3-tab navigacija (Analysis, Fine-tuning, Model Access)
- Intuitivni drag-and-drop upload
- Real-time progress tracking
- Automatski download modela
- LIME i SHAP objašnjenja

### 14.3 Buduća proširenja

**Kratkoročni ciljevi (1-3 mjeseca):**
- JWT autentifikacija
- OAuth 2.0 (Google, GitHub)
- Rate limiting
- Monitoring dashboard

**Srednjoročni ciljevi (3-6 mjeseci):**
- PostgreSQL migracija
- Batch processing API
- Model marketplace
- Advanced analytics

**Dugoročni ciljevi (6-12 mjeseci):**
- Multi-modal analysis (image, video, audio)
- API za treće strane
- Kubernetes deployment
- Microservices architecture

### 14.4 Preporuke za produkciju

**Obavezno prije deploya:**

1. ✅ **SSL/HTTPS** - Let's Encrypt certifikati
2. ✅ **Autentifikacija** - JWT ili OAuth 2.0
3. ✅ **Rate limiting** - Zaštita od abuse
4. ✅ **Monitoring** - Sentry, Prometheus
5. ✅ **Backups** - Automatski dnevni backups
6. ✅ **Logging** - Strukturirano logiranje s rotacijom
7. ✅ **Error handling** - Graceful degradation
8. ✅ **Documentation** - API dokumentacija (Swagger)

---

## 15. DODATAK

### 15.1 Pojmovnik (Glossary)

| Pojam | Definicija |
|-------|------------|
| **BERT** | Bidirectional Encoder Representations from Transformers - transformer model za razumijevanje teksta |
| **DeBERTa** | Decoding-enhanced BERT with disentangled attention - poboljšana verzija BERT-a |
| **Fine-tuning** | Transfer learning tehnika - prilagodba pretreniranog modela na specifičnu domenu |
| **LIME** | Local Interpretable Model-agnostic Explanations - tehnika za objašnjavanje ML predviđanja |
| **SHAP** | SHapley Additive exPlanations - game-theory pristup objašnjavanju modela |
| **Token** | Osnovna jedinica teksta za model (može biti riječ, podriječ ili znak) |
| **Transformer** | Neural network arhitektura bazirana na attention mehanizmu |
| **XAI** | Explainable AI - objašnjivi umjetni inteligencija |
| **Inference** | Proces korištenja treniranog modela za predviđanje |
| **Epoch** | Jedan prolazak kroz cijeli training dataset |
| **Batch size** | Broj uzoraka obrađenih prije ažuriranja modela |
| **Learning rate** | Parametar koji kontrolira brzinu učenja modela |

### 15.2 Korisni linkovi

**Hugging Face modeli:**
- [bert-base-uncased](https://huggingface.co/bert-base-uncased) - Base BERT model
- [microsoft/deberta-v3-base](https://huggingface.co/microsoft/deberta-v3-base)
- [BERT documentation](https://huggingface.co/docs/transformers/model_doc/bert)

**Dokumentacija:**
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vue.js Documentation](https://vuejs.org/guide/introduction.html)
- [LIME GitHub](https://github.com/marcotcr/lime)
- [SHAP Documentation](https://shap.readthedocs.io/)

**Znanstveni radovi:**
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - Original Transformer paper
- [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805)
- [DeBERTa: Decoding-enhanced BERT with Disentangled Attention](https://arxiv.org/abs/2006.03654)
- [LIME: "Why Should I Trust You?"](https://arxiv.org/abs/1602.04938)
- [SHAP: A Unified Approach to Interpreting Model Predictions](https://arxiv.org/abs/1705.07874)

### 15.3 Dataseti za treniranje

**Javno dostupni dataseti:**

| Dataset | Veličina | Domena | Link |
|---------|----------|--------|------|
| LIAR | 12.8K | Politika | [Link](https://paperswithcode.com/dataset/liar) |
| FakeNewsNet | 23K | Vijesti | [Link](https://github.com/KaiDMML/FakeNewsNet) |
| FEVER | 185K | Fact verification | [Link](https://fever.ai/) |
| CoAID | 4.3K | COVID-19 | [Link](https://github.com/cuilimeng/CoAID) |
| Climate FEVER | 1.5K | Klimatske promjene | [Link](https://www.climatefever.ai/) |

**Format podataka za treniranje:**

```csv
text,label
"Climate change is a hoax.",deceptive
"Scientific consensus supports climate change.",truthful
"Vaccines cause autism.",deceptive
"Vaccines are safe and effective.",truthful
```

### 15.4 Troubleshooting FAQ

#### Q: Model ne učitava / CUDA out of memory

**A:** Forsaj CPU ili smanji batch size:
```python
# 1. Forsaj CPU
DEVICE = 'cpu'

# 2. Koristi manji batch size
DEFAULT_BATCH_SIZE = 8

# 3. Očisti GPU cache
import torch
torch.cuda.empty_cache()
```

#### Q: Frontend ne može spojiti na backend

**A:** Provjeri API URL i CORS:
```javascript
// frontend/src/config.js
export const API_BASE_URL = 'http://localhost:5000';

// backend/app.py
from flask_cors import CORS
CORS(app)
```

#### Q: Model download traje predugo

**A:** Koristi resume:
```python
from transformers import AutoModel

model = AutoModel.from_pretrained(
    'bert-base-uncased',
    resume_download=True,
    cache_dir='./models'
)
```

### 15.5 Command reference

**Backend komande:**

```bash
# Start backend
python backend/app.py

# Download modela
python download_models.py

# Run tests
python -m unittest discover backend/tests/

# Install requirements
pip install -r backend/requirements.txt

# Create virtual environment
python -m venv venv
```

**Frontend komande:**

```bash
# Start dev server
npm run serve

# Build production
npm run build

# Run tests
npm run test:unit

# Install dependencies
npm install
```

### 15.6 License

**MIT License**

```
Copyright (c) 2025 [Your Name/Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED.
```

### 15.7 Kontakt i podrška

**Email:** support@deceptiondetector.com  
**GitHub:** https://github.com/yourusername/deception-detector  
**Bug reports:** Koristi GitHub Issues  
**Feature requests:** Koristi GitHub Discussions  

---

**KRAJ SPECIFIKACIJE**

Verzija: 1.0  
Datum: 2025-11-03

---
