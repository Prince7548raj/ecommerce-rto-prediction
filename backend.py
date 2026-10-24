from pathlib import Path
import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="E-Commerce RTO Prediction API")

# Model path resolve karein
MODEL_PATH = Path(__file__).resolve().parent / "my_model.pkl"

with MODEL_PATH.open("rb") as file:
    loaded_model = pickle.load(file)


class Data(BaseModel):
    city_tier: str
    payment_mode: str
    product_category: str
    customer_type: str
    past_orders: int
    past_rto_count: int
    order_value_inr: float
    discount_pct: float
    order_hour: int
    is_sale_day: int
    phone_verified: int
    address_quality_score: float
    pincode_risk_score: float
    promised_delivery_days: int
    courier_partner: str


@app.post("/predict")
def pred(data: Data):
    input_dict = data.model_dump()

    input_df = pd.DataFrame([input_dict])

    prediction = loaded_model.predict(input_df)
    predicted_value = prediction[0]

    # Predict probability agar model support karta ho
    predicted_proba = None
    if hasattr(loaded_model, "predict_proba"):
        probabilities = loaded_model.predict_proba(input_df)[0]
        predicted_proba = round(float(probabilities[1]), 4)

    if hasattr(predicted_value, "item"):
        predicted_value = predicted_value.item()

    if not isinstance(predicted_value, (int, float, str, bool, type(None))):
        predicted_value = str(predicted_value)

    result_label = "RTO" if predicted_value == 1 else "Delivered"

    return {
        "status": "success",
        "predicted_class_target": predicted_value,
        "prediction_label": result_label,
        "rto_probability": predicted_proba
    }


@app.get("/")
def read_root():
    return {"message": "E-Commerce RTO Prediction API is running"}


@app.get("/Home")
def get_home():
    return {"Message": "This is the home page"}