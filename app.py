# app.py
import streamlit as st
import requests

# ─── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Bank Churn Prediction",
    page_icon="🏦",
    layout="centered"
)

# ─── API configuration ─────────────────────────────────────────────
# API_URL = "http://localhost:8000/predict" 
API_URL= 'https://a2-backend-y07r.onrender.com'
# ─── Title & description ───────────────────────────────────────────
st.title("🏦 Bank Customer Churn Prediction")
st.markdown("""
Enter the customer information below.  
The prediction is performed via a **FastAPI ML service**.
""")

# ─── Input form ────────────────────────────────────────────────────
with st.form("customer_form"):
    col1, col2 = st.columns(2)

    with col1:
        credit_score = st.number_input("Credit Score", 300, 850, value=650, step=1)
        geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", 18, 92, value=40, step=1)
        tenure = st.number_input("Tenure (years)", 0, 10, value=5, step=1)

    with col2:
        balance = st.number_input("Balance (€)", 0.0, 250000.0, value=50000.0, step=1000.0)
        num_products = st.selectbox("Number of Products", [1, 2, 3, 4], index=1)
        has_credit_card = st.selectbox(
            "Has Credit Card", [1, 0],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )
        is_active_member = st.selectbox(
            "Is Active Member", [1, 0],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )
        estimated_salary = st.number_input(
            "Estimated Salary (€)", 0.0, 200000.0, value=50000.0, step=1000.0
        )

    submitted = st.form_submit_button(
        "Predict Churn", type="primary", use_container_width=True
    )

# ─── Prediction via FastAPI ────────────────────────────────────────
if submitted:
    payload = {
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_products,
        "HasCrCard": has_credit_card,
        "IsActiveMember": is_active_member,
        "EstimatedSalary": estimated_salary
    }

    try:
        with st.spinner("Calling prediction service..."):
            response = requests.post(API_URL, json=payload, timeout=5)

        if response.status_code == 200:
            result = response.json()

            prob = result["churn_probability"]
            risk_level = result["risk_level"]

            # ─── Result display ────────────────────────────────────
            st.subheader("Prediction Result")
            st.metric("Churn Probability", f"{prob:.1%}", delta_color="inverse")

            if prob > 0.5:
                st.error(f"**{risk_level}**")
                st.info("Consider retention strategies: offers, outreach, loyalty benefits.")
            else:
                st.success(f"**{risk_level}**")
                st.info("Customer appears stable. No immediate action required.")

        else:
            st.error("Prediction service returned an error.")
            st.json(response.json())

    except requests.exceptions.RequestException as e:
        st.error("Could not connect to prediction API.")
        st.caption(str(e))

# ─── Footer ────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Frontend: Streamlit • Backend: FastAPI • Model: TensorFlow + Scikit-learn")
