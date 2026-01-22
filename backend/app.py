from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD")
)

cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    text TEXT
)
""")
conn.commit()

@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "POST":
        text = request.json["text"]
        cur.execute("INSERT INTO messages (text) VALUES (%s)", (text,))
        conn.commit()
        return {"status": "saved"}
    else:
        cur.execute("SELECT text FROM messages")
        rows = cur.fetchall()
        return jsonify([r[0] for r in rows])

app.run(host="0.0.0.0", port=5000)

