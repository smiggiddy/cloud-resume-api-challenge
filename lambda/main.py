from base64 import b64decode
import functions_framework
from google.auth.environment_vars import CREDENTIALS
from google.cloud import firestore
from json import loads
import os
from uuid import uuid4
from google.oauth2 import service_account


PROJECT_NAME = os.getenv("PROJECT_NAME", "DEFAULT")
DATABASE_NAME = os.getenv("DATABASE_NAME", "DEFAULT")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "DEFAULT")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "NONE")

json_acct_info = loads(b64decode(GOOGLE_APPLICATION_CREDENTIALS))
credentials = service_account.Credentials.from_service_account_info(json_acct_info)

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
