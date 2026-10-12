from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import os

load_dotenv(dotenv_path=".env", override=True)

app = Flask(__name__)

client = MongoClient(
    os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/"),
    serverSelectionTimeoutMS=3000
)

db = client["digitalRiskDB"]
brands = db["brands"]


@app.route("/")
def home():
    all_brands = list(brands.find().sort("_id", -1))
    return render_template("brand.html", all_brands=all_brands)


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
        return "Brand name is required!", 400

    brands.insert_one(brand_data)

    return redirect(url_for("home"))


@app.route("/edit-brand/<brand_id>", methods=["GET", "POST"])
def edit_brand(brand_id):
    try:
        object_id = ObjectId(brand_id)
    except Exception:
        return "Invalid brand ID", 400

    brand = brands.find_one({"_id": object_id})

    if brand is None:
        return "Brand not found", 404

    if request.method == "POST":
        updated_data = {
            "brand_name": request.form.get("brand_name", "").strip(),
            "website": request.form.get("website", "").strip(),
            "logo_url": request.form.get("logo_url", "").strip(),
            "social_accounts": request.form.get("social_accounts", "").strip(),
            "mobile_apps": request.form.get("mobile_apps", "").strip()
        }

        if not updated_data["brand_name"]:
            return "Brand name is required!", 400

        brands.update_one(
            {"_id": object_id},
            {"$set": updated_data}
        )

        return redirect(url_for("home"))

    return render_template("edit_brand.html", brand=brand)


@app.route("/delete-brand/<brand_id>", methods=["POST"])
def delete_brand(brand_id):
    try:
        object_id = ObjectId(brand_id)
    except Exception:
        return "Invalid brand ID", 400

    result = brands.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        return "Brand not found", 404

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)