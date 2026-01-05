# Setup Guide - Recipe Generator

Complete step-by-step guide to set up the Recipe Generator application.

## System Requirements

- Python 3.11 or higher
- 2GB RAM minimum
- 500MB disk space
- Windows, macOS, or Linux

## Quick Start (5 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/jablack10716/recipe-generator.git
cd recipe-generator
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
alembic upgrade head
```

### 5. Configure Environment
Create `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
AI_MODEL_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

### 6. Run Application
```bash
# Windows (PowerShell)
.\run_app.ps1

# macOS/Linux
python -m uvicorn app.main:app --reload
```

Visit `http://localhost:8001`

---

## Detailed Setup

### Setting Up AI Providers

#### Option A: Ollama (Free, Local)

1. **Download Ollama**
   - Visit https://ollama.ai/
   - Download and install for your OS

2. **Start Ollama**
   ```bash
   ollama serve
   ```

3. **Pull a Model**
   ```bash
   ollama pull llama3.2
   ```

4. **Configure**
   ```env
   AI_MODEL_PROVIDER=ollama
   OLLAMA_HOST=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   ```

#### Option B: Google Gemini (Cloud-Based)

1. **Get API Key**
   - Go to https://aistudio.google.com/
   - Click "Get API Key"
   - Create API key
   - Copy the key

2. **Configure**
   ```env
   GEMINI_API_KEY=paste_your_key_here
   AI_MODEL_PROVIDER=gemini
   ```

3. **Verify Setup**
   ```bash
   python test_ai_providers.py
   ```

### Database Setup

The app uses SQLite with Alembic migrations.

**Initial Setup:**
```bash
alembic upgrade head
```

**Create New Migration** (after model changes):
```bash
alembic revision --autogenerate -m "Description"
```

**Apply Migrations:**
```bash
alembic upgrade head
```

**Rollback Last Migration:**
```bash
alembic downgrade -1
```

### Running the Application

#### Windows (PowerShell)
```powershell
.\run_app.ps1
```

#### Windows (Command Prompt)
```cmd
python -m uvicorn app.main:app --reload
```

#### macOS/Linux
```bash
python -m uvicorn app.main:app --reload
```

The application will start on `http://127.0.0.1:8001`

### Development Mode

For development with auto-reload:
```bash
python -m uvicorn app.main:app --reload --log-level debug
```

### Production Mode

For production deployment:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError" when running app

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`

### Issue: Database errors on startup

**Solution:**
```bash
# Reset database
rm recipes.db
alembic upgrade head
```

### Issue: Ollama not responding

**Solution:**
1. Check if Ollama is running: `ollama serve`
2. Verify port is correct in `.env`: `OLLAMA_HOST=http://localhost:11434`
3. Check model is installed: `ollama list`
4. Pull model if needed: `ollama pull llama3.2`

### Issue: Gemini API errors

**Solution:**
1. Verify API key is correct
2. Check quota at https://aistudio.google.com/
3. Run test: `python test_ai_providers.py`

### Issue: Port 8001 already in use

**Solution:**
```bash
# Use different port
python -m uvicorn app.main:app --port 8002 --reload
```

### Issue: Recipe parsing returns empty

**Solution:**
- Try a different website (some sites block scrapers)
- Try with Gemini AI (more flexible than standard scraper)
- Try with Ollama as fallback
- Check network connectivity

---

## Testing

### Run All Tests
```bash
pytest tests/
```

### Test Specific Module
```bash
pytest tests/test_models.py
```

### Test AI Providers
```bash
python test_ai_providers.py
```

### Test Ollama Only
```bash
python test_ollama.py
```

---

## Project Structure

```
recipe-generator/
├── app/
│   ├── main.py              # FastAPI routes and main app
│   ├── ai_parser.py         # AI recipe parsing logic
│   ├── database.py          # Database setup and session
│   ├── models.py            # SQLAlchemy ORM models
│   ├── ollama_client.py     # Legacy Ollama support
│   └── templates/           # HTML templates
│       ├── base.html
│       ├── home.html
│       ├── edit_recipe.html
│       ├── recipe_detail.html
│       └── recipes_list.html
├── alembic/                 # Database migrations
│   ├── env.py
│   ├── versions/
│   └── alembic.ini
├── tests/                   # Test files
├── .env                     # Environment variables (not in git)
├── .env.example            # Example environment file
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── SETUP.md                # This file
├── run_app.ps1             # Windows startup script
├── test_ollama.py          # Ollama test script
├── test_ai_providers.py    # AI provider test
└── debug_scrape.py         # Web scraper debugging

```

---

## Environment Variables

### .env File Example

```env
# Google Gemini API Key (get from https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key

# AI Model Provider Selection
# Options: ollama, gemini
AI_MODEL_PROVIDER=ollama

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

---

## Performance Tips

1. **First Import Slow?** 
   - First run loads models into memory
   - Subsequent imports are faster

2. **Improve Scraping Speed**
   - Use standard scraper (fastest)
   - Ollama is slower but free
   - Gemini is balanced (needs API key)

3. **Reduce Memory Usage**
   - Switch to smaller Ollama model: `ollama pull tinyllama`
   - Use only Gemini (no local models)

---

## Next Steps

1. Import your first recipe!
2. Configure your preferred AI provider
3. Organize recipes with categories
4. Check out the app features

## Support

For issues or questions:
1. Check the README.md
2. Review error messages in browser console
3. Check terminal output for Python errors
4. Review test files for usage examples

Happy cooking! 🍳
