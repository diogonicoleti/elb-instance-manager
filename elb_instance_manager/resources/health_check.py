from flask_restful import Resource


class HealthCheckResource(Resource):
    def get(self):
        "Returns OK when the app is up and running"
        return {'status': 'OK'}, 200
