import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL
)
""")

# عينات بيانات للتجربة
cur.execute("INSERT INTO records (title, description) VALUES (?, ?)",
            ("تحليل مالي", "خدمة التحليل المالي الاحترافي."))

cur.execute("INSERT INTO records (title, description) VALUES (?, ?)",
            ("دراسة جدوى", "دراسة جدوى تفصيلية للمشروعات."))

conn.commit()
conn.close()

print("Database created!")
