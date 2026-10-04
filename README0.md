# PROJECT ZERO — Tech0 Search 統合講義（配布版）

社内ナレッジ検索エンジン **Tech0 Search** を、6週間かけて1つのアプリとして育てる実践プロジェクトの配布パッケージです。

## 📦 フォルダ構成

**① 事前学習 → ② 本編** の順に、フォルダ単位で進みます。各フォルダは**それだけで完結**しているので、開いたフォルダの中だけを見れば OK です。

```
配布版_PROJECT_ZERO/
├── README.md                       # このファイル（最初に読む）
│
├── 1_事前学習/                      ← ① まずここ
│   ├── 事前学習_Webアプリとフレームワーク・Streamlit基礎.md   # 本文（Web/フレームワーク/Streamlit基礎）
│   ├── app.py                      # 虫食い課題（`____` を埋める）
│   ├── app_answer.py               # その答え
│   ├── requirements.txt            # 必要なライブラリ
│   └── pic/                        # 本文で使う画像
│
└── 2_本編_PROJECT_ZERO/             ← ② 次にここ（W1〜W6）
    ├── PROJECT_ZERO_統合講義_W1.ipynb     # 本編ノートブック（週ごとに分割）★ふだんはこちら
    ├── PROJECT_ZERO_統合講義_W2.ipynb
    ├── PROJECT_ZERO_統合講義_W3.ipynb
    ├── PROJECT_ZERO_統合講義_W4.ipynb
    ├── PROJECT_ZERO_統合講義_W5.ipynb
    ├── PROJECT_ZERO_統合講義_W6.ipynb
    ├── PROJECT_ZERO_統合講義_W1-W6.ipynb   # 通し版（全6週が1ファイル。検索・通読用）
    ├── pages_w1.json               # W1で使うページデータ（8キー・手動登録のみ）
    ├── pages_w2.json               # W2で使うページデータ（W1の5件＋クロール済み4件・13キー）
    ├── search.py                   # W1 Step 4 の虫食い課題
    ├── search_answer.py            # その答え
    ├── pic/                        # ノートで使う画像
    └── answers/                    # 各週の完成コード（詰まったら見る）
        ├── w1/  app.py, search.py, pages_w1.json, requirements.txt
        ├── w2/  app.py, crawler.py, search.py, pages_w2.json, requirements.txt
        ├── w3/  app.py, database.py, schema.sql, search_fulltext.py, crawler.py, pages_w2.json, requirements.txt
        └── w4/  app.py, ranking.py, database.py, schema.sql, crawler.py, pages_w2.json, requirements.txt
```

## 📦 必要なライブラリ

各フォルダの `requirements.txt` でまとめて入れられます。

```bash
cd （動かしたいフォルダ）
pip install -r requirements.txt
streamlit run app.py
```

| 週 | 追加で必要になるもの |
|---|---|
| 事前学習・W1 | `streamlit` |
| W2・W3 | ＋ `requests`・`beautifulsoup4`（クローラー） |
| W4 | ＋ `scikit-learn`（TF-IDF） |

> `pip` が見つからない場合は `python3 -m pip` を使ってください。Homebrew の Python では仮想環境の作成（`python3 -m venv .venv` → `source .venv/bin/activate`）が必要なことがあります。

> ⚠️ **`app.py` が2種類あります**（迷ったらここを確認）
> - `1_事前学習/app.py` … **Streamlit の練習用**。虫食いを埋めるだけのファイル。
> - `answers/w1〜w4/app.py` … **本編の成果物の答え**。W1 以降で自分が書く `app.py` はこちら側です。

## ✍️ 写経・答え合わせの使い方

| 教材 | 書く場所 | 答え |
|------|----------|------|
| 事前学習の虫食い課題 | **`1_事前学習/app.py`** の `____` を埋める | 同じフォルダの `app_answer.py` |
| ノートの「■ 写経（1）〜（7）」 | **W1ノートのコードセル**をそのまま実行（▶）。余裕があれば自分で打ち直す | セルの下の実行結果 |
| `search.py`（W1 Step 4） | **`2_本編_PROJECT_ZERO/search.py`（虫食い）** の `____` を埋める | 同じフォルダの `search_answer.py` |
| 各週の `app.py` | **アプリ用フォルダを自分で作って新規作成**（W1 = `tech0-search/`。W2 以降は版を上げる：`tech0-search-v0.2/` → W3 で DB 化 → W4 = `tech0-search-v1.0/`） | **`2_本編_PROJECT_ZERO/answers/w1〜w4/`**（動く完成コード一式） |

