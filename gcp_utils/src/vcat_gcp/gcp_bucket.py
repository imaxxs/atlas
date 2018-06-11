class GCPBucket(object):

    def __init__(self, name):
        from vcat_gcp.global_state import connection_manager

        self._connection = connection_manager.bucket_connection()
        self._bucket = self._connection.get_bucket(name)

    def upload_from_string(self, name, data):
        self._blob(name).upload_from_string(data)

    def upload_from_file(self, name, input_file):
        self._blob(name).upload_from_file(input_file)

    def exists(self, name):
        return self._blob(name).exists()

    def download_as_string(self, name):
        return self._blob(name).download_as_string()

    def download_to_file(self, name, output_file):
        return self._blob(name).download_to_file(output_file)

    def list_files(self, pathname):
        from os.path import dirname
        from os.path import basename
        from fnmatch import fnmatch

        directory = dirname(pathname)
        path_filter = basename(pathname)

        objects = self._bucket.list_blobs(
            prefix=directory + '/', delimiter='/')
        object_names = [bucket_object.name for bucket_object in objects]
        object_file_names = [basename(path) for path in object_names]
        return filter(lambda path: fnmatch(path, path_filter), object_file_names)

    def _blob(self, name):  
        return self._bucket.blob(name)