import os
import uuid

from pathlib import Path
from flask import Flask, request, jsonify, send_file

from DataSynthesizer.DataDescriber import DataDescriber
from DataSynthesizer.DataGenerator import DataGenerator

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
  return anonimize_file(file_name=file_name)


def anonimize_file(file_name):
  upload_dirpath = os.path.join(Path(__file__).parent.parent.absolute(), 'uploaded')
  anon_dirpath = os.path.join(Path(__file__).parent.parent.absolute(), 'anonimized')
  data_path = os.path.join(anon_dirpath, f'{file_name}.csv')
  describe_path = os.path.join(anon_dirpath, f'{file_name}_desc.json')

  epsilon = 1
  threshold_value = 20
  degree_of_bayesian_network = 2

  describer = DataDescriber(category_threshold=threshold_value)
  describer.describe_dataset_in_correlated_attribute_mode(dataset_file=os.path.join(upload_dirpath, f'{file_name}.csv'), 
                                                        epsilon=epsilon,
                                                        k=degree_of_bayesian_network)
  describer.save_dataset_description_to_file(describe_path)
  generator = DataGenerator()
  generator.generate_dataset_in_correlated_attribute_mode(1000, describe_path) # resolve this params
  generator.save_synthetic_data(data_path)

  return send_file(data_path, as_attachment=True)

if __name__ == "__main__":
    app.run()