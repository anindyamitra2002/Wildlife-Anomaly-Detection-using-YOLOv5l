from location_generator import *
from load_data import load_data
from model import *
from notification import *
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import os
import shutil



app = FastAPI(debug=True)
templates = Jinja2Templates(directory="./")


app.mount("/img", StaticFiles(directory="static/img"), name="img")  # Serve static files
app.mount("/css", StaticFiles(directory="static/css"), name="css")  # Serve static files
app.mount("/lib", StaticFiles(directory="static/lib"), name="lib")  # Serve static files
app.mount("/lib", StaticFiles(directory="static/lib/lightbox"), name="lib_lightbox")  # Serve static files
app.mount("/js", StaticFiles(directory="static/js"), name="js")  # Serve static files
app.mount("/temp", StaticFiles(directory="static/temp"), name="temp")  # Serve static files
app.mount("/out", StaticFiles(directory="static/out"), name="out")  # Serve static files



given_lat = 22.606803
given_lon = 85.338173

max_distance_km = 20

@app.get("/", response_class=HTMLResponse)
async def get_upload_page():
    request = {
        "title": "index"
    }
    return templates.TemplateResponse("static/index.html", {"request": request})


@app.get("/{title}")
async def get_upload_page(title: str):
    title = title.split('.')[0]
    request = {
        "title": {title}
    }
    return templates.TemplateResponse(f"static/{title}.html", {"request": request})


@app.post("/upload/")
async def Predict_video(video: UploadFile = File(...), selected_class: str = Form(...), getAlert: bool = Form(False)):
    
    temp_video_path = f"/temp/{video.filename}"
    os.makedirs("static/temp", exist_ok=True)
    with open(f'static/{temp_video_path}', "wb") as f:
        shutil.copyfileobj(video.file, f)

    # result = load_data()
    # predicted_video_path = '/out/output_video.webm'

    result, predicted_video_path = predictVideo(temp_video_path, selected_class)

    updated_result = add_random_location(result, given_lat, given_lon, max_distance_km)
    print(getAlert)

    if getAlert:
        sendAlert(updated_result)

    return JSONResponse(content={"video_data_uri": temp_video_path, "predicted_video_url": predicted_video_path, "results": updated_result})
