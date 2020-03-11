
class ArtifactDownloader(object):

    def __init__(self, archiver):
        self._archiver = archiver
    
    def download_files(self, source_directory, download_directory):
        for file_path in self._artifact_file_list(source_directory):
            self._download_file(file_path, download_directory)

    def _artifact_file_list(self, source_directory):
        from fnmatch import fnmatch

        file_list = self._archiver.fetch_miscellaneous('job_artifact_listing.pkl')
        return [file_path for file_path in file_list if fnmatch(file_path, source_directory + '*') and not self._foundations_artifact(file_path)]

    def _foundations_artifact(self, file_path):
        from fnmatch import fnmatch
        from functools import reduce

        matchings = [
            'foundations*/*',
            'jobs/*',
            'model_serving/*',
            'venv/*',
            'template/*',
            'docker_image_version.sh',
            'download_gui_images.sh',
            'foundations_gui.sh',
            'foundations_package_manifest.yaml',
            'foundations_requirements.txt',
            'job.tgz',
            'run.env',
            'run.sh',
            '*.bin',
        ]

        file_matches = [fnmatch(file_path, match) for match in matchings]
        return reduce(lambda lhs, rhs: lhs or rhs, file_matches)

    def _download_file(self, file_path, download_directory):
        from os import makedirs
        from os.path import dirname

        target_path = download_directory + '/' + file_path
        directory = dirname(target_path)
        makedirs(directory, exist_ok=True)
        self._archiver.fetch_persisted_file(file_path, target_path)
