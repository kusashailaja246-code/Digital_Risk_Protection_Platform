import streamlit as st
import pandas as pd
from urllib.parse import urlparse
from datetime import datetime
import os
from detector import detect_lookalike, scan_candidates
from brand_database import create_database, add_brand, get_all_brands

st.set_page_config(
    page_title="Social Media Risk Monitor",
    page_icon="🛡️",
    layout="wide"
)
st.title("🛡️ Digital Risk Protection Platform")
st.caption("Monitor social media, detect brand impersonation, and manage brand records.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📱 Social Media",
    "🔍 Brand Detection",
    "🏢 Brand Database",
    "🌐 Website Proxy",
    "📱 App Store Monitor"
])
with tab2:
    st.header("🔍 Brand Impersonation Detection")
    st.write("Check whether a name looks similar to your official brand.")

    brand_name = st.text_input(
        "Official Brand Name",
        key="brand_detect_name"
    )

    candidates_text = st.text_area(
        "Enter names to check (one per line)",
        key="brand_detect_candidates"
    )

    if st.button("Scan Brand Names"):
        if not brand_name.strip() or not candidates_text.strip():
            st.warning("Enter the brand name and candidate names.")
        else:
            from detector import scan_candidates

            candidates = [
                name.strip()
                for name in candidates_text.splitlines()
                if name.strip()
            ]

            results = scan_candidates(brand_name.strip(), candidates)

            for result in results:
                st.write("---")
                st.write("Candidate:", result["candidate"])
                st.write("Risk Score:", result["risk_score"], "/100")
                st.write("Severity:", result["severity"])
                st.write("Reasons:", ", ".join(result["reasons"]))
with tab3:
    st.header("🏢 Official Brand Database")

    from brand_database import create_database, add_brand, get_all_brands

    create_database()

    brand_name = st.text_input("Brand Name", key="db_brand")
    website = st.text_input("Official Website", key="db_website")
    keywords = st.text_input("Keywords (comma separated)", key="db_keywords")

    if st.button("Add Brand"):
        if brand_name.strip() and website.strip():
            add_brand(brand_name.strip(), website.strip(), keywords.strip())
            st.success("Brand saved successfully!")
        else:
            st.warning("Enter the brand name and official website.")

    st.subheader("Saved Brands")
    brands = get_all_brands()

    if brands:
        st.dataframe(
            [
                {
                    "Brand": b[1],
                    "Official Website": b[2],
                    "Keywords": b[3]
                }
                for b in brands
            ],
            use_container_width=True
        )
    else:
        st.info("No brands saved yet.")
with tab4:
    st.header("🌐 AI Website & Brand Risk Analysis")

    from website_analyzer import TASKS, fetch_website, analyze_with_genai

    task = st.selectbox(
        "Select detection task",
        list(TASKS.keys()),
        key="proxy_task"
    )

    brand_name = st.text_input(
        "Brand or Company Name",
        key="proxy_brand"
    )

    official_url = st.text_input(
        "Official Website (optional)",
        key="proxy_official"
    )

    suspicious_url = st.text_input(
        "Suspicious Website or Profile URL (optional)",
        key="proxy_suspicious"
    )

    brand_details = st.text_area(
        "Known Official Brand Details",
        key="proxy_details"
    )

    supporting_evidence = st.text_area(
        "Supporting Evidence",
        key="proxy_evidence"
    )

    if st.button("Analyze Asset", key="proxy_analyze"):
        if not brand_name.strip():
            st.warning("Enter the brand name.")
        elif not suspicious_url.strip() and not supporting_evidence.strip():
            st.warning("Enter a suspicious URL or supporting evidence.")
        else:
            try:
                page_evidence = {}

                if suspicious_url.strip():
                    page_evidence["suspicious_asset"] = fetch_website(
                        suspicious_url
                    )

                if official_url.strip():
                    page_evidence["official_reference"] = fetch_website(
                        official_url
                    )

                with st.spinner("AI is analyzing the evidence..."):
                    result = analyze_with_genai(
                        task=task,
                        brand_name=brand_name,
                        official_url=official_url,
                        suspicious_url=suspicious_url,
                        brand_details=brand_details,
                        supporting_evidence=supporting_evidence,
                        page_evidence=page_evidence
                    )

                st.subheader("Assessment Results")
                st.write("**Classification:**", result["classification"])
                st.write("**Confidence:**", result.get("confidence", "Unknown"))

                for section in [
                    "reasons",
                    "warning_signs",
                    "missing_evidence",
                    "recommended_actions"
                ]:
                    st.markdown("### " + section.replace("_", " ").title())
                    for item in result.get(section, []):
                        st.write("- " + item)

                st.markdown("### Limitations")
                st.write(result.get("limitations", "Not specified."))

                st.download_button(
                    "Download Assessment JSON",
                    data=__import__("json").dumps(
                        result, indent=2, ensure_ascii=False
                    ),
                    file_name="brand_risk_assessment.json",
                    mime="application/json"
                )

            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
with tab5:
    import json
    import streamlit as st
    from app_store_monitor import analyze_app

    st.header("📲 App Store Risk Detection")
    st.caption("Rule-based screening of app details. Not a live store scan.")

    app_name = st.text_input("App Name", key="store_app_name")
    developer = st.text_input("Developer Name", key="store_developer")
    rating = st.slider("App Rating", 0.0, 5.0, 3.0, 0.5, key="store_rating")
    description = st.text_area("App Description", key="store_description")

    if st.button("Analyze App", key="store_analyze"):
        if not app_name.strip():
            st.warning("Please enter an app name.")
        else:
            result = analyze_app(
                app_name=app_name,
                developer=developer,
                description=description,
                rating=rating
            )

            st.subheader("Assessment Result")
            st.metric("Risk Score", f"{result['Risk Score']}/100")
            st.write("Severity:", result["Severity"])
            st.write("App:", result["App Name"])
            st.write("Developer:", result["Developer"])

            st.subheader("Warning Indicators")
            for reason in result["Reasons"]:
                st.write(f"- {reason}")

            st.download_button(
                "Download Report",
                data=json.dumps(result, indent=2),
                file_name="app_risk_report.json",
                mime="application/json"
            )
