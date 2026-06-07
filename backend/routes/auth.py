from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_conn
from auth_helper import hash_password, verify_password, create_token

router = APIRouter()

BADGE_MAP = {
    ("film", "Dark"): "Dark Aesthetic Cinephile",
    ("film", "Epic"): "Epic Storyteller",
    ("film", "Dreamy"): "Dreamy Visionary",
    ("musik", "Chill"): "Chill Vibes Curator",
    ("musik", "Energetic"): "Energetic Soul",
    ("musik", "Melancholic"): "Indie Soul Listener",
}

class RegisterIn(BaseModel):
    username: str
    password: str
    bio: str = ""
    fav_type: str = "film"
    fav_mood: str = "Epic"

class LoginIn(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(data: RegisterIn):
    badge = BADGE_MAP.get((data.fav_type, data.fav_mood), "Vibe Explorer")
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO users (username, password, bio, badge) VALUES (?,?,?,?)",
            (data.username, hash_password(data.password), data.bio, badge)
        )
        conn.commit()
        return {"message": "Registered successfully!", "badge": badge}
    except Exception:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()

@router.post("/login")
def login(data: LoginIn):
    conn = get_conn()
    user = conn.execute("SELECT * FROM users WHERE username=?", (data.username,)).fetchone()
    conn.close()
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user["id"], user["username"])
    return {"token": token, "username": user["username"], "badge": user["badge"], "bio": user["bio"]}
