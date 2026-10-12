import json
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Digital Risk Protection Platform",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Digital Risk Protection Platform")
st.caption("Monitor and assess potential digital risks.")

selected_tab = st.radio(
    "Choose a module",
    [
        "📱 Social Media",
        "🔍 Brand Detection",
        "🏢 Brand Database",
        "🌐 Website Proxy",
        "📲 App Store Monitor"
    ],
    horizontal=True,
    key="module_navigation"
)

# 1. Social Media Monitoring
if selected_tab == "📱 Social Media":
    st.header("📱 Social Media Monitoring")
    st.info(
        "Enter profile details to perform a basic "
        "rule-based risk check. This is not live monitoring."
    )

    username = st.text_input("Profile Username")
    profile_url = st.text_input("Profile URL")
    description = st.text_area("Profile Description")

    if st.button("Check Profile", key="check_profile"):
        if not username.strip() and not profile_url.strip():
            st.warning("Enter a username or profile URL.")
        else:
            text = f"{username} {profile_url} {description}".lower()
            indicators = []

            if any(word in text for word in [
                "free money", "giveaway", "urgent payment",
                "verify password", "send otp"
            ]):
                indicators.append("Potential scam-related wording")

            if profile_url and not profile_url.startswith(
                ("https://", "http://")
            ):
                indicators.append("URL format should be reviewed")

            if indicators:
                st.warning("Potential warning indicators found.")
                for item in indicators:
                    st.write(f"- {item}")
            else:
                st.success(
                    "No listed warning indicators found. "
                    "This does not prove the profile is safe."
                )

# 2. Brand Detection
elif selected_tab == "🔍 Brand Detection":
    st.header("🔍 Look-alike Brand Detection")

    from detector import scan_candidates

    brand = st.text_input("Official Brand Name")
    candidates = st.text_area(
        "Candidate domains or names",
        placeholder="example-brand.com\nexamplebrand-support.com"
    )

    if st.button("Scan Candidates", key="scan_brands"):
        if not brand.strip() or not candidates.strip():
            st.warning("Enter a brand name and candidate list.")
        else:
            candidate_list = [
                line.strip()
                for line in candidates.splitlines()
                if line.strip()
            ]

            try:
                results = scan_candidates(brand, candidate_list)
                st.subheader("Detection Results")
                st.dataframe(
                    pd.DataFrame(results),
                    use_container_width=True
                )
            except Exception as exc:
                st.error(f"Brand detection failed: {exc}")

# 3. Brand Database
elif selected_tab == "🏢 Brand Database":
    st.header("🏢 Official Brand Database")

    from brand_database import (
        create_database,
        add_brand,
        get_all_brands
    )

    create_database()

    brand_name = st.text_input("Brand Name", key="db_brand")
    website = st.text_input("Official Website", key="db_website")
    keywords = st.text_input(
        "Keywords (comma separated)",
        key="db_keywords"
    )

    if st.button("Add Brand", key="add_brand"):
        if brand_name.strip() and website.strip():
            try:
                add_brand(
                    brand_name.strip(),
                    website.strip(),
                    keywords.strip()
                )
                st.success("Brand saved successfully!")
            except Exception as exc:
                st.error(f"Could not save brand: {exc}")
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

# 4. Website Proxy
elif selected_tab == "🌐 Website Proxy":
    st.header("🌐 AI Website & Brand Risk Analysis")

    try:
        from website_analyzer import (
            TASKS,
            fetch_website,
            analyze_with_genai
        )

        task = st.selectbox(
            "Analysis Type",
            list(TASKS.keys()),
            key="proxy_task"
        )
        brand_name = st.text_input("Brand Name", key="proxy_brand")
        official_url = st.text_input(
            "Official Website (optional)",
            key="proxy_official"
        )
        suspicious_url = st.text_input(
            "Suspicious Website URL (optional)",
            key="proxy_suspicious"
        )
        brand_details = st.text_area(
            "Brand Details",
            key="proxy_details"
        )
        supporting_evidence = st.text_area(
            "Additional Evidence",
            key="proxy_evidence"
        )

        if st.button("Analyze Website", key="proxy_analyze"):
            if not brand_name.strip():
                st.warning("Enter the brand name.")
            elif not suspicious_url.strip() and not supporting_evidence.strip():
                st.warning("Enter a URL or provide evidence.")
            else:
                try:
                    page_evidence = {}

                    if suspicious_url.strip():
                        page_evidence["suspicious_asset"] = (
                            fetch_website(suspicious_url)
                        )

                    if official_url.strip():
                        page_evidence["official_reference"] = (
                            fetch_website(official_url)
                        )

                    with st.spinner("Analyzing submitted evidence..."):
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
                    st.write(
                        "Classification:",
                        result.get("classification", "Unknown")
                    )
                    st.write(
                        "Confidence:",
                        result.get("confidence", "Unknown")
                    )

                    for section in [
                        "reasons",
                        "warning_signs",
                        "missing_evidence",
                        "recommended_actions"
                    ]:
                        st.markdown(
                            f"### {section.replace('_', ' ').title()}"
                        )
                        for item in result.get(section, []):
                            st.write(f"- {item}")

                    st.markdown("### Limitations")
                    st.write(result.get("limitations", "Not specified."))

                    st.download_button(
                        "Download Assessment JSON",
                        data=json.dumps(
                            result,
                            indent=2,
                            ensure_ascii=False
                        ),
                        file_name="brand_risk_assessment.json",
                        mime="application/json"
                    )

                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")

    except Exception as exc:
        st.error(
            "Website Analyzer could not be loaded. "
            f"Check Website_Analyzer.py and its dependencies. Details: {exc}"
        )

# 5. App Store Monitor
elif selected_tab == "📲 App Store Monitor":
    st.header("📲 App Store Risk Detection")
    st.caption(
        "Rule-based screening only; this does not fetch live app-store data."
    )

    from app_store_monitor import analyze_app

    app_name = st.text_input("App Name", key="store_app_name")
    developer = st.text_input("Developer Name", key="store_developer")
    rating = st.slider(
        "App Rating",
        0.0,
        5.0,
        3.0,
        0.5,
        key="store_rating"
    )
    description = st.text_area(
        "App Description",
        key="store_description"
    )

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
                data=json.dumps(result, indent=2, ensure_ascii=False),
                file_name="app_risk_report.json",
                mime="application/json"
            )