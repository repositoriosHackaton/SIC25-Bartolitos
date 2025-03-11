from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  # Importar StaticFiles
import numpy as np
import pandas as pd
import joblib

app = FastAPI()

# Montar la carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="./public/static"), name="static")

# Configurar Jinja2 para las plantillas HTML
templates = Jinja2Templates(directory="./public/template")

# Cargar el modelo y el scaler
model = joblib.load("./public/modelo/O-IIA_OIIA.pkl")
scaler = joblib.load("./public/modelo/scaler.pkl")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": -1})

@app.post("/predict")
async def predict(
    season: int = Form(...),
    location: int = Form(...),
    cloud_cover: int = Form(...),
    temp: float = Form(...),
    humidity_porcent: float = Form(...),
    wind_speed: float = Form(...),
    precipitation: float = Form(...),
    pressure: float = Form(...),
    uv: float = Form(...),
    visibility: float = Form(...),
):
    # Crear un array con los datos del formulario
    data_array = np.array([
        temp,              # Temperature
        humidity_porcent,  # Humidity
        wind_speed,        # Wind Speed
        precipitation,     # Precipitation (%)
        cloud_cover,       # Cloud Cover
        pressure,          # Atmospheric Pressure
        uv,                # UV Index
        season,            # Season
        visibility,        # Visibility (km)
        location,          # Location
    ])

    # Convertir el array a un DataFrame con nombres de columnas
    df_predict = pd.DataFrame([data_array], columns=[
        "Temperature",
        "Humidity",
        "Wind Speed",
        "Precipitation (%)",
        "Cloud Cover",
        "Atmospheric Pressure",
        "UV Index",
        "Season",
        "Visibility (km)",
        "Location"
    ])

    # Escalar los datos de predicción usando el scaler ajustado
    df_scaled = scaler.transform(df_predict)

    # Hacer la predicción
    prediccion = model.predict(df_scaled)

    # Convertir el resultado de int64 a int
    result = int(prediccion[0])

    # Devolver una respuesta JSON con el resultado
    return JSONResponse(content={"result": result})