# Recipe Generator - Features Guide

Complete documentation of all Recipe Generator features and how to use them.

## Table of Contents
1. [Recipe Import](#recipe-import)
2. [Recipe Scaling](#recipe-scaling)
3. [Recipe Management](#recipe-management)
4. [Categories](#categories)
5. [AI Providers](#ai-providers)

---

## Recipe Import

### Overview
The recipe importer uses an intelligent cascading system to extract recipe data from URLs. It tries multiple methods to ensure reliability.

### Import Methods (In Order)

#### 1. Standard Web Scraper (Primary)
- **Speed**: Very fast (< 2 seconds)
- **Reliability**: High for popular recipe sites
- **Cost**: Free, no API keys needed
- **Supported Sites**: 1000+ including AllRecipes, Food Network, Serious Eats, etc.
- **Fallback**: If this fails, tries Gemini AI

#### 2. Gemini AI (Secondary)
- **Speed**: Moderate (10-30 seconds)
- **Reliability**: Very high for any website
- **Cost**: Requires Google Gemini API key (limited free tier)
- **Coverage**: Works on any website (more flexible than standard scraper)
- **Fallback**: If this fails, tries Ollama

#### 3. Ollama Local AI (Tertiary)
- **Speed**: Slower (30-60 seconds)
- **Reliability**: High
- **Cost**: Free (runs on your computer)
- **Coverage**: Works on any website
- **Fallback**: Manual entry

### How to Import

1. **Go to Home Page**
   - Navigate to `http://localhost:8001`

2. **Paste Recipe URL**
   - Example: `https://www.allrecipes.com/recipe/12345/my-recipe/`

3. **Click "Fetch Recipe"**
   - Progress bar shows import is in progress
   - Message indicates which method is being used

4. **Review Results**
   - Edit any incorrect data
   - Add recipe to categories
   - Upload custom image URL if desired

5. **Save Recipe**
   - Click "Save recipe" button
   - Recipe is now in your collection

### What Gets Extracted

The importer extracts:
- ✅ Recipe title
- ✅ Ingredient list (one per line)
- ✅ Step-by-step instructions
- ✅ Prep time (minutes)
- ✅ Cook time (minutes)
- ✅ Servings
- ✅ Recipe image URL
- ✅ Source URL

### Troubleshooting Imports

**"Could not parse that link"**
- Site might not be a recipe site or blocks scrapers
- Try with Gemini AI (more flexible)
- Or manually add the recipe

**Ingredients/instructions look wrong**
- Edit them in the preview before saving
- The app allows full editing

**Missing image**
- You can add one manually by pasting an image URL

**Getting empty results**
- Check your internet connection
- Verify the URL is correct
- Try a different recipe site

---

## Recipe Scaling

### Overview
Instantly scale any recipe up or down by adjusting the number of servings. All ingredient amounts update automatically!

### How to Use

1. **Open a Recipe**
   - Click any recipe from the list
   - Recipe detail page loads

2. **Find Servings Control**
   - Look in the top right above the ingredients
   - Shows current servings with +/− buttons

3. **Adjust Servings**
   - Click **−** to decrease servings
   - Click **+** to increase servings
   - Or type a number directly

4. **Watch Ingredients Update**
   - All amounts change instantly
   - Fractions convert intelligently
   - Non-numeric items stay the same

### Examples

**Recipe: 4 servings**

Original ingredients:
- 2 cups all-purpose flour
- 1/2 cup butter
- 1 tablespoon sugar
- Salt to taste

**Scale to 2 servings:**
- 1 cup all-purpose flour
- 1/4 cup butter
- 1/2 tablespoon sugar
- Salt to taste

**Scale to 8 servings:**
- 4 cups all-purpose flour
- 1 cup butter
- 2 tablespoons sugar
- Salt to taste

### How Scaling Works

1. **Detects Amount and Unit**
   - Parses "2 cups flour" as: amount=2, unit=cups, item=flour

2. **Calculates Scale Factor**
   - Scale factor = new servings / original servings
   - Example: 8 servings / 4 servings = 2.0

3. **Multiplies Amount**
   - New amount = original amount × scale factor
   - Example: 1/2 cup × 2.0 = 1 cup

4. **Converts to Fractions**
   - Decimals become readable fractions
   - 0.25 → 1/4, 0.5 → 1/2, 0.75 → 3/4

5. **Reconstructs Ingredient**
   - Result: "1 cup butter"

### Supported Units

The app recognizes these units:
- Volume: cup, tablespoon, teaspoon, ml, liter
- Weight: gram, kilogram, ounce, pound
- Other: piece, clove, slice, etc.

### Limitations

- **Non-numeric ingredients**: "Salt to taste" stays as-is
- **Cooking times**: Don't change (adjust manually if needed)
- **Complex descriptions**: May not parse perfectly (edit manually)
- **Fractional servings**: You can use 0.5, 1.5, 2.5, etc.

---

## Recipe Management

### Creating Recipes

#### Option 1: Import from URL
- Best for most recipes
- Automatic extraction saves time
- Editable before saving

#### Option 2: Manual Entry
- Use "Add manually" link
- Type all details yourself
- Best for personal/family recipes

### Editing Recipes

1. **View Recipe**
   - Click recipe from list

2. **Click Edit Button**
   - (if available, or edit via the list)

3. **Modify Fields**
   - Title, ingredients, instructions
   - Times, servings, image URL

4. **Save Changes**
   - Click "Save recipe"

### Deleting Recipes

1. **View Recipe**
   - Click recipe from list

2. **Click Delete Button**
   - (usually in the detail view or list)

3. **Confirm Deletion**
   - Recipe is removed permanently

### Viewing Recipes

- **List View**: See all recipes at once
- **Detail View**: Full recipe with image and scaling controls
- **Search**: (Future feature)

---

## Categories

### What Are Categories?

Categories let you organize recipes by type:
- Breakfast, Lunch, Dinner
- Appetizers, Sides, Desserts
- Quick Meals, Slow Cooker, etc.

### Creating Categories

1. **When Saving a Recipe**
   - Go to "New category" field
   - Type category name
   - It's created automatically

2. **Multiple Categories**
   - A recipe can have multiple categories
   - Check multiple boxes when editing

### Using Categories

- Filter recipes by category (feature coming soon)
- Organize your recipe collection
- Make recipes easier to find

### Color-Coding

Categories can have colors (shown as colored badges):
- Visual organization
- Easy scanning of recipes
- Customizable in future updates

---

## AI Providers

### Overview
The app uses AI to intelligently extract recipe data when standard scraping fails.

### Available Providers

#### Ollama (Local)
```
Setup: ollama install + ollama pull llama3.2
Speed: 30-60 seconds
Cost: Free
Models: llama3.2, mistral, neural-chat, etc.
```

**Pros:**
- No API keys or accounts needed
- Completely free
- Runs on your computer
- Works offline

**Cons:**
- Slower than cloud AI
- Uses system resources
- First run takes longer
- Requires model download

#### Gemini (Google Cloud)
```
Setup: Get API key from https://aistudio.google.com/
Speed: 10-30 seconds
Cost: Free tier available (limited calls)
Models: Gemini-pro
```

**Pros:**
- Faster than Ollama
- High quality extractions
- Free tier available
- No local setup needed

**Cons:**
- Requires internet
- API key needed
- Limited free quota
- Paid after free tier

### Switching Providers

The app automatically tries:
1. Standard scraper
2. Gemini AI (if key provided)
3. Ollama (if running)

To use only one provider, set in `.env`:
```env
AI_MODEL_PROVIDER=ollama  # or gemini
```

### Testing Providers

Run the test script:
```bash
python test_ai_providers.py
```

Output shows which providers work:
```
OLLAMA: ✓ Working
GEMINI: ✓ Working
```

---

## Tips & Best Practices

### Performance
- **First import slow?** Models load into memory first time
- **Want faster?** Standard scraper is always fastest
- **Limited data?** Use Gemini with API key

### Quality
- **Recipes not parsing well?** Try with AI instead of standard scraper
- **Manual fixes?** Edit in the preview before saving
- **Complex layouts?** Gemini AI handles these better

### Organization
- **Use categories** to keep recipes organized
- **Save source URL** to reference original later
- **Update regularly** as you test and improve recipes

### Scaling
- **Fractional servings** work: 0.5, 1.5, 2.5, etc.
- **Edit manually** for complex scaling needs
- **Copy recipe** and adjust servings for variations

---

## Keyboard Shortcuts (Future)

- `Ctrl+/` - Search recipes
- `Ctrl+N` - New recipe
- `Ctrl+E` - Edit recipe
- `Esc` - Go back

---

## Common Questions

**Q: Can I scale cooking times?**
A: Currently no, only ingredient amounts scale. We're adding this feature soon.

**Q: Can I print recipes?**
A: Use your browser's print function (Ctrl+P). Better printer support coming soon.

**Q: Can I share recipes?**
A: Currently no sharing, but you can copy the recipe details. Sharing feature coming.

**Q: What if OCR is wrong?**
A: Edit the recipe before saving. The AI tries its best but manual review is always good.

**Q: Can I import shopping lists?**
A: Not yet, but we're planning this feature.

---

## Report Issues

Found a bug or have a feature request?
- Create an issue on GitHub
- Include what you were doing
- Describe what happened
- Suggest expected behavior

