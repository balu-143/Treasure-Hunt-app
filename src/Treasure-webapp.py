from flask import Flask, request, session, redirect, url_for, render_template_string
import random
import os

app = Flask(__name__)
app.secret_key = "replace_with_secure_key"

ROWS = range(1, 6)
COLS = range(1, 6)
MAX_ATTEMPTS = 20


def new_game():
    session["treasure"] = {
        "row": random.choice(list(ROWS)),
        "col": random.choice(list(COLS)),
    }
    session["attempts"] = 0
    session["message"] = ""


def location_hint(user_row, user_col, tr_row, tr_col):
    moves = []
    if user_row > tr_row:
        moves.append("UP")
    if user_row < tr_row:
        moves.append("DOWN")
    if user_col > tr_col:
        moves.append("LEFT")
    if user_col < tr_col:
        moves.append("RIGHT")
    return "🎉 Exact spot!" if not moves else " → ".join(moves)


# =======================
# HTML PAGE WITH GRID
# =======================

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Treasure Hunt</title>
    <style>
        body { font-family: Arial; margin: 30px; }
        table { border-collapse: collapse; margin-top: 20px; }
        th, td {
            border: 1px solid #444;
            padding: 8px 12px;
            text-align: center;
        }
        th { background-color: #eee; }
        .msg { margin-top: 20px; font-size: 20px; }
        input { padding: 5px; font-size: 16px; }
        button { padding: 6px 16px; font-size: 16px; }
        a { margin-top: 20px; display: inline-block; }
    </style>
</head>
<body>

<h1>Treasure Hunt</h1>
<p>Guess the treasure location (row & column between 1 and 5).</p>

<form method="POST">
    <label>Row (1–5):</label>
    <input type="number" name="row" min="1" max="5" required>
    &nbsp;&nbsp;
    <label>Column (1–5):</label>
    <input type="number" name="col" min="1" max="5" required>
    <button type="submit">Guess</button>
</form>

<!-- MESSAGE -->
<div class="msg">{{ message }}</div>

<p>Attempts: {{ attempts }} / {{ max_attempts }}</p>

/resetReset Game</a>


<!-- YOUR GRID RENDERED IN HTML -->
<h2>Grid</h2>
<table>
    <!-- Column headers -->
    <tr>
        <th></th>
        {% for c in cols %}
        <th>{{ c }}</th>
        {% endfor %}
    </tr>

    <!-- Rows -->
    {% for r in rows %}
    <tr>
        <th>{{ r }}</th>
        {% for c in cols %}
        <td>{{ c }}{{ r }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
</table>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    if "treasure" not in session:
        new_game()

    if request.method == "POST":
        guess_row = int(request.form.get("row"))
        guess_col = int(request.form.get("col"))

        tr = session["treasure"]
        tr_row = tr["row"]
        tr_col = tr["col"]

        session["attempts"] += 1

        # Win
        if guess_row == tr_row and guess_col == tr_col:
            session["message"] = f"🎉 You found the treasure at ({tr_row}, {tr_col})!"
        else:
            session["message"] = "Hint: " + location_hint(guess_row, guess_col, tr_row, tr_col)

        # Lost
        if session["attempts"] >= MAX_ATTEMPTS:
            session["message"] = f"❌ Out of attempts! Treasure was at ({tr_row}, {tr_col})."

    return render_template_string(
        HTML_PAGE,
        rows=ROWS,
        cols=COLS,
        attempts=session["attempts"],
        max_attempts=MAX_ATTEMPTS,
        message=session["message"]
    )


@app.route("/reset")
def reset():
    new_game()
    return redirect(url_for("index"))


if __name__ == "__main__":
   # app.run(debug=True)

   port = int(os.getenv("PORT", "5000"))
    # IMPORTANT: bind to 0.0.0.0 so it's reachable from outside the container
   app.run(host="0.0.0.0", port=port, debug=False)