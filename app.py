import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
import certifi

app = Flask(__name__)
client = MongoClient("mongodb+srv://diana:diana12345@insiteblog-application.7n6bk.mongodb.net/test", tlsCAFile=certifi.where())
app.db = client.insiteblog


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

    entries_with_date = []
    for entry in app.db.entries.find({}):
        entries_with_date.append((
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
        ))
    return render_template("home.html", entries=entries_with_date)


