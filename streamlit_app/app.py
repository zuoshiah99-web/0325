import streamlit as st
import pymssql
import os

st.set_page_config(page_title="TriSys", layout="centered")

# ── DB 連線 ──────────────────────────────────────────────────
def get_conn():
    return pymssql.connect(
        server=st.secrets["DB_SERVER"],
        port=int(st.secrets["DB_PORT"]),
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_DATABASE"],
        charset="UTF-8",
    )

# ── 登入頁 ───────────────────────────────────────────────────
def login_page():
    st.title("系統登入")
    with st.form("login_form"):
        user_id = st.text_input("帳號")
        pw = st.text_input("密碼", type="password")
        submitted = st.form_submit_button("登入")
    if submitted:
        try:
            conn = get_conn()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT user_id, user_name FROM [user] WHERE user_id=%s AND pw=%s", (user_id, pw))
            row = cur.fetchone()
            conn.close()
            if row:
                st.session_state["user"] = row
                st.rerun()
            else:
                st.error("帳號或密碼錯誤")
        except Exception as e:
            st.error(f"連線失敗：{e}")

# ── 主選單 ───────────────────────────────────────────────────
def main_page():
    user = st.session_state["user"]
    st.title("三層式系統")
    st.write(f"歡迎，{user['user_name']}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("客戶資料維護", use_container_width=True):
            st.session_state["page"] = "cust"; st.rerun()
        if st.button("商品資料維護", use_container_width=True):
            st.session_state["page"] = "item"; st.rerun()
    with col2:
        if st.button("廠商資料維護", use_container_width=True):
            st.session_state["page"] = "fact"; st.rerun()
        if st.button("用戶資料維護", use_container_width=True):
            st.session_state["page"] = "user"; st.rerun()
    st.divider()
    if st.button("登出"):
        st.session_state.clear(); st.rerun()

# ── 通用 CRUD 頁 ─────────────────────────────────────────────
def crud_page(title, table, fields, id_field, extra_query=None):
    st.title(title)
    if st.button("← 返回主選單"):
        st.session_state.pop(f"edit_{table}", None)
        st.session_state["page"] = "main"; st.rerun()

    q = st.text_input("查詢（代碼 / 名稱）")
    conn = get_conn()
    cur = conn.cursor(as_dict=True)
    if q:
        cur.execute(f"SELECT * FROM [{table}] WHERE {id_field} LIKE %s OR {fields[1]['key']} LIKE %s ORDER BY {id_field}",
                    (f"%{q}%", f"%{q}%"))
    else:
        cur.execute(f"SELECT * FROM [{table}] ORDER BY {id_field}")
    rows = cur.fetchall()

    if extra_query:
        cur.execute(extra_query["sql"])
        extra_rows = cur.fetchall()
    conn.close()

    edit_key = f"edit_{table}"
    editing = st.session_state.get(edit_key, {})

    st.subheader("新增 / 修改")
    with st.form(f"form_{table}"):
        vals = {}
        for f in fields:
            disabled = (f["key"] == id_field and bool(editing))
            if f.get("select"):
                options = [""] + [r[extra_query["val"]] for r in extra_rows]
                labels  = ["-- 請選擇 --"] + [f"{r[extra_query['val']]} {r[extra_query['label']]}" for r in extra_rows]
                default = editing.get(f["key"], "")
                idx = next((i for i, v in enumerate(options) if v == default), 0)
                chosen = st.selectbox(f["label"], labels, index=idx)
                vals[f["key"]] = options[labels.index(chosen)] if chosen != "-- 請選擇 --" else ""
            else:
                vals[f["key"]] = st.text_input(f["label"], value=editing.get(f["key"], ""), disabled=disabled)
        c1, c2 = st.columns(2)
        save  = c1.form_submit_button("儲存修改" if editing else "確認新增")
        clear = c2.form_submit_button("清除")

    if save:
        try:
            conn = get_conn()
            cur = conn.cursor()
            if editing:
                set_clause = ", ".join([f"{f['key']}=%s" for f in fields if f["key"] != id_field])
                set_vals   = [vals[f["key"]] for f in fields if f["key"] != id_field]
                cur.execute(f"UPDATE [{table}] SET {set_clause} WHERE {id_field}=%s", (*set_vals, editing[id_field]))
                st.success("修改成功")
            else:
                placeholders = ",".join(["%s"] * len(fields))
                cur.execute(f"INSERT INTO [{table}] VALUES ({placeholders})", [vals[f["key"]] for f in fields])
                st.success("新增成功")
            conn.commit(); conn.close()
            st.session_state.pop(edit_key, None); st.rerun()
        except Exception as e:
            st.error(str(e))
    if clear:
        st.session_state.pop(edit_key, None); st.rerun()

    st.subheader(f"資料清單（{len(rows)} 筆）")
    header = st.columns([2, 3, 3, 1, 1])
    for i, f in enumerate(fields):
        header[i].markdown(f"**{f['label']}**")
    for row in rows:
        cols = st.columns([2, 3, 3, 1, 1])
        for i, f in enumerate(fields):
            cols[i].write(row.get(f["key"], ""))
        if cols[len(fields)].button("修改", key=f"e_{row[id_field]}"):
            st.session_state[edit_key] = row; st.rerun()
        if cols[len(fields)+1].button("刪除", key=f"d_{row[id_field]}"):
            conn = get_conn(); cur = conn.cursor()
            cur.execute(f"DELETE FROM [{table}] WHERE {id_field}=%s", (row[id_field],))
            conn.commit(); conn.close(); st.rerun()

# ── 路由 ─────────────────────────────────────────────────────
if "user" not in st.session_state:
    login_page()
else:
    page = st.session_state.get("page", "main")
    if page == "main":
        main_page()
    elif page == "cust":
        crud_page("客戶資料維護", "cust",
                  [{"key":"cust_id","label":"客戶代碼"},{"key":"cust_name","label":"客戶名稱"},{"key":"remark","label":"備註說明"}],
                  "cust_id")
    elif page == "fact":
        crud_page("廠商資料維護", "fact",
                  [{"key":"fact_id","label":"廠商代碼"},{"key":"fact_name","label":"廠商名稱"},{"key":"remark","label":"備註說明"}],
                  "fact_id")
    elif page == "item":
        crud_page("商品資料維護", "item",
                  [{"key":"item_id","label":"商品代碼"},{"key":"item_name","label":"商品名稱"},
                   {"key":"fact_code","label":"主供應商","select":True}],
                  "item_id",
                  extra_query={"sql":"SELECT fact_id, fact_name FROM fact ORDER BY fact_id","val":"fact_id","label":"fact_name"})
    elif page == "user":
        crud_page("用戶資料維護", "user",
                  [{"key":"user_id","label":"用戶代碼"},{"key":"user_name","label":"用戶名稱"},{"key":"pw","label":"用戶密碼"}],
                  "user_id")
