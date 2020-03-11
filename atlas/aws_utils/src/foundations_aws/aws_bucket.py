
class AWSBucket(object):

    def __init__(self, name):
        from foundations_aws.global_state import connection_manager

        self._connection = connection_manager.bucket_connection()

        split_name = name.split('/', 1)
        self._bucket_name = split_name[0]

        if len(split_name) > 1:
            self._key_prefix = split_name[1] + '/'
        else:
            self._key_prefix = ''

    def upload_from_string(self, name, data):
        self._upload_object(name, data)

    def upload_from_file(self, name, input_file):
        self._upload_object(name, input_file)

    def exists(self, name):
        from botocore.exceptions import ClientError

        try:
            self._connection.head_object(Bucket=self._bucket_name, Key=self._object_key(name))
            return True
        except ClientError:
            return False

    def download_as_string(self, name):
        object_body = self._get_object_body(name)
        return object_body.read()

    def download_to_file(self, name, output_file):
        for chunk in self._get_object_body(name).iter_chunks():
            output_file.write(chunk)

        output_file.flush()
        output_file.seek(0)

    def list_files(self, pathname):
        from os.path import dirname
        from os.path import basename
        from fnmatch import fnmatch

        directory = dirname(pathname)
        path_filter = basename(pathname)

        if not (directory == '.' or directory == ''):
            prefix = directory + '/'
        else:
            prefix = ''

        object_responses = self._connection.list_objects_v2(
            Bucket=self._bucket_name, Prefix=self._object_key(prefix), Delimiter='/')
        
        if 'Contents' in object_responses:
            object_names = [bucket_object['Key'] for bucket_object in object_responses['Contents']]
            object_file_names = [basename(path) for path in object_names]
            for path in object_file_names:
                if fnmatch(path, path_filter):
                    yield prefix + path
        
        if 'CommonPrefixes' in object_responses:
            for new_prefix in object_responses['CommonPrefixes']:
                yield new_prefix['Prefix']

    def remove(self, name):
        self._connection.delete_object(Bucket=self._bucket_name, Key=self._object_key(name))
    
    def move(self, source, destination):
        if source != destination:
            source_info = {'Bucket': self._bucket_name, 'Key': self._object_key(source)}

            self._connection.copy_object(Bucket=self._bucket_name, CopySource=source_info, Key=self._object_key(destination))
            self.remove(source)

    def _object_key(self, name):
        return self._key_prefix + name

    def _get_object_body(self, name):
        response = self._connection.get_object(Bucket=self._bucket_name, Key=self._object_key(name))
        return response['Body']

    def _upload_object(self, name, to_upload):
        self._connection.put_object(Bucket=self._bucket_name, Key=self._object_key(name), Body=to_upload)

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)