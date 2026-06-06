# SUMMIFY AI — Complete Setup & AI Maintenance Guide

---

# Overview

SUMMIFY AI is a fully local NLP-powered application designed for:

* News Article Summarization
* Zero-Shot News Classification
* Sentiment Analysis
* Word Cloud Visualization

The project uses:

* Streamlit
* Hugging Face Transformers
* PyTorch
* NLTK
* DistilBART
* DistilBERT

This guide explains:

* complete setup,
* offline configuration,
* project structure,
* troubleshooting,
* local model architecture,
* and future AI maintenance context.

---

# 1. System Requirements

## Minimum Requirements

* Windows 10/11
* 8 GB RAM
* Intel i5 / Ryzen 5
* 10 GB free storage

## Recommended

* 16 GB RAM
* SSD storage
* Stable internet connection (only for first-time setup)

---

# 2. Install Python

## Required Version

```text
Python 3.10.11
```

Download:
https://www.python.org/downloads/release/python-31011/

During installation:

* Enable `Add Python to PATH`
* Enable `Install for all users`

Verify installation:

```powershell
py -3.10 --version
```

Expected:

```text
Python 3.10.11
```

---

# 3. Extract Project

Recommended location:

```text
D:\SUMMIFY
```

Expected structure:

```text
SUMMIFY/
│
├── SOURCE_CODE/
├── venv/
└── Start_Summify.bat
```

---

# 4. Create Virtual Environment

Open PowerShell inside:

```text
D:\SUMMIFY
```

Run:

```powershell
py -3.10 -m venv venv
```

---

# 5. Activate Virtual Environment

Run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Then:

```powershell
venv\Scripts\Activate.ps1
```

Verify:

```powershell
python --version
```

Expected:

```text
Python 3.10.11
```

---

# 6. Install Dependencies

Move into source folder:

```powershell
cd SOURCE_CODE
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install requirements:

```powershell
pip install -r requirements.txt
```

---

# 7. Download NLTK Resources

Run:

```powershell
python
```

Inside Python:

```python
import nltk
nltk.download('vader_lexicon')
exit()
```

---

# 8. Local AI Model Structure

The project is configured for fully local offline execution.

Expected structure:

```text
SOURCE_CODE/
│
├── models/
│   ├── bart-large-mnli/
│   ├── distilbart-cnn-12-6/
│   └── distilbert-sentiment/
```

These folders contain:

* model weights
* tokenizer files
* configs
* inference settings

No internet is required after setup.

---

# 9. Project Architecture

```text
SUMMIFY/
│
├── SOURCE_CODE/
│   ├── DATASET/
│   ├── models/
│   │   ├── bart-large-mnli/
│   │   ├── distilbart-cnn-12-6/
│   │   └── distilbert-sentiment/
│   │
│   ├── Summify_AI.py
│   ├── requirements.txt
│   ├── logo.png
│   ├── default_image.png
│   └── Start_Summify.bat
│
├── venv/
│
└── backups/
```

---

# 10. Run Application

## Manual Run

Inside:

```text
D:\SUMMIFY\SOURCE_CODE
```

Run:

```powershell
streamlit run Summify_AI.py
```

---

## One-Click Launcher

Double-click:

```text
Start_Summify.bat
```

Launcher content:

```bat
@echo off

cd /d D:\SUMMIFY\SOURCE_CODE

D:\SUMMIFY\venv\Scripts\python.exe -m streamlit run Summify_AI.py

