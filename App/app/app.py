import boto3
import logging
import os
from botocore.exceptions import ClientError, ParamValidationError

DYNAMODB_ENDPOINT = os.environ.get("DYNAMODB_ENDPOINT", "http://localhost:8000")
dynamodb = boto3.client(
    "dynamodb", region_name="us-west-2", endpoint_url=DYNAMODB_ENDPOINT
)

logging.basicConfig(
    level=logging.INFO,
    filename="fetch_secret.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def fetch_secret(codeName):
    try:
        response = dynamodb.get_item(
            TableName="devops-challenge", Key={"codeName": {"S": codeName}}
        )
        logging.info(f"Fetched item from DynamoDB: {response}")
    except ClientError as e:
        logging.error(f"ClientError fetching from DynamoDB: {e}")
        return None
    except ParamValidationError as e:
        logging.error(f"ParamValidationError fetching from DynamoDB: {e}")
        return None
    else:
        if "Item" in response:
            secret_code = response["Item"]["secretCode"]["S"]
            logging.info(f"Successfully retrieved secret code: {secret_code}")
            return secret_code
        else:
            logging.warning("Secret code not found in DynamoDB.")
            return None
