# =============================================================
# answers/w2/app.py — Tech0 Search v0.2（W2 完成版）
# 検索は W1 の部分一致（search.py）を流用。新機能はクローラー。
# 起動： streamlit run app.py （search.py / crawler.py / pages_w2.json が同じフォルダに必要）
# =============================================================
import streamlit as st
import json
from datetime import date
from search import search_pages, highlight_match   # W1 流用（部分一致）
from crawler import crawl_url                      # W2 の新機能

# ── データの読み書き ──
@st.cache_data
def load_pages():
    with open("pages_w2.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_pages(pages):
    with open("pages_w2.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

def add_page(pages, page):
    """クロール結果を pages_w2.json 用の形式に整えて追加する"""
    page["id"] = len(pages) + 1
    page.setdefault("author", "クローラー")
    page.setdefault("category", "クロール")
    page.setdefault("created_at", str(date.today()))
    pages.append(page)
    save_pages(pages)

# ── ページ設定・タイトル ──
st.set_page_config(page_title="Tech0 Search v0.2", page_icon="🔍")
st.title("🔍 Tech0 Search v0.2")
st.caption("PROJECT ZERO — 社内ナレッジ検索エンジン【自動クロール搭載】")

tab1, tab2, tab3, tab4 = st.tabs(["検索", "クロール", "手動登録", "一覧"])
pages = load_pages()

# ── 検索タブ（W1 流用・部分一致） ──
with tab1:
    st.subheader("🔍 キーワード検索")
    query = st.text_input("🔑 キーワードを入力")
    if query:
        results = search_pages(query, pages)
        st.markdown(f"**検索結果: {len(results)}件**")
        st.divider()
        for page in results:
            st.markdown(f"### [{page['title']}]({page['url']})")
            st.markdown(highlight_match(page["description"], query))
            col1, col2 = st.columns(2)
            col1.caption(f"👤 {page.get('author', '不明')}")
            col2.caption(f"📊 {page.get('word_count', '-')} 語")
            st.divider()

# ── クロールタブ（単体＋一括） ──
with tab2:
    st.subheader("🤖 自動クローラー")

    # 単体クロール
    st.markdown("**単体クロール**")
    url_input = st.text_input("クロールしたいURL")
    if st.button("🤖 クロール実行"):
        if url_input:
            with st.spinner(f"クロール中: {url_input}"):
                result = crawl_url(url_input)
            if result.get("crawl_status") == "success":
                st.success(f"✅ 取得成功: {result['title']}")
                st.caption(f"📊 {result['word_count']} 語 ／ 🔗 リンク {len(result['links'])} 件")
                add_page(pages, result)
                st.cache_data.clear()
                st.info("pages_w2.json に登録しました")
            else:
                st.error(f"❌ 取得失敗: {result.get('error')}")

    st.divider()

    # 一括クロール
    st.markdown("**一括クロール**（URLを改行区切りで入力）")
    urls_text = st.text_area("URLリスト", height=120)
    if st.button("📋 一括クロール実行"):
        urls = [u.strip() for u in urls_text.splitlines() if u.strip().startswith("http")]
        if not urls:
            st.error("有効なURLが見つかりませんでした")
        else:
            ok = 0
            for u in urls:
                with st.spinner(f"クロール中: {u}"):
                    result = crawl_url(u)
                if result.get("crawl_status") == "success":
                    add_page(pages, result)
                    ok += 1
                    st.success(f"✅ {result['title']}")
                else:
                    st.error(f"❌ 失敗: {u}")
            st.cache_data.clear()
            st.info(f"{ok} / {len(urls)} 件を登録しました")

# ── 手動登録タブ（W1 と同じ） ──
with tab3:
    st.subheader("📝 手動でページを登録")

    # st.rerun() で画面を作り直すと直前の表示は消えるので、
    # 「登録した」印を st.session_state に残して、走り直した後に読む（W1 と同じ）
    if st.session_state.get("registered"):
        st.success("登録完了！")
        st.session_state["registered"] = False

    with st.form("register_form"):
        url         = st.text_input("URL")
        title       = st.text_input("タイトル")
        description = st.text_area("説明")
        keywords    = st.text_input("キーワード（カンマ区切り）")
        author      = st.text_input("作成者")
        submitted   = st.form_submit_button("登録する")
    if submitted:
        if not url or not title:
            st.error("URL とタイトルは必須です")
        else:
            pages.append({
                "id": len(pages) + 1, "title": title, "url": url,
                "description": description,
                "keywords": [k.strip() for k in keywords.split(",") if k.strip()],
                "author": author, "created_at": str(date.today()), "category": "共有",
            })
            save_pages(pages)
            st.cache_data.clear()
            st.session_state["registered"] = True   # 「登録した」印を残す
            st.rerun()

# ── 一覧タブ ──
with tab4:
    st.subheader(f"📚 登録済みページ一覧（{len(pages)}件）")
    for page in pages:
        status = page.get("crawl_status", "manual")
        icon = "🤖" if status == "success" else "📄"
        with st.expander(f"{icon} {page['title']}"):
            st.markdown(page.get("description", "") or "（説明なし）")
            st.caption(f"👤 {page.get('author', '不明')}　📊 {page.get('word_count', '-')} 語　🏷 {status}")
            st.caption(f"🔗 {page['url']}")
