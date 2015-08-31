# coding: utf-8

from boto.s3.bucket import Bucket
from thumbor.utils import logger
from tornado.concurrent import return_future

import thumbor.loaders.http_loader as http_loader

from tc_aws.aws.connection import get_connection


@return_future
def load(context, url, callback):
    enable_http_loader = context.config.get('AWS_ENABLE_HTTP_LOADER', default=False)

    if enable_http_loader and url.startswith('http'):
        return http_loader.load_sync(context, url, callback, normalize_url_func=_normalize_url)

    bucket, key = _get_bucket_and_key(context, url)

    if _validate_bucket(context, bucket):
        bucket_loader = Bucket(
            connection=get_connection(context),
            name=bucket
        )
        file_key = None
        try:
            file_key = bucket_loader.get_key(url)
        except Exception, e:
            logger.warn("ERROR retrieving image from S3 {0}: {1}".format(url, str(e)))

        if file_key:
            callback(file_key.read())
            return

    callback(None)
