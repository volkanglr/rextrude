import requests
import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
API_KEY= os.getenv("MESHY_API_KEY")

app = FastAPI()

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

@app.get("/")
def read_root():
    return {"message": "Rextrude server is running."}

@app.post("/generate")
def generate_model():
    payload = {
        "image_url": "https://picsum.photos/512",
        "target_formats": ["glb"],
    }

    response = requests.post(
        "https://api.meshy.ai/openapi/v1/image-to-3d",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    task_id = response.json()["result"]
    status_url = f"https://api.meshy.ai/openapi/v1/image-to-3d/{task_id}"
    while True:
        status_response= requests.get(status_url, headers=headers)
        task = status_response.json()
        status = task["status"]

        if status == "SUCCEEDED":
            glb_url = task["model_urls"]["glb"]
            return {"model_url": glb_url}
         
        if status == "FAILED":
            return {"error": "Generation failed"}
            
        time.sleep(5)         #Checking repeatedly for the generation status