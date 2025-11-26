# 🦷 ScanAI - Dental Disease Classification System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Model Accuracy](https://img.shields.io/badge/Accuracy-92.28%25-brightgreen.svg)]()

> **AI-Powered Dental Health Analysis Platform** - Early detection and classification of oral diseases using Vision Transformer (ViT-B/16) deep learning architecture.

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Model Performance](#-model-performance)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Training Pipeline](#-training-pipeline)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#%EF%B8%8F-disclaimer)

---

## 🎯 Overview

**ScanAI** is a full-stack web application that leverages state-of-the-art computer vision to classify dental diseases from intraoral photographs. Built with FastAPI and PyTorch, it provides users with instant AI-powered analysis, detailed PDF reports, and personalized recommendations for six common oral health conditions.

This project is an AI-powered web application for dental disease classification. Users can upload dental images and get an analysis of potential diseases.

### 🎯 What It Does

ScanAI analyzes dental images to detect and classify oral health conditions, providing confidence scores, treatment recommendations, and professional-grade PDF reports. The system uses a Vision Transformer model trained on 6,000+ labeled dental images with **92.28% accuracy**.

### 🏥 Classified Conditions

The model identifies **6 distinct oral health states:**

| Condition | Description | F1-Score |
|-----------|-------------|----------|
| **Calculus** | Hardened plaque deposits (tartar) on teeth | 0.736 |
| **Caries** | Dental cavities and tooth decay | 0.978 |
| **Gingivitis** | Gum inflammation and early periodontal disease | 0.870 |
| **Healthy Teeth** | Normal, healthy oral condition | 0.815 |
| **Mouth Ulcer** | Aphthous ulcers and oral lesions | 0.991 |
| **Tooth Discoloration** | Staining and enamel discoloration | 0.969 |

---

## ✨ Key Features

### 🔐 Authentication & Security
- **Multi-provider OAuth**: Google and Facebook social login
- **JWT-based sessions**: Secure token authentication with expiry
- **Password hashing**: Bcrypt-secured credential storage
- **MongoDB persistence**: User profiles and analysis history

### 🖼️ Image Processing
- **Batch upload**: Analyze up to 5 images simultaneously
- **Drag-and-drop UI**: Intuitive image selection interface
- **Format support**: JPEG, PNG, AVIF, WebP
- **Preprocessing pipeline**: Automatic resize, normalization, augmentation

### 🤖 AI Analysis Engine
- **Vision Transformer (ViT-B/16)**: State-of-the-art architecture
- **92.28% accuracy**: Validated on 1,516 test images
- **Multi-image aggregation**: Combines findings across uploads
- **Confidence scoring**: Per-class probability distributions
- **Focal Loss training**: Handles class imbalance effectively

### 📄 Professional Reporting
- **PDF generation**: Medical-grade styled reports (ReportLab)
- **Personalized recommendations**: Condition-specific care instructions
- **Technical metadata**: Model version, confidence metrics, timestamps
- **Email delivery**: Automated SMTP report distribution

### 📊 User Features
- **Analysis history**: Track past diagnoses and trends
- **Dashboard interface**: Clean, responsive HTML/CSS/JS frontend
- **Real-time results**: Instant feedback on upload
- **Mobile-friendly**: Responsive design for all devices

---

## 📈 Model Performance

### Overall Metrics

```
Test Accuracy:        92.28%
Weighted F1-Score:    0.922
Macro F1-Score:       0.893
Test Set Size:        1,516 images
Training Set Size:    ~5,000 images
```

### Per-Class Performance

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|----------|
| Calculus | 79.3% | 68.7% | 0.736 | 195 |
| Caries | 98.0% | 97.6% | **0.978** | 296 |
| Gingivitis | 83.6% | 90.7% | 0.870 | 353 |
| Healthy Teeth | 84.6% | 78.6% | 0.815 | 14 |
| Mouth Ulcer | 99.2% | 99.0% | **0.991** | 382 |
| Tooth Discoloration | 97.1% | 96.7% | 0.969 | 276 |

### Training Details

- **Architecture**: Vision Transformer (ViT-B/16) with custom classification head
- **Loss Function**: Focal Loss (γ=2.0) for class imbalance
- **Optimizer**: AdamW with weight decay (1e-3)
- **Training Strategy**: Two-phase (feature extraction → fine-tuning)
- **Regularization**: Dropout (0.5), gradient clipping, early stopping
- **Hardware**: CUDA-enabled GPU with mixed precision (AMP)

---

## 🛠️ Technology Stack

### Backend (Python 3.9+)

| Component | Technology | Purpose |
|-----------|------------|----------|
| **Web Framework** | FastAPI 0.100+ | Async REST API, automatic docs |
| **Database** | MongoDB + Motor | Async NoSQL persistence |
| **AI/ML** | PyTorch 2.0+, Torchvision | Model inference, image transforms |
| **Authentication** | python-jose, Passlib, Authlib | JWT, password hashing, OAuth |
| **Image Processing** | Pillow (PIL) | Format conversion, preprocessing |
| **PDF Generation** | ReportLab | Professional report rendering |
| **Email** | smtplib, email-validator | SMTP delivery, validation |
| **Environment** | python-dotenv | Configuration management |

### Frontend

- **HTML5/CSS3**: Semantic markup, responsive layouts
- **Vanilla JavaScript**: DOM manipulation, fetch API calls
- **No build tools**: Direct browser execution

### DevOps & Tools

- **Version Control**: Git/GitHub
- **Dependency Management**: pip, requirements.txt
- **Environment**: Virtual environments (venv)
- **Logging**: Python logging module with file/console handlers

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐  │
│  │  Landing   │  │   Login    │  │     Dashboard      │  │
│  │   Page     │  │   /Signup  │  │  (Upload/Results)  │  │
│  └────────────┘  └────────────┘  └────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼────────────────────────────────────┐
│                    FastAPI Backend                          │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Routes:  /auth  |  /api/upload  |  /api/analysis  │  │
│  └───────────────────┬─────────────┬───────────────────┘  │
│                      │             │                       │
│  ┌──────────────────▼─┐  ┌────────▼──────────┐           │
│  │  Auth Services     │  │  Analysis Services │           │
│  │  - JWT Handler    │  │  - Model Inference │           │
│  │  - OAuth (G/FB)   │  │  - PDF Generator   │           │
│  │  - Password Hash  │  │  - Email Service   │           │
│  └──────────┬─────────┘  └────────┬───────────┘           │
│             │                     │                        │
│  ┌──────────▼─────────────────────▼───────────┐           │
│  │         Configuration & Settings           │           │
│  │  (database.py, settings.py, .env)          │           │
│  └──────────┬─────────────────────┬───────────┘           │
└─────────────┼─────────────────────┼───────────────────────┘
              │                     │
     ┌────────▼──────────┐  ┌───────▼──────────┐
     │  MongoDB Atlas    │  │  PyTorch Model   │
     │  - Users          │  │  - ViT-B/16      │
     │  - Analyses       │  │  - final_model   │
     │  - Reports        │  │  - class_names   │
     └───────────────────┘  └──────────────────┘
```

### Request Flow (Image Analysis)

1. **Upload**: User drags images → Frontend POST `/api/upload`
2. **Storage**: Backend saves to `uploads/{email}/images/`
3. **Inference**: `model_inference.py` loads ViT model → preprocesses → predicts
4. **Aggregation**: Combines multi-image results → primary + additional findings
5. **PDF Generation**: `pdf_generator.py` renders report with recommendations
6. **Email**: `email_service.py` sends PDF via SMTP (optional)
7. **Database**: Saves analysis metadata to MongoDB
8. **Response**: Returns JSON with findings + PDF download link

---

## 📁 Project Structure

```
ScanAI/
├── backend/                          # FastAPI application core
│   ├── app.py                        # Main entry point, route registration
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Environment variables (create this)
│   │
│   ├── auth/                         # Authentication module
│   │   ├── jwt_handler.py            # JWT token generation/validation
│   │   └── oauth_handlers.py         # Google/Facebook OAuth flows
│   │
│   ├── config/                       # Configuration management
│   │   ├── database.py               # MongoDB connection (Motor)
│   │   └── settings.py               # Environment variable loading
│   │
│   ├── model/                        # AI model artifacts
│   │   ├── final_model.pth           # Trained ViT weights (~330MB)
│   │   └── class_names.json          # Class label mapping
│   │
│   ├── routes/                       # API route definitions
│   │   ├── auth.py                   # /auth/* endpoints
│   │   ├── upload.py                 # /api/upload endpoint
│   │   └── analysis.py               # /api/analysis/* endpoints
│   │
│   ├── services/                     # Business logic layer
│   │   ├── model_inference.py        # PyTorch model loading/prediction
│   │   ├── pdf_generator.py          # ReportLab PDF creation
│   │   └── email_service.py          # SMTP email delivery
│   │
│   └── uploads/                      # User data storage (gitignored)
│       └── {email}/
│           ├── images/               # Uploaded dental photos
│           └── reports/              # Generated PDF reports
│
├── frontend/                         # Static web interface
│   ├── index.html                    # Landing page
│   ├── login.html                    # Authentication UI
│   ├── dashboard.html                # Main analysis interface
│   └── static/
│       ├── css/
│       │   └── main.css              # Styling
│       ├── js/
│       │   └── main.js               # Client-side logic
│       └── images/                   # UI assets
│
├── data_management/                  # Dataset preparation scripts
│   ├── prepare_dataset.py            # Train/val/test split
│   ├── augment_imbalanced_classes.py # SMOTE-style augmentation
│   ├── data_raw/                     # Original labeled images (gitignored)
│   └── data_split/                   # Processed dataset (gitignored)
│       ├── train/
│       ├── val/
│       └── test/
│
├── training_pipeline/                # Model training code
│   ├── train_model_daddy_og.ipynb    # Full training notebook
│   ├── classification_report.json    # Final test metrics
│   ├── metrics/                      # Training curves (gitignored)
│   └── misclassified_samples/        # Error analysis (gitignored)
│
├── .gitignore                        # Git exclusions
├── README.md                         # This file
└── LICENSE                           # MIT License
```

### Key Files Explained

| File | Purpose |
|------|----------|
| `backend/app.py` | FastAPI app initialization, middleware, route inclusion |
| `backend/services/model_inference.py` | Loads ViT model, preprocesses images, runs inference |
| `backend/services/pdf_generator.py` | Creates medical-style PDF reports with ReportLab |
| `backend/config/settings.py` | Loads `.env` variables, defines default configs |
| `frontend/static/js/main.js` | Handles image upload, API calls, result rendering |
| `training_pipeline/train_model_daddy_og.ipynb` | Complete training pipeline with Focal Loss |
| `data_management/prepare_dataset.py` | Splits raw data into train/val/test sets |

---

## 🚀 Installation & Setup

### Prerequisites

| Requirement | Version | Download |
|-------------|---------|----------|
| **Python** | 3.9+ | [python.org](https://www.python.org/downloads/) |
| **MongoDB** | 4.4+ (Atlas or local) | [mongodb.com](https://www.mongodb.com/try/download/community) |
| **Git** | Latest | [git-scm.com](https://git-scm.com/downloads) |

### Quick Start (Windows PowerShell)

#### 1️⃣ Clone the Repository

```powershell
git clone https://github.com/rushildhube/ScanAI.git
cd ScanAI
```

#### 2️⃣ Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **Note**: If you encounter execution policy errors, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### 3️⃣ Install Dependencies

```powershell
pip install --upgrade pip
pip install -r backend/requirements.txt
```

**Dependencies include:**
- `fastapi`, `uvicorn[standard]` - Web framework
- `torch`, `torchvision` - ML inference
- `motor` - MongoDB async driver
- `python-jose[cryptography]`, `passlib[bcrypt]`, `authlib` - Auth
- `reportlab`, `Pillow` - PDF/image processing
- `python-dotenv` - Environment config

#### 4️⃣ Configure Environment Variables

Create `backend/.env` with the following:

```env
# Required
SECRET_KEY="your-secret-key-min-32-chars"
MONGO_DB_URL="mongodb+srv://user:pass@cluster.mongodb.net/"
MONGO_DB_NAME="dental_app_db"

# Optional (for OAuth)
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
FACEBOOK_CLIENT_ID="your-facebook-app-id"
FACEBOOK_CLIENT_SECRET="your-facebook-app-secret"

# Optional (for email reports)
EMAIL_ADDRESS="your-email@gmail.com"
EMAIL_PASSWORD="your-app-specific-password"
```

**Generate a secure SECRET_KEY:**

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**MongoDB Setup Options:**

- **Cloud (Recommended)**: [MongoDB Atlas Free Tier](https://www.mongodb.com/cloud/atlas/register)
  - Create cluster → Get connection string → Add to `MONGO_DB_URL`
  
- **Local**: Install MongoDB Community → Use `mongodb://localhost:27017/`

**Email Configuration (Gmail):**

1. Enable 2FA on your Google account
2. Generate App Password: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Use app password in `EMAIL_PASSWORD`

#### 5️⃣ Verify Model Files

Ensure these files exist:

```
backend/model/
├── final_model.pth        # Trained ViT model weights (~330MB)
└── class_names.json       # Class label mapping
```

> **Note**: If `MODEL_PATH` in `backend/config/settings.py` uses absolute paths, update them to match your local directory structure.

#### 6️⃣ Run the Server

```powershell
cd backend
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**Expected output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [PID] using WatchFiles
Connected to MongoDB Atlas...
```

#### 7️⃣ Access the Application

- **Frontend**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs (Swagger UI)
- **ReDoc**: http://127.0.0.1:8000/redoc

### Alternative Setup (Linux/macOS)

```bash
# Clone and navigate
git clone https://github.com/rushildhube/ScanAI.git
cd ScanAI

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Install and run
pip install -r backend/requirements.txt
cd backend
uvicorn app:app --reload
```

---

## 📖 Usage Guide

### Web Interface Workflow

#### Step 1: Access & Authentication

1. Navigate to http://127.0.0.1:8000
2. Choose authentication method:
   - **Email/Password**: Register new account or login
   - **Google OAuth**: One-click social login
   - **Facebook OAuth**: One-click social login

#### Step 2: Upload Images

1. Access the **Dashboard** after login
2. Upload images via:
   - **Drag & Drop**: Drop files into upload zone
   - **File Browser**: Click to select files
3. **Limits**: Max 5 images per analysis, formats: JPG, PNG, AVIF, WebP
4. **Tips**: Use clear, well-lit intraoral photos for best results

#### Step 3: Analyze

1. Click **"Analyze Images"** button
2. Wait for processing (typically 3-5 seconds)
3. **Backend Process**:
   - Images saved to `uploads/{email}/images/`
   - Model inference on each image
   - Aggregation of findings
   - PDF report generation

#### Step 4: Review Results

**Dashboard displays:**
- **Primary Finding**: Most confident diagnosis
- **Confidence Score**: Model certainty (0-100%)
- **Additional Findings**: Other detected conditions
- **Per-Image Results**: Individual analysis breakdown

#### Step 5: Download/Email Report

- **Download PDF**: Click "Download Report" button
- **Email Report**: Enter email → Click "Send to Email"
- **Report Contents**:
  - Patient information
  - AI diagnosis with confidence levels
  - Image analysis breakdown
  - Personalized recommendations
  - Technical metadata
  - Medical disclaimer

### Example Analysis Output

```json
{
  "primary_finding": {
    "class": "Caries",
    "confidence": 0.9763
  },
  "additional_findings": [
    {"class": "Gingivitis", "confidence": 0.4521}
  ],
  "image_results": [
    {"image_id": "abc123.jpg", "finding": "Caries", "confidence": 0.98},
    {"image_id": "def456.jpg", "finding": "Caries", "confidence": 0.97}
  ],
  "timestamp": "2025-11-26T10:30:00Z"
}
```

---

## 🔌 API Documentation

### Authentication Endpoints

#### Register User

```http
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "age": 30,
  "mobile": "+1234567890",
  "city": "New York",
  "state": "NY",
  "sex": "Male"
}
```

**Response:**

```json
{
  "message": "User registered successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

#### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

#### OAuth Login

```http
GET /auth/login/google
GET /auth/login/facebook
```

Redirects to OAuth provider → Callback to `/auth/callback/{provider}`

### Analysis Endpoints

#### Upload Images

```http
POST /api/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

files: [File, File, ...] (max 5)
```

**Response:**

```json
{
  "message": "Images uploaded successfully",
  "file_paths": [
    "uploads/john@example.com/images/uuid1.jpg",
    "uploads/john@example.com/images/uuid2.jpg"
  ]
}
```

#### Analyze Images

```http
POST /api/analysis
Authorization: Bearer {token}
Content-Type: application/json

{
  "image_paths": [
    "uploads/john@example.com/images/uuid1.jpg"
  ]
}
```

**Response:**

```json
{
  "analysis_id": "507f1f77bcf86cd799439012",
  "primary_finding": {
    "class": "Caries",
    "confidence": 0.9763
  },
  "additional_findings": [...],
  "image_results": [...],
  "pdf_path": "uploads/john@example.com/reports/report_20251126.pdf",
  "timestamp": "2025-11-26T10:30:00Z"
}
```

#### Get Analysis History

```http
GET /api/analysis/history
Authorization: Bearer {token}
```

**Response:**

```json
{
  "analyses": [
    {
      "analysis_id": "507f1f77bcf86cd799439012",
      "timestamp": "2025-11-26T10:30:00Z",
      "primary_finding": "Caries",
      "confidence": 0.9763
    }
  ]
}
```

### Interactive API Documentation

Once the server is running, visit:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

Test all endpoints directly in the browser with auto-generated forms.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
