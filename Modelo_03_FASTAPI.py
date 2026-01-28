from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pickle
import numpy as np
import pandas as pd

# Cargar el modelo y el scaler desde los archivos .pkl
with open('pipeline_malware.pkl', 'rb') as archivo_modelo:
    modelo = pickle.load(archivo_modelo)

#with open('scaler.pkl', 'rb') as archivo_scaler:
#    scaler = pickle.load(archivo_scaler)

# Definir las características esperadas
columnas = [
            'Flow Duration','Total Fwd Packets','Total Backward Packets',
            'Total Length of Fwd Packets','Fwd Packet Length Max','Fwd Packet Length Min',
            'Fwd Packet Length Mean','Flow Bytes/s','Flow Packets/s','Flow IAT Mean',
            'Fwd IAT Total','Bwd IAT Total','Active Mean','Idle Mean'
            ]

# Crear la aplicación FastAPI
app = FastAPI(title="Detección de Malware")

# Definir el modelo de datos de entrada utilizando Pydantic
class Malware(BaseModel):
    flow_duration: float = Field(alias="Flow Duration")
    total_fwd_packets: float = Field(alias="Total Fwd Packets")
    total_bwd_packets: float = Field(alias="Total Backward Packets")
    total_len_fwd: float = Field(alias="Total Length of Fwd Packets")
    fwd_max: float = Field(alias="Fwd Packet Length Max")
    fwd_min: float = Field(alias="Fwd Packet Length Min")
    fwd_mean: float = Field(alias="Fwd Packet Length Mean")
    flow_bytes_s: float = Field(alias="Flow Bytes/s")
    flow_pkts_s: float = Field(alias="Flow Packets/s")
    flow_iat_mean: float = Field(alias="Flow IAT Mean")
    fwd_iat_total: float = Field(alias="Fwd IAT Total")
    bwd_iat_total: float = Field(alias="Bwd IAT Total")
    active_mean: float = Field(alias="Active Mean")
    idle_mean: float = Field(alias="Idle Mean")
    
# Definir el endpoint para predicción
@app.post("/prediccion/")
async def predecir_malware(deteccion: Malware):
    try:
        # Convertir la entrada en un DataFrame
        datos_entrada = pd.DataFrame([deteccion.dict(by_alias=True)], columns=columnas)
        
        # Escalar las características
        #datos_entrada_scaled = scaler.transform(datos_entrada)
         # Asegurar orden correcto de columnas
        datos_entrada = datos_entrada[columnas]

        # Realizar la predicción
        prediccion = modelo.predict(datos_entrada) # cambio
        probabilidad = modelo.predict_proba(datos_entrada)[:, 1] #cambio
        
        # Construir la respuesta
        resultado = {
            "EsMalware": bool(prediccion[0]),
            "ProbabilidadMalware": float(probabilidad[0])
        }
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))