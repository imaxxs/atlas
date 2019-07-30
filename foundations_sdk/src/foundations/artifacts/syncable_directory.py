"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class SyncableDirectory(object):

    def __init__(self, key, directory_path, local_job_id, remote_job_id, auto_download=True):
        from foundations_contrib.archiving import load_archive

        self._key = key
        self._directory_path = directory_path
        self._local_job_id = local_job_id
        self._remote_job_id = remote_job_id
        self._archive = load_archive('artifact_archive')

        if auto_download:
            self.download()
        
    def __str__(self):
        return self._directory_path

    def upload(self):
        import os
        from foundations_contrib.archiving.upload_artifacts import list_of_files_to_upload_from_artifact_path
        from foundations_contrib.global_state import log_manager

        if self._local_job_id is None:
            foundations_syncable_directory_logger = log_manager.get_logger(__name__)
            foundations_syncable_directory_logger.warning('local_job_id required for uploading artifacts')
        else:
            file_listing = list_of_files_to_upload_from_artifact_path(self._directory_path)
            old_timestamps = self._redis().hgetall(f'jobs:{self._local_job_id}:synced_artifacts:{self._key}:timestamps')
            decoded_old_timestamps = {file_name.decode(): float(file_timestamp) for file_name, file_timestamp in old_timestamps.items()}

            for file in file_listing:
                remote_path = file[len(self._directory_path)+1:]
                timestamp = os.stat(file).st_mtime

                self._redis().hmset(f'jobs:{self._local_job_id}:synced_artifacts:{self._key}:timestamps', {remote_path: timestamp})
                self._redis().sadd(f'jobs:{self._local_job_id}:synced_artifacts:{self._key}', remote_path)

                if remote_path not in decoded_old_timestamps or timestamp > decoded_old_timestamps[remote_path]:
                    self._archive.append_file(f'synced_directories/{self._key}', file, self._local_job_id, remote_path)

    def download(self):
        import os
        import os.path as path

        file_listing = self._redis().smembers(f'jobs:{self._remote_job_id}:synced_artifacts:{self._key}')
        file_listing = [file.decode() for file in file_listing]

        old_timestamps = self._redis().hgetall(f'jobs:{self._local_job_id}:synced_artifacts:{self._key}:timestamps')
        decoded_old_timestamps = {file_name.decode(): float(file_timestamp) for file_name, file_timestamp in old_timestamps.items()}

        for file in file_listing:
            result_path = f'{self._directory_path}/{file}'
            dirname = path.dirname(result_path)
            os.makedirs(dirname, exist_ok=True)

            if not path.isfile(result_path) or os.stat(result_path).st_mtime < decoded_old_timestamps[file]:
                self._archive.fetch_file_path_to_target_file_path(
                    f'synced_directories/{self._key}', 
                    file, 
                    self._remote_job_id,
                    result_path
                )

    def _redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection
