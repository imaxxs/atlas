
from foundations_contrib.utils import file_archive_name
from foundations_contrib.utils import file_archive_name_with_additional_prefix


class BucketPipelineArchive(object):

    def __init__(self, bucket_constructor, *constructor_args, **constructor_kwargs):
        self._bucket = bucket_constructor(
            *constructor_args, **constructor_kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def append(self, name, item, prefix=None):
        from foundations_internal.serializer import serialize

        serialized_item = serialize(item)
        self.append_binary(name, serialized_item, prefix)

    def append_binary(self, name, serialized_item, prefix=None):
        arcname = file_archive_name(prefix, name)
        self._bucket.upload_from_string(arcname, serialized_item)

    def append_file(self, file_prefix, file_path, prefix=None, target_name=None):
        from os.path import basename

        name = target_name or basename(file_path)
        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, name)
        with open(file_path, 'rb') as file:
            self._bucket.upload_from_file(arcname, file)

    def fetch(self, name, prefix=None):
        from foundations_internal.serializer import deserialize

        serialized_item = self.fetch_binary(name, prefix)
        return deserialize(serialized_item)

    def fetch_binary(self, name, prefix=None):
        arcname = file_archive_name(prefix, name)
        if self._bucket.exists(arcname):
            return self._bucket.download_as_string(arcname)
        else:
            return None

    def fetch_file_path(self, file_prefix, file_path, prefix=None):
        from os.path import basename

        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, basename(file_path))

        return self._download_file_from_archive(arcname, file_path)

    def fetch_file_path_to_target_file_path(self, file_prefix, file_path, prefix, target_file_path):
        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, file_path)

        return self._download_file_from_archive(arcname, target_file_path)

    def list_files(self, pathname, prefix):
        arcname = file_archive_name(prefix, pathname)
        return self._bucket.list_files(arcname)

    def exists(self, name, prefix=None):
        name_in_archive = file_archive_name(prefix, name)
        return self._bucket.exists(name_in_archive)

    def _download_file_from_archive(self, arcname, target_file_path):
        if self._bucket.exists(arcname):
            with open(target_file_path, 'w+b') as target_file:
                self._bucket.download_to_file(arcname, target_file)
            return True
        return False
