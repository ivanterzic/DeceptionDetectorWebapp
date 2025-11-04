# KORISNIČKI PRIRUČNIK - DECEPTION DETECTOR

**Verzija:** 1.0  
**Datum:** 2025-11-04

---

## SADRŽAJ

1. [Uvod](#1-uvod)
2. [Što je Deception Detector?](#2-što-je-deception-detector)
3. [Instalacija](#3-instalacija)
4. [Korištenje aplikacije](#4-korištenje-aplikacije)
5. [Analiza teksta](#5-analiza-teksta)
6. [Treniranje vlastitih modela](#6-treniranje-vlastitih-modela)
7. [Pristup vlastitim modelima](#7-pristup-vlastitim-modelima)
8. [Razumijevanje rezultata](#8-razumijevanje-rezultata)
9. [Rješavanje problema](#9-rješavanje-problema)
10. [Često postavljana pitanja](#10-često-postavljana-pitanja)

---

## 1. UVOD

### 1.1 Svrha priručnika

Ovaj priručnik pruža upute za korištenje **Deception Detector** aplikacije - alata za analizu vjerodostojnosti tekstualnog sadržaja. Priručnik je namijenjen krajnjim korisnicima bez potrebe za tehničkim znanjem.

### 1.2 Za kogo je ovaj priručnik?

- 📰 Novinari i fact-checkeri
- 🎓 Istraživači i studenti
- 👥 Bilo tko tko želi provjeriti vjerodostojnost tekstualnog sadržaja

---

## 2. ŠTO JE DECEPTION DETECTOR?

### 2.1 Opis

**Deception Detector** je web aplikacija koja koristi umjetnu inteligenciju za analizu teksta i detekciju potencijalno obmanjujućeg ili nevjerodostojnog sadržaja.

### 2.2 Glavne mogućnosti

✅ **Analiza teksta** - Analizirajte bilo koji tekst do 1300 znakova  
✅ **Više modela** - Odaberite između 6 pretreniranih modela  
✅ **Vlastiti modeli** - Trenirajte modele na vlastitim podatcima  
✅ **Vizualna objašnjenja** - Razumijte zašto je tekst označen kao vjerodostojan ili obmanjujući  
✅ **Jednostavno dijeljenje** - Dijelite vlastite modele pomoću 6-znamenkastog koda

### 2.3 Dostupni modeli

| Model | Specijalizacija | Preporučeno za |
|-------|-----------------|----------------|
| **BERT Climate Change** | Klimatske promjene | Tekstove o klimatskim promjenama |
| **BERT COVID-19** | COVID-19 vijesti | Tekstove o zdravstvu i pandemiji |
| **BERT Combined** | Općenito | Različite teme |
| **DeBERTa Climate Change** | Klimatske promjene | Napredna analiza klime |
| **DeBERTa COVID-19** | COVID-19 vijesti | Napredna zdravstvena analiza |
| **DeBERTa Combined** | Općenito | Različite teme (bolji od BERT) |

---

## 3. INSTALACIJA

### 3.1 Preduvjeti

Potrebno je instalirati:
- Python 3.8 ili noviji
- Node.js 14 ili noviji
- Minimalno 8 GB RAM-a
- ~10 GB slobodnog prostora na disku

### 3.2 Korak-po-korak instalacija (Windows)

**1. Preuzmite projekt:**
```powershell
git clone https://github.com/yourusername/deception-detector.git
cd deception-detector\webapp
```

**2. Pokrenite setup skriptu:**
```powershell
.\setup.bat
```

**3. Preuzmite AI modele:**
```powershell
.\download-models.bat
```

**4. Pokrenite aplikaciju:**
```powershell
# Prvi terminal - Backend
.\start-backend.bat

# Drugi terminal - Frontend
.\start-frontend.bat
```

**5. Otvorite preglednik:**
```
http://localhost:8080
```

### 3.3 Instalacija (Linux/macOS)

**1. Preuzmite i postavite projekt:**
```bash
git clone https://github.com/yourusername/deception-detector.git
cd deception-detector/webapp

# Backend setup
python3 -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt

# Preuzmite modele
python3 ../download_models.py
```

**2. Frontend setup:**
```bash
cd ../frontend
npm install
```

**3. Pokrenite aplikaciju:**
```bash
# Terminal 1: Backend
cd backend
source ../venv/bin/activate
python app.py

# Terminal 2: Frontend
cd frontend
npm run serve
```

---

## 4. KORIŠTENJE APLIKACIJE

### 4.1 Navigacija

Aplikacija ima tri glavna taba:

📊 **Analysis** - Analizirajte tekst s pretreniranim modelima  
🎯 **Fine-tuning** - Trenirajte vlastite modele  
🔑 **Model Access** - Pristupite vlastitim modelima pomoću koda

### 4.2 Prvi koraci

1. Otvorite aplikaciju u pregledniku (`http://localhost:8080`)
2. Kliknite na **Analysis** tab (već je odabran po defaultu)
3. Unesite tekst koji želite analizirati
4. Odaberite model
5. Kliknite **Analyze Text**

![Screenshot 1: Početni ekran aplikacije sa logom i navigacijom](./docs/screenshots/01-pocetni-ekran.png)
*Prikaz glavnog ekrana: logo u gornjem lijevom kutu, tri navigacijska taba (Analysis, Fine-tuning, Model Access), aktivan Analysis tab označen crvenom bojom.*

---

## 5. ANALIZA TEKSTA

### 5.1 Unos teksta za analizu

**Način 1: Ručni unos**
1. Kliknite u polje za unos teksta
2. Upišite ili zalijepite tekst (do 1300 znakova)
3. Pratite brojač znakova u donjem desnom kutu

**Način 2: Kopiraj-Zalijepi**
1. Kopirajte tekst iz drugog izvora (Ctrl+C)
2. Zalijepite u polje (Ctrl+V)

![Screenshot 2: Unos teksta u textarea polje](./docs/screenshots/02-unos-teksta.png)
*Prikaz tekstualnog polja sa djelomično unesenim tekstom. Vidljiv brojač znakova (npr. "287 / 1300"), dropdown za odabir modela, i omogućen "Analyze Text" gumb.*

### 5.2 Odabir modela

Iz padajućeg izbornika odaberite model:

- Za tekstove o klimatskim promjenama → **BERT/DeBERTa Climate Change**
- Za tekstove o COVID-19 → **BERT/DeBERTa COVID-19**
- Za ostale teme → **BERT/DeBERTa Combined**

**Savjet:** DeBERTa modeli su točniji, ali sporiji od BERT modela.

### 5.3 Analiza i rezultati

**Pokretanje analize:**
1. Kliknite gumb **Analyze Text**
2. Pričekajte 1-3 sekunde
3. Rezultati će se prikazati automatski

**Tumačenje rezultata:**

```
┌─────────────────────────────────────┐
│  PREDICTION                         │
│  ◉ Truthful                   87.3% │  ← Vjerodostojan (87.3% sigurnosti)
│  ○ Deceptive                  12.7% │  ← Obmanjujući (12.7% vjerojatnosti)
└─────────────────────────────────────┘
```

**Što znače postoci?**

| Confidence | Značenje | Akcija |
|------------|----------|--------|
| 90-100% | Vrlo visoka sigurnost | Možete vjerovati rezultatu |
| 70-89% | Visoka sigurnost | Rezultat je pouzdan |
| 50-69% | Umjerena sigurnost | Provjerite dodatno |
| < 50% | Niska sigurnost | Koristite drugi model |

### 5.4 Primjeri

**Primjer 1: Vjerodostojan tekst**
```
Tekst: "Climate change is supported by overwhelming scientific 
evidence from multiple independent research institutions."

Rezultat: ✅ Truthful (92.4%)
```

**Primjer 2: Obmanjujući tekst**
```
Tekst: "Climate change is a hoax invented by scientists to 
get research funding."

Rezultat: ⚠️ Deceptive (88.7%)
```

![Screenshot 3: Rezultati analize - Truthful tekst](./docs/screenshots/03-rezultat-truthful.png)
*Rezultat za vjerodostojan tekst: zeleni ◉ Truthful 92.4%, sivi ○ Deceptive 7.6%. Prikazan originalni tekst i LIME/SHAP objašnjenja.*

![Screenshot 4: Rezultati analize - Deceptive tekst](./docs/screenshots/04-rezultat-deceptive.png)
*Rezultat za obmanjujući tekst: crveni ◉ Deceptive 88.7%, sivi ○ Truthful 11.3%.*

---

## 6. TRENIRANJE VLASTITIH MODELA

### 6.1 Zašto trenirati vlastiti model?

- 🎯 **Specijalizacija** - Prilagodite model svojoj specifičnoj domeni
- 📊 **Bolji rezultati** - Veća točnost na vašim podatcima
- 🔒 **Privatnost** - Vaši podatci ostaju kod vas

### 6.2 Priprema podataka

**Format CSV datoteke:**

```csv
text,label
"Ovo je vjerodostojan tekst.",truthful
"Ovo je obmanjujući tekst.",deceptive
"Još jedan vjerodostojan primjer.",truthful
```

**Pravila:**
- ✅ CSV format s dvije kolone: `text` i `label`
- ✅ Minimalno 100 primjera (preporučeno 500+)
- ✅ Balansirana distribucija (~50% truthful, ~50% deceptive)
- ✅ Maksimalna veličina datoteke: 100 MB
- ❌ Prazni redovi nisu dozvoljeni
- ❌ Tekst ne smije biti duži od 1300 znakova

![Screenshot 5: CSV upload zona](./docs/screenshots/05-csv-upload.png)
*Drag & drop zona sa "Browse files" gumbom. Prikazan primjer validiranog CSV-a: ✓ Valid CSV format, 1,000 rows, distribucija 48% deceptive / 52% truthful.*

### 6.3 Upload CSV datoteke

**Korak 1: Odaberite Fine-tuning tab**

**Korak 2: Upload datoteke**
- Kliknite **Browse files** ili
- Povucite CSV datoteku u drag & drop zonu

**Korak 3: Validacija**
Aplikacija će automatski provjeriti datoteku i prikazati:
```
✓ Valid CSV format
📊 1,000 rows detected
📈 Distribution: 48% deceptive, 52% truthful
📝 Sample texts shown below
```

![Screenshot: Upload i validacija] (TODO)

### 6.4 Konfiguracija treniranja

**Odabir base modela:**
- **bert-base-uncased** - Brži, manji, dobar za CPU (110M parametara)
- **microsoft/deberta-v3-base** - Točniji, sporiji (184M parametara)

**Ime modela:**
- Unesite opisno ime (npr. "Moj Climate Model")
- Koristit će se za identifikaciju modela

**Training parametri:**

| Parametar | Raspon | Default | Opis |
|-----------|--------|---------|------|
| **Epochs** | 1-10 | 3 | Broj prolazaka kroz podatke |
| **Batch Size** | 4-32 | 16 | Broj uzoraka po iteraciji |
| **Learning Rate** | 1e-5 - 5e-5 | 2e-5 | Brzina učenja |
| **Validation Split** | 10-30% | 20% | Postotak podataka za validaciju |

**Preporuke:**
- Više epochs = bolja točnost, ali duže treniranje
- Manji batch size ako nemate GPU
- Zadržite default learning rate

![Screenshot 6: Konfiguracija parametara treniranja](./docs/screenshots/06-training-config.png)
*Forma sa svim parametrima: Model Name input, Base Model dropdown, Epochs slider (1-10), Batch Size slider (4-32), Learning Rate input, Validation Split slider (10-30%). Prikazan estimated training time.*

### 6.5 Pokretanje treniranja

**1. Kliknite "Start Training"**

**2. Spremite svoj 6-znamenkasti kod!**
```
┌──────────────────────────────────────┐
│  Training started!                   │
│  Your model code: abc123             │
│  ⚠️ SAVE THIS CODE!                  │
│  You'll need it to access your model │
└──────────────────────────────────────┘
```

**⚠️ VAŽNO:** Ovaj kod je jedini način za pristup vašem modelu!

**3. Pratite progres**

Tijekom treniranja vidjet ćete:
- Progress bar (0-100%)
- Trenutni epoch (npr. "Epoch 2/3")
- Training loss (smanjuje se = dobro)
- Validation accuracy (povećava se = dobro)
- Preostalo vrijeme

![Screenshot 7: Progress treniranja](./docs/screenshots/07-training-progress.png)
*Modal prozor sa progress barom (npr. 52%), prikazan model code "abc123" (⚠️ SAVE THIS CODE!), Epoch 3/5, Training Loss: 0.421, Validation Accuracy: 82.3%, Time Remaining: ~11 minutes.*

![Screenshot 8: Treniranje završeno](./docs/screenshots/08-training-complete.png)
*✅ Training completed! Progress bar 100%, Final Validation Accuracy: 89.5%, Total time: 22 minutes. Gumbi: "Go to Model Access", "Train Another Model", "Close".*

**4. Čekanje završetka**

Procijenjeno vrijeme:
- Manje od 500 primjera: 5-10 min
- 500-2000 primjera: 10-20 min
- 2000-5000 primjera: 20-40 min
- Više od 5000 primjera: 40+ min

**Brzina ovisi o:**
- GPU vs CPU (GPU je 10-20x brži)
- Veličini dataseta
- Broju epochs
- Base modelu (BERT brži od DeBERTa)

### 6.6 Završetak treniranja

Kada je treniranje gotovo, vidjet ćete:
```
✅ Training completed!
📊 Final Validation Accuracy: 89.5%
⏱️ Total time: 15 minutes
🔑 Model code: abc123

✓ Training Loss: 0.234
✓ Validation Loss: 0.312
```

**Sljedeći koraci:**
- Kopirajte model code negdje sigurno
- Kliknite **Go to Model Access** za testiranje modela
- Model će biti dostupan 7 dana

![Screenshot 10: Informacije o modelu](./docs/screenshots/10-model-info.png)
*Card sa svim info: 📦 Ime modela, Base Model, Created/Expires datumi (zelena boja - 7 days remaining), Status: ✅ Ready, Training Metrics (Accuracy: 89.5%, Epochs: 5, Samples: 1,000). Gumbi: "Analyze Text" i "Download Model".*

---

## 7. PRISTUP VLASTITIM MODELIMA

### 7.1 Unos koda

**1. Kliknite na "Model Access" tab**

**2. Unesite 6-znamenkasti kod**
```
┌──────────────────────────────────────┐
│  Enter your model code:              │
│  [a][b][c][1][2][3]                  │
│          [Access Model]              │
└──────────────────────────────────────┘
```

**3. Kliknite "Access Model"**

![Screenshot 9: Unos koda za pristup modelu](./docs/screenshots/09-model-code-input.png)
*6 pojedinačnih input boxova za kod (npr. [a][b][c][1][2][3]), "Access Model" gumb, tekst ispod: "Enter your 6-character model code".*

### 7.2 Informacije o modelu

Nakon uspješnog pristupa, vidjet ćete:

```
┌──────────────────────────────────────┐
│  📦 Moj Climate Model                │
│  ────────────────────────────────    │
│  Base Model: bert-base-uncased       │
│  Created: 2025-11-04 10:30          │
│  Expires: 2025-11-11 10:30          │
│  Status: ✅ Ready                     │
│                                      │
│  Training Metrics:                   │
│  • Final Accuracy: 89.5%             │
│  • Epochs: 3                         │
│  • Training Samples: 1,000           │
│                                      │
│  [Analyze Text]  [Download Model]   │
└──────────────────────────────────────┘
```

### 7.3 Korištenje vlastitog modela

**Analiza teksta:**
1. Kliknite **Analyze Text**
2. Unesite tekst koji želite analizirati
3. Kliknite **Analyze**
4. Rezultati će biti prikazani kao i kod pretreniranih modela

### 7.4 Preuzimanje modela

**Zašto preuzeti model?**
- 💾 Sigurnosna kopija (model se briše nakon 7 dana)
- 📤 Dijeljenje s kolegama
- 🔄 Korištenje u drugim aplikacijama

**Kako preuzeti:**

**1. Kliknite "Download Model"**

**2. Pratite progress:**
```
┌──────────────────────────────────────┐
│  📥 Downloading Model                │
├──────────────────────────────────────┤
│  Progress: ██████████░░ 65%         │
│  Phase: Compressing model files      │
│  Size: 234 / 500 MB                  │
│                                      │
│  Files: 3 / 6 completed              │
│  ⏱️ Time: ~15s remaining             │
└──────────────────────────────────────┘
```

**3. Spremite ZIP datoteku**

Datoteka će se preuzeti kao: `deception_model_abc123.zip`

![Screenshot 11: Download progress](./docs/screenshots/11-download-progress.png)
*Modal "📥 Downloading Model": Progress bar 54%, Phase: "Compressing tokenizer files", Size: 267 / 500 MB, Files: 3 / 6 completed, Time: ~8s remaining.*

### 7.5 Sadržaj ZIP datoteke

```
deception_model_abc123.zip
├── model.safetensors          (glavni model, ~500 MB)
├── config.json                (konfiguracija modela)
├── tokenizer.json             (tokenizer)
├── tokenizer_config.json      (tokenizer config)
├── special_tokens_map.json    (specijalni tokeni)
├── vocab.txt                  (vokabular)
└── README.txt                 (upute za korištenje)
```

### 7.6 Rok trajanja modela

⚠️ **Vlastiti modeli se automatski brišu nakon 7 dana!**

**Preostalo vrijeme vidite u model info:**
```
Expires: 2025-11-11 10:30 (3 days remaining)
```

**Što učiniti:**
- Preuzmite model prije isteka roka
- Ili ga ponovno trenirajte i dobijete novi kod

---

## 8. RAZUMIJEVANJE REZULTATA

### 8.1 LIME objašnjenja

**Što je LIME?**
LIME (Local Interpretable Model-agnostic Explanations) pokazuje koje riječi su najviše utjecale na odluku modela.

**Kako čitati LIME vizualizaciju:**

```
Climate change is a serious global issue supported by science.
[zeleno] [zeleno]  [crveno] [neutral] [zeleno] [zeleno] [zeleno]
```

**Boje:**
- 🟢 **Zeleno** = Riječi koje podržavaju "Truthful" predikciju
- 🔴 **Crveno** = Riječi koje podržavaju "Deceptive" predikciju
- ⚪ **Neutralno** = Riječi bez značajnog utjecaja

**Intenzitet boje** = Jačina utjecaja

![Screenshot 12: LIME objašnjenje](./docs/screenshots/12-lime-explanation.png)
*Tekst sa obojenim riječima: zelene riječi ("scientific", "evidence", "research") podržavaju Truthful, crvene ("hoax", "fake") podržavaju Deceptive. Legend sa 🟢 Supports Truthful, 🔴 Supports Deceptive, ⚪ Neutral.*

### 8.2 SHAP objašnjenja

**Što je SHAP?**
SHAP (SHapley Additive exPlanations) koristi game theory za objašnjenje važnosti riječi.

**Kako čitati SHAP vizualizaciju:**

Slično kao LIME, ali s preciznim numeričkim vrijednostima:

```
"climate" → +0.42 (jako podržava Truthful)
  - "hoax"    → -0.38 (jako podržava Deceptive)
  - "is"      → +0.01 (neutralno)
```

![Screenshot 13: SHAP objašnjenje](./docs/screenshots/13-shap-explanation.png)
*Tekst sa intenzitetom boja sličan LIME + bar chart sa top 10 riječi i njihovim SHAP vrijednostima (pozitivne i negativne).*

### 8.3 Usporedba LIME i SHAP

| Aspekt | LIME | SHAP |
|--------|------|------|
| **Brzina** | Brži | Sporiji |
| **Preciznost** | Približna | Precizna |
| **Razumljivost** | Vrlo jednostavno | Malo kompleksnije |
| **Konzistentnost** | Može varirati | Uvijek ista |

**Preporuka:** Gledajte obje vizualizacije za najbolje razumijevanje!

### 8.4 Primjer analize

**Tekst:**
```
"Vaccines are dangerous and cause autism according to many doctors."
```

**Predikcija:** ⚠️ Deceptive (91.2%)

**LIME analiza:**
- 🔴 "dangerous" → Jako negativan signal
- 🔴 "cause autism" → Jako negativan signal
- 🔴 "according to many" → Vague claim signal
- 🟢 "vaccines" → Neutralno (kontekst ga čini negativnim)
- 🟢 "doctors" → Neutralno (lažni autoritet)

**Interpretacija:**
Model je prepoznao:
1. Alarmističke riječi ("dangerous")
2. Lažne medicinske tvrdnje ("cause autism")
3. Nejasne izvore ("many doctors")

---

## 9. RJEŠAVANJE PROBLEMA

### 9.1 Aplikacija se ne pokreće

**Problem:** Backend se ne pokreće

**Rješenja:**
1. Provjerite je li Python instaliran: `python --version`
2. Aktivirajte virtualenv:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Provjerite je li port 5000 slobodan:
   ```powershell
   netstat -ano | findstr :5000
   ```

**Problem:** Frontend se ne pokreće

**Rješenja:**
1. Provjerite je li Node.js instaliran: `node --version`
2. Reinstalirajte dependencies:
   ```bash
   cd frontend
   rm -rf node_modules
   npm install
   ```

### 9.2 Greška "CUDA out of memory"

**Što učiniti:**
1. Zatvorite aplikaciju
2. Otvorite `backend/config.py`
3. Promijenite liniju:
   ```python
   DEVICE = 'cpu'  # Umjesto 'cuda'
   ```
4. Ili smanjite batch size na 8 ili 4

### 9.3 Modeli se ne preuzimaju

**Problem:** Download modela traje predugo ili pada

**Rješenja:**
1. Provjerite internet vezu
2. Ponovno pokrenite download:
   ```bash
   python download_models.py
   ```
3. Download će nastaviti od mjesta gdje je stao

### 9.4 "Model not found" greška

**Uzroci:**
- ❌ Pogrešan kod (provjerite tipfeler)
- ❌ Model je istekao (više od 7 dana)
- ❌ Model je obrisan zbog čišćenja

**Što učiniti:**
- Ponovno trenirajte model s istim podatcima

### 9.5 CSV upload ne radi

**Česte greške:**

| Greška | Uzrok | Rješenje |
|--------|-------|----------|
| "Invalid CSV format" | Pogrešan format | Provjerite da imate `text,label` header |
| "File too large" | > 100 MB | Smanjite broj primjera |
| "Empty file" | Nema podataka | Provjerite sadržaj datoteke |
| "Missing label column" | Nema `label` kolone | Dodajte `label` kolonu |

**Primjer ispravnog CSV-a:**
```csv
text,label
"Tekst 1",truthful
"Tekst 2",deceptive
```

### 9.6 Rezultati izgledaju čudno

**Problem:** Model daje neočekivane rezultate

**Mogući uzroci:**
1. **Pogrešan model** - Koristite model specijaliziran za vašu domenu
2. **Tekst prekratak** - Minimalno 20-30 riječi
3. **Tekst predugačak** - Maksimalno 1300 znakova
4. **Miješani jezik** - Modeli su trenirani na engleskom

**Što učiniti:**
- Probajte drugi model
- Reformulirajte tekst
- Provjerite LIME/SHAP za razumijevanje

### 9.7 Frontend ne vidi backend

**Greška u konzoli:** "Network Error" ili "CORS policy"

**Rješenje:**
1. Provjerite je li backend pokrenut na portu 5000
2. Otvorite http://localhost:5000/api/models u pregledniku
3. Trebali biste vidjeti JSON s modelima

Ako ne radi:
- Restartajte backend
- Provjerite firewall postavke

---

## 10. ČESTO POSTAVLJANA PITANJA

### 10.1 Općenito

**P: Mogu li koristiti aplikaciju offline?**  
O: Da, nakon što preuzmete modele, aplikacija radi potpuno offline.

**P: Podržava li aplikaciju druge jezike osim engleskog?**  
O: Trenutno ne. Modeli su trenirani isključivo na engleskim tekstovima.

**P: Koliko teksta mogu analizirati?**  
O: Maksimalno 1300 znakova (~200 riječi) po analizi.

**P: Je li aplikacija besplatna?**  
O: Da, potpuno je besplatna i open-source.

### 10.2 Modeli

**P: Koji je najbolji model?**  
O: Ovisi o sadržaju:
- Za klimatske promjene: **DeBERTa Climate Change**
- Za COVID-19: **DeBERTa COVID-19**
- Za općenite teme: **DeBERTa Combined**

**P: Koliko su modeli točni?**  
O: Između 85-92% ovisno o modelu i domeni teksta.

**P: Mogu li koristiti model na drugim jezicima?**  
O: Ne, modeli su trenirani samo na engleskom.

### 10.3 Treniranje

**P: Koliko primjera trebam za treniranje?**  
O: Minimalno 100, ali preporučujemo 500+ za dobre rezultate.

**P: Koliko dugo traje treniranje?**  
O: 10-30 minuta ovisno o broju primjera i dostupnosti GPU-a.

**P: Trebam li GPU?**  
O: Ne, ali GPU značajno ubrzava treniranje (10-20x).

**P: Mogu li zaustaviti treniranje?**  
O: Ne, treniranje mora završiti do kraja. Progress se ne sprema.

**P: Što ako zatvori aplikaciju tijekom treniranja?**  
O: Treniranje će se prekinuti i morat ćete početi ispočetka.

### 10.4 Vlastiti modeli

**P: Koliko dugo je model dostupan?**  
O: 7 dana od završetka treniranja.

**P: Mogu li produljiti rok trajanja?**  
O: Ne, ali možete preuzeti model i ponovno ga uploadati (buduća funkcionalnost).

**P: Što ako zaboravim kod?**  
O: Nažalost, nema načina za oporavak. Treba ponovno trenirati model.

**P: Mogu li dijeliti kod s drugima?**  
O: Da, svatko s kodom može pristupiti modelu.

**P: Koliko modela mogu trenirati?**  
O: Nema limita, ali maksimalno 100 aktivnih modela istovremeno u sustavu.

### 10.5 Sigurnost i privatnost

**P: Gdje se spremaju moji podatci?**  
O: Lokalno na vašem računalu. Ništa se ne šalje na cloud.

**P: Mogu li drugi vidjeti moje modele?**  
O: Ne, osim ako im ne date 6-znamenkasti kod.

**P: Što se događa s mojim CSV podacima nakon uploada?**  
O: Brišu se automatski nakon završetka treniranja.

**P: Je li aplikacija sigurna?**  
O: Da, nema vanjske komunikacije i nema autentifikacije (nema user accounta).

---

## 11. DODATAK

### 11.1 Tehnički zahtjevi

**Minimum:**
- CPU: 4 cores
- RAM: 8 GB
- Disk: 10 GB
- OS: Windows 10, macOS 10.14, Linux (Ubuntu 18.04+)

**Preporučeno:**
- CPU: 8+ cores
- RAM: 16 GB
- GPU: NVIDIA s 8 GB+ VRAM
- Disk: 50 GB SSD

### 11.2 Ograničenja

**Tekst:**
- Maksimalno 1300 znakova po analizi
- Samo engleski jezik
- Minimum ~20 riječi za pouzdane rezultate

**Treniranje:**
- CSV datoteka do 100 MB
- Minimalno 100 primjera
- Maksimalno 10 epochs

**Modeli:**
- Zadržavaju se 7 dana
- Maksimalno 100 aktivnih modela u sustavu

### 11.3 Pojmovnik

| Pojam | Objašnjenje |
|-------|-------------|
| **Truthful** | Vjerodostojan, istinit sadržaj |
| **Deceptive** | Obmanjujući, lažan sadržaj |
| **Confidence** | Sigurnost modela (0-100%) |
| **BERT** | AI model za razumijevanje teksta |
| **DeBERTa** | Napredna verzija BERT-a (točnija) |
| **Fine-tuning** | Treniranje modela na vlastitim podatcima |
| **Epoch** | Jedan prolazak kroz sve podatke |
| **Validation** | Testiranje točnosti modela |
| **LIME** | Metoda za objašnjavanje rezultata |
| **SHAP** | Napredna metoda za objašnjavanje |
