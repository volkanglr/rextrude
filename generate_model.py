import requests
import os
import time
from dotenv import load_dotenv

#Starts an Image-to-3D task with meshy and provides the task-id.

load_dotenv()
API_KEY= os.getenv("MESHY_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

payload = {
    "image_url": "https://picsum.photos/512",
    "target_formats": ["glb"],
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/image-to-3d",
    headers=headers,
    json=payload
)

print("Status code:", response.status_code)

if 200 <= response.status_code < 300:
    task_id = response.json()["result"]
    print("Task started. task_id:", task_id)

    status_url = f"https://api.meshy.ai/openapi/v1/image-to-3d/{task_id}"

    while True:
        status_response= requests.get(status_url, headers=headers)
        task = status_response.json()
        status = task["status"]
        progress = task.get("progress", 0)
        print(f" Status: {status} ({progress}%)")

        if status == "SUCCEEDED":
            glb_url = task["model_urls"]["glb"]
            print("Download-URL:", glb_url)
            model_response = requests.get(glb_url)
            model_response.raise_for_status
            with open("model.glb", "wb") as file:
                file.write(model_response.content)

            print("Saved as model.glb")
            break
        if status == "FAILED":
            print("Generation failed.")
            break

        time.sleep(5)         #Checking repeatedly for the generation status

    
else:
    print("Something went wrong. Answer from server:")
    print(response.text)