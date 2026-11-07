
from flask import Flask, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB = "saimx.db"

def setup():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                coins INTEGER DEFAULT 0
            )
        """)

setup()

PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SAIMX Coin</title>
<style>
body {
    background: #090909;
    color: white;
    text-align: center;
    font-family: Arial;
    padding: 30px 15px;
}
h1 { color: #f5c542; font-size: 34px; }
.balance { font-size: 30px; margin: 30px; }
.coin {
    width: 190px;
    height: 190px;
    border-radius: 50%;
    background: linear-gradient(145deg,#ffe477,#b8860b);
    color: #171000;
    font-size: 35px;
    font-weight: bold;
    border: 7px solid #fff0a8;
    box-shadow: 0 0 35px #d9a900;
    cursor: pointer;
}
.coin:active { transform: scale(.94); }
p { color: #aaa; }
</style>
</head>
<body>
<h1>SAIMX COIN</h1>
<p>Tap and earn coins!</p>
<div class="balance">
    <span id="coins">0</span> 🪙
</div>
<button class="coin" onclick="tap()">SAIMX</button>
<p>اضغط على العملة لجمع النقاط</p>
<script>
async function update() {
    const r = await fetch('/api/state');
    const d = await r.json();
    document.getElementById('coins').innerText = d.coins;
}
async function tap() {
    const r = await fetch('/api/tap', {method:'POST'});
    const d = await r.json();
    document.getElementById('coins').innerText = d.coins;
}
update();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

@app.route("/api/state")
def state():
    with sqlite3.connect(DB) as con:
        con.execute("INSERT OR IGNORE INTO players (id) VALUES (1)")
        coins = con.execute(
            "SELECT coins FROM players WHERE id=1"
        ).fetchone()[0]
    return jsonify(coins=coins)

@app.route("/api/tap", methods=["POST"])
def tap():
    with sqlite3.connect(DB) as con:
        con.execute("INSERT OR IGNORE INTO players (id) VALUES (1)")
        con.execute("UPDATE players SET coins=coins+1 WHERE id=1")
        coins = con.execute(
            "SELECT coins FROM players WHERE id=1"
        ).fetchone()[0]
    return jsonify(coins=coins)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
  
