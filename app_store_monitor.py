import re
import pandas as pd

def analyze_app(app_name, developer, description, rating=0):
    risk_score = 0
    reasons = []

    text = f"{app_name} {developer} {description}".lower()

    suspicious_words = [
        "cracked", "free money", "guaranteed reward",
        "password", "otp", "hack", "unofficial"
    ]

    for word in suspicious_words:
        if word in text:
            risk_score += 15
            reasons.append(f"Suspicious keyword: {word}")

    if not developer.strip():
        risk_score += 20
        reasons.append("Developer information missing")

    if not description.strip():
        risk_score += 10
        reasons.append("App description missing")

    if rating < 2 and rating > 0:
        risk_score += 15
        reasons.append("Low user rating")

    risk_score = min(risk_score, 100)

    if risk_score >= 50:
        severity = "High Risk"
    elif risk_score >= 25:
        severity = "Medium Risk"
    else:
        severity = "Low Risk"

    return {
        "App Name": app_name,
        "Developer": developer,
        "Risk Score": risk_score,
        "Severity": severity,
        "Reasons": reasons or ["No listed warning indicators"]
    }


def analyze_apps(apps):
    return pd.DataFrame([
        analyze_app(**app) for app in apps
    ])