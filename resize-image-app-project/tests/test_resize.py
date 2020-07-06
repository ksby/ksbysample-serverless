import json
import unittest

import boto3
from moto import mock_s3


@mock_s3
class TestResizeService(unittest.TestCase):
    UPLOAD_BUCKET = 'ksbysample-upload-bucket'
    RESIZE_BUCKET = 'ksbysample-resize-bucket'

    def setUp(self):
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=TestResizeService.UPLOAD_BUCKET)
        s3_client.create_bucket(Bucket=TestResizeService.RESIZE_BUCKET)

    def tearDown(self):
        s3 = boto3.resource('s3')
        upload_bucket = s3.Bucket(TestResizeService.UPLOAD_BUCKET)
        upload_bucket.objects.all().delete()
        upload_bucket.delete()
        resize_bucket = s3.Bucket(TestResizeService.RESIZE_BUCKET)
        resize_bucket.objects.all().delete()
        resize_bucket.delete()

    def test_resize(self):
        from resize_service import handler

        s3_client = boto3.client('s3')
        s3_client.upload_file('tests/sample.jpg', TestResizeService.UPLOAD_BUCKET, 'sample.jpg')

        with open('tests/s3_event.json', 'r') as f:
            event = json.load(f)

        handler.resize(event, None)

        thumb_object = s3_client.get_object(Bucket=TestResizeService.RESIZE_BUCKET,
                                            Key='sample_thumb.jpg')
        self.assertEqual(thumb_object['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertGreater(int(thumb_object['ResponseMetadata']['HTTPHeaders']['content-length']), 0)

        # 生成されたサムネイル画像をダウンロードすることも出来る（実際に作成される）
        # s3_client.download_file(TestResizeService.RESIZE_BUCKET, 'sample_thumb.jpg',
        #                         'tests/sample_thumb.jpg')
