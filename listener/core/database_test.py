import sqlite3

try:
    conn = sqlite3.connect("/Users/t3ntman/Desktop/rat.db")

    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hostname FROM tasks")
        print(cursor.fetchone())

except Exception:
    raise

finally:
    conn.close()
