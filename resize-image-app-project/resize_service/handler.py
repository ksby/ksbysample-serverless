import logging
import os
import re
import uuid
from urllib.parse import unquote_plus

import boto3
from PIL import Image

thumbnail_size = 320, 180

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')


def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(thumbnail_size)
        image.save(resized_path)


def resize(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        # ディレクトリの場合には何もしない
        if key.endswith('/'):
            return

        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        resized_path = '/tmp/resized-{}'.format(tmpkey)

        filename = key.split('/')[-1]
        dirname = re.sub(filename + '$', '', key)
        basename, ext = os.path.splitext(filename)
        resized_key = '{}{}_thumb{}'.format(dirname, basename, ext)

        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, resized_path)
        s3_client.upload_file(resized_path, "ksbysample-resize-bucket", resized_key)
        logger.info('サムネイルを生成しました({})'.format(resized_key))
