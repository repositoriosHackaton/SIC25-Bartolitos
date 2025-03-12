from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
from PIL import Image
import io

app = FastAPI()

# Montar la carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="./public/static"), name="static")

# Configurar Jinja2 para las plantillas HTML
templates = Jinja2Templates(directory="./public/template")

# Cargar los modelos
model = joblib.load("./public/modelo/O-IIA_OIIA.pkl")
scaler = joblib.load("./public/modelo/scaler.pkl")
image_model = load_model("./public/modelo_img/mejor_modelo_clima_v2.h5")

#cargar el main hud
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": -1})

#predecccion mediante formulario
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

#prediccion mediante imagen
@app.post("/predict_image")
async def predict_image(image: UploadFile = File(...)):
    # Leer la imagen
    contents = await image.read()
    img = Image.open(io.BytesIO(contents))
    
    # Preprocesar la imagen
    img = img.resize((224, 224))  # Ajustar al tamaño que espera el modelo
    img_array = np.array(img)
    img_array = img_array / 255.0  # Normalizar
    img_array = np.expand_dims(img_array, axis=0)  # Agregar dimensión de batch
    
    # Hacer la predicción
    prediccion = image_model.predict(img_array)
    result = int(np.argmax(prediccion[0]))
    
    # Devolver una respuesta JSON con el resultado
    return JSONResponse(content={"result": result})