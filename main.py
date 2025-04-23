"""Main file to deploy all the resources"""
import os
import boto3
from deploy_scripts import stack_deploy
from retrive_vpc_info import fetch_vpc_subnets
from upload_file import replace_placeholder, upload_file

lambda_client = boto3.client('lambda')

template_name = 'templates/rds-deploy.yaml'
file_zip = 'copy_function.py'
lambda_function_name = "rds-write-lambda-psg"
lambda_code_bucket = os.getenv("BUCKET")
stack_name = 'assignment4-1'
source_bucket_name = os.getenv("HOSTING_BUCKET")
lambda_layer = "rds-pymysql-layer"
api_gateway_stage_name = "Test"
webpage_name = "index.html"
rest_api_name = "assign-4-api"
rds_database_name = "another_db"
secret_manager_name = "MySecrets"
lambda_rds_get = "lambda-function.zip"
lambda_rds_write = "rds-initial.zip"
lambda_layer_file = "python.zip"
region = 'ap-south-1'

get_vpc_subnets = fetch_vpc_subnets()

parameter = [
        {
            'ParameterKey': 'S3BucketName',
            'ParameterValue': source_bucket_name
        },
        {
            'ParameterKey': 'UIFileName',
            'ParameterValue': webpage_name
        },
        {
            'ParameterKey': 'RestApiName',
            'ParameterValue': rest_api_name
        },
        {
            'ParameterKey': 'RdsDatabseName',
            'ParameterValue': rds_database_name
        },
        {
            'ParameterKey': 'SecretName',
            'ParameterValue': secret_manager_name
        },
        {
            'ParameterKey': 'CodeBucket',
            'ParameterValue': lambda_code_bucket
        },
        {
            'ParameterKey': 'LambdaKey',
            'ParameterValue': lambda_rds_get
        },
        {
            'ParameterKey': 'LambdaHandler',
            'ParameterValue': lambda_rds_get.split('.')[0]+".lambda_handler"
        },
        {
            'ParameterKey': 'LambdaKey1',
            'ParameterValue': lambda_rds_write
        },
        {
            'ParameterKey': 'LambdaHandler1',
            'ParameterValue': lambda_rds_write.split('.')[0]+".lambda_handler"
        },
        {
            'ParameterKey': 'LambdaLayerFile',
            'ParameterValue': lambda_layer_file
        },
        {
            'ParameterKey': 'LambdaLayerName',
            'ParameterValue': lambda_layer
        },
        {
            'ParameterKey': 'LambdaFunctionName',
            'ParameterValue': lambda_function_name
        },
        {
            'ParameterKey': 'ApiGatewayStageName',
            'ParameterValue': api_gateway_stage_name
        },
        {
            'ParameterKey': 'Subnets',
            'ParameterValue': get_vpc_subnets[1]
        },
        {
            'ParameterKey': 'VpcId',
            'ParameterValue': get_vpc_subnets[0]
        }
]

opening_temp = open(template_name)
reading = opening_temp.read()

call_create_stack = stack_deploy.StackCreation(stack_name, reading, parameter)

call_create_stack.create_stack()
api_endpoint = call_create_stack.stack_status()

print(api_endpoint)


replace_placeholder(api_endpoint)
upload_file()

try:
    lambda_client.invoke(FunctionName=lambda_function_name)
except Exception as err:
    print("Lambda error:  ", err)
