"""This program is used to fill api in html file and upload it to S3"""
import boto3
import os
import logging


s3_client = boto3.client('s3')
logging.getLogger().setLevel("INFO")


def replace_placeholder(api_endpoint):
    cwd = os.path.join(os.getcwd(), "webpage/index.html")
    try:
        with open(cwd, 'r') as file:
            html_content = file.read()
    except FileNotFoundError as e:
        logging.error("File not found")
        raise Exception(e)
    modified_content = html_content.replace("{{api_placeholder}}", api_endpoint)
    try:
        with open(cwd, 'w') as file:
            file.write(modified_content)
    except IOError as err:
        logging.error("Not able to write in file")
        raise Exception(err)


def upload_file():
    bucket_name = os.getenv("HOSTING_BUCKET")
    cwd = os.path.join(os.getcwd(), "webpage/index.html")
    try:
        s3_client.put_object(
            Body=cwd,
            Bucket=bucket_name,
            Key="index.html",
            ContentType='text/html',
            ACL='public-read'
        )
    except s3_client.exceptions.NoSuchBucket as error:
        logging.error("Bucket does not exists")
        raise Exception(error)


if __name__ == "__main__":
    replace_placeholder("another_thing")
