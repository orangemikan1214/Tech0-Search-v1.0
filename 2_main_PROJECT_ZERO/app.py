import streamlit as st
from database import init_db, insert_page, get_all_pages, log_search
from crawler import fetch_page, parse_html, crawl_url
from datetime import date
from search_fulltext import search_fulltext
from ranking import get_engine, rebuild_index

init_db()  # DB を初期化（テーブルがなければ作る）
st.set_page_config(page_title="Tech0 Search v0.3", page_icon="🐈")
st.title("🔍 Tech0 Search v0.3")
st.title("PROJECT ZERO - 社内ナレッジ検索エンジン")

tab1, tab2, tab3, tab4 = st.tabs(["検索", "クロール", "手動登録", "一覧"])

with tab1:
    query = st.text_input("キーワードを入力")
    if query:
        pages   = get_all_pages()    
        results = search_fulltext(query, pages)   
        st.markdown(f"**検索結果: {len(results)}件**（match_count順）")
        st.divider()
        for r in results:
            st.markdown(f"### [{r['title']}]({r['url']})")
            st.markdown(f"🔢 マッチ数: **{r['match_count']}** 回")
            if r.get("preview"):
                st.caption(r["preview"])
            st.divider()

 

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