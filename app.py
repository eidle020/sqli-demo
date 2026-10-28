# ----- App Setup -----
from flask import Flask, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    cur.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    conn.commit()
    conn.close()

# ----- Routes -----
@app.route("/")
def home():
    return '''
        <h2>Login</h2>
        <form method="POST" action="/login">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <input type="submit" value="Log in">
        </form>
    '''

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    # VULNERABLE: user input is concatenated directly into the SQL query
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cur.execute(query)

    # SAFE: parameterized query - user input is passed separately, never as SQL
    #query = "SELECT * FROM users WHERE username = ? AND password = ?"
    #cur.execute(query, (username, password))

    result = cur.fetchone()

    conn.close()

    if result:
        return "<h3>Login successful! Welcome, " + username + ".</h3>"
    else:
        return "<h3>Login failed. Invalid credentials.</h3>"

# ----- Start the app -----
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
