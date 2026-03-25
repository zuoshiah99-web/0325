from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from db import get_conn

router = APIRouter()

class Fact(BaseModel):
    fact_id: str
    fact_name: Optional[str] = None
    remark: Optional[str] = None

class FactUpdate(BaseModel):
    fact_name: Optional[str] = None
    remark: Optional[str] = None

@router.get("/")
def list_fact(q: Optional[str] = None):
    conn = get_conn()
    cur = conn.cursor(as_dict=True)
    if q:
        cur.execute("SELECT * FROM fact WHERE fact_id LIKE %s OR fact_name LIKE %s ORDER BY fact_id",
                    (f"%{q}%", f"%{q}%"))
    else:
        cur.execute("SELECT * FROM fact ORDER BY fact_id")
    rows = cur.fetchall()
    conn.close()
    return rows

@router.post("/")
def add_fact(body: Fact):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO fact VALUES (%s,%s,%s)", (body.fact_id, body.fact_name, body.remark))
    conn.commit(); conn.close()
    return {"message": "新增成功"}

@router.put("/{fact_id}")
def update_fact(fact_id: str, body: FactUpdate):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE fact SET fact_name=%s, remark=%s WHERE fact_id=%s",
                (body.fact_name, body.remark, fact_id))
    conn.commit(); conn.close()
    return {"message": "修改成功"}

@router.delete("/{fact_id}")
def delete_fact(fact_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM fact WHERE fact_id=%s", (fact_id,))
    conn.commit(); conn.close()
    return {"message": "刪除成功"}
