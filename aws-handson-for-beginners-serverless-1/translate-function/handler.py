import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

translate = boto3.client('translate')

def lambda_handler(event, context):

    # logger.info(event)

    input_text = 'おはよう'

    response = translate.translate_text(
        Text=input_text,
        SourceLanguageCode='ja',
        TargetLanguageCode='en'
    )

    output_text = response.get('TranslatedText')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'output_text': output_text
        })
    }
