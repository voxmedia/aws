#coding: utf-8

import calendar
from datetime import datetime, timedelta
import hashlib
from json import loads, dumps

from os.path import splitext, join

from thumbor.storages import BaseStorage
from thumbor.utils import logger

from boto.s3.bucket import Bucket
from boto.s3.key import Key
from dateutil.parser import parse as parse_ts

import tc_aws.connection

class Storage(BaseStorage):


    def __init__(self, context):
        BaseStorage.__init__(self, context)
        self.storage = self.__get_s3_bucket()

    def __get_s3_bucket(self):
        return Bucket(
            connection=tc_aws.connection.get_connection(self.context),
            name=self.context.config.STORAGE_BUCKET
        )

    def put(self, path, bytes):
        file_abspath = self.normalize_path(path)

        file_key=Key(self.storage)
        file_key.key = file_abspath

        file_key.set_contents_from_string(bytes,
            encrypt_key = self.context.config.S3_STORAGE_SSE,
            reduced_redundancy = self.context.config.S3_STORAGE_RRS
        )

        return path

    def put_crypto(self, path):
        if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            return

        file_abspath = self.normalize_path(path)

        if not self.context.server.security_key:
            raise RuntimeError("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")

        crypto_path = '%s.txt' % splitext(file_abspath)[0]

        file_key=Key(self.storage)
        file_key.key = crypto_path

        file_key.set_contents_from_string(self.context.server.security_key,
            encrypt_key = self.context.config.S3_STORAGE_SSE,
            reduced_redundancy = self.context.config.S3_STORAGE_RRS
        )

        return crypto_path

    def put_detector_data(self, path, data):
        file_abspath = self.normalize_path(path)

        path = '%s.detectors.txt' % splitext(file_abspath)[0]

        file_key=Key(self.storage)
        file_key.key = path

        file_key.set_contents_from_string(dumps(data),
            encrypt_key = self.context.config.S3_STORAGE_SSE,
            reduced_redundancy = self.context.config.S3_STORAGE_RRS
        )

        return path

    def get_crypto(self, path):
        file_abspath = self.normalize_path(path)
        crypto_path = "%s.txt" % (splitext(file_abspath)[0])

        file_key = self.storage.get_key(crypto_path)
        if not file_key:
            return None

        return file_key.read()

    def get(self, path):

        file_abspath = self.normalize_path(path)

        file_key = self.storage.get_key(file_abspath)

        if not file_key or self.is_expired(file_key):
            logger.debug("[STORAGE] s3 key not found at %s" % file_abspath)
            return None

        return file_key.read()

    def get_detector_data(self, path):
        file_abspath = self.normalize_path(path)
        path = '%s.detectors.txt' % splitext(file_abspath)[0]

        file_key = self.storage.get_key(path)

        if not file_key or self.is_expired(path):
            return None

        return loads(file_key.read())

    def exists(self, path):
        file_abspath = self.normalize_path(path)
        file_key = self.storage.get_key(file_abspath)
        if not file_key:
            return False
        return True

    def normalize_path(self, path):
        root_path = self.context.config.STORAGE_AWS_STORAGE_ROOT_PATH
        path_segments = [path]
        return join(root_path, *path_segments)


    def is_expired(self, key):
        if key:
            expire_in_seconds = self.context.config.STORAGE_EXPIRATION_SECONDS

            #Never expire
            if expire_in_seconds is None or expire_in_seconds == 0:
                return False

            timediff = datetime.now() - self.utc_to_local(parse_ts(key.last_modified))
            return timediff.seconds > expire_in_seconds
        else:
            #If our key is bad just say we're expired
            return True

    def remove(self, path):

        if not self.exists(path):
            return

        if not self.storage.delete_key(path):
            return False
        return True

    def utc_to_local(self, utc_dt):
        # get integer timestamp to avoid precision lost
        timestamp = calendar.timegm(utc_dt.timetuple())
        local_dt = datetime.fromtimestamp(timestamp)
        assert utc_dt.resolution >= timedelta(microseconds=1)
        return local_dt.replace(microsecond=utc_dt.microsecond)

    def resolve_original_photo_path(self,filename):
        return filename
