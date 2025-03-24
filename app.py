from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import joblib
import io
import os

app = FastAPI()

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load models with more robust error handling
binary_model = None
multi_class_model = None

try:
    model_dir = "D:/capstone/final/models/"
    binary_model = joblib.load(os.path.join(model_dir, "logistic_regressor_binary.pkl"))
    multi_class_model = joblib.load(os.path.join(model_dir, "random_forest_multi.pkl"))
    print("Models loaded successfully")
except Exception as e:
    print(f"Error loading models: {e}")
    print("The API will run but predictions will not work until models are properly loaded")

@app.get("/")
async def home():
    return {"message": "API is running! Use /predict to make predictions."}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
        
        # Data preprocessing
        # Remove 'label' column if it exists
        if "label" in df.columns:
            df = df.drop(columns=["label"])
            
        # Convert categorical columns to numbers
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = pd.factorize(df[col])[0]
        
        # Handle missing values
        df = df.fillna(0)
        
        # Check if models are loaded
        if binary_model is None or multi_class_model is None:
            return {"error": "Models not loaded properly. Check server logs."}
            
        # Make predictions
        prediction_binary = binary_model.predict(df).tolist()
        prediction_multi = multi_class_model.predict(df).tolist()
        
        # Get prediction probabilities if available
        binary_proba = []
        multi_proba = []
        
        try:
            if hasattr(binary_model, 'predict_proba'):
                binary_proba = binary_model.predict_proba(df).tolist()
            
            if hasattr(multi_class_model, 'predict_proba'):
                multi_proba = multi_class_model.predict_proba(df).tolist()
        except Exception as e:
            print(f"Could not get prediction probabilities: {e}")
        
        return {
            "binary_prediction": prediction_binary,
            "multi_class_prediction": prediction_multi,
            "binary_probabilities": binary_proba,
            "multi_probabilities": multi_proba
        }
    except Exception as e:
        return {"error": str(e)}