pause
```

---

# 11. Open Application

Open browser:

```text
http://localhost:8501
```

---

# 12. Offline Verification

1. Disconnect internet
2. Launch application
3. Test:

   * summarization
   * classification
   * sentiment analysis

If everything works:

* setup is fully local
* models are correctly configured

---

# 13. Recommended Backup

Backup the entire:

```text
D:\SUMMIFY
```

This preserves:

* source code
* local models
* datasets
* virtual environment
* launcher
* dependencies

---

# 14. Explanation of Key Setup Decisions

## Why Python 3.10.11?

The project depends on older Transformer ecosystem compatibility.

Python 3.10 provides:

* stable Transformers support
* reliable pipeline registration
* stable tokenizer behavior
* PyTorch compatibility

Newer versions like:

* Python 3.12
* Python 3.13
* Python 3.14

may break NLP dependencies.

---

## Why Virtual Environment?

The virtual environment isolates:

* PyTorch
* Transformers
* Streamlit
* tokenizers
* dependency versions

This avoids:

* global conflicts
* broken package upgrades
* system-wide dependency corruption

---

## Why Local Models?

Local model storage ensures:

* offline execution
* portability
* reproducibility
* no Hugging Face dependency
* faster startup

The application behaves as a self-contained AI system.

---

## Why Streamlit?

Streamlit enables:

* rapid UI development
* interactive NLP interfaces
* lightweight deployment
* local browser hosting

without backend infrastructure complexity.

---

## Why DistilBART?

DistilBART is used for:

* abstractive summarization
* reduced memory usage
* faster inference
* efficient local execution

---

## Why BART Large MNLI?

`facebook/bart-large-mnli` powers:

* zero-shot classification
* contextual category prediction
* dynamic NLP inference

without training a custom classifier.

---

## Why DistilBERT Sentiment?

The sentiment model provides:

* lightweight inference
* polarity prediction
* real-time performance

suitable for local CPU execution.

---

# 15. AI ASSISTANT CONTEXT — INTERNAL MAINTENANCE GUIDE

This section is specifically intended for:

* AI assistants
* LLMs
* future maintainers
* debugging agents
* automation systems

to understand the architecture and recovery strategy of this project.

---

# PROJECT IDENTITY

Project Name:

* SUMMIFY AI

Project Type:

* Offline NLP Web Application

Primary Domain:

* Natural Language Processing

Core Functionalities:

1. Summarization
2. Zero-Shot Classification
3. Sentiment Analysis
4. Word Cloud Visualization

Frontend:

* Streamlit

Backend:

* Python 3.10.11

Execution:

* Fully Offline Localhost Application

---

# CRITICAL ENVIRONMENT REQUIREMENTS

## STRICT PYTHON REQUIREMENT

```text
Python 3.10.11
```

Avoid upgrading blindly to:

* Python 3.12+
* unstable Transformers stacks

Observed failure example:

```python
KeyError: "Unknown task summarization"
```

Root cause:

* incompatible Transformers registration
* Python ecosystem mismatch

---

# MAIN EXECUTION ENTRYPOINT

Application:

```text
SOURCE_CODE/Summify_AI.py
```

Launcher:

```text
SOURCE_CODE/Start_Summify.bat
```

Execution:

```powershell
D:\SUMMIFY\venv\Scripts\python.exe -m streamlit run Summify_AI.py
```

Direct interpreter invocation is preferred over PATH-based activation.

---

# TRANSFORMER PIPELINES

## Summarization

Model:

```text
sshleifer/distilbart-cnn-12-6
```

Local path:

```python
./models/distilbart-cnn-12-6
```

Pipeline:

```python
pipeline(
    "summarization",
    model="./models/distilbart-cnn-12-6"
)
```

---

## Zero-Shot Classification

Model:

```text
facebook/bart-large-mnli
```

Local path:

```python
./models/bart-large-mnli
```

Pipeline:

```python
pipeline(
    "zero-shot-classification",
    model="./models/bart-large-mnli"
)
```

Categories:

```python
[
    "Sports",
    "Politics",
    "Technology",
    "Health",
    "Entertainment",
    "Business"
]
```

---

## Sentiment Analysis

Model:

```text
distilbert-base-uncased-finetuned-sst-2-english
```

Local path:

```python
./models/distilbert-sentiment
```

Pipeline:

```python
pipeline(
    "sentiment-analysis",
    model="./models/distilbert-sentiment"
)
```

---

# NLTK REQUIREMENTS

Required resource:

```python
nltk.download('vader_lexicon')
```

Failure symptom:

```python
LookupError: Resource vader_lexicon not found
```

---

# IMPORTANT TROUBLESHOOTING HISTORY

## PowerShell Execution Policy Error

Observed:

```powershell
running scripts is disabled on this system
```

Fix:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

---

## Transformers Pipeline Failure

Observed:

```python
KeyError: "Unknown task summarization"
```

Resolved by:

* Python 3.10.11
* stable Transformers stack

Stable versions:

```text
transformers==4.39.3
tokenizers==0.15.2
huggingface_hub==0.22.2
```

---

## Hugging Face Connectivity Failure

Observed:

```python
OSError: couldn't connect to huggingface.co
```

Resolved by:

* local model migration
* direct local-path loading
* offline-first architecture

---

# DATASET REQUIREMENTS

Expected Excel columns:

```python
[
    "title",
    "text",
    "category",
    "summary",
    "published_date",
    "top_image",
    "section"
]
```

---

# PERFORMANCE CHARACTERISTICS

* CPU-only execution supported
* first model load is slower
* subsequent inference is faster
* moderate RAM usage expected

Recommended:

* 16GB RAM

---

# PROJECT PHILOSOPHY

This project prioritizes:

* offline execution
* local inference
* portability
* academic NLP experimentation
* transformer-based research

NOT intended as:

* enterprise inference infrastructure
* scalable production deployment

---

# FUTURE IMPROVEMENT IDEAS

Potential upgrades:

1. GPU acceleration
2. Docker support
3. SQLite/PostgreSQL integration
4. REST API backend
5. Ollama/local LLM integration
6. Multi-language NLP
7. PDF export
8. Better UI/UX
9. Fine-tuned summarization
10. Authentication system

---

# FINAL NOTES

SUMMIFY AI is now configured as:

* a fully offline NLP platform
* a portable transformer-based AI application
* a self-contained academic AI system

The project no longer depends on:

* Hugging Face online cache
* internet connectivity
* external APIs

All NLP operations execute locally on the machine.
