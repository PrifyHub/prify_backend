from flask import Flask
from flask_restful import Api
from distutils.command.config import config
from pathlib import Path
from werkzeug.middleware.proxy_fix import ProxyFix
import prify.config as config
from prify.synthetics_api import SynthetizeCorrelated, SynthetizeCorrelatedDataset, SynthetizeCorrelatedStatus

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

api.add_resource(SynthetizeCorrelated, '/synthetics/correlated')
api.add_resource(SynthetizeCorrelatedStatus, '/synthetics/correlated/status/<string:file_id>')
api.add_resource(SynthetizeCorrelatedDataset, '/synthetics/correlated/dataset/<string:file_id>')

if __name__ == '__main__':
    Path(config.anonymized_folder).mkdir(parents=True, exist_ok=True)
    Path(config.uploaded_folder).mkdir(parents=True, exist_ok=True)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    from sql_alchemy import banco
    banco.init_app(app)
    
    app.run(debug=True)