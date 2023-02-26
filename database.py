from sqlite3 import connect

db = connect("day_r.db", check_same_thread=False, timeout=20)
cur = db.cursor()

cur.execute('PRAGMA journal_mode=WAL')

commit = lambda: db.commit()
