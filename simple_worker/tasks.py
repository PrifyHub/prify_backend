import os
import queue
import time
from unittest import result
from urllib import request
from DataSynthesizer.DataDescriber import DataDescriber
from DataSynthesizer.DataGenerator import DataGenerator
from flask import send_file

from asyncio.log import logger
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery('simple_worker', broker='amqp://localhost',
                            backend='mongodb://localhost:27017/mydb')


#anonymized_folder = "C:\\Users\\aglailson\\Documents\\Prify\\Versão nova\\prify_backend\\tmp\\anonymized\\"
anonymized_folder = "../tmp/anonymized/"
uploaded_folder = "../tmp/uploaded/"

@app.task(bind=True)
def anonimyze_file(self, file_name):
    
    logger.info('Got Request - Starting work')
    #print (AsyncResult(request.id).state)
    data_path = os.path.join(anonymized_folder, f'{file_name}.csv')
    result = "tmp\\anonymized\\" + f'{file_name}.csv'
    describe_path = os.path.join(anonymized_folder, f'{file_name}_desc.json')

    output_size = 1000
    epsilon = 1
    threshold_value = 20
    degree_of_bayesian_network = 2

    print(f'Running w/ parametes: size={output_size} eps={epsilon} thr={threshold_value} deg={degree_of_bayesian_network}')

    describer = DataDescriber(category_threshold=threshold_value)
    describer.describe_dataset_in_correlated_attribute_mode(dataset_file=os.path.join(uploaded_folder, f'{file_name}.csv'), 
                                                            epsilon=epsilon,
                                                            k=degree_of_bayesian_network)
    describer.save_dataset_description_to_file(describe_path)
    generator = DataGenerator()
    generator.generate_dataset_in_correlated_attribute_mode(output_size, describe_path) # resolve this params
    generator.save_synthetic_data(data_path)

    logger.info('Work Finished')
    
    return result
        