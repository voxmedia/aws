#coding: utf-8

from thumbor.result_storages import BaseStorage

from tc_aws.aws.storage import AwsStorage

class Storage(BaseStorage, AwsStorage):
    def __init__(self, context):
        AwsStorage.__init__(self, context)
        BaseStorage.__init__(self, context)

    def put(self, bytes):
        self.set(bytes, self.normalize_path(self.context.request.url))
