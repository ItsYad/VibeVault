from fastapi import APIRouter, Depends
from database import get_conn
from auth_helper import get_current_user
import random

router = APIRouter()

@router.get("/")
def get_items(type: str = None, genre: str = None, mood: str = None, user=Depends(get_current_user)):
    conn = get_conn()
    query = "SELECT * FROM items WHERE 1=1"
    params = []
    if type:
        query += " AND type=?"; params.append(type)
    if genre:
        query += " AND genre=?"; params.append(genre)
    if mood:
        query += " AND mood=?"; params.append(mood)
    items = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(i) for i in items]

@router.get("/surprise")
def surprise_me(type: str = None, user=Depends(get_current_user)):
    conn = get_conn()
    query = "SELECT * FROM items"
    params = []
    if type:
        query += " WHERE type=?"; params.append(type)
    items = conn.execute(query, params).fetchall()
    conn.close()
    if not items:
        return {"message": "No items found"}
    return dict(random.choice(items))
