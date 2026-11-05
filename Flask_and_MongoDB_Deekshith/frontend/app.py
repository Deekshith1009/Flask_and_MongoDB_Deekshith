import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Load .env from the project root (one folder above frontend)
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH, override=True, encoding="utf-8-sig")

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError(f"MONGO_URL is missing. Looked for: {ENV_PATH} (file exists: {ENV_PATH.exists()})")

app = Flask(__name__)

# Connection: client -> database -> collection
client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
db = client["flask_and_mongodb"]
collection = db["users"]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # Basic validation: show the error on the same page
        if not name or not email:
            return render_template(
                "index.html",
                error="Name and email are required.",
                name=name, email=email, message=message,
            )

        try:
            collection.insert_one({"name": name, "email": email, "message": message})
        except PyMongoError as e:
            # Error: stay on the same page and show the error (no redirect)
            return render_template(
                "index.html",
                error=f"Could not save your data: {e}",
                name=name, email=email, message=message,
            )

        # Success: redirect to another page
        return redirect(url_for("success"))

    return render_template("index.html", error=None, name="", email="", message="")


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)