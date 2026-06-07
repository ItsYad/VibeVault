from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import get_conn
from auth_helper import get_current_user

router = APIRouter()

class CollectionIn(BaseModel):
    item_id: int
    status: str = "saved"

@router.get("/")
def get_collection(user=Depends(get_current_user)):
    conn = get_conn()
    rows = conn.execute("""
        SELECT i.*, uc.status FROM user_collection uc
        JOIN items i ON uc.item_id = i.id
        WHERE uc.user_id=?
    """, (user["user_id"],)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.post("/")
def add_to_collection(data: CollectionIn, user=Depends(get_current_user)):
    conn = get_conn()
    existing = conn.execute(
        "SELECT id FROM user_collection WHERE user_id=? AND item_id=?",
        (user["user_id"], data.item_id)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE user_collection SET status=? WHERE user_id=? AND item_id=?",
            (data.status, user["user_id"], data.item_id)
        )
    else:
        conn.execute(
            "INSERT INTO user_collection (user_id, item_id, status) VALUES (?,?,?)",
            (user["user_id"], data.item_id, data.status)
        )
    conn.commit()
    conn.close()
    return {"message": "Collection updated!"}

@router.delete("/{item_id}")
def remove_from_collection(item_id: int, user=Depends(get_current_user)):
    conn = get_conn()
    conn.execute("DELETE FROM user_collection WHERE user_id=? AND item_id=?", (user["user_id"], item_id))
    conn.commit()
    conn.close()
    return {"message": "Removed from collection"}
