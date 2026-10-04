import streamlit as st
from database import init_db, insert_page, get_all_pages, log_search
from crawler import fetch_page, parse_html, crawl_url
from datetime import date
from search_fulltext import search_fulltext
from ranking import get_engine, rebuild_index

init_db()  # DB を初期化（テーブルがなければ作る）

@st.cache_resource
def load_and_index():
    """全ページを DB から読み込み TF-IDF インデックスを構築する。
    @st.cache_resource により、アプリ起動中は一度だけ実行される。"""
    pages = get_all_pages()
    if pages:
        rebuild_index(pages)
    return pages

pages = load_and_index()
engine = get_engine()

st.set_page_config(page_title="Tech0 Search v1.0", page_icon="🐈")
st.title("🔍 Tech0 Search v1.0")
st.title("PROJECT ZERO - 社内ナレッジ検索エンジン")

tab1, tab2, tab3, tab4 = st.tabs(["検索", "クロール", "手動登録", "一覧"])

with tab1:
    st.subheader("キーワード検索")

    col_serach, col_options = st.columns([3, 1])
    with col_serach:
        query = st.text_input("キーワードを入力", label_visibility="collapsed")

    with col_options:
        top_n = st.selectbox("表示件数", [10, 20, 50], index=0)

    if query:
        results = engine.search(query, top_n=top_n) 
        log_search(query, len(results))  # 検索するたびに自動記録（W6発展で実装）
  
        st.markdown(f"**検索結果: {len(results)}件")
        st.divider()

        if results:
            for i, page in enumerate(results, start=1):
                with st.container():
                    col_rank, col_title, col_score = st.columns([1, 6, 2])
                    with col_rank:
                        st.markdown(f"### {i}.")
                    with col_title:
                        st.markdown(f"### [{page['title']}]")
                    with col_score:
                        st.metric("スコア", f"{page['relevance_score']}",
                                  delta=f"基準: {page['base_score']}")
                    desc = page.get("description", "")
                    if desc:
                        st.markdown(f"*{desc[:200]}{'...' if len(desc) > 200 else ''}")

                    kw = page.get("keywords", "") or ""
                    if kw:
                        # keywords は DB から読むと list、手動で入れると "A,B,C" の文字列になる。
                        # ranking.py と同じく、どちらでも動くようにしておく。
                        kw_list = [k.strip() for k in kw.split(",")] if isinstance(kw, str) else list(kw)
                        tags = " ".join([f"`{k}`" for k in kw_list[:5] if k])
                        st.markdown(f"🏷️ {tags}")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1: st.caption(f"👤 {page.get('author', '不明') or '不明'}")
                    with col2: st.caption(f"📊 {page.get('word_count', 0)} 語")
                    with col3: st.caption(f"📁 {page.get('category', '未分類') or '未分類'}")
                    with col4: st.caption(f"📅 {(page.get('crawled_at', '') or '')[:10]}")

                    st.markdown(f"🔗 [{page['url']}]({page['url']})")
                    st.divider()
        else:
            st.info("該当するページが見つかりませんでした")

with tab2:
    st.write("単体クロール")
    url_input = st.text_input("クロールするURLを入力してください")
    if st.button("クロール実行"):
        if url_input:
            result = crawl_url(url_input)
            if result["crawl_status"] == "success":
                st.success(f"✅クロール成功: {url_input}")
                st.write("タイトル:", result["title"])
                st.write("説明:", result["description"])
                st.write("キーワード:", ", ".join(result["keywords"]))
                st.write("本文の文字数:", result["word_count"])
                insert_page(result)
                st.cache_data.clear()  # キャッシュをクリアして次回の検索で新しいデータを反映させる
                st.success("クロール結果を保存しました。")
            else:
                st.error(f"クロール失敗: {result.get('error')}")

    st.write("一括クロール")
    #URLリスト入力してforループでクロールし、保存する
    urls_text = st.text_area("URLリスト（1行に1つのURL）")
    if st.button("全ページをクロール"):
        urls = [url.strip() for url in urls_text.splitlines() if url.strip().startswith("http")]
        if not urls:
            st.error("有効なURLが入力されていません。")
        else:
            ok = 0
            for url in urls:
                result = crawl_url(url)
                if result["crawl_status"] == "success":

                    insert_page(result)
                    ok += 1
                    st.success(f"✅クロール成功: {url}")
                else:
                    st.error(f"クロール失敗: {url} - {result.get('error')}")
            st.info(f"✅クロール完了: {ok}件成功 / {len(urls)}件中")

with tab3:
    if st.session_state.get("registered"):
        st.success("登録完了！")
        st.session_state["registered"] = False  

    with st.form('register_form'):
        url         = st.text_input("URL")
        title       = st.text_input("タイトル")
        description = st.text_area("説明")
        keywords    = st.text_input("キーワード（カンマ区切り）")
        author      = st.text_input("作成者")
        category    = st.selectbox("カテゴリ", ["お祭り", "チーム","事例", "企画", "業務マニュアル", "研修", "共有"])
        submitted   = st.form_submit_button("登録する")        

    if submitted:
        if not url or not title:
            st.error("URLとタイトルは必須です。")
        else:
            new_page = {
                "id"         : len(pages) + 1,
                "title"      : title,
                "url"        : url,
                "description": description,
                "keywords"   : [kw.strip() for kw in keywords.split(",") if kw.strip()],
                "author"     : author,
                "category"   : category,
                "created_at" : date.today().isoformat(),
            }
        insert_page(new_page)
        st.cache_data.clear()  # キャッシュをクリアして次回の検索で新しいデータを反映させる
        st.session_state['registered'] = True
        st.rerun()

with tab4:
    pages = get_all_pages()
    st.subheader(f"📚 DB 登録済みページ一覧（{len(pages)}件")
    for page in pages:
        with st.expander(page["title"]):
            st.write(page["description"])
            st.write("キーワード:", ", ".join(page["keywords"]))
            st.write("著者:", page["author"])