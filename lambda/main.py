import flask
from flask.json import jsonify
import functions_framework
from google.cloud import firestore
import os
from uuid import uuid4


PROJECT_NAME = os.getenv("PROJECT_NAME", "DEFAULT")
DATABASE_NAME = os.getenv("DATABASE_NAME", "DEFAULT")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "DEFAULT")
TOKEN = os.getenv("TOKEN", "")


class Resumes:
    def __init__(self, project, db_name) -> None:
        self.db = firestore.Client(project=project, database=db_name)

    def random_uuid(self):
        """
        return str: unique random UUID for each record that will be entered into the Obj database
        """
        return str(uuid4())

    def check_content_type(self, request: flask.Request):
        return request.content_type == "application/json"

    def check_token(self, token):
        return token == TOKEN

    def add_resume(self, data):
        """
        return bool: True if successful upload. False if an issue
        """

        document_id = self.random_uuid()

        try:
            self.db.collection(COLLECTION_NAME).document(document_id).set(data)
            return True
        except:
            return False

    def fetch_all_resumes(self):
        """
        return list: of resume data
        """

        try:
            resumes = self.db.collection(COLLECTION_NAME).stream()
            resume_data = [doc.to_dict() for doc in resumes]

            return flask.jsonify(resume_data), 200

        except:
            return flask.jsonify({"error": "no resumes found"}), 404

    def post_handler(self, data):
        """
        function handles the uploads the resume JSON payload to the database

        returns: response + JSON matching the purposed action
        """
        if self.add_resume(data):
            return (
                flask.jsonify({"success": "resume added into the collection"}),
                200,
            )
        else:
            return (
                flask.jsonify({"error": "unable to add resume to the collection."}),
                401,
            )


try:
    resumes = Resumes(project=PROJECT_NAME, db_name=DATABASE_NAME)
except:
    pass


@functions_framework.http
def http_handler(request: flask.Request) -> flask.typing.ResponseReturnValue:

    match request.method:
        case "GET":
            data = resumes.fetch_all_resumes()
            return data
            # return flask.jsonify({"status": "OK"}), 200

        case "POST":
            # fail immediately if the content type is not json
            if not resumes.check_content_type(request):
                return (
                    flask.jsonify({"error": "content type must be application/json"}),
                    406,
                )

            # Simple Auth to protect the POST method from abuse
            if not resumes.check_token(request.headers.get("resume-token")):
                return flask.jsonify({"error": "unauthorized"}), 401

            data = request.get_json()
            return resumes.post_handler(data)

        case _:
            # default catch all
            return flask.jsonify({"error": "client error"}), 400
