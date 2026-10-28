# CardioPredict

Predicción de riesgo de **enfermedad cardíaca** con una red neuronal **MLP**.

## Estructura

- `train_model.py`: entrena el modelo (Keras con PyTorch como backend) y guarda la curva de aprendizaje.
- `modelo_corazon.keras` y `scaler.pkl`: modelo entrenado y escalador de datos.
- `main.py`: API en **FastAPI** que recibe los datos del paciente y devuelve la predicción.
- `frontend/`: página web para ingresar los datos y ver el resultado.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Luego abrir `frontend/index.html` en el navegador.
