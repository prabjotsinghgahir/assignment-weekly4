import json
import logging
import os
import boto3
import pymysql

sm_client = boto3.client('secretsmanager')
logging.getLogger().setLevel("INFO")


def get_secrets():
    try:
        response = sm_client.get_secret_value(
            SecretId=os.getenv('secret')
        )
        return response['SecretString']
    except sm_client.exceptions.ResourceNotFoundException as e:
        logging.error("Secrets not present")
        raise Exception(e)

def lambda_handler(event, context):
    customer_id = int(event['queryStringParameters']['MY-FIELD'])
    sm_response = get_secrets()
    try:
        conn = pymysql.connect(
            host=json.loads(sm_response)['host'],
            user=json.loads(sm_response)['username'],
            password=json.loads(sm_response)['password'],
        )
        db_name = json.loads(sm_response)['dbname']
        cur = conn.cursor()
        sql = '''use %s''' % db_name
        cur.execute(sql)
        sql = '''select count(*) from Transactions where customer_id=%i''' % customer_id
        cur.execute(sql)
        output = cur.fetchone()
    except pymysql.err.OperationalError as er:
        logging.error(f"Error: {er}")
        raise Exception(er)
    print(output)
    print(type(output))
    return {
        'statusCode': 200,
        'body': "Transaction Count:  " + json.dumps(output[0])
    }
