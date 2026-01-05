# run_app.ps1 - Start the recipe app on port 8001

.\.venv\Scripts\uvicorn.exe app.main:app --port 8001 --reload
