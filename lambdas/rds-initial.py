import logging
import boto3
import os
import pymysql
import json

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
    sm_response = get_secrets()
    try:
        conn = pymysql.connect(
            host=json.loads(sm_response)['host'],
            user=json.loads(sm_response)['username'],
            password=json.loads(sm_response)['password'],

        )
    except pymysql.err.OperationalError as er:
        logging.error("Not able to connect to database")
        raise Exception(er)

    db_name = json.loads(sm_response)['dbname']
    cur = conn.cursor()
    sql = '''use %s''' % db_name
    cur.execute(sql)
    t1 = '''create table Customer(
        id int not null auto_increment,
        name text,
        customer_id int,
        primary key (id)
        )'''
    t2 = '''create table Account(
        id int not null auto_increment,
        account_number int,
        customer_id int,
        primary key (id)
        )'''
    t3 = '''create table Transactions(
        id int not null auto_increment,
        transaction_amount int,
        customer_id int,
        primary key (id)
        )'''
    try:
        cur.execute(t1)
    except pymysql.err.OperationalError:
        logging.warning("Table already exists")
    try:
        cur.execute(t2)
    except pymysql.err.OperationalError:
        logging.warning("Table already exists")
    try:
        cur.execute(t3)
    except pymysql.err.OperationalError:
        logging.warning("Table already exists")
    finally:
        tb1 = '''insert into Customer(name, customer_id) values ('%s','%i')''' % ('customer_name1', 100)
        cur.execute(tb1)
        tb1 = '''insert into Customer(name, customer_id) values ('%s','%i')''' % ('customer_name2', 101)
        cur.execute(tb1)
        tb2 = '''insert into Account(account_number, customer_id) values ('%i','%i')''' % (12345, 100)
        cur.execute(tb2)
        tb2 = '''insert into Account(account_number, customer_id) values ('%i','%i')''' % (12225, 101)
        cur.execute(tb2)
        tb3 = '''insert into Transactions(transaction_amount, customer_id) values ('%i','%i')''' % (1000, 100)
        cur.execute(tb3)
        tb3 = '''insert into Transactions(transaction_amount, customer_id) values ('%i','%i')''' % (1100, 100)
        cur.execute(tb3)
        tb3 = '''insert into Transactions(transaction_amount, customer_id) values ('%i','%i')''' % (1200, 101)
        cur.execute(tb3)
        tb3 = '''insert into Transactions(transaction_amount, customer_id) values ('%i','%i')''' % (1200, 100)
        cur.execute(tb3)
        tb3 = '''insert into Transactions(transaction_amount, customer_id) values ('%i','%i')''' % (1000, 101)
        cur.execute(tb3)
        conn.commit()
    sql = '''show tables'''
    cur.execute(sql)
    output = cur.fetchall()
    print(output)