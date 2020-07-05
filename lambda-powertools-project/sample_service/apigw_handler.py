import json
import os

import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_xray_sdk.core import xray_recorder

logger = Logger()
tracer = Tracer()

dynamodb_sample_table_tbl = boto3.resource('dynamodb').Table('sample-table')
sqs_client = boto3.client('sqs')
sns_client = boto3.client('sns')
lambda_client = boto3.client('lambda')


# @logger.inject_lambda_context を付けておくとログ出力時に context にセットされている
# function_name 等の情報がセットされる
# Capturing context Lambda info
# https://awslabs.github.io/aws-lambda-powertools-python/core/logger/#capturing-context-lambda-info
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def recv_msg(event, context):
    # API Gateway に発行された traceId は event.headers.X-Amzn-Trace-Id にセットされている
    # Lambda 用に発行された traceId は xray_recorder.current_segment().trace_id にセットされている
    awsTraceHeader = event['headers']['X-Amzn-Trace-Id']
    logger.structure_logs(append=True,
                          AWSTraceHeader=awsTraceHeader,
                          traceId=xray_recorder.current_segment().trace_id)
    logger.debug(event)

    request_body = json.loads(event['body'])
    # logger.info({
    #     "orderNumber": request_body['orderNumber'],
    #     "orderDate": request_body['orderDate']
    # })

    for orderedItem in request_body['orderedItem']:
        logger.structure_logs(append=True,
                              orderNumber=request_body['orderNumber'],
                              orderItemNumber=orderedItem['orderItemNumber']
                              )
        put_item_to_dynamodb(request_body['orderNumber'], orderedItem)
        send_message_to_sqs(os.environ['QUEUE_URL'], event['body'])
        send_message_to_sns(os.environ['TOPIC_ARN'], event['body'])
        call_process_sync(event['body'])
        call_process_async(event['body'])

    # logger.structure_logs(append=False) を呼ぶと @logger.inject_lambda_context
    # でセットされた項目まで消える
    logger.structure_logs(append=False)
    logger.info('テスト')

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


@tracer.capture_method
def put_item_to_dynamodb(orderNumber, orderedItem):
    dynamodb_sample_table_tbl.put_item(
        Item={
            'orderNumber': orderNumber,
            'orderItemNumber': orderedItem['orderItemNumber'],
            'orderQuantity': orderedItem['orderQuantity'],
            'productID': orderedItem['productID'],
            'category': orderedItem['category'],
            'price': orderedItem['price']
        }
    )
    logger.info('sample-table に追加しました')


@tracer.capture_method
def send_message_to_sqs(queue_url, body):
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=body
    )
    logger.info('SampleQueue にメッセージを送信しました')


@tracer.capture_method
def send_message_to_sns(topic_arn, body):
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=body
    )
    logger.info('SampleTopic にメッセージを送信しました')


@tracer.capture_method
def call_process_sync(body):
    response = lambda_client.invoke(
        FunctionName='sample-service-dev-processSync',
        Payload=body
    )
    logger.info('processSync を同期で呼び出ししました')


@tracer.capture_method
def call_process_async(body):
    response = lambda_client.invoke_async(
        FunctionName='sample-service-dev-processAsync',
        InvokeArgs=body
    )
    logger.info('processAsync を非同期で呼び出ししました')
