
# Despliegue de Modelo de ML a través de API

Este proyecto tiene como objetivo desarrollar y desplegar un modelo de Machine Learning en la nube, exponiéndolo a través de una API REST utilizando FastAPI y Uvicorn.

El modelo fue entrenado previamente en Python, evaluado mediante una métrica explícita y exportado como archivo .pkl, el cual es cargado al iniciar la aplicación para realizar predicciones sin reentrenamiento.

La solución implementa un flujo completo de operacionalización de Data Science en un entorno Cloud real:

Dataset → Modelo ML → Exportación .pkl → API FastAPI → GitHub → Deploy Cloud → API LIVE


#Descripción del Objetivo del modelo 

📌 Descripción general

    Este proyecto implementa un modelo de Machine Learning para la detección de malware a partir de métricas de tráfico de red. El objetivo es clasificar flujos de red como benignos o maliciosos (o entre múltiples clases) utilizando técnicas de preprocesamiento, reducción de dimensionalidad y un clasificador robusto basado en Random Forest.

    El flujo completo está encapsulado en un pipeline de Scikit-learn, lo que garantiza consistencia entre entrenamiento, evaluación y uso en producción.

🎯 Objetivo del modelo

    Detectar comportamiento malicioso en tráfico de red mediante:

    Análisis de métricas estadísticas de flujos (duración, bytes, paquetes, tiempos de inter-arribo, actividad e inactividad).

    Aprendizaje supervisado sobre la variable objetivo Class.

    Evaluación con métricas estándar de clasificación y curvas ROC.

    Persistencia del modelo entrenado para reutilización.

🧠 Enfoque de Machine Learning

    El modelo sigue el siguiente pipeline:

    Imputación de valores faltantes

    Reemplaza valores NaN (incluidos infinitos) usando la media de cada variable.

    Estandarización

    Normaliza las variables numéricas (media 0, desviación estándar 1).

    Reducción de dimensionalidad (PCA)

    Conserva el 95% de la varianza explicada, reduciendo ruido y correlación entre variables.

    Clasificación

    Se utiliza un RandomForestClassifier con:

    100 árboles

    Balanceo automático de clases

    Semilla fija para reproducibilidad


📊 Variables utilizadas

    El modelo trabaja exclusivamente con variables numéricas de tráfico de red, tales como:

    Duración del flujo

    Paquetes y bytes por segundo

    Métricas de paquetes forward y backward

    Tiempos de inter-arribo (IAT)

    Periodos activos e inactivos del flujo

    La variable objetivo es:

    Class → tipo de tráfico 'benign' 'adware' 'malware'


🧪 Evaluación del modelo

    El dataset se divide en:

        75% entrenamiento

        25% prueba, manteniendo la proporción de clases (stratified split)

    Se calculan las siguientes métricas:

        Accuracy

        Precision (weighted)

        F1-Score (weighted)

        ROC-AUC

        Binario: curva ROC clásica

        Multiclase: One-Vs-Rest (OvR)

    Además, se generan:

        Matriz de confusión

        Curva ROC


Estructura del proyecto

    ├── dataset_malware.csv
    ├── modelo_deteccion_malware.py
    ├── pipeline_malware.pkl
    ├── README.md
## Requisitos de Entorno

⚙️ Requisitos del entorno

Python 3.10.x - testeado

pip 

Sistema operativo: Windows
## Instrucciones para Correr API Localmente

1.- Clonar el repositorio Localmente con (la dirección depende de tu repositorio en github)
 
    git clone https://github.com/USUARIO/NOMBRE_REPOSITORIO.git 

2.- Ubicar la máquina en el repositorio clonado para trabajar en ese entorno con el comando (la dirección dependerá de dónde quieres clonar tu github)

    cd C:\Users\Downloads\Taller_cloud_2026

3.- Crear y activar un entorno virtual 

    python -m venv venv
    venv\Scripts\activate

4.- Instalar dependencias (demora unos minutos)

    pip install -r requirements.txt

5.- Ejecutar la API con Uvicorn (asegurar que Uvicorn está instalado en la misma terminal)

    python -m pip install fastapi "uvicorn[standard]"

6.- Verificar que FastAPI quedó instalado
    
    python -m pip show fastapi

7.- Correr el modelo desde la termina con el comando 

    uvicorn Modelo_03_FASTAPI:app --reload --reload-dir 

8.- Para detener la API presionar las teclas (en la terminal)

    ctrl + C
## Ejemplo del request al endpoint / predict

END POINT

    POST /predict/

Request: Este endpoint recibe un JSON con las siguientes features numéricas

    { "Flow Duration": 0.40378,
    "Total Fwd Packets": 0.7865,
    "Total Backward Packets": 0.654,
    "Total Length of Fwd Packets": 0.8760,
    "Fwd Packet Length Max": 01429,
    "Fwd Packet Length Min": 0.635,
    "Fwd Packet Length Mean": 0.89252,
    "Flow Bytes/s": 0.5091,
    "Flow Packets/s": 0.981,
    "Flow IAT Mean": 0.2312,
    "Fwd IAT Total": 0.534,
    "Bwd IAT Total": 1.0,
    "Active Mean": 0.4123,
    "Idle Mean": 0.098
    }   
 

Response (JSON de salida)

    {
    "EsMalware": true,
    "ProbabilidadMalware": 0.8734
    }

## Plataforma Cloud usada para el deploy


La API fue desplegada utilizando la plataforma **Render**, 
empleando un runtime de Python y un archivo Procfile para la ejecución 
del servidor Uvicorn. La aplicación se encuentra disponible mediante 
una URL pública proporcionada por la plataforma.


https://taller-cloud-2026.onrender.com/docs