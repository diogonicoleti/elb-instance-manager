from flask import Flask
from flask_restful import Api
from resources.elb import ELB
from resources.health_check import HealthCheck

app = Flask(__name__)
api = Api(app)

api.add_resource(ELB, '/elb/<string:elb_name>')
api.add_resource(HealthCheck, '/healthcheck')

if __name__ == '__main__':
    app.run(debug=True)
