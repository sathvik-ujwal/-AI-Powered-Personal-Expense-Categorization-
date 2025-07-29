from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from pymongo import MongoClient
import pickle
import numpy as np
import datetime
from functools import wraps
import joblib


model = joblib.load('models/xgb_best_model.pkl')
label_mapping = joblib.load('models/label_mapping.pkl')
vectorizer = joblib.load('models/tfidf_vectorizer.pkl')

# Flask + MongoDB setup
app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

client = MongoClient("mongodb+srv://<sathvik>:<dPx79QjaWGzejXdI>@petcluster.yy9ay.mongodb.net/?retryWrites=true&w=majority&appName=PetCluster")
db = client["expense"]
transactions = db["transactions"]


# Prediction function
def predict_category(text):
    X = vectorizer.transform([text])
    y_pred = model.predict(X)
    return label_mapping[int(y_pred[0])]

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        description = request.form["description"]
        amount = float(request.form["amount"])
        category = predict_category(description)

        transactions.insert_one({
            "description": description,
            "amount": amount,
            "category": category,
            "date": datetime.datetime.utcnow().date().isoformat()
        })

        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/transactions")
def all_transactions():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    user_txns = list(transactions.find({"user": username}))
    return render_template("transactions.html", transactions=user_txns)

@app.route("/api/category_summary")
def category_summary():
    if "username" not in session:
        return jsonify({"labels": [], "values": []}), 401

    username = session["username"]

    pipeline = [
        { "$match": { "user": username } }, 
        {
            "$group": {
                "_id": "$category",
                "total": {"$sum": "$amount"}
            }
        }
    ]
    summary = list(transactions.aggregate(pipeline))
    labels = [entry["_id"] for entry in summary]
    values = [entry["total"] for entry in summary]
    return jsonify({"labels": labels, "values": values})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        user = db.users.find_one({"username": username})
        if user:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("User not found. Please sign up.")
            return redirect(url_for("signup"))
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        if db.users.find_one({"username": username}):
            flash("User already exists. Please log in.")
            return redirect(url_for("login"))
        db.users.insert_one({"username": username})
        flash("Signup successful. Please log in.")
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
