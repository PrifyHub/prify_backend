from pathlib import Path

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

import prify.config as config
from prify import apis

def init():    
    Path(config.anonymized_folder).mkdir(parents=True, exist_ok=True)
    Path(config.uploaded_folder).mkdir(parents=True, exist_ok=True)
        
if __name__ == "__main__":
    init()
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    apis.api.init_app(app)
    app.run(debug=True)
