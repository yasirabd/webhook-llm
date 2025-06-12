import os
import time
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def upload_dataset(file_path):
    with open(file_path, "rb") as f:
        response = client.files.create(
            file=f,
            purpose="fine-tune"
        )
    print("File uploaded:", response.id)
    return response.id

def start_fine_tune(training_file_id, base_model="gpt-4o-mini-2024-07-18"):
    response = client.fine_tuning.jobs.create(
        training_file=training_file_id,
        model=base_model,
        # method={
        #     "type": "supervised",
        #     "supervised": {
        #         "hyperparameters": {"n_epochs": 2},
        #     },
        # },
    )
    print("Fine-tune job started:", response.id)
    return response.id

def wait_finetune(job_id):
    while True:
        status = client.fine_tuning.jobs.retrieve(job_id).status
        print(f"Status: {status}")
        if status in ["succeeded", "failed", "cancelled"]:
            break
        time.sleep(30)

if __name__ == "__main__":
    file_path = "finetune/data/conversations.jsonl"
    # uploaded_file_id = upload_dataset(file_path)
    # start_fine_tune(uploaded_file_id)
    wait_finetune("ftjob-0vT4vMwZEVRvhY6CF1rR4Q6R")