import json
import logging
import os

import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def notify_slack(event, context):
    msg = {
        'text': event['Records'][0]['Sns']['Message']
    }
    encoded_msg = json.dumps(msg).encode('utf-8')
    res = requests.post(os.environ['SLACK_WEBHOOK_URL'], data=encoded_msg)
    logger.info(res.status_code)
    logger.info(res.headers)
    logger.info(res.text)
