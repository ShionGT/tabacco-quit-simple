import sqlite3
from datetime import datetime, timedelta, date
import random

random.seed(42)

conn = sqlite3.connect("tabacco.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS smokes (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        smoked_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
    )
""")
conn.execute("DELETE FROM smokes")

start = date(2026, 8, 28)
daily_counts = [7, 8, 8, 7, 6, 8, 9, 7, 8, 8, 7, 8, 9]  # 合計100本分

windows = [
    (7, 0, 8, 30),
    (9, 0, 10, 30),
    (11, 30, 13, 0),
    (14, 0, 16, 0),
    (17, 0, 18, 30),
    (19, 0, 21, 0),
    (21, 30, 23, 15),
]


def rand_time_in(h1, m1, h2, m2):
    start_m = h1 * 60 + m1
    end_m = h2 * 60 + m2
    t = random.randint(start_m, end_m)
    return t // 60, t % 60, random.randint(0, 59)


rows = []
for i, n in enumerate(daily_counts):
    d = start + timedelta(days=i)
    pool = windows[:]
    random.shuffle(pool)
    times = []
    seen = set()
    for j in range(n):
        h, m, s = rand_time_in(*pool[j % len(pool)])
        t = datetime(d.year, d.month, d.day, h, m, s)
        while t.strftime("%Y-%m-%d %H:%M:%S") in seen:
            t += timedelta(seconds=1)
        seen.add(t.strftime("%Y-%m-%d %H:%M:%S"))
        times.append(t)
    rows.extend(sorted(times))

conn.executemany(
    "INSERT INTO smokes (smoked_at) VALUES (?)",
    [(t.strftime("%Y-%m-%d %H:%M:%S"),) for t in rows],
)
conn.commit()
print(conn.execute("SELECT COUNT(*) FROM smokes").fetchone()[0], "rows written")
conn.close()
