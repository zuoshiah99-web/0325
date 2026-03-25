from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from db import get_conn

router = APIRouter()

class Item(BaseModel):
    item_id: str
    item_name: Optional[str] = None
    fact_code: Optional[str] = None

class ItemUpdate(BaseModel):
    item_name: Optional[str] = None
    fact_code: Optional[str] = None

@router.get("/")
def list_item(q: Optional[str] = None):
    conn = get_conn()
    cur = conn.cursor(as_dict=True)
    if q:
        cur.execute("SELECT * FROM item WHERE item_id LIKE %s OR item_name LIKE %s ORDER BY item_id",
                    (f"%{q}%", f"%{q}%"))
    else:
        cur.execute("SELECT * FROM item ORDER BY item_id")
    rows = cur.fetchall()
    conn.close()
    return rows

@router.post("/")
def add_item(body: Item):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO item VALUES (%s,%s,%s)", (body.item_id, body.item_name, body.fact_code))
    conn.commit(); conn.close()
    return {"message": "新增成功"}

@router.put("/{item_id}")
def update_item(item_id: str, body: ItemUpdate):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE item SET item_name=%s, fact_code=%s WHERE item_id=%s",
                (body.item_name, body.fact_code, item_id))
    conn.commit(); conn.close()
    return {"message": "修改成功"}

@router.delete("/{item_id}")
def delete_item(item_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM item WHERE item_id=%s", (item_id,))
    conn.commit(); conn.close()
    return {"message": "刪除成功"}
