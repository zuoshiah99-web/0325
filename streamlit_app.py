import streamlit as st
import pymssql
import pandas as pd

# ── DB Config ─────────────────────────────────────────────────────
DB_CONFIG = {
    "server": "163.17.141.61",
    "port": 8000,
    "database": "gemio11",
    "user": "nutc11",
    "password": "Nutc@2026",
}

# ── Login Credentials ─────────────────────────────────────────────
LOGIN_ID = "nutc11"
LOGIN_PW = "Nutc@2026"


def get_conn():
    return pymssql.connect(**DB_CONFIG)


# ── CSS ───────────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        /* ── Global ── */
        [data-testid="stAppViewContainer"] {
            background: #f0f4f8;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a2a4a 0%, #243b6e 100%);
        }
        [data-testid="stSidebar"] * {
            color: #e8eef7 !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.15);
        }
        /* Sidebar buttons: transparent bg with white border & text */
        [data-testid="stSidebar"] .stButton > button {
            background: rgba(255,255,255,0.08) !important;
            color: #e8eef7 !important;
            border: 1px solid rgba(255,255,255,0.30) !important;
            font-weight: 600;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255,255,255,0.20) !important;
            border-color: rgba(255,255,255,0.60) !important;
            transform: none;
            box-shadow: none;
        }

        /* ── Page header card ── */
        .page-header {
            background: linear-gradient(135deg, #1a2a4a 0%, #2e5fa3 100%);
            color: white;
            padding: 18px 28px;
            border-radius: 12px;
            margin-bottom: 20px;
            font-size: 22px;
            font-weight: 700;
            letter-spacing: 1px;
            box-shadow: 0 4px 12px rgba(30,60,120,0.18);
        }

        /* ── Tab styling ── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: #dce6f5;
            border-radius: 10px;
            padding: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 8px 22px;
            font-weight: 600;
            color: #2e5fa3;
        }
        .stTabs [aria-selected="true"] {
            background: #2e5fa3 !important;
            color: white !important;
        }

        /* ── Forms ── */
        [data-testid="stForm"] {
            background: white;
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        }

        /* ── Buttons ── */
        .stButton > button, .stFormSubmitButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(46,95,163,0.3);
        }

        /* ── Dataframe ── */
        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        }

        /* ── Login card ── */
        .login-card {
            background: white;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(30,60,120,0.12);
            max-width: 420px;
            margin: 60px auto 0;
            text-align: center;
        }
        .login-title {
            font-size: 28px;
            font-weight: 800;
            color: #1a2a4a;
            margin-bottom: 6px;
        }
        .login-sub {
            color: #7a90b0;
            margin-bottom: 28px;
            font-size: 14px;
        }

        /* ── Sidebar user badge ── */
        .user-badge {
            background: rgba(255,255,255,0.12);
            border-radius: 10px;
            padding: 10px 14px;
            margin: 8px 0 16px;
            font-size: 14px;
        }

        /* ── Main menu buttons ── */
        .menu-btn {
            background: white;
            border-radius: 16px;
            padding: 36px 20px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(30,60,120,0.10);
            cursor: pointer;
            transition: all 0.2s;
            border: 2px solid transparent;
        }
        .menu-btn:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(30,60,120,0.18);
            border-color: #2e5fa3;
        }
        .menu-icon { font-size: 48px; margin-bottom: 12px; }
        .menu-label { font-size: 18px; font-weight: 700; color: #1a2a4a; }
        .menu-sub { font-size: 13px; color: #7a90b0; margin-top: 4px; }

        .main-welcome {
            text-align: center;
            padding: 30px 0 10px;
        }
        .main-welcome h1 { color: #1a2a4a; font-size: 32px; font-weight: 800; }
        .main-welcome p  { color: #7a90b0; font-size: 15px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── Login ─────────────────────────────────────────────────────────
def login_page():
    inject_css()
    st.markdown(
        """
        <div class="login-card">
            <div class="login-title">TriSys</div>
            <div class="login-sub">三層式資料維護系統</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        with st.form("login_form"):
            user_id = st.text_input("用戶代碼", placeholder="請輸入帳號")
            password = st.text_input("密碼", type="password", placeholder="請輸入密碼")
            submitted = st.form_submit_button("登 錄", use_container_width=True, type="primary")

        if submitted:
            if user_id == LOGIN_ID and password == LOGIN_PW:
                st.session_state.logged_in = True
                st.session_state.uid = user_id
                st.session_state.uname = user_id
                st.rerun()
            else:
                st.error("帳號或密碼錯誤，請重試。")


# ── Page header helper ─────────────────────────────────────────────
def page_header(icon, title):
    st.markdown(
        f'<div class="page-header">{icon}&nbsp;&nbsp;{title}</div>',
        unsafe_allow_html=True,
    )


# ── Main Menu ─────────────────────────────────────────────────────
def main_menu():
    st.markdown(
        f"""
        <div class="main-welcome">
            <h1>歡迎，{st.session_state.uid}</h1>
            <p>請選擇要操作的功能</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    menus = [
        ("👥", "客戶資料維護", "CUST"),
        ("🏭", "廠商資料維護", "FACT"),
        ("📦", "商品資料維護", "ITEM"),
        ("👤", "用戶資料維護", "USER"),
    ]

    cols = st.columns(4, gap="large")
    for col, (icon, label, key) in zip(cols, menus):
        with col:
            st.markdown(
                f"""
                <div class="menu-btn">
                    <div class="menu-icon">{icon}</div>
                    <div class="menu-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button(f"進入", key=f"btn_{key}", use_container_width=True, type="primary"):
                st.session_state.page = label
                st.rerun()


# ── CUST 客戶資料維護 ──────────────────────────────────────────────
def cust_page():
    page_header("👥", "客戶資料維護")
    q, add, mod, dele = st.tabs(["🔍 查詢", "➕ 新增", "✏️ 修改", "🗑️ 刪除"])

    with q:
        kw = st.text_input("搜尋（客戶代碼 / 客戶名稱）", key="cust_kw", placeholder="輸入關鍵字...")
        try:
            conn = get_conn()
            cur = conn.cursor(as_dict=True)
            if kw:
                cur.execute(
                    "SELECT cust_id 客戶代碼, cust_name 客戶名稱, remark 備註 FROM cust "
                    "WHERE cust_id LIKE %s OR cust_name LIKE %s ORDER BY cust_id",
                    (f"%{kw}%", f"%{kw}%"),
                )
            else:
                cur.execute(
                    "SELECT cust_id 客戶代碼, cust_name 客戶名稱, remark 備註 FROM cust ORDER BY cust_id"
                )
            rows = cur.fetchall()
            cur.close(); conn.close()
            st.caption(f"共 {len(rows)} 筆")
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"查詢失敗：{e}")

    with add:
        with st.form("cust_add"):
            c1, c2 = st.columns(2)
            cid   = c1.text_input("客戶代碼")
            cname = c2.text_input("客戶名稱")
            remark = st.text_input("備註說明")
            if st.form_submit_button("新增", type="primary", use_container_width=True):
                try:
                    conn = get_conn(); cur = conn.cursor()
                    cur.execute("INSERT INTO cust (cust_id, cust_name, remark) VALUES(%s,%s,%s)", (cid, cname, remark))
                    conn.commit(); cur.close(); conn.close()
                    st.success("新增成功！")
                except Exception as e:
                    st.error(f"新增失敗：{e}")

    with mod:
        cid = st.text_input("輸入要修改的客戶代碼", key="cust_mod_id")
        if cid:
            try:
                conn = get_conn(); cur = conn.cursor(as_dict=True)
                cur.execute("SELECT * FROM cust WHERE cust_id=%s", (cid,))
                row = cur.fetchone(); cur.close(); conn.close()
                if row:
                    with st.form("cust_mod"):
                        c1, c2 = st.columns(2)
                        new_name   = c1.text_input("客戶名稱", value=row["cust_name"])
                        new_remark = c2.text_input("備註說明", value=row.get("remark") or "")
                        if st.form_submit_button("儲存修改", type="primary", use_container_width=True):
                            try:
                                conn = get_conn(); cur = conn.cursor()
                                cur.execute("UPDATE cust SET cust_name=%s,remark=%s WHERE cust_id=%s", (new_name, new_remark, cid))
                                conn.commit(); cur.close(); conn.close()
                                st.success("修改成功！")
                            except Exception as e:
                                st.error(f"修改失敗：{e}")
                else:
                    st.warning("查無此客戶代碼")
            except Exception as e:
                st.error(f"查詢失敗：{e}")

    with dele:
        with st.form("cust_del"):
            cid_del = st.text_input("輸入要刪除的客戶代碼")
            if st.form_submit_button("確認刪除", type="primary", use_container_width=True):
                try:
                    conn = get_conn(); cur = conn.cursor()
                    cur.execute("DELETE FROM cust WHERE cust_id=%s", (cid_del,))
                    conn.commit(); cur.close(); conn.close()
                    st.success("刪除成功！")
                except Exception as e:
                    st.error(f"刪除失敗：{e}")


# ── FACT 廠商資料維護 ──────────────────────────────────────────────
def fact_page():
    page_header("🏭", "廠商資料維護")
    q, add, mod, dele = st.tabs(["🔍 查詢", "➕ 新增", "✏️ 修改", "🗑️ 刪除"])

    with q:
        kw = st.text_input("搜尋（廠商代碼 / 廠商名稱）", key="fact_kw", placeholder="輸入關鍵字...")
        try:
            conn = get_conn(); cur = conn.cursor(as_dict=True)
            if kw:
                cur.execute(
                    "SELECT fact_id 廠商代碼, fact_name 廠商名稱, remark 備註 FROM fact "
                    "WHERE fact_id LIKE %s OR fact_name LIKE %s ORDER BY fact_id",
                    (f"%{kw}%", f"%{kw}%"),
                )
            else:
                cur.execute("SELECT fact_id 廠商代碼, fact_name 廠商名稱, remark 備註 FROM fact ORDER BY fact_id")
            rows = cur.fetchall(); cur.close(); conn.close()
            st.caption(f"共 {len(rows)} 筆")
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"查詢失敗：{e}")

    with add:
        with st.form("fact_add"):
            c1, c2 = st.columns(2)
            fid    = c1.text_input("廠商代碼")
            fname  = c2.text_input("廠商名稱")
            remark = st.text_input("備註說明")
            if st.form_submit_button("新增", type="primary", use_container_width=True):
                try:
                    conn = get_conn(); cur = conn.cursor()
                    cur.execute("INSERT INTO fact (fact_id, fact_name, remark) VALUES(%s,%s,%s)", (fid, fname, remark))
                    conn.commit(); cur.close(); conn.close()
                    st.success("新增成功！")
                except Exception as e:
                    st.error(f"新增失敗：{e}")

    with mod:
        fid = st.text_input("輸入要修改的廠商代碼", key="fact_mod_id")
        if fid:
            try:
                conn = get_conn(); cur = conn.cursor(as_dict=True)
                cur.execute("SELECT * FROM fact WHERE fact_id=%s", (fid,))
                row = cur.fetchone(); cur.close(); conn.close()
                if row:
                    with st.form("fact_mod"):
                        c1, c2 = st.columns(2)
                        new_name   = c1.text_input("廠商名稱", value=row["fact_name"])
                        new_remark = c2.text_input("備註說明", value=row.get("remark") or "")
                        if st.form_submit_button("儲存修改", type="primary", use_container_width=True):
                            try:
                                conn = get_conn(); cur = conn.cursor()
                                cur.execute("UPDATE fact SET fact_name=%s,remark=%s WHERE fact_id=%s", (new_name, new_remark, fid))
                                conn.commit(); cur.close(); conn.close()
                                st.success("修改成功！")
                            except Exception as e:
                                st.error(f"修改失敗：{e}")
                else:
                    st.warning("查無此廠商代碼")
            except Exception as e:
                st.error(f"查詢失敗：{e}")

    with dele:
        with st.form("fact_del"):
            fid_del = st.text_input("輸入要刪除的廠商代碼")
            if st.form_submit_button("確認刪除", type="primary", use_container_width=True):
                try:
                    conn = get_conn(); cur = conn.cursor()
                    cur.execute("DELETE FROM fact WHERE fact_id=%s", (fid_del,))
                    conn.commit(); cur.close(); conn.close()
                    st.success("刪除成功！")
                except Exception as e:
                    st.error(f"刪除失敗：{e}")


# ── ITEM 商品資料維護 ──────────────────────────────────────────────
def get_fact_options():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT fact_id, fact_name FROM fact ORDER BY fact_id")
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows


def item_page():
    page_header("📦", "商品資料維護")
    q, add, mod, dele = st.tabs(["🔍 查詢", "➕ 新增", "✏️ 修改", "🗑️ 刪除"])

    with q:
        kw = st.text_input("搜尋（商品代碼 / 商品名稱）", key="item_kw", placeholder="輸入關鍵字...")
        try:
            conn = get_conn(); cur = conn.cursor(as_dict=True)
            if kw:
                cur.execute(
                    "SELECT i.item_id 商品代碼, i.item_name 商品名稱, "
                    "i.fact_code 廠商代碼, f.fact_name 廠商名稱 "
                    "FROM item i LEFT JOIN fact f ON i.fact_code=f.fact_id "
                    "WHERE i.item_id LIKE %s OR i.item_name LIKE %s ORDER BY i.item_id",
                    (f"%{kw}%", f"%{kw}%"),
                )
            else:
                cur.execute(
                    "SELECT i.item_id 商品代碼, i.item_name 商品名稱, "
                    "i.fact_code 廠商代碼, f.fact_name 廠商名稱 "
                    "FROM item i LEFT JOIN fact f ON i.fact_code=f.fact_id ORDER BY i.item_id"
                )
            rows = cur.fetchall(); cur.close(); conn.close()
            st.caption(f"共 {len(rows)} 筆")
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"查詢失敗：{e}")

    with add:
        try:
            facts = get_fact_options()
            fact_labels = [f"{r[0]}  {r[1]}" for r in facts]
            fact_id_map = {f"{r[0]}  {r[1]}": r[0] for r in facts}
            with st.form("item_add"):
                c1, c2 = st.columns(2)
                iid   = c1.text_input("商品代碼")
                iname = c2.text_input("商品名稱")
                fact_sel = st.selectbox("主供應商", fact_labels)
                if st.form_submit_button("新增", type="primary", use_container_width=True):
                    conn = get_conn(); cur = conn.cursor()
                    cur.execute("INSERT INTO item (item_id, item_name, fact_code) VALUES(%s,%s,%s)", (iid, iname, fact_id_map[fact_sel]))
                    conn.commit(); cur.close(); conn.close()
                    st.success("新增成功！")
        except Exception as e:
            st.error(f"新增失敗：{e}")

    with mod:
        iid = st.text_input("輸入要修改的商品代碼", key="item_mod_id")
        if iid:
            try:
                conn = get_conn(); cur = conn.cursor(as_dict=True)
                cur.execute("SELECT * FROM item WHERE item_id=%s", (iid,))
                row = cur.fetchone(); cur.close(); conn.close()
                if row:
                    facts = get_fact_options()
                    fact_labels = [f"{r[0]}  {r[1]}" for r in facts]
                    fact_id_map = {f"{r[0]}  {r[1]}": r[0] for r in facts}
                    curr_idx = next((i for i, r in enumerate(facts) if r[0] == row["fact_code"]), 0)
                    with st.form("item_mod"):
                        c1, c2 = st.columns(2)
                        new_name = c1.text_input("商品名稱", value=row["item_name"])
                        new_fact = c2.selectbox("主供應商", fact_labels, index=curr_idx)
                        if st.form_submit_button("儲存修改", type="primary", use_container_width=True):
                            conn = get_conn(); cur = conn.cursor()
                            cur.execute("UPDATE item SET item_name=%s,fact_code=%s WHERE item_id=%s", (new_name, fact_id_map[new_fact], iid))
                            conn.commit(); cur.close(); conn.close()
                            st.success("修改成功！")
                else:
                    st.warning("查無此商品代碼")
            except Exception as e:
                st.error(f"查詢失敗：{e}")

    with dele:
        with st.form("item_del"):
            iid_del = st.text_input("輸入要刪除的商品代碼")
            if st.form_submit_button("確認刪除", type="primary", use_container_width=True):
                try:
                    conn = get_conn(); cur = conn.cursor()
                    cur.execute("DELETE FROM item WHERE item_id=%s", (iid_del,))
                    conn.commit(); cur.close(); conn.close()
                    st.success("刪除成功！")
                except Exception as e:
                    st.error(f"刪除失敗：{e}")


# ── USER 用戶資料維護 ──────────────────────────────────────────────
def user_page():
    page_header("👤", "用戶資料維護")
    q, add, mod, dele = st.tabs(["🔍 查詢", "➕ 新增", "✏️ 修改", "🗑️ 刪除"])

    with q:
        kw = st.text_input("搜尋（用戶代碼 / 用戶名稱）", key="user_kw", placeholder="輸入關鍵字...")
        try:
            conn = get_conn(); cur = conn.cursor(as_dict=True)
            if kw:
                cur.execute(
                    "SELECT user_id 用戶代碼, user_name 用戶名稱, pw 密碼 FROM [user] "
                    "WHERE user_id LIKE %s OR user_name LIKE %s ORDER BY user_id",
                    (f"%{kw}%", f"%{kw}%"),
                )
            else:
                cur.execute("SELECT user_id 用戶代碼, user_name 用戶名稱, pw 密碼 FROM [user] ORDER BY user_id")
            rows = cur.fetchall(); cur.close(); conn.close()
            st.caption(f"共 {len(rows)} 筆")
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"查詢失敗：{e}")

    with add:
        with st.form("user_add"):
            c1, c2, c3 = st.columns(3)
            uid   = c1.text_input("用戶代碼")
            uname = c2.text_input("用戶名稱")
            upw   = c3.text_input("密碼")
            if st.form_submit_button("新增", type="primary", use_container_width=True):
                try:
                    conn = get_conn(); cur = conn.cursor()
                    cur.execute("INSERT INTO [user] (user_id, user_name, pw) VALUES(%s,%s,%s)", (uid, uname, upw))
                    conn.commit(); cur.close(); conn.close()
                    st.success("新增成功！")
                except Exception as e:
                    st.error(f"新增失敗：{e}")

    with mod:
        uid = st.text_input("輸入要修改的用戶代碼", key="user_mod_id")
        if uid:
            try:
                conn = get_conn(); cur = conn.cursor(as_dict=True)
                cur.execute("SELECT * FROM [user] WHERE user_id=%s", (uid,))
                row = cur.fetchone(); cur.close(); conn.close()
                if row:
                    with st.form("user_mod"):
                        c1, c2 = st.columns(2)
                        new_name = c1.text_input("用戶名稱", value=row["user_name"])
                        new_pw   = c2.text_input("密碼", value=row["pw"])
                        if st.form_submit_button("儲存修改", type="primary", use_container_width=True):
                            try:
                                conn = get_conn(); cur = conn.cursor()
                                cur.execute("UPDATE [user] SET user_name=%s,pw=%s WHERE user_id=%s", (new_name, new_pw, uid))
                                conn.commit(); cur.close(); conn.close()
                                st.success("修改成功！")
                            except Exception as e:
                                st.error(f"修改失敗：{e}")
                else:
                    st.warning("查無此用戶代碼")
            except Exception as e:
                st.error(f"查詢失敗：{e}")

    with dele:
        with st.form("user_del"):
            uid_del = st.text_input("輸入要刪除的用戶代碼")
            if st.form_submit_button("確認刪除", type="primary", use_container_width=True):
                try:
                    conn = get_conn(); cur = conn.cursor()
                    cur.execute("DELETE FROM [user] WHERE user_id=%s", (uid_del,))
                    conn.commit(); cur.close(); conn.close()
                    st.success("刪除成功！")
                except Exception as e:
                    st.error(f"刪除失敗：{e}")


# ── Main ──────────────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="TriSys", page_icon="🗂️", layout="wide")
    inject_css()

    if not st.session_state.get("logged_in"):
        login_page()
        return

    with st.sidebar:
        st.markdown("## 🗂️ TriSys")
        st.markdown(
            f'<div class="user-badge">👤&nbsp;&nbsp;{st.session_state.uid}</div>',
            unsafe_allow_html=True,
        )
        st.divider()
        if st.button("🏠 主畫面", use_container_width=True):
            st.session_state.page = "主畫面"
            st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        for label in ["👥 客戶資料維護", "🏭 廠商資料維護", "📦 商品資料維護", "👤 用戶資料維護"]:
            clean = label[2:].strip()
            if st.button(label, use_container_width=True, key=f"side_{clean}"):
                st.session_state.page = clean
                st.rerun()
        st.divider()
        if st.button("登出", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    page = st.session_state.get("page", "主畫面")
    dispatch = {
        "主畫面":     main_menu,
        "客戶資料維護": cust_page,
        "廠商資料維護": fact_page,
        "商品資料維護": item_page,
        "用戶資料維護": user_page,
    }
    dispatch.get(page, main_menu)()


main()