> **まず自分で書く → 動かない → 答えと見比べる** の順で使ってください。
> `answers/` の各フォルダは自己完結しており、そのまま `streamlit run app.py` で起動できます。

## 📚 学習の順序

1. **`1_事前学習/`** を開き、`事前学習_Webアプリとフレームワーク・Streamlit基礎.md` を読む（Webアプリの前提／フレームワーク選定／Streamlit基礎／使うコンポーネント＋虫食い課題）。
2. **`2_本編_PROJECT_ZERO/`** に進み、`PROJECT_ZERO_統合講義_W1.ipynb` → `W2` → … → `W6` の順に開いて、検索エンジン Tech0 Search を W1〜W6 で育てる。

## 📓 週ごとのノートブックについて

本編ノートは **1週＝1ファイル**（`_W1.ipynb`〜`_W6.ipynb`）に分かれています。**その週のファイルだけを開けば OK** です。

| ノート | 中身 |
|--------|------|
| `_W1.ipynb` | 3. / 3.3（導入）＋ **3.3.1 W1** ｜ Tech0 Search v0.1 |
| `_W2.ipynb` | 3. / 3.3（導入）＋ **3.3.2 W2** ｜ v0.2 自動化（クローラー） |
| `_W3.ipynb` | 3. / 3.3（導入）＋ **3.3.3 W3** ｜ データをDBへ移す |
| `_W4.ipynb` | 3. / 3.3（導入）＋ **3.3.4 W4** ｜ v1.0 ランキング（TF-IDF） |
| `_W5.ipynb` | 3. / 3.3（導入）＋ **3.3.5 W5** ｜ 役員会に向けた発表準備 |
| `_W6.ipynb` | 3. / 3.3（導入）＋ **3.3.6 W6** ｜ 最終発表 ＋ **3.4／3.5**（Next Action・まとめ） |

- **冒頭の「3. 講義の目的」「3.3 PROJECT ZERO の全体像」は6ファイルすべてに入っています**。毎週その週のファイルを開くだけで、全体のどこにいるかを確認できます。
- 講義の締めにあたる **3.4（自分でWebアプリを作る思考プロセス）／3.5 まとめ** は、最終週の `_W6.ipynb` の末尾に入っています。
- `PROJECT_ZERO_統合講義_W1-W6.ipynb`（**通し版**）も残してあります。中身は6ファイルと同一で、全体を通して読みたいときや横断検索したいときに使ってください。

## 🖼 画像について

ノートブック・md 内の画像は **すべて同じフォルダの `pic/` への相対リンク（markdown記法）** です（base64埋め込み・HTML `<img>`・notebook attachment は排除済み）。
**`.ipynb`・`.md` は、隣にある `pic/` ごとフォルダ単位で移動**してください（ファイル単体で抜き出すと画像が表示されません）。
週ごとの6ファイルも **同じ `2_本編_PROJECT_ZERO/pic/` を共有**しています。W1〜W6 のノートだけを別の場所へ動かす場合も、`pic/` を一緒に持っていってください。

| 画像 | 使うノート | 用途 |
|------|-----------|------|
| `2_本編_PROJECT_ZERO/pic/w1_hero.jpg` | `_W1.ipynb` | W1 完成画面（ゴール提示） |
| `2_本編_PROJECT_ZERO/pic/w1_codemap.png` | `_W1.ipynb` | 画面×コード対応マップ |
| `2_本編_PROJECT_ZERO/pic/w4_cosine.png` | `_W4.ipynb` | W4 コサイン類似度の図解 |
| `2_本編_PROJECT_ZERO/pic/img_Cloud.jpg` | `_W6.ipynb` | 3.4.2 デプロイ先（クラウド）の図 |
| `1_事前学習/pic/img032〜036 ほか` | 事前学習の `.md` | 導入・フレームワーク選定・環境構築の図 |

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

## 🚀 アプリの起動

```bash
# app.py があるフォルダに移動してから
cd （app.py があるフォルダのパス）
streamlit run app.py
# → ブラウザで http://localhost:8501 が開けば成功
```
