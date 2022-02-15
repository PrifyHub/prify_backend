from flask_restx import Api

from .synthetics_api import api as synthetics_api

api = Api(title="Prify REST API", version="0.1", description="Prify REST Api Description",)

api.add_namespace(synthetics_api)