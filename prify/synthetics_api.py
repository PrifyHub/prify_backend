import os
import uuid
import pymongo
import boto3

import prify.config as config
from flask import jsonify, request, send_file
from flask_restx import Namespace, Resource
from celery import Celery
from celery.result import AsyncResult

api = Namespace("synthetics")

simple_app = Celery('simple_worker', broker='amqp://localhost',
                                    backend='mongodb://localhost:27017/mydb')
@api.route("/correlated")
class SynthetizeCorrelated(Resource):
    
    def post(self):
        

        file_name = str(uuid.uuid4())

        uploaded_file = request.files['file']

        if uploaded_file.mimetype != 'text/csv':
            return jsonify({'status': 'error', 'message': 'The file type must be CSV.'})

        
        api.logger.info("Invoking Method ")
        uploaded_file.save(os.path.join(config.uploaded_folder, file_name+'.csv')) # we should delete this data after the process
        r = simple_app.send_task('tasks.anonimyze_file', kwargs={'file_name':file_name})
        api.logger.info(r.backend)
        return r.id, 202
        #return self.anonimyze_file(file_name=file_name)

#Status da Task
@api.route("/simple_task_status/<task_id>")
class SimpleStatus(Resource):
    def get(self, task_id):
        stat = simple_app.AsyncResult(task_id, app=simple_app)
        #stat = AsyncResult(task_id).state

        if(stat.state == 'PENDING') :
            print("Invoking Method ")
            return "Status of the Task " + stat.state, 200

        elif(stat.state == 'SUCCESS') :
            print("Invoking Method ")
            return "Status of the Task " + stat.state, 302
        
    

    
#Resultado da Task
@api.route('/simple_task_result/<task_id>')
class SimpleResult(Resource):
    def get(self, task_id):
        res = simple_app.AsyncResult(task_id)
        
        #return "Result of the Task " + str(res.result)
        return send_file(res.result, as_attachment=True)
