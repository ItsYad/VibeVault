from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import auth, items, collection, moodboard

app = FastAPI(title="VibeVault API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(collection.router, prefix="/collection", tags=["Collection"])
app.include_router(moodboard.router, prefix="/moodboard", tags=["Moodboard"])

@app.get("/")
def root():
    return {"message": "VibeVault API is running!"}
