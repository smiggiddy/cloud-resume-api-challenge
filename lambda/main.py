import flask
import functions_framework
from google.cloud import firestore
import os
from uuid import uuid4


PROJECT_NAME = os.getenv("PROJECT_NAME", "DEFAULT")
DATABASE_NAME = os.getenv("DATABASE_NAME", "DEFAULT")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "DEFAULT")


class Resumes:
    def __init__(self, project, db_name) -> None:
        self.db = firestore.Client(project=project, database=db_name)

    def random_uuid(self):
        """
        return str: random UUID
        """
        return str(uuid4())

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

            return flask.jsonify(resumes), 200

        except:
            return flask.jsonify({"error": "no resumes found"}), 404


try:
    resumes = Resumes(project=PROJECT_NAME, db_name=DATABASE_NAME)
except:
    pass


@functions_framework.http
def http_handler(request: flask.request) -> flask.typing.ResponseReturnValue:

    match request.method:
        case "GET":
            return flask.jsonify({"status": "OK"}), 200
        case "POST":
            if resumes.add_document(request):
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
            return flask.jsonify({"error": "client error"}), 400
