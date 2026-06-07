from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import get_conn
from auth_helper import get_current_user

router = APIRouter()

class MoodboardIn(BaseModel):
    theme_color: str = "#6C63FF"
    quote: str = ""
    is_public: bool = False

@router.get("/")
def get_moodboard(user=Depends(get_current_user)):
    conn = get_conn()
    mb = conn.execute("SELECT * FROM moodboards WHERE user_id=?", (user["user_id"],)).fetchone()
    if not mb:
        conn.close()
        return {"theme_color": "#6C63FF", "quote": "", "is_public": False, "pinned_items": []}
    pinned = conn.execute("""
        SELECT i.* FROM user_collection uc
        JOIN items i ON uc.item_id = i.id
        WHERE uc.user_id=? AND uc.status='pinned'
    """, (user["user_id"],)).fetchall()
    conn.close()
    result = dict(mb)
    result["pinned_items"] = [dict(p) for p in pinned]
    return result

@router.post("/")
def save_moodboard(data: MoodboardIn, user=Depends(get_current_user)):
    conn = get_conn()
    existing = conn.execute("SELECT id FROM moodboards WHERE user_id=?", (user["user_id"],)).fetchone()
    if existing:
        conn.execute(
            "UPDATE moodboards SET theme_color=?, quote=?, is_public=? WHERE user_id=?",
            (data.theme_color, data.quote, int(data.is_public), user["user_id"])
        )
    else:
        conn.execute(
            "INSERT INTO moodboards (user_id, theme_color, quote, is_public) VALUES (?,?,?,?)",
            (user["user_id"], data.theme_color, data.quote, int(data.is_public))
        )
    conn.commit()
    conn.close()
    return {"message": "Moodboard saved!"}
