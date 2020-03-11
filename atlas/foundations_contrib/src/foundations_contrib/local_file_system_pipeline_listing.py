

class LocalFileSystemPipelineListing(object):

    def __init__(self, path=None):
        from os import getcwd
        from os.path import abspath
        from foundations_contrib.bucket_pipeline_listing import BucketPipelineListing
        from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

        bucket_path = path or getcwd()
        bucket_path = abspath(bucket_path)
        self._listing = BucketPipelineListing(
            LocalFileSystemBucket, bucket_path)

    def track_pipeline(self, pipeline_name):
        return self._listing.track_pipeline(pipeline_name)

    def get_pipeline_names(self):
        return self._listing.get_pipeline_names()
