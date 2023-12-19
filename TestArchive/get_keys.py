import os
import boto3
import json
import dotenv
from botocore.exceptions import ClientError
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
print(dotenv_path) 

def get_ucb_key():

    secret_name = "biapp/tool1/key"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)
    os.environ["UCB_API_KEY"] = secret['key']
    dotenv.set_key(dotenv_path, "UCB_API_KEY", os.environ["UCB_API_KEY"])

def get_applitools_key():

    secret_name = "biapp/tool2/key"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)
    os.environ["APPLITOOLS_API_KEY"] = secret['key']
    dotenv.set_key(dotenv_path, "APPLITOOLS_API_KEY", os.environ["APPLITOOLS_API_KEY"])
    #return secret

def get_testmo_secret():

    secret_name = "biapp/tool3/key"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)
    os.environ["TESTMO_TOKEN"] = secret['key']
    dotenv.set_key(dotenv_path, "TESTMO_TOKEN", os.environ["TESTMO_TOKEN"])
    #return secret

get_ucb_key()
get_applitools_key()
get_testmo_secret()