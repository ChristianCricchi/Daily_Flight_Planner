# Import necessary libraries
import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

# Initialise the Flask application
app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Initialise PyMongo
mongo = PyMongo(app)


# Route for the home page
@app.route("/")
def home():
    return redirect(url_for("login"))


# Route to get flights
@app.route("/get_flights")
def get_flights():
    flights = list(mongo.db.flights.find())
    return render_template("flights.html", flights=flights)


# Route for searching flights
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    flights = list(mongo.db.flights.find({"$text": {"$search": query}}))
    return render_template("flights.html", flights=flights)

# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if the username already exists in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Hello, Username already exists!")
            return redirect(url_for("register"))
            
        # Register new user
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


# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}) 

        if existing_user:
            # Ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], 
                    request.form.get("password")):
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
            # Username does not exist
            flash("Incorrect Username and/or Password, please try again!")
            return redirect(url_for("login"))

    return render_template("login.html")



# Route for user profile
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Grab the session user's username from database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:    
        return render_template("profile.html", username=username)
    return redirect(url_for("login"))  


# Route for user logout
@app.route("/logout")
def logout():
    # Remove user from session cookies
    flash("Goodbye, you have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Route to add a new flight
@app.route("/add_flight", methods=["GET", "POST"])
def add_flight():
    if request.method == "POST":
        special_assistance = "on" if request.form.get(
            "special_assistance") else "off"
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


# Route to edit an existing flight
@app.route("/edit_flight/<flight_id>", methods=["GET", "POST"])
def edit_flight(flight_id):
    if request.method == "POST":
        special_assistance = "on" if request.form.get(
            "special_assistance") else "off"
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
        mongo.db.flights.update_one({"_id": ObjectId(flight_id)}, {
            "$set": submit})
        flash("Flight Successfully Updated")
        return redirect(url_for("get_flights"))
    flight = mongo.db.flights.find_one({"_id": ObjectId(flight_id)})
    dispatcher = mongo.db.dispatcher.find().sort("dispatch_name", 1)
    return render_template(
        "edit_flight.html", flight=flight, dispatcher=dispatcher)


# Route to dispatch a flight
@app.route("/dispatched_flight/<flight_id>")
def dispatched_flight(flight_id):
    mongo.db.flights.delete_one({"_id": ObjectId(flight_id)})
    flash("Flight Successfully Dispatched")
    return redirect(url_for("get_flights"))


# Route to get dispatch information
@app.route("/get_dispatch")
def get_dispatch():
    dispatch = list(mongo.db.dispatcher.find().sort("dispatch_name", 1))
    return render_template("dispatch.html", dispatch=dispatch)


# Route to add a new dispatcher
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


# Route to edit an existing dispatcher
@app.route("/edit_dispatch/<dispatch_id>", methods=["GET", "POST"])
def edit_dispatch(dispatch_id): 
    if request.method == "POST":
        submit = {
            "dispatch_name": request.form.get("dispatch_name"),
            "id": request.form.get("id"),
        } 
        mongo.db.dispatcher.update_one({"_id": ObjectId(dispatch_id)}, {
            "$set": submit})
        flash("Dispatcher Successfully Updated")
        return redirect(url_for("get_dispatch"))
    dispatch = mongo.db.dispatcher.find_one({"_id": ObjectId(dispatch_id)})
    return render_template("edit_dispatch.html", dispatch=dispatch)


# Route to delete a dispatcher
@app.route("/delete_dispatch/<dispatch_id>")
def delete_dispatch(dispatch_id):
    mongo.db.dispatcher.delete_one({"_id": ObjectId(dispatch_id)})
    flash("Dispatcher Successfully Deleted")
    return redirect(url_for("get_dispatch"))


# Route for the About page
@app.route("/about")
def about():
    return render_template("about.html")


# Route to view reports
@app.route('/report')
def report():
    reports = mongo.db.report.find()
    return render_template('report.html', reports=reports)


# Route to add a new report
@app.route('/add_report', methods=['POST'])
def add_report():
    if request.method == 'POST':
        new_report = {
            'flight_number': request.form.get('flight_number'),
            'dispatcher_name': request.form.get('dispatcher_name'),
            'report_content': request.form.get('report_content')
        }
        mongo.db.report.insert_one(new_report)
        flash("Report Successfully Added")
        return redirect(url_for('report'))


# Route to add a new report
@app.route('/edit_report/<report_id>', methods=['GET', 'POST'])
def edit_report(report_id):
    if request.method == 'POST':
        updated_report = {
            'flight_number': request.form.get('flight_number'),
            'dispatcher_name': request.form.get('dispatcher_name'),
            'report_content': request.form.get('report_content')
        }
        mongo.db.report.update_one({'_id': ObjectId(report_id)}, {
            '$set': updated_report})
        flash("Report Successfully Updated")
        return redirect(url_for('report'))
    report = mongo.db.report.find_one({'_id': ObjectId(report_id)})
    return render_template('edit_report.html', report=report)


# Route to delete a report
@app.route('/delete_report/<report_id>')
def delete_report(report_id):
    mongo.db.report.delete_one({'_id': ObjectId(report_id)})
    flash("Report Successfully Delete")
    return redirect(url_for('report'))


# Start the application
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)   
