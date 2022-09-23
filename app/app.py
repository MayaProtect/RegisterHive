import flask
from flask_cors import CORS, cross_origin
from app.hive import Hive
import json


class RegisterHive:
    def __init__(self, params: dict):
        self.app = flask.Flask(__name__)
        self.mongo_host = params['mongo_host']
        self.mongo_port = params['mongo_port']
        self.mongo_db = params['mongo_db']

        CORS(self.app)

        self.app.add_url_rule('/hives', 'register_hives', self.register_hives, methods=['POST'])

    @cross_origin()
    def register_hives(self):
        request_body = flask.request.get_json()
        if request_body is None:
            return flask.jsonify({
                "status": "error",
                "message": "The request body is empty"
            }), 400

        try:
            hive = Hive(request_body)
            hive.save(self.mongo_host, self.mongo_port, self.mongo_db)
        except Exception as e:
            return flask.jsonify({
                "status": "error",
                "message": str(e)
            }), 400

        return flask.Response(json.dumps(hive.__to_json__()), status=201)

    def run(self):
        self.app.run(host='0.0.0.0', port=8080)
