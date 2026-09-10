from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, date
from collections import Counter

app = Flask(__name__)

@app.template_filter("number_format")
def number_format(n):
    return f"{n:,}"

DB_NAME = "golden_marlboro.db"

PACK_PRICE = 620   # ¥
CIGS_PER_PACK = 20


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS smokes (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            smoked_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        conn = get_db()
        conn.execute("INSERT INTO smokes (smoked_at) VALUES (datetime('now','localtime'))")
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn = get_db()

    total = conn.execute("SELECT COUNT(*) AS c FROM smokes").fetchone()["c"]

    # 今日の本数
    today = date.today().isoformat()
    today_count = conn.execute(
        "SELECT COUNT(*) AS c FROM smokes WHERE date(smoked_at) = ?", (today,)
    ).fetchone()["c"]

    # 日別カウント
    rows = conn.execute("""
        SELECT date(smoked_at) AS d, COUNT(*) AS c
        FROM smokes
        GROUP BY d
        ORDER BY d DESC
    """).fetchall()
    daily = [dict(r) for r in rows]

    avg_per_day = round(total / len(daily), 1) if daily else 0

    # 1日の平均喫煙間隔（時間）
    times = [r[0] for r in conn.execute("SELECT smoked_at FROM smokes ORDER BY smoked_at ASC").fetchall()]
    avg_interval = 0
    if len(times) > 1:
        gaps = []
        for i in range(1, len(times)):
            a = datetime.strptime(times[i-1], "%Y-%m-%d %H:%M:%S")
            b = datetime.strptime(times[i],   "%Y-%m-%d %H:%M:%S")
            gaps.append((b - a).total_seconds())
        avg_gap = sum(gaps) / len(gaps)
        avg_interval = round(avg_gap / 60, 1)  # 分

    # 推定消費箱数
    packs_exact = total / CIGS_PER_PACK
    packs_full  = total // CIGS_PER_PACK
    packs_remain = total % CIGS_PER_PACK
    cost = (packs_full + (1 if packs_remain else 0)) * PACK_PRICE  # 開けた箱の金額

    conn.close()

    return render_template(
        "index.html",
        total=total,
        today_count=today_count,
        avg_per_day=avg_per_day,
        avg_interval=avg_interval,
        packs_exact=round(packs_exact, 1),
        packs_full=packs_full,
        packs_remain=packs_remain,
        cost=cost,
        daily=daily,
        pack_price=PACK_PRICE,
        cig_per_pack=CIGS_PER_PACK,
    )


@app.route("/delete_last", methods=["POST"])
def delete_last():
    """誤登録を取り消す（最新1件削除）"""
    conn = get_db()
    conn.execute("DELETE FROM smokes WHERE id = (SELECT MAX(id) FROM smokes)")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
