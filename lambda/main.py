import flask
from flask.json import jsonify
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
        except Exception as e:
            print(e)

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
def http_handler(request: flask.Request) -> flask.typing.ResponseReturnValue:

    if request.method == "GET":
        return flask.jsonify({"status": "OK"}), 200

    elif request.method == "POST":
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

    else:
        # default catch all
        return flask.jsonify({"error": "client error"}), 400
