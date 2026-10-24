import streamlit as st
import requests
import os

st.set_page_config(
    page_title="E-Commerce RTO Predictor",
    layout="centered"
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/predict")

st.title("📦 E-Commerce RTO Prediction App")
st.write(
    "Enter order, customer, and delivery details "
    "to predict whether the order will result in Return to Origin (RTO)."
)

with st.form("prediction_form"):
    st.subheader("📋 Order & Customer Features")

    city_tier = st.selectbox(
        "City Tier",
        options=["Metro", "Tier-2", "Tier-3", "Rural"],
        index=1
    )

    payment_mode = st.selectbox(
        "Payment Mode",
        options=["COD", "Prepaid"],
        index=0
    )

    product_category = st.selectbox(
        "Product Category",
        options=["Footwear", "Fashion", "Home & Kitchen", "Accessories", "Electronics", "Beauty"],
        index=0
    )

    customer_type = st.selectbox(
        "Customer Type",
        options=["Repeat", "New"],
        index=0
    )

    past_orders = st.number_input(
        "Past Orders Count",
        min_value=0, max_value=50, value=3, step=1
    )

    past_rto_count = st.number_input(
        "Past RTO Count",
        min_value=0, max_value=20, value=1, step=1
    )

    order_value_inr = st.number_input(
        "Order Value (INR)",
        min_value=0.0, value=259.0, step=50.0
    )

    discount_pct = st.number_input(
        "Discount Percentage (%)",
        min_value=0.0, max_value=100.0, value=48.0, step=1.0
    )

    order_hour = st.number_input(
        "Order Hour (0 - 23)",
        min_value=0, max_value=23, value=22, step=1
    )

    is_sale_day = st.selectbox(
        "Is Sale Day?",
        options=[0, 1],
        format_func=lambda x: "Yes (1)" if x == 1 else "No (0)",
        index=0
    )

    phone_verified = st.selectbox(
        "Phone Verified?",
        options=[1, 0],
        format_func=lambda x: "Yes (1)" if x == 1 else "No (0)",
        index=1
    )

    address_quality_score = st.number_input(
        "Address Quality Score (0 - 100)",
        min_value=0.0, max_value=100.0, value=72.0, step=1.0
    )

    pincode_risk_score = st.number_input(
        "Pincode Risk Score (0 - 100)",
        min_value=0.0, max_value=100.0, value=30.3, step=0.5
    )

    promised_delivery_days = st.number_input(
        "Promised Delivery Days",
        min_value=1, max_value=30, value=10, step=1
    )

    courier_partner = st.selectbox(
        "Courier Partner",
        options=["Delhivery", "Shadowfax", "India Post", "Xpressbees", "Ecom Express"],
        index=0
    )

    submit_button = st.form_submit_button("🔮 Predict RTO Risk")

if submit_button:
    payload = {
        "city_tier": city_tier,
        "payment_mode": payment_mode,
        "product_category": product_category,
        "customer_type": customer_type,
        "past_orders": int(past_orders),
        "past_rto_count": int(past_rto_count),
        "order_value_inr": float(order_value_inr),
        "discount_pct": float(discount_pct),
        "order_hour": int(order_hour),
        "is_sale_day": int(is_sale_day),
        "phone_verified": int(phone_verified),
        "address_quality_score": float(address_quality_score),
        "pincode_risk_score": float(pincode_risk_score),
        "promised_delivery_days": int(promised_delivery_days),
        "courier_partner": courier_partner
    }

    with st.spinner("Generating prediction..."):
        try:
            response = requests.post(
                BACKEND_URL,
                json=payload,
                timeout=30
            )

            if response.ok:
                result = response.json()

                if result.get("status") == "success":
                    target_val = result.get("predicted_class_target")
                    label = result.get("prediction_label", "Unknown")
                    prob = result.get("rto_probability")

                    if target_val == 1 or target_val == "1":
                        st.error(f"⚠️ High Risk: Order Likely to be **RTO** (Class: {target_val})")
                    else:
                        st.success(f"✅ Safe: Order Likely to be **Delivered** (Class: {target_val})")

                    if prob is not None:
                        st.info(f"📊 Probability of RTO: **{prob * 100:.2f}%**")
                else:
                    st.error(f"Unexpected response: {result}")
            else:
                st.error(
                    f"Backend returned HTTP {response.status_code}"
                )
                st.code(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to FastAPI. "
                "Check that the backend is running on port 8000."
            )

        except requests.exceptions.Timeout:
            st.error("The backend request timed out.")

        except requests.exceptions.RequestException as exc:
            st.error(f"Request failed: {exc}")

        except ValueError:
            st.error("The backend returned an invalid JSON response.")