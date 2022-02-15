import os
import uuid
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from flask_restx import Namespace, Resource, fields

from DataSynthesizer.DataDescriber import DataDescriber
from DataSynthesizer.DataGenerator import DataGenerator

api = Namespace("synthetics", description="Synthetic Data Generation Description")



@api.route("/correlated")
class SynthetizeCorrelated(Resource):
    
    @api.doc("Receive and generate dataset", params={'file': 'csv file'})    
    def post(self):
        file_name = str(uuid.uuid4())
        upload_dirpath = os.path.join(Path(__file__).parent.parent.absolute(), 'uploaded')
        uploaded_file = request.files['file']

        if uploaded_file.mimetype != 'text/csv':
            return jsonify({'status': 'error', 'message': 'The file type must be CSV.'})

        uploaded_file.save(os.path.join(upload_dirpath, file_name+'.csv')) # we should delete this data after the process
        return anonimyze_file(file_name=file_name)


def anonimyze_file(file_name):
    upload_dirpath = os.path.join(Path(__file__).parent.parent.absolute(), 'uploaded')
    anon_dirpath = os.path.join(Path(__file__).parent.parent.absolute(), 'anonymized')
    data_path = os.path.join(anon_dirpath, f'{file_name}.csv')
    describe_path = os.path.join(anon_dirpath, f'{file_name}_desc.json')

    output_size = request.args.get('sz', default = 1000, type = int)
    epsilon = request.args.get('eps', default = 1, type = int)
    threshold_value = request.args.get('threshold_value', default = 20, type = int)
    degree_of_bayesian_network = request.args.get('degree', default = 2, type = int)

    print(f'Running w/ parametes: size={output_size} eps={epsilon} thr={threshold_value} deg={degree_of_bayesian_network}')

    describer = DataDescriber(category_threshold=threshold_value)
    describer.describe_dataset_in_correlated_attribute_mode(dataset_file=os.path.join(upload_dirpath, f'{file_name}.csv'), 
                                                            epsilon=epsilon,
                                                            k=degree_of_bayesian_network)
    describer.save_dataset_description_to_file(describe_path)
    generator = DataGenerator()
    generator.generate_dataset_in_correlated_attribute_mode(output_size, describe_path) # resolve this params
    generator.save_synthetic_data(data_path)

    return send_file(data_path, as_attachment=True)