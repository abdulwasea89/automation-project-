import os
from google.cloud import firestore, storage
from google.auth.exceptions import DefaultCredentialsError
from dotenv import load_dotenv

load_dotenv()
# Forcefully set the correct path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/abdulwasea/Documents/Abdul/projects/automation-project-/automation/service-account.json"


def test_firestore_connection(project_id: str):
    try:
        db = firestore.Client(project=project_id)
        test_doc_ref = db.collection("test-connection").document("ping")
        test_doc_ref.set({"status": "ok"})
        print("[✅] Firestore write successful.")
    except Exception as e:
        print(f"[❌] Firestore connection failed: {e}")

def test_storage_connection(project_id: str, bucket_name: str):
    try:
        client = storage.Client(project=project_id)
        bucket = client.bucket(bucket_name)
        blobs = list(bucket.list_blobs())
        print(f"[✅] Storage access successful. Found {len(blobs)} files in bucket '{bucket_name}'.")
    except Exception as e:
        print(f"[❌] Cloud Storage connection failed: {e}")

if __name__ == "__main__":
    project_id = os.getenv("GCP_PROJECT_ID", "ai-chatbot-463111")
    bucket_name = os.getenv("GCP_BUCKET_NAME", "zoko-ai-media")

    print(f"🔍 Testing GCP services with project ID: {project_id}")

    # Optional: log credentials path
    creds_path = "/home/abdulwasea/Documents/Abdul/projects/automation-project-/automation/service-account.json"
    if creds_path and os.path.exists(creds_path):
        print(f"[🔐] Using credentials from: {creds_path}")
    else:
        print("[⚠️] GOOGLE_APPLICATION_CREDENTIALS not set or file does not exist. Using default application credentials.")

    # Run tests
    test_firestore_connection(project_id)
    test_storage_connection(project_id, bucket_name)
