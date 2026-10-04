# PROJECT ZERO — Tech0 Search 統合講義（W1〜W4 配布版）

社内ナレッジ検索エンジン **Tech0 Search** を、週ごとに1つのアプリとして育てる実践プロジェクトの配布パッケージです。
この配布版には **W1〜W4（宿題範囲）** が入っています。

## 📦 フォルダ構成

進めるのは `2_main_PROJECT_ZERO/` の中だけです。開いたフォルダの中を見れば完結します。

```
PROJECT_ZERO_w1-4/
├── README.md                       # このファイル（最初に読む）
│
└── 2_main_PROJECT_ZERO/
    ├── PROJECT_ZERO_統合講義_W1.ipynb     # 本編ノートブック（週ごとに1ファイル）★ふだんはこちら
    ├── PROJECT_ZERO_統合講義_W2.ipynb
    ├── PROJECT_ZERO_統合講義_W3.ipynb
    ├── PROJECT_ZERO_統合講義_W4.ipynb
    ├── pages_w1.json               # W1で使うページデータ（5件・8キー・手動登録のみ）
    ├── pages_w2.json               # W2で使うページデータ（W1の5件＋クロール済み4件・13キー）
    ├── search.py                   # W1 Step 4 の虫食い課題
    ├── search_answer.py            # その答え
    ├── schema.sql                  # W3 Step 1 で使うDB設計（pages / keywords）
    ├── test_output.json            # W1 写経（4）JSON書き込みの出力サンプル
    ├── pic/                        # ノートで使う画像
    └── answers/                    # 各週の完成コード（詰まったら見る）
        ├── w1/  app.py, search.py, pages_w1.json, requirements.txt
        ├── w2/  app.py, crawler.py, search.py, pages_w2.json, requirements.txt
        ├── w3/  app.py, database.py, schema.sql, search_fulltext.py, crawler.py, pages_w2.json, requirements.txt
        └── w4/  app.py, ranking.py, database.py, schema.sql, crawler.py, pages_w2.json, requirements.txt
```

## 📦 必要なライブラリ

各 `answers/w1〜w4/` の `requirements.txt` でまとめて入れられます。

```bash
cd （動かしたいフォルダ）
pip install -r requirements.txt
streamlit run app.py
```

| 週 | 追加で必要になるもの |
|---|---|
| W1 | `streamlit` |
| W2・W3 | ＋ `requests`・`beautifulsoup4`（クローラー） |
| W4 | ＋ `scikit-learn`（TF-IDF） |

> W3 で使う SQLite は Python 標準ライブラリ（`sqlite3`）なので、追加インストールは不要です。

> `pip` が見つからない場合は `python3 -m pip` を使ってください。Homebrew の Python では仮想環境の作成（`python3 -m venv .venv` → `source .venv/bin/activate`）が必要なことがあります。

## ✍️ 写経・答え合わせの使い方

| 教材 | 書く場所 | 答え |
|------|----------|------|
| ノートの「■ 写経（1）〜（7）」 | **W1ノートのコードセル**をそのまま実行（▶）。余裕があれば自分で打ち直す | セルの下の実行結果 |
| `search.py`（W1 Step 4） | **`2_main_PROJECT_ZERO/search.py`（虫食い）** の `____` を埋める | 同じフォルダの `search_answer.py` |
| 各週の `app.py` | **アプリ用フォルダを自分で作って新規作成**（W1 = `tech0-search/`。W2 以降は版を上げる：`tech0-search-v0.2/` → W3 で DB 化 → W4 = `tech0-search-v1.0/`） | **`2_main_PROJECT_ZERO/answers/w1〜w4/`**（動く完成コード一式） |

> **まず自分で書く → 動かない → 答えと見比べる** の順で使ってください。
> `answers/` の各フォルダは自己完結しており、そのまま `streamlit run app.py` で起動できます。

## 📚 学習の順序

**`2_main_PROJECT_ZERO/`** を開き、`PROJECT_ZERO_統合講義_W1.ipynb` → `W2` → `W3` → `W4` の順に進めて、検索エンジン Tech0 Search を育てます。

## 📓 週ごとのノートブックについて

本編ノートは **1週＝1ファイル**（`_W1.ipynb`〜`_W4.ipynb`）に分かれています。**その週のファイルだけを開けば OK** です。

