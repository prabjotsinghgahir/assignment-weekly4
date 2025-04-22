"""Main file to deploy all the resources"""
import os
from deploy_scripts import stack_deploy

template_name = 'templates/rds-deploy.yaml'
file_zip = 'copy_function.py'
lambda_function_name = "cf-lambda-copy-s3"
lambda_code_bucket = os.getenv("BUCKET")
stack_name = 'assignment4'
source_bucket_name = "cf-static-website-psg1"
region = 'ap-south-1'


parameter = [
        {
            'ParameterKey': 'S3BucketName',
            'ParameterValue': source_bucket_name
        }
]

opening_temp = open(template_name)
reading = opening_temp.read()

call_create_stack = stack_deploy.StackCreation(stack_name, reading, parameter)

call_create_stack.create_stack()
call_create_stack.stack_status()
