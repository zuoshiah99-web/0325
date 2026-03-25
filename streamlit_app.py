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


def get_conn():
    return pymssql.connect(**DB_CONFIG)


# ── Login ─────────────────────────────────────────────────────────
def login_page():
    st.title("TriSys 系統登錄")
    with st.form("login_form"):
        user_id = st.text_input("用戶代碼")
        password = st.text_input("密碼", type="password")
        submitted = st.form_submit_button("登錄")
    if submitted:
        try:
            conn = get_conn()
            cur = conn.cursor(as_dict=True)
            cur.execute(
                "SELECT user_id, user_name FROM [user] WHERE user_id=%s AND pw=%s",
                (user_id, password),
            )
            row = cur.fetchone()
            cur.close()
            conn.close()
            if row:
                st.session_state.logged_in = True
                st.session_state.uid = row["user_id"]
                st.session_state.uname = row["user_name"]
                st.rerun()
            else:
                st.error("帳號或密碼錯誤")
        except Exception as e:
            st.error(f"連線失敗：{e}")


# ── CUST 客戶資料維護 ──────────────────────────────────────────────
def cust_page():
    st.header("客戶資料維護")
    q, add, mod, dele = st.tabs(["查詢", "新增", "修改", "刪除"])

    with q:
        kw = st.text_input("搜尋（客戶代碼 / 客戶名稱）", key="cust_kw")
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
            st.dataframe(pd.DataFrame(cur.fetchall()), use_container_width=True)
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"查詢失敗：{e}")

    with add:
        with st.form("cust_add"):
            c1, c2 = st.columns(2)
            cid = c1.text_input("客戶代碼")
            cname = c2.text_input("客戶名稱")
            remark = st.text_input("備註說明")
            if st.form_submit_button("新增"):
                try:
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO cust (cust_id, cust_name, remark) VALUES(%s, %s, %s)",
                        (cid, cname, remark),
                    )
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("新增成功")
                except Exception as e:
                    st.error(f"新增失敗：{e}")

    with mod:
        cid = st.text_input("輸入要修改的客戶代碼", key="cust_mod_id")
        if cid:
            try:
                conn = get_conn()
                cur = conn.cursor(as_dict=True)
                cur.execute("SELECT * FROM cust WHERE cust_id=%s", (cid,))
                row = cur.fetchone()
                cur.close()
                conn.close()
                if row:
                    with st.form("cust_mod"):
                        c1, c2 = st.columns(2)
                        new_name = c1.text_input("客戶名稱", value=row["cust_name"])
                        new_remark = c2.text_input("備註說明", value=row.get("remark") or "")
                        if st.form_submit_button("儲存修改"):
                            try:
                                conn = get_conn()
                                cur = conn.cursor()
                                cur.execute(
                                    "UPDATE cust SET cust_name=%s, remark=%s WHERE cust_id=%s",
                                    (new_name, new_remark, cid),
                                )
                                conn.commit()
                                cur.close()
                                conn.close()
                                st.success("修改成功")
                            except Exception as e:
                                st.error(f"修改失敗：{e}")
                else:
                    st.warning("查無此客戶代碼")
            except Exception as e:
                st.error(f"查詢失敗：{e}")

    with dele:
        with st.form("cust_del"):
            cid_del = st.text_input("輸入要刪除的客戶代碼")
            if st.form_submit_button("刪除", type="primary"):
                try:
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM cust WHERE cust_id=%s", (cid_del,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("刪除成功")
                except Exception as e:
                    st.error(f"刪除失敗：{e}")


