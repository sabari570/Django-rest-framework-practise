import sqlite3

# Path to your SQLite database file
db_path = 'db.sqlite3'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Delete all migration entries
cursor.execute("DELETE FROM django_migrations;")

# Commit changes and close the connection
conn.commit()
conn.close()

print("All migrations have been cleared successfully!")