| ノート | 中身 | 成果物 |
|--------|------|--------|
| `_W1.ipynb` | 3. / 3.3（導入）＋ **3.3.1 W1** | Tech0 Search v0.1（JSON＋部分一致検索） |
| `_W2.ipynb` | 3. / 3.3（導入）＋ **3.3.2 W2** | v0.2 自動化（クローラー） |
| `_W3.ipynb` | 3. / 3.3（導入）＋ **3.3.3 W3** | データを JSON から DB（SQLite）へ移す ＋ 全文検索 |
| `_W4.ipynb` | 3. / 3.3（導入）＋ **3.3.4 W4** | v1.0 ランキング（TF-IDF・コサイン類似度）＋ デプロイ |

- **冒頭の「3. 講義の目的」「3.3 PROJECT ZERO の全体像」は4ファイルすべてに入っています**。毎週その週のファイルを開くだけで、全体のどこにいるかを確認できます。
- W5（発表準備）／W6（最終発表）と、締めの 3.4／3.5 はこの配布版には含まれていません（別途配布）。

## 🖼 画像について

ノートブック内の画像は **すべて同じフォルダの `pic/` への相対リンク（markdown記法）** です（base64埋め込み・HTML `<img>`・notebook attachment は排除済み）。
**`.ipynb` は、隣にある `pic/` ごとフォルダ単位で移動**してください（ファイル単体で抜き出すと画像が表示されません）。
週ごとの4ファイルは **同じ `2_main_PROJECT_ZERO/pic/` を共有**しています。

| 画像 | 使うノート | 用途 |
|------|-----------|------|
| `pic/w1_hero.jpg` | `_W1.ipynb` | W1 完成画面（ゴール提示） |
| `pic/w1_codemap.png` | `_W1.ipynb` | 画面×コード対応マップ |
| `pic/w4_cosine.png` | `_W4.ipynb` | W4 コサイン類似度の図解 |
| `pic/img_Cloud.jpg` | （現在は未参照） | デプロイ先（クラウド）の図。W6 で使用 |

## 🗺 W1 の進め方（構成）— `PROJECT_ZERO_統合講義_W1.ipynb`

```
Step 0  完成画面を掴む（正解＝ゴールを最初に見る）
Step 1  作るものの「全体像」を“抽象”でつかむ
        1-1 データの流れ（固有名詞なし）
        1-2 3つの役割（見た目／データ／処理）
        1-3 役割を実ファイルに紐づける（関心の分離・設計図）
Step 2  【ファイル別①】app.py    … 見た目 → 「動かない」を体感
Step 3  【ファイル別②】pages_w1.json … データの器
Step 4  【ファイル別③】search.py  … 検索ロジック
Step 5  3ファイルを統合して app.py を完成
Step 6  練習問題
Step 7  アプリを起動して CDO レビューへ
```

> **設計思想**：まず「全体像（抽象）」を上から眺め、そのあと **ファイルごと** に
> 「そのファイルが全体像のどこを担うのか」を確かめながら実装します。
> 固有名詞（ファイル名・関数名）は「作る直前」まで出しません。

## 🗺 W2〜W4 の進め方（構成）

| 週 | Step の流れ | 新しく増えるファイル |
|---|---|---|
| W2 | Step 0 UI差分設計 → 1 設計図 → 2 `pages_w2.json` を読む → 3 クローラーを作る → 4 `app.py` に統合 → 5 ミニアレンジ課題 | `crawler.py` |
| W3 | Step 0 全体像（替えるのは「貯め方」だけ）→ 1 `schema.sql` → 2 `database.py` → 3 全文検索 → 4 `app.py` に組み込む | `schema.sql`・`database.py`・`search_fulltext.py` |
| W4 | Step 0 UI設計 → 1 設計図＆役割分担 → 2 TF-IDF → 3 コサイン類似度 → 4 `SearchEngine` クラス → 5 `app.py` v1.0 に統合＋デプロイ | `ranking.py` |

## 🚀 アプリの起動

```bash
# app.py があるフォルダに移動してから
cd （app.py があるフォルダのパス）
streamlit run app.py
# → ブラウザで http://localhost:8501 が開けば成功
```
