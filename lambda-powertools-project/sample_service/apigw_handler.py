import json

from aws_lambda_powertools import Logger

logger = Logger()


# @logger.inject_lambda_context を付けておくとログ出力時に context にセットされている
# function_name 等の情報がセットされる
# Capturing context Lambda info
# https://awslabs.github.io/aws-lambda-powertools-python/core/logger/#capturing-context-lambda-info
@logger.inject_lambda_context
def recv_msg(event, context):
    logger.debug(event['body'])
    request_body = json.loads(event['body'])
    logger.info({
        "orderNumber": request_body['orderNumber'],
        "orderDate": request_body['orderDate']
    })

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
