import MySQLdb

def reset_db():
    try:
        # Connect to MySQL (as root, no password, localhost - based on settings.py)
        db = MySQLdb.connect(user="root", passwd="", host="localhost")
        cursor = db.cursor()
        print("Dropping database student_db...")
        cursor.execute("DROP DATABASE IF EXISTS student_db")
        print("Creating database student_db...")
        cursor.execute("CREATE DATABASE student_db")
        print("Database reset successful!")
        db.close()
    except Exception as e:
        print(f"Error resetting DB: {e}")

if __name__ == '__main__':
    reset_db()
