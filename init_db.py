import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Check if table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if c.fetchone():
        # Print current columns
        c.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in c.fetchall()]
        print("📋 Existing users table columns:", columns)

        # Add missing 'email' column
        if 'email' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN email TEXT")
            print("✅ Added missing 'email' column to users table.")
    else:
        # Create new table with all columns
        c.execute('''
            CREATE TABLE users (
                username TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        print("✅ Created new users table with email column.")

    conn.commit()
    conn.close()
    print("✅ Database schema checked and updated.")

if __name__ == "__main__":
    init_db()
