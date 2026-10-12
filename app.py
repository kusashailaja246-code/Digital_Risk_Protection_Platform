from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = MongoClient(
    os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/"),
    serverSelectionTimeoutMS=3000
)

db = client["digitalRiskDB"]
brands = db["brands"]


@app.route("/")
def home():
    brand_list = list(brands.find().sort("brand_name", 1))
    return render_template("brand.html", brands=brand_list)


@app.route("/test-db")
def test_db():
    try:
        client.admin.command("ping")
        return "MongoDB connected successfully!"
    except Exception as e:
        return f"MongoDB connection failed: {e}", 500


@app.route("/save-brand", methods=["POST"])
def save_brand():
    brand_data = {
        "brand_name": request.form.get("brand_name", "").strip(),
        "website": request.form.get("website", "").strip(),
        "logo_url": request.form.get("logo_url", "").strip(),
        "social_accounts": request.form.get("social_accounts", "").strip(),
        "mobile_apps": request.form.get("mobile_apps", "").strip()
    }

    if not brand_data["brand_name"]:
        return "Brand name is required.", 400

    brands.update_one(
        {"brand_name": brand_data["brand_name"]},
        {"$set": brand_data},
        upsert=True
    )

    return redirect(url_for("home"))


@app.route("/edit-brand/<brand_id>", methods=["GET", "POST"])
def edit_brand(brand_id):
    try:
        object_id = ObjectId(brand_id)
    except Exception:
        return "Invalid brand ID.", 400

    brand = brands.find_one({"_id": object_id})

    if brand is None:
        return "Brand profile not found.", 404

    if request.method == "POST":
        brand_data = {
            "brand_name": request.form.get("brand_name", "").strip(),
            "website": request.form.get("website", "").strip(),
            "logo_url": request.form.get("logo_url", "").strip(),
            "social_accounts": request.form.get("social_accounts", "").strip(),
            "mobile_apps": request.form.get("mobile_apps", "").strip()
        }

        if not brand_data["brand_name"]:
            return "Brand name is required.", 400

        brands.update_one(
            {"_id": object_id},
            {"$set": brand_data}
        )

        return redirect(url_for("home"))

    return render_template("edit_brand.html", brand=brand)


@app.route("/delete-brand/<brand_id>", methods=["POST"])
def delete_brand(brand_id):
    try:
        brands.delete_one({"_id": ObjectId(brand_id)})
        return redirect(url_for("home"))
    except Exception as e:
        return f"Unable to delete brand: {e}", 400


if __name__ == "__main__":
    app.run(debug=True)