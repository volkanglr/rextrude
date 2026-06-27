import requests
import os
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
else:
    print("Something went wrong. Answer from server:")
    print(response.text)