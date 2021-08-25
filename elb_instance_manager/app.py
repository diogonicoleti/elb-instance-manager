from flask import Flask
from flask_restful import Api
from resources.elb import ELBResource
from resources.health_check import HealthCheckResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ELBResource, '/elb/<string:elb_name>')
api.add_resource(HealthCheckResource, '/healthcheck')

if __name__ == '__main__':
    app.run(debug=True)
