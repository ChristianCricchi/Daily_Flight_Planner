import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")

# new
@app.route("/")
def index():
    if 'user' in session:
        return redirect(url_for('get_flights'))
    return redirect(url_for('login'))


@app.route("/get_flights")
def get_flights():
    flights = list(mongo.db.flights.find())
    return render_template("flights.html", flights=flights)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if the username already exists in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Hello, Username already exists!")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")) 
        }  
        mongo.db.users.insert_one(register)  

        # Store the authenticated user's data in a session cookie
        session["user"] = request.form.get("username").lower()
        flash("User account created!") 
        return redirect(url_for("profile", username=session["user"])) 

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome at DFPlanner {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"])) 
            else:
                # Invalid password match
                flash("Incorrect Username and/or Password, please try again!")
                return redirect(url_for("login"))

        else:
            # Username doesn't exist
            flash("Incorrect Username and/or Password, please try again!")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Grab the session user's username from database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:    
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))  


@app.route("/logout")
def logout():
    # Remove user from session cookies
    flash("Goodbye, you have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_flight")
def add_flight():
    return render_template("add_flight.html")



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)