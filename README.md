# Recipe Generator

A web application for importing and managing recipes with AI-powered parsing capabilities. The app can extract recipe data from URLs using multiple methods: standard web scraping, Google Gemini AI, or local Ollama models.

## Features

- **Smart Recipe Import**: Automatically tries multiple methods to extract recipe data from URLs
  - Standard web scraper (fastest, for supported recipe sites)
  - Google Gemini AI (cloud-based, more reliable for complex layouts)
  - Local Ollama models (free, runs locally)
  
- **Intelligent Fallback System**: Automatically cascades through import methods if one fails
- **Recipe Management**: Add, edit, and organize recipes with categories
- **Responsive Web UI**: Modern, dark-themed interface built with Tailwind CSS
- **Progress Indicator**: Visual feedback while recipes are being fetched

## Architecture

### Technology Stack
- **Backend**: FastAPI, SQLAlchemy, Alembic
- **Frontend**: Jinja2 templates, Tailwind CSS
- **Database**: SQLite (with Alembic migrations)
- **AI Integration**: Google Gemini API, Local Ollama
- **Web Scraping**: recipe-scrapers library

### Project Structure
```
recipe-generator/
├── app/
│   ├── main.py              # FastAPI app and routes
│   ├── ai_parser.py         # AI recipe parsing logic
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── ollama_client.py     # Ollama integration (legacy)
│   └── templates/           # Jinja2 HTML templates
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── run_app.ps1             # PowerShell startup script
```

## Installation

### Prerequisites
- Python 3.11+
- Windows/macOS/Linux
- (Optional) Ollama installed for local AI parsing

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/jablack10716/recipe-generator.git
   cd recipe-generator
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   alembic upgrade head
   ```

5. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # AI Model Selection - Options: ollama, gemini
   AI_MODEL_PROVIDER=ollama
   
   # Ollama Configuration
   OLLAMA_HOST=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   ```

6. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload
   # Or on Windows with the provided script:
   .\run_app.ps1
   ```

   The app will be available at `http://localhost:8001`

## Configuration

### AI Provider Selection

The app automatically tries import methods in this order:
1. **Standard Web Scraper** - Fast, works for most recipe sites
2. **Gemini AI** - Google's cloud AI (requires API key)
3. **Ollama** - Local AI model (free, requires local installation)

To get a Gemini API key:
1. Visit https://aistudio.google.com/
2. Generate an API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

To use Ollama locally:
1. Install Ollama from https://ollama.ai/
2. Run `ollama serve` in a terminal
3. Pull a model: `ollama pull llama3.2`
4. Set `AI_MODEL_PROVIDER=ollama` in `.env`

## Usage

### Importing Recipes

1. Open the app at `http://localhost:8001`
2. Paste a recipe URL
3. Click "Fetch recipe"
4. The app will automatically try multiple methods to extract the recipe
5. Review and edit the extracted data
6. Add categories and click "Save recipe"

### Supported Recipe Sites

The standard web scraper supports 1000+ recipe sites including:
- AllRecipes.com
- Food Network
- Serious Eats
- Simply Recipes
- And many more (see [recipe-scrapers documentation](https://github.com/hhursev/recipe-scrapers))

## API Endpoints

### GET `/` 
Main page - recipe import form

### POST `/import`
Import a recipe from a URL
- Returns: Recipe preview page for editing

### GET `/recipes`
View all saved recipes

### GET `/recipes/<id>`
View a specific recipe

### POST `/recipes`
Save a new recipe or edit existing

### GET `/recipes/<id>/edit`
Edit recipe page

### DELETE `/recipes/<id>`
Delete a recipe

### GET `/manual`
Manual recipe entry form

### GET `/categories`
Manage recipe categories

## Development

### Running Tests
```bash
pytest tests/
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

### Testing AI Providers
```bash
python test_ai_providers.py
```

## Troubleshooting

### "Could not parse that link"
- The standard web scraper doesn't support that site
- Try with an AI provider (Gemini or Ollama) which is more flexible
- Or manually enter the recipe

### Ollama not responding
- Make sure Ollama is running: `ollama serve`
- Check that the model is downloaded: `ollama pull llama3.2`
- Verify `OLLAMA_HOST` in `.env` is correct

### Gemini API errors
- Verify your API key is correct in `.env`
- Check your API quota at https://aistudio.google.com/
- Ensure you have an active Google account

### Ingredients show escaped characters
- This is usually from the HTML extraction process
- The app automatically cleans up most issues
- You can manually edit in the recipe editor

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Future Enhancements

- [ ] Image upload and management
- [ ] Recipe sharing via URL
- [ ] Nutritional information parsing
- [ ] Shopping list generation
- [ ] Recipe scaling by servings
- [ ] Dark/light theme toggle
- [ ] Export to PDF
- [ ] Mobile app

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [recipe-scrapers](https://github.com/hhursev/recipe-scrapers) - For web scraping support
- [FastAPI](https://fastapi.tiangolo.com/) - For the web framework
- [Ollama](https://ollama.ai/) - For local AI models
- [Google Gemini](https://gemini.google.com/) - For cloud AI capabilities
