📦 E-Commerce RTO Prediction App

An end-to-end machine learning application that predicts whether an e-commerce order will result in RTO (Return to Origin), so sellers can flag high-risk orders (especially COD) before shipping.

The model is served through a FastAPI backend, consumed by a Streamlit frontend, containerized with Docker Compose, and deployed on AWS EC2.

🔗 Live Demo: http://3.25.224.111:8501

🎯 Problem Statement

In Indian e-commerce, a large share of orders (especially Cash on Delivery) get returned to the seller undelivered. Every RTO costs forward and reverse shipping, packaging, and lost inventory time. This project predicts the probability of RTO for an order using order, customer, and delivery details.

✨ Features
Predicts RTO / Not RTO along with the RTO probability (%)
Inputs: City Tier, Payment Mode, Product Category, Pincode Risk Score, Promised Delivery Days, Courier Partner, and other order details
REST API with auto-generated Swagger docs (/docs)
Simple, interactive web UI built with Streamlit
One-command setup with Docker Compose
Deployed on AWS EC2

🛠️ Tech Stack
Layer	Technology
ML Model	Python, scikit-learn (Logistic Regression with Pipeline), pandas, NumPy
Backend	FastAPI, Uvicorn, Pydantic
Frontend	Streamlit, Requests
Containerization	Docker, Docker Compose
Deployment	AWS EC2 (Ubuntu)
Version Control	Git, GitHub
🏗️ Architecture
User (Browser)
      │
      ▼
Streamlit Frontend  (port 8501)
      │   HTTP POST /predict
      ▼
FastAPI Backend     (port 8000)
      │
      ▼
Trained Model (my_model.pkl)  →  RTO prediction + probability

Both services run as separate containers and talk to each other over the Docker Compose network.

📁 Project Structure
ecommerce-rto-prediction/
├── backend.py            # FastAPI app: loads model, exposes /predict
├── frontend.py           # Streamlit UI
├── my_model.pkl          # Trained model pipeline
├── notebook.ipynb        # Data cleaning, EDA, model training
├── requirements.txt      # Python dependencies
├── Dockerfile.backend    # Backend image
├── Dockerfile.frontend   # Frontend image
├── docker-compose.yml    # Runs both services together
└── README.md
🚀 Run Locally

Prerequisites: Docker Desktop installed and running.

bash
# 1. Clone the repository
git clone https://github.com/Prince7548raj/ecommerce-rto-prediction.git
cd ecommerce-rto-prediction

# 2. Build and start both services
docker compose up --build

Then open:

Frontend: http://localhost:8501
API docs (Swagger): http://localhost:8000/docs

To stop the app:

bash
docker compose down
☁️ Deployment on AWS EC2
Launch an Ubuntu EC2 instance (t3.micro)
Open inbound ports 22 (SSH) and 8501 (Streamlit) in the security group
Install Docker and Docker Compose on the instance
Clone this repo and run:
bash
sudo docker compose up -d --build
Access the app at http://<EC2-PUBLIC-IP>:8501


👤 Author

Prince Raj GitHub: @Prince7548raj