# ── FACT 廠商資料維護 ──────────────────────────────────────────────
def fact_page():
    st.header("廠商資料維護")
    q, add, mod, dele = st.tabs(["查詢", "新增", "修改", "刪除"])

    with q:
        kw = st.text_input("搜尋（廠商代碼 / 廠商名稱）", key="fact_kw")
        try:
            conn = get_conn()
            cur = conn.cursor(as_dict=True)
            if kw:
                cur.execute(
                    "SELECT fact_id 廠商代碼, fact_name 廠商名稱, remark 備註 FROM fact "
                    "WHERE fact_id LIKE %s OR fact_name LIKE %s ORDER BY fact_id",
                    (f"%{kw}%", f"%{kw}%"),
                )
            else:
                cur.execute(
                    "SELECT fact_id 廠商代碼, fact_name 廠商名稱, remark 備註 FROM fact ORDER BY fact_id"
                )
            st.dataframe(pd.DataFrame(cur.fetchall()), use_container_width=True)
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"查詢失敗：{e}")

    with add:
        with st.form("fact_add"):
            c1, c2 = st.columns(2)
            fid = c1.text_input("廠商代碼")
            fname = c2.text_input("廠商名稱")
            remark = st.text_input("備註說明")
            if st.form_submit_button("新增"):
                try:
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO fact (fact_id, fact_name, remark) VALUES(%s, %s, %s)",
                        (fid, fname, remark),
                    )
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("新增成功")
                except Exception as e:
                    st.error(f"新增失敗：{e}")

    with mod:
        fid = st.text_input("輸入要修改的廠商代碼", key="fact_mod_id")
        if fid:
            try:
                conn = get_conn()
                cur = conn.cursor(as_dict=True)
                cur.execute("SELECT * FROM fact WHERE fact_id=%s", (fid,))
                row = cur.fetchone()
                cur.close()
                conn.close()
                if row:
                    with st.form("fact_mod"):
                        c1, c2 = st.columns(2)
                        new_name = c1.text_input("廠商名稱", value=row["fact_name"])
                        new_remark = c2.text_input("備註說明", value=row.get("remark") or "")
                        if st.form_submit_button("儲存修改"):
                            try:
                                conn = get_conn()
                                cur = conn.cursor()
                                cur.execute(
                                    "UPDATE fact SET fact_name=%s, remark=%s WHERE fact_id=%s",
                                    (new_name, new_remark, fid),
                                )
                                conn.commit()
                                cur.close()
                                conn.close()
                                st.success("修改成功")
                            except Exception as e:
                                st.error(f"修改失敗：{e}")
                else:
                    st.warning("查無此廠商代碼")
            except Exception as e:
                st.error(f"查詢失敗：{e}")

    with dele:
        with st.form("fact_del"):
            fid_del = st.text_input("輸入要刪除的廠商代碼")
            if st.form_submit_button("刪除", type="primary"):
                try:
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM fact WHERE fact_id=%s", (fid_del,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("刪除成功")
                except Exception as e:
                    st.error(f"刪除失敗：{e}")


# ── ITEM 商品資料維護 ──────────────────────────────────────────────
def get_fact_options():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT fact_id, fact_name FROM fact ORDER BY fact_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows  # list of (fact_id, fact_name)


def item_page():
    st.header("商品資料維護")
    q, add, mod, dele = st.tabs(["查詢", "新增", "修改", "刪除"])

    with q:
        kw = st.text_input("搜尋（商品代碼 / 商品名稱）", key="item_kw")
        try:
            conn = get_conn()
            cur = conn.cursor(as_dict=True)
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
            st.dataframe(pd.DataFrame(cur.fetchall()), use_container_width=True)
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"查詢失敗：{e}")

    with add:
        try:
            facts = get_fact_options()
            fact_labels = [f"{r[0]}  {r[1]}" for r in facts]
            fact_id_map = {f"{r[0]}  {r[1]}": r[0] for r in facts}
            with st.form("item_add"):
                c1, c2 = st.columns(2)
                iid = c1.text_input("商品代碼")
                iname = c2.text_input("商品名稱")
                fact_sel = st.selectbox("主供應商", fact_labels)
                if st.form_submit_button("新增"):
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO item (item_id, item_name, fact_code) VALUES(%s, %s, %s)",
                        (iid, iname, fact_id_map[fact_sel]),
                    )
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("新增成功")
        except Exception as e:
            st.error(f"新增失敗：{e}")

    with mod:
        iid = st.text_input("輸入要修改的商品代碼", key="item_mod_id")
        if iid:
            try:
                conn = get_conn()
                cur = conn.cursor(as_dict=True)
                cur.execute("SELECT * FROM item WHERE item_id=%s", (iid,))
                row = cur.fetchone()
                cur.close()
                conn.close()
                if row:
                    facts = get_fact_options()
                    fact_labels = [f"{r[0]}  {r[1]}" for r in facts]
                    fact_id_map = {f"{r[0]}  {r[1]}": r[0] for r in facts}
                    curr_idx = next(
                        (i for i, r in enumerate(facts) if r[0] == row["fact_code"]), 0
                    )
                    with st.form("item_mod"):
                        c1, c2 = st.columns(2)
                        new_name = c1.text_input("商品名稱", value=row["item_name"])
                        new_fact = c2.selectbox("主供應商", fact_labels, index=curr_idx)
                        if st.form_submit_button("儲存修改"):
                            conn = get_conn()
                            cur = conn.cursor()
                            cur.execute(
                                "UPDATE item SET item_name=%s, fact_code=%s WHERE item_id=%s",
                                (new_name, fact_id_map[new_fact], iid),
                            )
                            conn.commit()
                            cur.close()
                            conn.close()
                            st.success("修改成功")
                else:
                    st.warning("查無此商品代碼")
            except Exception as e:
                st.error(f"查詢失敗：{e}")

    with dele:
        with st.form("item_del"):
            iid_del = st.text_input("輸入要刪除的商品代碼")
            if st.form_submit_button("刪除", type="primary"):
                try:
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM item WHERE item_id=%s", (iid_del,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("刪除成功")
                except Exception as e:
                    st.error(f"刪除失敗：{e}")


