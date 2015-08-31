# coding: utf-8

from boto.s3.bucket import Bucket
from thumbor.utils import logger
from tornado.concurrent import return_future

import thumbor.loaders.http_loader as http_loader

from tc_aws.aws.connection import get_connection

def _get_bucket(url, root_path=None):
    """
    Returns a tuple containing bucket name and bucket path.
    url: A string of the format /bucket.name/file/path/in/bucket
    """

    url_by_piece = url.lstrip("/").split("/")
    bucket_name = url_by_piece[0]

    if root_path is not None:
        url_by_piece[0] = root_path
    else:
        url_by_piece = url_by_piece[1:]

    bucket_path = "/".join(url_by_piece)

    return bucket_name, bucket_path


def _normalize_url(url):
    """
    :param url:
    :return: exactly the same url since we only use http loader if url stars with http prefix.
    """
    return url


def _validate_bucket(context, bucket):
    allowed_buckets = context.config.get('S3_ALLOWED_BUCKETS', default=None)
    return not allowed_buckets or bucket in allowed_buckets

def _generate_presigned_url(context, bucket, key):
    connection = get_connection(context)
    expiry = 60 * 60
    presigned_url = connection.generate_url(
        expiry,
        'GET',
        bucket,
        key,
    )
    return presigned_url

@return_future
def load(context, url, callback):
    bucket, key = _get_bucket_and_key(context, url)

    if _validate_bucket(context, bucket):
        presigned_url = _generate_presigned_url(context, bucket, key)
        http_loader.load_sync(context, presigned_url, callback, normalize_url_func=_normalize_url)

    callback(None)
