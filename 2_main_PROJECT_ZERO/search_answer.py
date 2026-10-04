# search_answer.py — W1 検索ロジック（答え・完成版）
# ------------------------------------------------------------------
# search.py（虫食い）の答え。まず自分で埋めてから、詰まったらここを見ること。
# ------------------------------------------------------------------
import re


def search_pages(query: str, pages: list) -> list:
    """キーワードでページを絞り込む（部分一致）"""

    # ① キーワードが空欄ならすぐ終了（空リストを返す）
    if not query.strip():
        return []                # ← 空のリストを返す

    results = []
    query_lower = query.lower()  # ← 小文字に統一（大文字小文字を無視するため）

    for page in pages:           # ページを1件ずつ取り出してループ

        # title + description + keywords を1つの文字列に結合して検索対象にする
        search_text = " ".join([
            page["title"],
            page["description"],
            " ".join(page["keywords"]),
        ])

        # キーワードが search_text に含まれていたら results に追加
        if query_lower in search_text.lower():
            results.append(page)  # ← append でリストに追加

    return results


def highlight_match(text: str, query: str) -> str:
    """説明文の中のキーワードを **太字** にする"""

    if not query:                # キーワードが空なら何もしない
        return text

    pattern = re.compile(
        re.escape(query),        # 特殊文字が含まれても壊れない安全策
        re.IGNORECASE            # ← 大文字・小文字を区別しない
    )

    # マッチした部分を **キーワード** に置換する（Markdownの太字）
    return pattern.sub(f"**{query}**", text)
