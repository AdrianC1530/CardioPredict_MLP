document.getElementById('predict-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // UI Elements
    const formCard = document.querySelector('.form-card');
    const resultCard = document.getElementById('result-card');
    const submitBtn = document.getElementById('submit-btn');
    const loader = document.getElementById('loader');
    const btnText = submitBtn.querySelector('span');

    // Muestra estado de carga
    submitBtn.disabled = true;
    btnText.textContent = 'Analizando...';
    loader.style.display = 'block';

    // Recolectar datos del formulario
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    // Convertir todos los valores a números
    for (let key in data) {
        data[key] = Number(data[key]);
    }

    try {
        // Enviar datos a la API (FastAPI backend asume puerto 8000)
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Error en el servidor API');
        }

        const result = await response.json();
        
        // Simular un pequeño retardo para la animación (UX)
        setTimeout(() => {
            mostrarResultados(result, formCard, resultCard);
            
            // Restaurar botón
            submitBtn.disabled = false;
            btnText.textContent = 'Analizar Paciente';
            loader.style.display = 'none';
        }, 800);

    } catch (error) {
        alert("Error al conectar con la API. Asegúrate de que el backend esté corriendo en http://localhost:8000.\nDetalle: " + error.message);
        submitBtn.disabled = false;
        btnText.textContent = 'Analizar Paciente';
        loader.style.display = 'none';
    }
});

function mostrarResultados(result, formCard, resultCard) {
    // Ocultar form, mostrar resultados
    formCard.classList.add('hidden');
    resultCard.classList.remove('hidden');

    const diagElement = document.getElementById('diagnosis');
    const probFill = document.getElementById('progress-bar');
    const probText = document.getElementById('prob-text');

    const probPercentage = (result.probability * 100).toFixed(1);

    // Resetear UI
    diagElement.className = 'diagnosis';
    
    if (result.prediction === 1) {
        diagElement.textContent = result.diagnosis;
        diagElement.classList.add('positive');
        probFill.style.backgroundColor = 'var(--accent)';
    } else {
        diagElement.textContent = result.diagnosis;
        diagElement.classList.add('negative');
        probFill.style.backgroundColor = 'var(--safe)';
    }

    // Animar barra de progreso
    setTimeout(() => {
        probFill.style.width = `${probPercentage}%`;
        
        // Animar números (Contador)
        let currentProb = 0;
        const interval = setInterval(() => {
            currentProb += 1.5;
            if (currentProb >= probPercentage) {
                currentProb = probPercentage;
                clearInterval(interval);
            }
            probText.textContent = `${currentProb.toFixed(1)}%`;
        }, 20);

    }, 100);
}

document.getElementById('reset-btn').addEventListener('click', () => {
    document.querySelector('.form-card').classList.remove('hidden');
    document.getElementById('result-card').classList.add('hidden');
    document.getElementById('progress-bar').style.width = '0%';
    document.getElementById('prob-text').textContent = '0%';
});

// Auto-fill para pruebas rápidas
window.addEventListener('keydown', (e) => {
    // Presiona Ctrl+Shift+S para auto-llenar con un caso Sano
    if (e.ctrlKey && e.shiftKey && e.key === 'S') {
        document.getElementById('age').value = 45;
        document.getElementById('sex').value = 0;
        document.getElementById('cp').value = 2;
        document.getElementById('trestbps').value = 110;
        document.getElementById('chol').value = 220;
        document.getElementById('fbs').value = 0;
        document.getElementById('restecg').value = 0;
        document.getElementById('thalach').value = 160;
        document.getElementById('exang').value = 0;
        document.getElementById('oldpeak').value = 0;
        document.getElementById('slope').value = 1;
        document.getElementById('ca').value = 0;
        document.getElementById('thal').value = 3;
    }
    // Presiona Ctrl+Shift+E para auto-llenar con un caso Enfermo
    if (e.ctrlKey && e.shiftKey && e.key === 'E') {
        document.getElementById('age').value = 65;
        document.getElementById('sex').value = 1;
        document.getElementById('cp').value = 4;
        document.getElementById('trestbps').value = 150;
        document.getElementById('chol').value = 290;
        document.getElementById('fbs').value = 1;
        document.getElementById('restecg').value = 2;
        document.getElementById('thalach').value = 120;
        document.getElementById('exang').value = 1;
        document.getElementById('oldpeak').value = 2.5;
        document.getElementById('slope').value = 2;
        document.getElementById('ca').value = 2;
        document.getElementById('thal').value = 7;
    }
});