# ── USER 用戶資料維護 ──────────────────────────────────────────────
def user_page():
    st.header("用戶資料維護")
    q, add, mod, dele = st.tabs(["查詢", "新增", "修改", "刪除"])

    with q:
        kw = st.text_input("搜尋（用戶代碼 / 用戶名稱）", key="user_kw")
        try:
            conn = get_conn()
            cur = conn.cursor(as_dict=True)
            if kw:
                cur.execute(
                    "SELECT user_id 用戶代碼, user_name 用戶名稱, pw 密碼 FROM [user] "
                    "WHERE user_id LIKE %s OR user_name LIKE %s ORDER BY user_id",
                    (f"%{kw}%", f"%{kw}%"),
                )
            else:
                cur.execute(
                    "SELECT user_id 用戶代碼, user_name 用戶名稱, pw 密碼 FROM [user] ORDER BY user_id"
                )
            st.dataframe(pd.DataFrame(cur.fetchall()), use_container_width=True)
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"查詢失敗：{e}")

    with add:
        with st.form("user_add"):
            c1, c2, c3 = st.columns(3)
            uid = c1.text_input("用戶代碼")
            uname = c2.text_input("用戶名稱")
            upw = c3.text_input("密碼")
            if st.form_submit_button("新增"):
                try:
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO [user] (user_id, user_name, pw) VALUES(%s, %s, %s)",
                        (uid, uname, upw),
                    )
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("新增成功")
                except Exception as e:
                    st.error(f"新增失敗：{e}")

    with mod:
        uid = st.text_input("輸入要修改的用戶代碼", key="user_mod_id")
        if uid:
            try:
                conn = get_conn()
                cur = conn.cursor(as_dict=True)
                cur.execute("SELECT * FROM [user] WHERE user_id=%s", (uid,))
                row = cur.fetchone()
                cur.close()
                conn.close()
                if row:
                    with st.form("user_mod"):
                        c1, c2 = st.columns(2)
                        new_name = c1.text_input("用戶名稱", value=row["user_name"])
                        new_pw = c2.text_input("密碼", value=row["pw"])
                        if st.form_submit_button("儲存修改"):
                            try:
                                conn = get_conn()
                                cur = conn.cursor()
                                cur.execute(
                                    "UPDATE [user] SET user_name=%s, pw=%s WHERE user_id=%s",
                                    (new_name, new_pw, uid),
                                )
                                conn.commit()
                                cur.close()
                                conn.close()
                                st.success("修改成功")
                            except Exception as e:
                                st.error(f"修改失敗：{e}")
                else:
                    st.warning("查無此用戶代碼")
            except Exception as e:
                st.error(f"查詢失敗：{e}")

    with dele:
        with st.form("user_del"):
            uid_del = st.text_input("輸入要刪除的用戶代碼")
            if st.form_submit_button("刪除", type="primary"):
                try:
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM [user] WHERE user_id=%s", (uid_del,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("刪除成功")
                except Exception as e:
                    st.error(f"刪除失敗：{e}")


# ── Main ──────────────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="TriSys", page_icon="🗂️", layout="wide")

    if not st.session_state.get("logged_in"):
        login_page()
        return

    with st.sidebar:
        st.title("TriSys")
        st.caption(f"歡迎，{st.session_state.uname}")
        st.divider()
        page = st.radio(
            "功能選單",
            ["客戶資料維護", "廠商資料維護", "商品資料維護", "用戶資料維護"],
        )
        st.divider()
        if st.button("登出", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    dispatch = {
        "客戶資料維護": cust_page,
        "廠商資料維護": fact_page,
        "商品資料維護": item_page,
        "用戶資料維護": user_page,
    }
    dispatch[page]()


main()
