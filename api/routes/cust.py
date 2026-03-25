from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from db import get_conn

router = APIRouter()

class Cust(BaseModel):
    cust_id: str
    cust_name: Optional[str] = None
    remark: Optional[str] = None

class CustUpdate(BaseModel):
    cust_name: Optional[str] = None
    remark: Optional[str] = None

@router.get("/")
def list_cust(q: Optional[str] = None):
    conn = get_conn()
    cur = conn.cursor(as_dict=True)
    if q:
        cur.execute("SELECT * FROM cust WHERE cust_id LIKE %s OR cust_name LIKE %s ORDER BY cust_id",
                    (f"%{q}%", f"%{q}%"))
    else:
        cur.execute("SELECT * FROM cust ORDER BY cust_id")
    rows = cur.fetchall()
    conn.close()
    return rows

@router.post("/")
def add_cust(body: Cust):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO cust VALUES (%s,%s,%s)", (body.cust_id, body.cust_name, body.remark))
    conn.commit(); conn.close()
    return {"message": "新增成功"}

@router.put("/{cust_id}")
def update_cust(cust_id: str, body: CustUpdate):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE cust SET cust_name=%s, remark=%s WHERE cust_id=%s",
                (body.cust_name, body.remark, cust_id))
    conn.commit(); conn.close()
    return {"message": "修改成功"}

@router.delete("/{cust_id}")
def delete_cust(cust_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM cust WHERE cust_id=%s", (cust_id,))
    conn.commit(); conn.close()
    return {"message": "刪除成功"}
