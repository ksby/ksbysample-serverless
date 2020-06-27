import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_msg(event, context):
    sqs_client = boto3.client('sqs')

    logger.info(event['body'])
    response = sqs_client.send_message(
        QueueUrl=os.environ['QUEUE_URL'],
        MessageBody=event['body']
    )

    body = {
        "message": f"send message to sqs, MessageId = {response['MessageId']}",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