st.header("🛡️ Social Media Monitoring")
st.divider()

HISTORY_FILE = "scan_history.csv"

# Profile Analysis
st.subheader("🔍 Analyze a Social Media Profile")

platform = st.selectbox(
    "Select Platform",
    ["Instagram", "Facebook", "Twitter", "LinkedIn", "Other"]
)

brand = st.text_input("Official Brand Name")
username = st.text_input("Profile Username")
profile_url = st.text_input("Profile URL")

if st.button("Analyze Profile"):
    if not brand.strip() or not username.strip() or not profile_url.strip():
        st.warning("Please fill in all fields.")

    else:
        url = urlparse(profile_url.strip())

        if url.scheme not in ("http", "https") or not url.netloc:
            st.error("Enter a valid URL starting with https://")

        else:
            score = 0
            reasons = []

            # Check brand name
            if brand.lower().replace(" ", "") not in username.lower().replace(" ", ""):
                score += 30
                reasons.append(
                    "Username does not contain the brand name."
                )

            # Check numbers in username
            if any(char.isdigit() for char in username):
                score += 15
                reasons.append("Username contains numbers.")

            # Check suspicious keywords
            suspicious_words = [
                "verify",
                "free-gift",
                "claim-prize"
            ]

            if any(word in profile_url.lower() for word in suspicious_words):
                score += 40
                reasons.append(
                    "URL contains a suspicious keyword."
                )

            score = min(score, 100)

            # Determine risk level
            if score >= 60:
                risk_level = "High"
            elif score >= 30:
                risk_level = "Medium"
            else:
                risk_level = "Low"

            # Save scan history
            new_record = pd.DataFrame([{
                "Date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "Platform": platform,
                "Brand": brand,
                "Username": username,
                "URL": profile_url,
                "Risk Score": score,
                "Risk Level": risk_level
            }])

            new_record.to_csv(
                HISTORY_FILE,
                mode="a",
                header=not os.path.exists(HISTORY_FILE),
                index=False
            )

            # Display result
            st.subheader("📋 Risk Analysis Result")
            st.metric("Preliminary Risk Score", f"{score}/100")

            if risk_level == "High":
                st.error("🔴 HIGH RISK")
            elif risk_level == "Medium":
                st.warning("🟠 MEDIUM RISK")
            else:
                st.success("🟢 LOW RISK")

            if reasons:
                st.write("**Reasons:**")
                for reason in reasons:
                    st.write("- " + reason)
            else:
                st.write(
                    "No risk indicators detected by these basic rules."
                )

            st.caption(
                "Demo result only. This tool does not verify accounts "
                "or monitor live social media platforms."
            )

st.divider()

# Risk Summary Dashboard
st.subheader("📊 Risk Summary Dashboard")

if os.path.exists(HISTORY_FILE):
    summary_data = pd.read_csv(HISTORY_FILE)

    if not summary_data.empty and "Risk Level" in summary_data.columns:
        high_count = (summary_data["Risk Level"] == "High").sum()
        medium_count = (summary_data["Risk Level"] == "Medium").sum()
        low_count = (summary_data["Risk Level"] == "Low").sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("🔴 High Risk", int(high_count))
        col2.metric("🟠 Medium Risk", int(medium_count))
        col3.metric("🟢 Low Risk", int(low_count))
    else:
        st.info("Analyze a profile to see the risk summary.")
else:
    st.info("Analyze a profile to see the risk summary.")

# Risk Analysis Bar Chart
st.divider()
st.subheader("📊 Risk Analysis Chart")

if os.path.exists(HISTORY_FILE):
    chart_data = pd.read_csv(HISTORY_FILE)

    if not chart_data.empty and "Risk Level" in chart_data.columns:
        risk_counts = (
            chart_data["Risk Level"]
            .value_counts()
            .reindex(["High", "Medium", "Low"], fill_value=0)
        )

        chart_df = pd.DataFrame({
            "Risk Level": risk_counts.index,
            "Number of Scans": risk_counts.values
        })

        st.bar_chart(
            chart_df,
            x="Risk Level",
            y="Number of Scans",
            width="stretch"
        )
    else:
        st.info("Analyze profiles to display the chart.")
else:
    st.info("No scan data available for the chart.")

# Previous Scan History
st.divider()
st.subheader("📋 Previous Scan History")

if os.path.exists(HISTORY_FILE):
    history = pd.read_csv(HISTORY_FILE)

    if not history.empty:
        def color_risk(value):
            if value == "High":
                return "background-color: #ffcdd2; color: #b71c1c"
            elif value == "Medium":
                return "background-color: #ffe0b2; color: #e65100"
            return "background-color: #c8e6c9; color: #1b5e20"

        styled_history = history.style.map(
            color_risk,
            subset=["Risk Level"]
        )

        st.dataframe(
            styled_history,
            width="stretch"
        )

        st.download_button(
            "⬇️ Download Scan History CSV",
            data=history.to_csv(index=False).encode("utf-8"),
            file_name="scan_history.csv",
            mime="text/csv"
        )
    else:
        st.info("No scan history available yet.")
else:
    st.info("No scan history available yet.")
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
    app.run(debug=False, use_reloader=False)
