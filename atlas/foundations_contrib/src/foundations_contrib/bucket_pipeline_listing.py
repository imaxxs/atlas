

class BucketPipelineListing(object):

    def __init__(self, bucket_constructor, *constructor_args, **constructor_kwargs):
        self._bucket = bucket_constructor(
            *constructor_args, **constructor_kwargs)

    def track_pipeline(self, pipeline_name):
        self._log().debug('Tracking {}'.format(pipeline_name))
        existing_pipelines = self.get_pipeline_names()
        if not pipeline_name in existing_pipelines:
            self._bucket.upload_from_string(
                pipeline_name + '.tracker', pipeline_name)
        else:
            self._log().debug('{} already exists!'.format(pipeline_name))

    def get_pipeline_names(self):
        from foundations_contrib.utils import string_from_bytes
        from foundations_contrib.helpers.future import Future

        file_names = self._bucket.list_files('*.tracker')

        def get_pipeline_name(name):
            byte_file_names = self._bucket.download_as_string(name)
            return string_from_bytes(byte_file_names)

        return [get_pipeline_name(name) for name in file_names]

    def _log(self):
        from foundations_contrib.global_state import log_manager
        return log_manager.get_logger(__name__)
