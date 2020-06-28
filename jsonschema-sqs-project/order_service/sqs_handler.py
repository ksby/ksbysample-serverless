import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def recv_msg(event, context):
    sqs_client = boto3.client('sqs')

    response = sqs_client.receive_message(QueueUrl=os.environ['QUEUE_URL'])
    if 'Messages' in response:
        logger.info(response)
        for msg in response['Messages']:
            sqs_client.delete_message(QueueUrl=os.environ['QUEUE_URL'], ReceiptHandle=msg['ReceiptHandle'])
