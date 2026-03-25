from pathlib import Path

from fastapi import FastAPI, APIRouter, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from AI.groq import get_groq_response

# -----------------------
# FastAPI app & router
# -----------------------
app = FastAPI(title="HealthAI Recommendations API")
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://activity-planner-sigma.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Frontend static files
# -----------------------
FRONTEND_DIR = Path("Frontend")
FRONTEND_FILE = FRONTEND_DIR / "index.html"

# Mount static directory for assets (CSS, JS, images)
# app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# -----------------------
# Routes
# -----------------------

@router.get("/", response_class=HTMLResponse)
async def root() -> str:
    """Serve the main frontend HTML file."""
    if not FRONTEND_FILE.exists():
        raise HTTPException(status_code=404, detail="Frontend file not found")
    return FRONTEND_FILE.read_text(encoding="utf-8")


@router.post("/recommendations")
async def get_recommendations(payload: dict = Body(...)) -> dict:
    """
    Accept a prompt and return AI-generated recommendations.
    Expects payload to contain a 'prompt' key.
    """
    prompt = payload.get("prompt", "").strip()

    if not prompt:
        raise HTTPException(
            status_code=400,
            detail="Prompt is required",
        )

    result = await get_groq_response(prompt=prompt)
    return {"recommendations": result}


# Include the router in the main app
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
