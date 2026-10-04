# =============================================================
# answers/w1/app.py — Tech0 Search v0.1（W1 完成版）
# まず自分で書いてから見比べること！
# 起動： streamlit run app.py  （同じフォルダに search.py と pages_w1.json が必要）
# =============================================================
import streamlit as st
import json
from datetime import date
from search import search_pages, highlight_match   # Step 4 で作った関数

# ── ② データの読み書き関数（Step 3 で学んだ json.load / json.dump） ──
@st.cache_data
def load_pages():
    with open("pages_w1.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_pages(pages):
    with open("pages_w1.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

# ── ③ ページ設定・タイトル ──
st.set_page_config(page_title="Tech0 Search v0.1", page_icon="🔍")
st.title("🔍 Tech0 Search v0.1")
st.caption("PROJECT ZERO — 社内ナレッジ検索エンジン")

# ── ④ タブを作る ──
tab1, tab2, tab3 = st.tabs(["検索", "登録", "一覧"])
pages = load_pages()

# ── ⑤ 検索タブ ──
with tab1:
    st.subheader("🔍 キーワード検索")
    query = st.text_input("🔑 キーワードを入力")

    if query:
        results = search_pages(query, pages)          # Step 4 の関数
        st.markdown(f"**検索結果: {len(results)}件**")
        st.divider()

        for page in results:
            st.markdown(f"### [{page['title']}]({page['url']})")
            st.markdown(highlight_match(page["description"], query))  # キーワードを太字に
            tags = " , ".join([f"`{kw}`" for kw in page["keywords"]])
            st.markdown(f"🏷 {tags}")
            col1, col2 = st.columns(2)
            col1.caption(f"👤 {page['author']}")
            col2.caption(f"📅 {page['created_at']}")
            st.caption(f"🔗 {page['url']}")
            st.divider()

# ── ⑥ 登録タブ ──
with tab2:
    st.subheader("📝 ページを登録")

    # 直前の実行で登録が完了していたら、そのメッセージを出す。
    # st.rerun() で画面を作り直すと、それより前に表示したものは消えてしまうため、
    # 「登録した」という印を st.session_state に残して、走り直した後に読む。
    if st.session_state.get("registered"):
        st.success("登録完了！")
        st.session_state["registered"] = False   # 一度出したら印を消す

    with st.form("register_form"):
        url         = st.text_input("URL")
        title       = st.text_input("タイトル")
        description = st.text_area("説明")
        keywords    = st.text_input("キーワード（カンマ区切り）")
        author      = st.text_input("作成者")
        category    = st.selectbox("カテゴリ", ["事例", "企画", "業務マニュアル", "研修", "共有"])
        submitted   = st.form_submit_button("登録する")

    if submitted:
        if not url or not title:
            st.error("URL とタイトルは必須です")
        else:
            new_page = {
                "id"         : len(pages) + 1,
                "title"      : title,
                "url"        : url,
                "description": description,
                "keywords"   : [k.strip() for k in keywords.split(",") if k.strip()],
                "author"     : author,
                "created_at" : str(date.today()),
                "category"   : category,
            }
            pages.append(new_page)
            save_pages(pages)                       # Step 3 で学んだ json.dump
            st.cache_data.clear()                   # 古いキャッシュを捨てる
            st.session_state["registered"] = True   # 「登録した」印を残す
            st.rerun()                              # 画面を作り直す（印はここを越えて残る）

# ── ⑦ 一覧タブ ──
with tab3:
    st.subheader(f"📚 登録済みページ一覧（{len(pages)}件）")
    for page in pages:
        with st.expander(f"📄 {page['title']}"):
            st.markdown(page["description"])
            tags = " , ".join([f"`{kw}`" for kw in page["keywords"]])
            st.markdown(f"🏷 {tags}")
            st.caption(f"👤 {page['author']}　📅 {page['created_at']}　📁 {page.get('category', '')}")
            st.caption(f"🔗 {page['url']}")
