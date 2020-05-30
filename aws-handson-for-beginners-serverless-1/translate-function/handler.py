import datetime
import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

translate = boto3.client('translate')
dynamodb_translate_history_tbl = boto3.resource('dynamodb').Table('translate-history')

def lambda_handler(event, context):
    # logger.info(event)

    input_text = event['queryStringParameters']['input_text']

    response = translate.translate_text(
        Text=input_text,
        SourceLanguageCode='ja',
        TargetLanguageCode='en'
    )

    output_text = response.get('TranslatedText')

    dynamodb_translate_history_tbl.put_item(
        Item={
            'timestamp': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            'input_text': input_text,
            'output_text': output_text
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'output_text': output_text
        }),
        'isBase64Encoded': False,
        'headers': {}
    }
