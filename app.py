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
def home():
    return redirect(url_for("login"))


@app.route("/get_flights")
def get_flights():
    flights = list(mongo.db.flights.find())
    return render_template("flights.html", flights=flights)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    flights = list(mongo.db.flights.find({"$text": {"$search": query}}))
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
                    flash("Welcome {}".format(
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


@app.route("/add_flight", methods=["GET", "POST"])
def add_flight():
    if request.method == "POST":
        special_assistance = "on" if request.form.get("special_assistance") else "off"
        flight = {
            "dispatch_name": request.form.get("dispatch_name"),
            "stand": request.form.get("stand"),
            "comments": request.form.get("comments"),
            "special_assistance": special_assistance,
            "date": request.form.get("date"),
            "flight_inbound": request.form.get("flight_inbound"),
            "from": request.form.get("from"),
            "registration": request.form.get("registration"),
            "aircraft": request.form.get("aircraft"),
            "sta": request.form.get("sta"),
            "pax_inbound": request.form.get("pax_inbound"),
            "arrival": request.form.get("arrival"),
            "flight_outbound": request.form.get("flight_outbound"),
            "to": request.form.get("to"),
            "std": request.form.get("std"),
            "pax_outbound": request.form.get("pax_outbound"),
            "gate": request.form.get("gate"),
            "created_by": session["user"]
        }
        mongo.db.flights.insert_one(flight)
        flash("Flight Successfully Added")
        return redirect(url_for("get_flights"))

    dispatcher = mongo.db.dispatcher.find().sort("dispatch_name", 1)
    return render_template("add_flight.html", dispatcher=dispatcher)


@app.route("/edit_flight/<flight_id>", methods=["GET", "POST"])
def edit_flight(flight_id):

    if request.method == "POST":
        special_assistance = "on" if request.form.get("special_assistance") else "off"
        submit = {
            "dispatch_name": request.form.get("dispatch_name"),
            "stand": request.form.get("stand"),
            "comments": request.form.get("comments"),
            "special_assistance": special_assistance,
            "date": request.form.get("date"),
            "flight_inbound": request.form.get("flight_inbound"),
            "from": request.form.get("from"),
            "registration": request.form.get("registration"),
            "aircraft": request.form.get("aircraft"),
            "sta": request.form.get("sta"),
            "pax_inbound": request.form.get("pax_inbound"),
            "arrival": request.form.get("arrival"),
            "flight_outbound": request.form.get("flight_outbound"),
            "to": request.form.get("to"),
            "std": request.form.get("std"),
            "pax_outbound": request.form.get("pax_outbound"),
            "gate": request.form.get("gate"),
            "created_by": session["user"]
        }
        mongo.db.flights.update_one({"_id": ObjectId(flight_id)}, {"$set": submit})
        flash("Flight Successfully Updated")

    flight = mongo.db.flights.find_one({"_id": ObjectId(flight_id)})
    dispatcher = mongo.db.dispatcher.find().sort("dispatch_name", 1)
    return render_template("edit_flight.html", flight=flight, dispatcher=dispatcher)


@app.route("/dispatched_flight/<flight_id>")
def dispatched_flight(flight_id):
    mongo.db.flights.delete_one({"_id": ObjectId(flight_id)})
    flash("Flight Successfully Dispatched")
    return redirect(url_for("get_flights"))


@app.route("/get_dispatch")
def get_dispatch():
    dispatch = list(mongo.db.dispatcher.find().sort("dispatch_name", 1))
    return render_template("dispatch.html", dispatch=dispatch)


@app.route("/add_dispatch", methods=["GET", "POST"])
def add_dispatch():
     if request.method == "POST":
        dispatch = {
            "dispatch_name": request.form.get("dispatch_name"),
            "id": request.form.get("id"),
        }
        mongo.db.dispatcher.insert_one(dispatch)
        flash("New Dispatcher Added")
        return redirect(url_for("get_dispatch"))

     return render_template("add_dispatch.html")


@app.route("/edit_dispatch/<dispatch_id>", methods=["GET", "POST"])
def edit_dispatch(dispatch_id): 
    if request.method == "POST":
        submit = {
            "dispatch_name": request.form.get("dispatch_name"),
            "id": request.form.get("id"),
        } 
        mongo.db.dispatcher.update_one({"_id": ObjectId(dispatch_id)}, {"$set": submit})
        flash("Dispatcher Successfully Updated")
        return redirect(url_for("get_dispatch"))

    dispatch = mongo.db.dispatcher.find_one({"_id": ObjectId(dispatch_id)})
    return render_template("edit_dispatch.html", dispatch=dispatch)


@app.route("/delete_dispatch/<dispatch_id>")
def delete_dispatch(dispatch_id):
    mongo.db.dispatcher.delete_one({"_id": ObjectId(dispatch_id)})
    flash("Dispatcher Successfully Deleted")
    return redirect(url_for("get_dispatch"))


@app.route("/about")
def about():
    return render_template("about.html")

    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)