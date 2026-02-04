from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        city = request.form["city"]
        genre = request.form["genre"]
        contact = request.form["contact"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS djs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                city TEXT,
                genre TEXT,
                contact TEXT
            )
        """)

        cur.execute(
            "INSERT INTO djs (name, city, genre, contact) VALUES (?, ?, ?, ?)",
            (name, city, genre, contact)
        )

        conn.commit()
        conn.close()

        return redirect("/djs")

    return render_template("register.html")

@app.route("/djs")
def djs():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, city, genre, contact FROM djs")
    dj_list = cur.fetchall()
    conn.close()

    return render_template("djs.html", djs=dj_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
