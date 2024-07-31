import flask
from flask.json import jsonify
import functions_framework
from google.cloud import firestore
from google.oauth2 import service_account
import os
from uuid import uuid4


PROJECT_NAME = os.getenv("PROJECT_NAME", "DEFAULT")
DATABASE_NAME = os.getenv("DATABASE_NAME", "DEFAULT")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "DEFAULT")

creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
credentials = service_account.Credentials.from_service_account_file(creds)


class Resumes:
    def __init__(self, project, db_name) -> None:
        self.db = firestore.Client(
            project=project, database=db_name, credentials=credentials
        )

    def random_uuid(self):
        """
        return str: random UUID
        """
        return str(uuid4())

    def valid_json(self, request: flask.Request):
        return request.content_type == "application/json"

    def add_document(self, data):
        """
        return bool: True if successful upload. False if an issue
        """

        document_id = self.random_uuid()

        try:
            self.db.collection(COLLECTION_NAME).document(document_id).set(data)
            return True
        except:
            return False

    def get_resumes(self):
        """
        return list: of resume data
        """

        try:
            resumes = self.db.collection(COLLECTION_NAME).stream()
            resume_data = [doc.to_dict() for doc in resumes]

            return flask.jsonify(resume_data), 200

        except:
            return flask.jsonify({"error": "no resumes found"}), 404


try:
    resumes = Resumes(project=PROJECT_NAME, db_name=DATABASE_NAME)
except:
    pass


@functions_framework.http
def http_handler(request: flask.Request) -> flask.typing.ResponseReturnValue:

    match request.method:
        case "GET":
            data = resumes.get_resumes()
            return data
            # return flask.jsonify({"status": "OK"}), 200

        case "POST":
            # fail immediately if the content type is not json
            if not resumes.valid_json(request):
                return (
                    flask.jsonify({"error": "content type must be application/json"}),
                    406,
                )

            data = request.get_json()
            if resumes.add_document(data):
                return (
                    flask.jsonify({"success": "resume added into the collection"}),
                    200,
                )
            else:
                return (
                    flask.jsonify({"error": "unable to add resume to the collection."}),
                    401,
                )

        case _:
            # default catch all
            return flask.jsonify({"error": "client error"}), 400
