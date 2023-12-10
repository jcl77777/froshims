from SQL import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

#configure app
app = Flask(__name__)

#configure session
app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#connect to db
db = SQL("sqlite:///froshims.db")

SPORTS = [
    "Basketball",
    "Soccer",
    "Ultimate Frisbee"
]

books = [
    "Harry Potter 1",
    "Harry Potter 2"
]

@app.route('/')
def index():
    if not session.get("name"):
        return redirect('/login')
    return render_template("index.html", sports = SPORTS)

@app.login('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session["name"] = None
    return redirect("/")

@app.route('/deregister', methods=["POST"])
def deregister():

    #forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
    return redirect('/registrants')

@app.route('/register', methods=["POST"])
def register():
    #validate submission
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")
    
    #Remember registrant
    db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", name, sport)

    #confirm registration
    return redirect("/registrants")

@app.route('/registrants')
def registrants():
    registrants = db.execute("SELECT * FROM registrants")
    return render_template("registrants.html", registrants=registrants)

@app.route('/cart', methods=["GET", "POST"])
def cart():

    #ensure cart exists
    if "cart" not in session:
        session["cart"] = []

    #POST
    if request.method == "POST":
        id = request.form.get("id")
        if id:
            session["cart"].append(id)
        return redirect('/cart')
    
    #GET
    books = db.execute("SELECT * FROM books WHERE id IN (?)", session["cart"])
    return render_template("cart.html", books=books)