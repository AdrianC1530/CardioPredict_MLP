from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib
import os
os.environ['KERAS_BACKEND'] = 'torch'
import keras
app = FastAPI(title="Predicción de Enfermedad Cardíaca API")

# Habilitar CORS para que el frontend pueda comunicarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo y escalador al iniciar la aplicación
try:
    model = keras.saving.load_model("modelo_corazon.keras")
    scaler = joblib.load("scaler.pkl")
    print("Modelo y escalador cargados correctamente.")
except Exception as e:
    print(f"Advertencia: No se pudo cargar el modelo o escalador. Entrena el modelo primero. ({e})")

# Modelo de datos de entrada esperado
class PatientData(BaseModel):
    age: float
    sex: float
    cp: float
    trestbps: float
    chol: float
    fbs: float
    restecg: float
    thalach: float
    exang: float
    oldpeak: float
    slope: float
    ca: float
    thal: float

@app.get("/")
def read_root():
    return {"message": "API de Predicción de Enfermedad Cardíaca en línea."}

@app.post("/predict")
def predict_heart_disease(data: PatientData):
    try:
        # Extraer los datos en el orden correcto
        features = np.array([[
            data.age, data.sex, data.cp, data.trestbps, data.chol, data.fbs,
            data.restecg, data.thalach, data.exang, data.oldpeak, data.slope,
            data.ca, data.thal
        ]])
        
        # Escalar los datos usando el scaler entrenado
        features_scaled = scaler.transform(features)
        
        # Realizar la predicción
        prediction_prob = float(model.predict(features_scaled, verbose=0)[0][0])
        
        # Umbral de 0.5 para la clasificación binaria
        has_disease = bool(prediction_prob > 0.5)
        
        return {
            "prediction": 1 if has_disease else 0,
            "probability": float(prediction_prob),
            "diagnosis": "Positivo para Enfermedad Cardíaca" if has_disease else "Negativo (Sano)"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Para ejecutar: uvicorn main:app --reload
