
from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket
from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive


class LocalFileSystemPipelineArchive(object):

    def __init__(self, path=None):
        self._archive = BucketPipelineArchive(LocalFileSystemBucket, path)

    def __enter__(self):
        return self._archive.__enter__()

    def __exit__(self, exception_type, exception_value, traceback):
        return self._archive.__exit__(exception_type, exception_value, traceback)

    def append(self, name, item, prefix=None):
        return self._archive.append(name, item, prefix)

    def append_binary(self, name, serialized_item, prefix=None):
        return self._archive.append_binary(name, serialized_item, prefix)

    def append_file(self, file_prefix, file_path, prefix=None, target_name=None):
        return self._archive.append_file(file_prefix, file_path, prefix, target_name)

    def fetch(self, name, prefix=None):
        return self._archive.fetch(name, prefix)

    def fetch_binary(self, name, prefix=None):
        return self._archive.fetch_binary(name, prefix)

    def fetch_file_path(self, file_prefix, file_path, prefix=None):
        return self._archive.fetch_file_path(file_prefix, file_path, prefix)

    def fetch_file_path_to_target_file_path(self, file_prefix, file_path, prefix, target_name):
        return self._archive.fetch_file_path_to_target_file_path(file_prefix, file_path, prefix, target_name)
