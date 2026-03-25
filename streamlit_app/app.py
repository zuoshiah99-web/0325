import streamlit as st
import httpx
from config import API_BASE

st.set_page_config(page_title="TriSys", layout="centered")

def login_page():
    st.title("系統登入")
    with st.form("login_form"):
        user_id = st.text_input("帳號")
        pw = st.text_input("密碼", type="password")
        submitted = st.form_submit_button("登入")
    if submitted:
        try:
            res = httpx.post(f"{API_BASE}/auth/login", json={"user_id": user_id, "pw": pw})
            if res.status_code == 200:
                st.session_state["user"] = res.json()["user"]
                st.rerun()
            else:
                st.error("帳號或密碼錯誤")
        except Exception as e:
            st.error(f"連線失敗：{e}")

def main_page():
    user = st.session_state["user"]
    st.title("三層式系統")
    st.write(f"歡迎，{user['user_name']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("客戶資料維護", use_container_width=True):
            st.session_state["page"] = "cust"
            st.rerun()
        if st.button("商品資料維護", use_container_width=True):
            st.session_state["page"] = "item"
            st.rerun()
    with col2:
        if st.button("廠商資料維護", use_container_width=True):
            st.session_state["page"] = "fact"
            st.rerun()
        if st.button("用戶資料維護", use_container_width=True):
            st.session_state["page"] = "user"
            st.rerun()

    st.divider()
    if st.button("登出"):
        st.session_state.clear()
        st.rerun()

def crud_page(title, endpoint, fields, id_field):
    st.title(title)
    if st.button("← 返回主選單"):
        st.session_state["page"] = "main"
        st.rerun()

    # 查詢
    q = st.text_input("查詢（代碼 / 名稱）")
    params = {"q": q} if q else {}
    rows = httpx.get(f"{API_BASE}/{endpoint}/", params=params).json()

    # 新增 / 修改 表單
    st.subheader("新增 / 修改")
    edit_key = f"edit_{endpoint}"
    editing = st.session_state.get(edit_key, {})

    with st.form(f"form_{endpoint}"):
        vals = {}
        for f in fields:
            disabled = (f["key"] == id_field and bool(editing))
            if f.get("options"):
                options = [""] + [r[f["options_key"]] + " " + r[f["options_label"]] for r in f["options_data"]]
                default = editing.get(f["key"], "")
                idx = next((i for i, o in enumerate(options) if o.startswith(default)), 0)
                vals[f["key"]] = st.selectbox(f["label"], options, index=idx).split(" ")[0]
            else:
                vals[f["key"]] = st.text_input(f["label"], value=editing.get(f["key"], ""), disabled=disabled)

        col1, col2 = st.columns(2)
        save = col1.form_submit_button("儲存" if editing else "新增")
        clear = col2.form_submit_button("清除")

    if save:
        try:
            if editing:
                httpx.put(f"{API_BASE}/{endpoint}/{editing[id_field]}", json={k: v for k, v in vals.items() if k != id_field})
                st.success("修改成功")
            else:
                httpx.post(f"{API_BASE}/{endpoint}/", json=vals)
                st.success("新增成功")
            st.session_state.pop(edit_key, None)
            st.rerun()
        except Exception as e:
            st.error(str(e))
    if clear:
        st.session_state.pop(edit_key, None)
        st.rerun()

    # 清單
    st.subheader(f"資料清單（{len(rows)} 筆）")
    for row in rows:
        cols = st.columns([3, 3, 3, 1, 1])
        for i, f in enumerate(fields):
            cols[i].write(row.get(f["key"], ""))
        if cols[len(fields)].button("修改", key=f"e_{row[id_field]}"):
            st.session_state[edit_key] = row
            st.rerun()
        if cols[len(fields)+1].button("刪除", key=f"d_{row[id_field]}"):
            httpx.delete(f"{API_BASE}/{endpoint}/{row[id_field]}")
            st.rerun()

# ── 路由 ──────────────────────────────────────────────────────
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
        facts = httpx.get(f"{API_BASE}/fact/").json()
        crud_page("商品資料維護", "item",
                  [{"key":"item_id","label":"商品代碼"},
                   {"key":"item_name","label":"商品名稱"},
                   {"key":"fact_code","label":"主供應商","options":True,"options_key":"fact_id","options_label":"fact_name","options_data":facts}],
                  "item_id")
    elif page == "user":
        crud_page("用戶資料維護", "user",
                  [{"key":"user_id","label":"用戶代碼"},{"key":"user_name","label":"用戶名稱"},{"key":"pw","label":"用戶密碼"}],
                  "user_id")
