# se!/usr/bin/python
# -*- coding: utf-8 -*-
from mock import Mock

from pyvows import Vows, expect
from mock import patch
from datetime import datetime, timedelta
from dateutil import tz
import time  # so we can override time.time
mock_time = Mock()
mock_time.return_value = time.mktime((2009, 2, 17, 17, 3, 38, 1, 48, 0))

from thumbor.context import Context
from derpconf.config import Config

import boto
from boto.s3.key import Key

from moto import mock_s3

from fixtures.storage_fixture import IMAGE_PATH, IMAGE_BYTES

from tc_aws.loaders import presigning_loader

s3_bucket = 'thumbor-images-test'


@Vows.batch
class S3LoaderVows(Vows.Context):

    class CanLoadImage(Vows.Context):

        @mock_s3
        def topic(self):
            conn = boto.connect_s3()
            bucket = conn.create_bucket(s3_bucket)

            k = Key(bucket)
            k.key = IMAGE_PATH
            k.set_contents_from_string(IMAGE_BYTES)

            conf = Config()
            conf.define('S3_LOADER_BUCKET', s3_bucket, '')
            conf.define('S3_LOADER_ROOT_PATH', 'root_path', '')

            return Context(config=conf)

        def should_load_from_s3(self, topic):
            image = yield presigning_loader.load(topic, '/'.join(['root_path', IMAGE_PATH]))
            expect(image).to_equal(IMAGE_BYTES)

    class ValidatesBuckets(Vows.Context):

        def topic(self):
            conf = Config()
            conf.define('S3_ALLOWED_BUCKETS', [], '')

            return Context(config=conf)

        def should_load_from_s3(self, topic):
            image = yield presigning_loader.load(topic, '/'.join([s3_bucket, IMAGE_PATH]))
            expect(image).to_equal(None)

    class HandlesHttpLoader(Vows.Context):

        def topic(self):
            conf = Config()
            return Context(config=conf)

        def should_redirect_to_http(self, topic):
            with patch('thumbor.loaders.http_loader.load_sync') as mock_load_sync:
                yield presigning_loader.load(topic, 'http://foo.bar')
                expect(mock_load_sync.called).to_be_true()

    class CanBuildPresignedUrl(Vows.Context):

        def topic(self):
            conf = Config()
            return Context(config=conf)

        @patch('time.time', mock_time)
        def should_generate_presigned_urls(self, topic):
            url = presigning_loader._generate_presigned_url(
                topic, "bucket-name", "some-s3-key")
            expected = 'https://bucket-name.s3.amazonaws.com/some-s3-key?Signature=Z02q3AX5dNhL6Ov%2FECKDYtb2lGY%3D&Expires=1234890218&AWSAccessKeyId=AKIAIL4O5PGEUV4YUDSA'
            expect(url).to_equal(expected)
