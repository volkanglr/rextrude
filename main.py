import os
import fal_client
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File

load_dotenv()
API_KEY= os.getenv("MESHY_API_KEY")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Rextrude server is running."}

@app.post("/generate")
def generate_model(image: UploadFile = File(...)):
    image_bytes = image.file.read()
    image_url = fal_client.upload(image_bytes, image.content_type)

    result = fal_client.subscribe("fal-ai/trellis", arguments={"image_url": image_url},)

    return {"model_url": result["model_mesh"]["url"]}
    