from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database and create users table if it doesn't exist
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API to fetch the current user count
@app.route('/user_count', methods=['GET'])
def get_user_count():
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM users')
        count = c.fetchone()[0]
        conn.close()
        return jsonify({"user_count": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API to add a user to the waitlist
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (email) VALUES (?)', (email,))
        conn.commit()
        conn.close()
        return jsonify({"message": "User added successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)