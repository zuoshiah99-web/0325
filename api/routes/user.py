from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from db import get_conn

router = APIRouter()

class User(BaseModel):
    user_id: str
    user_name: Optional[str] = None
    pw: Optional[str] = None

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    pw: Optional[str] = None

@router.get("/")
def list_user(q: Optional[str] = None):
    conn = get_conn()
    cur = conn.cursor(as_dict=True)
    if q:
        cur.execute("SELECT * FROM [user] WHERE user_id LIKE %s OR user_name LIKE %s ORDER BY user_id",
                    (f"%{q}%", f"%{q}%"))
    else:
        cur.execute("SELECT * FROM [user] ORDER BY user_id")
    rows = cur.fetchall()
    conn.close()
    return rows

@router.post("/")
def add_user(body: User):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO [user] VALUES (%s,%s,%s)", (body.user_id, body.user_name, body.pw))
    conn.commit(); conn.close()
    return {"message": "新增成功"}

@router.put("/{user_id}")
def update_user(user_id: str, body: UserUpdate):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE [user] SET user_name=%s, pw=%s WHERE user_id=%s",
                (body.user_name, body.pw, user_id))
    conn.commit(); conn.close()
    return {"message": "修改成功"}

@router.delete("/{user_id}")
def delete_user(user_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM [user] WHERE user_id=%s", (user_id,))
    conn.commit(); conn.close()
    return {"message": "刪除成功"}
