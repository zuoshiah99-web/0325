from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_conn

router = APIRouter()

class LoginIn(BaseModel):
    user_id: str
    pw: str

@router.post("/login")
def login(body: LoginIn):
    conn = get_conn()
    cur = conn.cursor(as_dict=True)
    cur.execute("SELECT user_id, user_name FROM [user] WHERE user_id=%s AND pw=%s",
                (body.user_id, body.pw))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=401, detail="帳號或密碼錯誤")
    return {"user": row}
