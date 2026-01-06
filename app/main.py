from typing import List, Optional
import requests

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from recipe_scrapers import scrape_me
from sqlalchemy.orm import Session, joinedload

from .database import get_db
from .models import Category, Recipe, RecipeCategory
from .ai_parser import parse_recipe_with_ai, AI_MODEL_PROVIDER, GEMINI_API_KEY, OLLAMA_HOST

app = FastAPI(title="Recipe Importer")

templates = Jinja2Templates(directory="app/templates")


def _serialize_scraped(scraper) -> dict:
    """Normalize scraped recipe data into our expected shape."""
    def _join_lines(items: Optional[List[str]]) -> str:
        if not items:
            return ""
        cleaned = [item.strip() for item in items if item and item.strip()]
        return "\n".join(cleaned)

    def _safe_call(func, default=None):
        try:
            return func() or default
        except:
            return default

    return {
        "title": _safe_call(scraper.title, ""),
        "source_url": scraper.url or "",
        "ingredients": _join_lines(_safe_call(scraper.ingredients, [])),
        "instructions": _join_lines(_safe_call(scraper.instructions_list, [])),
        "prep_time_minutes": _safe_call(scraper.prep_time),
        "cook_time_minutes": _safe_call(scraper.cook_time),
        "servings": _safe_call(scraper.yields, ""),
        "image_url": _safe_call(scraper.image, ""),
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/manual", response_class=HTMLResponse)
def manual_entry(request: Request, db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.name).all()
    return templates.TemplateResponse(
        "edit_recipe.html",
        {
            "request": request,
            "recipe": {},
            "categories": categories,
            "error": None,
        },
    )


@app.post("/import", response_class=HTMLResponse)
async def import_recipe(
    request: Request,
    url: str = Form(...),
    db: Session = Depends(get_db),
):
    categories = db.query(Category).order_by(Category.name).all()
    recipe_data: dict = {}
    error: Optional[str] = None
    method_used = "standard"

    cleaned_url = url.strip()
    
    # Try 1: Standard scraper first (fastest and most reliable for supported sites)
    try:
        scraper = scrape_me(cleaned_url)
        recipe_data = _serialize_scraped(scraper)
        recipe_data["source_url"] = cleaned_url
        method_used = "standard"
    except Exception as e1:
        # Try 2: Fallback to Gemini AI
        try:
            import os
            os.environ["AI_MODEL_PROVIDER"] = "gemini"
            
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            resp = requests.get(cleaned_url, headers=headers, timeout=15)
            resp.raise_for_status()
            recipe_data = parse_recipe_with_ai(cleaned_url, resp.text)
            method_used = "gemini"
            
            if not recipe_data.get("title"):
                raise ValueError("Gemini returned empty result")
        except Exception as e2:
            # Try 3: Final fallback to Ollama
            try:
                import os
                os.environ["AI_MODEL_PROVIDER"] = "ollama"
                
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
                resp = requests.get(cleaned_url, headers=headers, timeout=15)
                resp.raise_for_status()
                recipe_data = parse_recipe_with_ai(cleaned_url, resp.text)
                method_used = "ollama"
                
                if not recipe_data.get("title"):
                    raise ValueError("Ollama returned empty result")
            except Exception as e3:
                error = f"All methods failed. Standard: {str(e1)[:50]}, Gemini: {str(e2)[:50]}, Ollama: {str(e3)[:50]}"
                method_used = "failed"

    # Ensure we have a dict even on error
    if not recipe_data:
        recipe_data = {
            "title": "",
            "source_url": cleaned_url,
            "ingredients": "",
            "instructions": "",
            "prep_time_minutes": None,
            "cook_time_minutes": None,
            "servings": "",
            "image_url": "",
        }
    
    # Add info about which method was successful
    if not error and method_used != "failed":
        success_message = f"Recipe imported using {method_used.upper()} method."
        if method_used != "standard":
            success_message += f" (Standard scraper failed, used {method_used.upper()} as fallback)"
    else:
        success_message = None

    return templates.TemplateResponse(
        "edit_recipe.html",
        {
            "request": request,
            "recipe": recipe_data,
            "categories": categories,
            "error": error,
            "success": success_message,
        },
    )


@app.post("/recipes")
async def create_recipe(
    request: Request,
    title: str = Form(...),
    source_url: str = Form(...),
    ingredients: str = Form(""),
    instructions: str = Form(""),
    prep_time_minutes: Optional[int] = Form(None),
    cook_time_minutes: Optional[int] = Form(None),
    servings: str = Form(""),
    image_url: str = Form(""),
    category_ids: List[int] = Form(default=[]),
    new_category: str = Form(""),
    db: Session = Depends(get_db),
):
    cleaned_title = title.strip()
    cleaned_url = source_url.strip()

    if not cleaned_title or not cleaned_url:
        raise HTTPException(status_code=400, detail="Title and source URL are required.")

    recipe = Recipe(
        title=cleaned_title,
        source_url=cleaned_url,
        ingredients=ingredients.strip(),
        instructions=instructions.strip(),
        prep_time_minutes=prep_time_minutes,
        cook_time_minutes=cook_time_minutes,
        servings=servings.strip() or None,
        image_url=image_url.strip() or None,
    )

    # Attach existing categories
    if category_ids:
        existing = (
            db.query(Category)
            .filter(Category.id.in_(category_ids))
            .order_by(Category.name)
            .all()
        )
        recipe.categories.extend(existing)

    # Create a new category if provided
    cleaned_new_cat = new_category.strip()
    if cleaned_new_cat:
        found = db.query(Category).filter(Category.name == cleaned_new_cat).first()
        if not found:
            found = Category(name=cleaned_new_cat)
            db.add(found)
            db.flush()  # ensures id is available
        recipe.categories.append(found)

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return RedirectResponse(url=f"/recipes/{recipe.id}", status_code=303)


@app.get("/recipes", response_class=HTMLResponse)
def list_recipes(
    request: Request,
    category_id: Optional[int] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Recipe).options(joinedload(Recipe.categories)).order_by(Recipe.created_at.desc())
    if category_id:
        query = query.join(RecipeCategory).filter(RecipeCategory.category_id == category_id)
    if q:
        search_term = f"%{q}%"
        query = query.filter(
            (Recipe.title.ilike(search_term)) |
            (Recipe.ingredients.ilike(search_term)) |
            (Recipe.instructions.ilike(search_term))
        )
    recipes = query.all()

    categories = db.query(Category).order_by(Category.name).all()

    return templates.TemplateResponse(
        "recipes_list.html",
        {
            "request": request,
            "recipes": recipes,
            "categories": categories,
            "selected_category_id": category_id,
            "search_query": q,
        },
    )


@app.get("/recipes/{recipe_id}", response_class=HTMLResponse)
def recipe_detail(recipe_id: int, request: Request, db: Session = Depends(get_db)):
    recipe = (
        db.query(Recipe)
        .options(joinedload(Recipe.categories))
        .filter(Recipe.id == recipe_id)
        .first()
    )
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return templates.TemplateResponse(
        "recipe_detail.html",
        {
            "request": request,
            "recipe": recipe,
        },
    )
