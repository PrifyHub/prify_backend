import os
import uuid

from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['POST'])
def index():
  file_name = str(uuid.uuid4())
  upload_dirpath = os.path.join(Path(__file__).parent.parent.absolute(), 'uploaded')
  uploaded_file = request.files['file']

  if uploaded_file.mimetype != 'text/csv':
    return jsonify({'status': 'error', 'message': 'The file type must be CSV.'})

  uploaded_file.save(os.path.join(upload_dirpath, file_name+'.csv')) # we should delete this data after the process
  return jsonify({'status': 'success', 'message': 'All the process is ok!'})


if __name__ == "__main__":
    app.run()