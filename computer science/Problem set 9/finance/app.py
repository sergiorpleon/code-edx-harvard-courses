import os

from cs50 import SQL
from flask import Flask, flash, redirect, url_for, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

     # Get user cash
    rows = db.execute(
            "SELECT * FROM users WHERE id = ?", session['user_id']
        )

    # if not rows:
    #    return apology('Database query failed. Please click "Portfolio" again, Heroku sometimes fails on first attempt')

    if len(rows) >= 1:
        cash = rows[0]["cash"]
    else:
        cash = 0

    # Get transactions
    transactions = db.execute(
            "SELECT * FROM transactions WHERE user_id = ?", session['user_id']
        )

    # if not transactions:
    #    return apology('Database query failed. Please click "Portfolio" again, query sometimes fails on first attempt')

    # Sum shares of symbols
    current_shares = {}
    for transaction in transactions:
        if transaction["symbol"] not in current_shares:
            current_shares[transaction["symbol"]] = 0

        if transaction["type"] == 'buy':
            current_shares[transaction["symbol"]] += transaction["shares"]
        elif transaction["type"] == 'sell':
            current_shares[transaction["symbol"]] -= transaction["shares"]

    # Get only shares bigger than zero
    stocks = {}
    for key, value in current_shares.items():
        if value > 0:
            stocks[key] = value

     # Get symbol current price
    total = cash
    current_prices = {}
    for key, value in stocks.items():
        price_symbol = lookup(key)

        current_prices[key] = price_symbol["price"]
        total = total + value * current_prices[key]

    return render_template("index.html", stocks=stocks, prices=current_prices, cash=cash, total=total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide shares", 400)

        # Ensure shares was digit
        if not (request.form.get("shares")).isdigit():
            return apology("You cannot purchase partial shares", 400)

        # Ensure shares was positive count
        if int(request.form.get("shares")) <=0:
            return apology("must provide positive shares", 400)

        # Ensure symbol is real
        quote = lookup(request.form.get("symbol"))
        if quote is None:
            return apology("symbol request not successfull", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", session['user_id']
        )
        cash = rows[0]["cash"]

        # Ensure extraction mount is not bigger than cash
        if float(quote['price'])*float(request.form.get("shares")) > float(cash):
            return apology("cash not successfull", 400)

        # Add row table transaction
        db.execute(
            "INSERT INTO transactions (symbol, shares, price, user_id, type) VALUES (?, ?, ?, ?, 'buy')",
                     quote['symbol'], int(request.form.get("shares")), quote['price'], session['user_id']
            )

        # Update user cash
        newcash = float(cash) - float(quote['price'])*float(request.form.get("shares"))
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
                     newcash, session['user_id']
            )

        flash("Bought!")
        return redirect("/")
    return render_template("buy.html")
    #Add table user - actions (symbol, shares, user_id)

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Query database for username
    rows = db.execute(
        "SELECT * FROM transactions WHERE user_id = ?", session['user_id']
    )

    return render_template("history.html", rows = rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure symbol is real
        quote = lookup(request.form.get("symbol"))
        if quote is None:
            return apology("symbol request not successfull", 400)

        return render_template("quoted.html", quote = quote)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide conformation password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and conformation password not math", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username not exists
        if len(rows) == 1:
            return apology("username already exist", 400)


        # Query database for username
        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                         request.form.get("username"), generate_password_hash(request.form.get("password"))
            )

        except ValueError:
            return apology("Invalid username", 400)

        # Redirect user to login page
        return redirect(url_for('login'))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide symbol", 400)

        # Ensure shares was positive number
        if int(request.form.get("shares")) <=0:
            return apology("must provide positive shares", 400)

        # Ensure symbol was real
        quote = lookup(request.form.get("symbol"))
        if quote is None:
            return apology("symbol request not successfull", 400)

        # Get count shares of symbol
        shares_buys = db.execute(
            "SELECT SUM(shares) FROM transactions WHERE symbol = ? AND user_id = ? AND type = 'buy'", quote["symbol"], session['user_id']
        )[0]["SUM(shares)"]
        shares_sells = db.execute(
            "SELECT SUM(shares) FROM transactions WHERE symbol = ? AND user_id = ? AND type = 'sell'", quote["symbol"], session['user_id']
        )[0]["SUM(shares)"]

        if shares_buys is None:
            return apology("dont has shares", 400)

        if shares_sells is None:
            shares_sells = 0

        shares_buys = shares_buys - shares_sells

        # Ensure shares input not is more than user shares
        if int(request.form.get("shares")) > shares_buys:
            return apology("cash not successfull", 400)

        # Add row table transaction
        db.execute(
            "INSERT INTO transactions (symbol, shares, price, user_id, type) VALUES (?, ?, ?, ?, 'sell')",
                     quote['symbol'],  int(request.form.get("shares")), quote['price'], session['user_id']
            )

        # Query database user cash
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", session['user_id']
        )
        cash = rows[0]['cash']

        # Update user cash
        newcash = float(cash) + float(quote['price'])*float(request.form.get("shares"))
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
                     newcash, session['user_id']
            )

        flash("Sell!")
        return redirect("/")

    # Get user transactions
    transactions = db.execute(
            "SELECT * FROM transactions WHERE user_id = ?", session['user_id']
        )

    # Count symbol shares
    current_shares = {}
    for transaction in transactions:
        if transaction["symbol"] not in current_shares:
            current_shares[transaction["symbol"]] = 0

        if transaction["type"] == 'buy':
            current_shares[transaction["symbol"]] += transaction["shares"]
        elif transaction["type"] == 'sell':
            current_shares[transaction["symbol"]] -= transaction["shares"]

    # Get only shares positive count
    stocks = {}
    for key, value in current_shares.items():
        if value > 0:
            stocks[key] = value

    return render_template("sell.html", symbols=stocks)

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("current_password"):
            return apology("must provide current password", 400)

        # Ensure password was submitted
        elif not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation_password"):
            return apology("must provide conformation password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"]
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("current_password")
        ):
            return apology("invalid password", 400)

        if request.form.get("new_password") != request.form.get("confirmation_password"):
            return apology("new password and conformation new password not math", 400)

        # Query database for username
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
                     generate_password_hash(request.form.get("new_password")), session['user_id']
            )

        # Forget any user_id
        session.clear()

        # Redirect user to home page
        return redirect(url_for('login'))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Buy shares of stock"""

    if request.method == "POST":
        # Ensure mount was submitted
        if not request.form.get("mount"):
            return apology("must provide mount", 400)

        # Ensure mount was positive count
        if int(request.form.get("mount")) <=0:
            return apology("must provide positive mount", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", session['user_id']
        )
        cash = rows[0]["cash"]

        # Update user cash
        newcash = float(cash) + float(request.form.get("mount"))
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
                     newcash, session['user_id']
            )

        flash("Added cash!")
        return redirect("/")
    return render_template("add.html")


if __name__ == '__main__':
   app.run(debug=True)


"""
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,  -- Cambiado a INTEGER
    price NUMERIC NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL,
    type TEXT DEFAULT 'buy' CHECK(type IN ('buy', 'sell')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

--not implement, use only transactions
CREATE TABLE user_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    symbol TEXT NOT NULL,
    shares NUMERIC NOT NULL,
    user_id INTEGER NOT NULL,  -- Declare user_id as INTEGER and NOT NULL
    FOREIGN KEY (user_id) REFERENCES users(id)  -- Set user_id as a foreign key
);

CREATE UNIQUE INDEX user_id_index ON transactions (user_id);
"""
