import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Configurar Keras para usar PyTorch como backend
import os
os.environ['KERAS_BACKEND'] = 'torch'
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

print("=== Predicción de Enfermedad Cardíaca con Keras MLP ===")

# 1. Cargar el dataset (Cleveland)
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
columns = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
           "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]

print("Descargando y procesando el dataset...")
df = pd.read_csv(url, names=columns, na_values="?")

# Eliminar filas con valores nulos
df = df.dropna()

# Binarizar el target (0 = sano, >0 = enfermo)
df['target'] = df['target'].apply(lambda x: 1 if x > 0 else 0)

print(f"Dimensiones del dataset después de limpieza: {df.shape}")

# Análisis de Balance de Clases
conteos = df['target'].value_counts(normalize=True) * 100
print("\n--- Balance de Clases ---")
print(f"Sanos (0): {conteos[0]:.2f}%")
print(f"Enfermos (1): {conteos[1]:.2f}%")
print("-> El dataset está balanceado, no se requiere oversampling.\n")

# Separar características (X) y objetivo (y)
X = df.drop("target", axis=1).values
y = df["target"].values

# Dividir en entrenamiento y prueba (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Estandarización de los datos (Z-score normalization)
# Centra los datos en 0 (media) con varianza 1 para optimizar retropropagación.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, 'scaler.pkl')
print("Escalador guardado como 'scaler.pkl'")

# 3. Diseño de la Arquitectura de la Red Neuronal Densa (Keras MLP)
model = Sequential([
    Dense(16, input_dim=13, activation='relu', name="Capa_Oculta_1"),
    Dropout(0.2, name="Regularizacion_Dropout"),
    Dense(8, activation='relu', name="Capa_Oculta_2"),
    Dense(1, activation='sigmoid', name="Capa_Salida")
])

print("\n--- Resumen Arquitectónico (Teórico vs Computacional) ---")
model.summary()

# 4. Compilación del Modelo
# binary_crossentropy: ideal para clasificaciones binarias con Sigmoid.
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# 5. Entrenamiento
print("\nIniciando entrenamiento con TensorFlow/Keras...")
history = model.fit(
    X_train_scaled, y_train,
    validation_split=0.2, # Conjunto de validación explícito
    epochs=100,
    batch_size=16,
    verbose=0
)

# 6. Evaluación final
loss, accuracy = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"\n--- Resultados Finales ---")
print(f"Pérdida (Loss) en Prueba: {loss:.4f}")
print(f"Precisión (Accuracy) en Prueba: {accuracy*100:.2f}%")

# Guardar el modelo en formato Keras
model.save("modelo_corazon.keras")
print("Modelo guardado como 'modelo_corazon.keras'")

# 7. Generar Curvas de Aprendizaje y Diagnóstico
plt.figure(figsize=(12, 5))

# Gráfica de Loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Entrenamiento')
plt.plot(history.history['val_loss'], label='Validación')
plt.title('Función de Pérdida (Loss)')
plt.xlabel('Época')
plt.ylabel('Pérdida')
plt.legend()

# Gráfica de Accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Entrenamiento')
plt.plot(history.history['val_accuracy'], label='Validación')
plt.title('Métrica de Precisión (Accuracy)')
plt.xlabel('Época')
plt.ylabel('Precisión')
plt.legend()

plt.tight_layout()
plt.savefig("curvas_aprendizaje.png")
print("Gráficas guardadas como 'curvas_aprendizaje.png'")
