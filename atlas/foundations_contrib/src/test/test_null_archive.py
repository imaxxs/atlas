
from foundations_spec import *

from foundations_contrib.null_archive import NullArchive

class TestNullArchive(Spec):

    @let
    def file_path(self):
        return self.faker.file_path()

    @let
    def prefix(self):
        return self.faker.uuid4()

    def test_list_files_always_returns_empty_list(self):
        archive = NullArchive()
        self.assertEqual([], archive.list_files(self.file_path, self.prefix))

    def test_list_files_without_prefix_always_returns_empty_list(self):
        archive = NullArchive()
        self.assertEqual([], archive.list_files(self.file_path))