import functions_framework
from google.auth.environment_vars import CREDENTIALS
from google.cloud import firestore
import os
from uuid import uuid4
import google.auth

credentials, project = google.auth.default()

PROJECT_NAME = os.getenv("PROJECT_NAME", "DEFAULT")
DATABASE_NAME = os.getenv("DATABASE_NAME", "DEFAULT")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "DEFAULT")

db = firestore.Client(
    project=PROJECT_NAME, database=DATABASE_NAME, credentials=credentials
)


def random_uuid():
    """
    return str: random UUID
    """
    return str(uuid4())


def add_document(data):
    """
    return bool: True if successful upload. False if an issue
    """

    document_id = random_uuid()

    try:
        db.collection(COLLECTION_NAME).document(document_id).set(data)
        return True
    except:
        return False


@functions_framework.http
def http_handler(request):

    # Return an HTTP response
    return "OK"
