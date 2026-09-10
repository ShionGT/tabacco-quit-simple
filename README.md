# 喫煙カウンター（Tobacco Quit Simple）

自分の喫煙本数を記録し、統計を可視化するシンプルなローカル Web アプリです。
Flask + SQLite で作られており、1人用・ローカル運用を想定しています。

---

## 機能

- **「喫煙した」ボタン**を押すだけで 1 本カウント
- **取り消しボタン**で誤登録を 1 件削除
- 下にスクロールすると以下の統計が表示されます：
  - 総喫煙本数
  - 推定消費箱数（Golden Marlboro 20本入り）
  - 1日あたりの平均喫煙本数
  - 平均喫煙間隔（次に吸うまでの平均時間）
  - 日別の喫煙記録（バー付き）

---

## たばこの設定

| 項品 | 値 |
|------|-----|
| 銘柄 | Golden Marlboro |
 | 1箱の価格 | 620 円 |
| 1箱の本数 | 20 本 |

> `app.py` の先頭にある `PACK_PRICE` と `CIGS_PER_PACK` を変更すれば別の銘柄にも対応できます。

---

## セットアップ手順

### 1. 必要なもの
- Python 3.9 以上
- pip

### 2. インストール

```bash
# リポジトリをクローン
git clone https://github.com/あなたのユーザー名/tabacco-quit-simple.git
cd tabacco-quit-simple

# 仮想環境を作成（推奨）
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# ライブラリをインストール
pip install -r requirements.txt
```

### 3. 起動

```bash
python app.py
```

ブラウザで以下を開いてください：

```
http://127.0.0.1:5000
```

これだけで使えます。データは `golden_marlboro.db`（SQLite）に自動保存されます。

---

## 📁 ファイル構成

```
tabacco-quit-simple/
├── app.py              # Flask メインアプリ
├── requirements.txt    # 依存ライブラリ
├── .gitignore          # Git 除外ファイル
├── templates/
│   └── index.html      # Web UI（日本語）
└── README.md           # このファイル
```

---

## 💾 データについて

- 記録は SQLite データベース `golden_marlboro.db` に保存されます
- データベースファイルは `.gitignore` に含まれているため、Git にはアップロードされません
- データをリセットしたい場合は `golden_marlboro.db` を削除してアプリを再起動してください

---

## 📊 統計の計算方法

| 統計 | 計算方法 |
|------|----------|
| 推定消費箱数 | 総本数 ÷ 20本 = 箱数（端数は切り上げて金額計算） |
| 1日あたり平均 | 総本数 ÷ 記録日数 |
| 平均喫煙間隔 | 隣接する喫煙記録の時間差の平均（分） |

---

## カスタマイズ

別のたばこに変更する場合：

```python
# app.py の上部を編集
PACK_PRICE = 620      # ← 1箱の価格（円）
CIGS_PER_PACK = 20    # ← 1箱の本数
```

> **※注意**: このアプリは喫煙記録の補助ツールです。禁煙を希望される方は医師にご相談ください。
