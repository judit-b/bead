from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

from .test import TestCase
from . import archive as m

import os
import zipfile

from . import layouts


class Test_Archive(TestCase):

    def test_extract_file(self):
        self.given_a_bead()
        self.when_file1_is_extracted()
        self.then_file1_has_the_expected_content()

    def test_extract_dir(self):
        self.given_a_bead()
        self.when_a_directory_is_extracted()
        self.then_directory_has_the_expected_files()
        self.then_file1_has_the_expected_content()

    def test_extract_nonexistant_dir(self):
        self.given_a_bead()
        self.when_a_nonexistent_directory_is_extracted()
        self.then_an_empty_directory_is_created()

    def test_content_hash(self):
        self.given_a_bead()
        self.when_content_hash_is_checked()
        self.then_content_hash_is_a_string()

    # implementation

    __bead = None
    __extractedfile = None
    __extracteddir = None
    __content_hash = None

    def given_a_bead(self):
        self.__bead = self.new_temp_dir() / 'bead.zip'
        z = zipfile.ZipFile(self.__bead, 'w')
        z.writestr(layouts.Archive.BEAD_META, b'{}')
        z.writestr('somefile1', b'''somefile1's known content''')
        z.writestr('path/file1', b'''?? file1's known content''')
        z.writestr('path/to/file1', b'''file1's known content''')
        z.writestr('path/to/file2', b'''file2's known content''')
        z.writestr(layouts.Archive.CHECKSUMS, b'some checksum')
        z.close()

    def when_file1_is_extracted(self):
        self.__extractedfile = self.new_temp_dir() / 'extracted_file'
        bead = m.Archive(self.__bead)
        bead.extract_file('path/to/file1', self.__extractedfile)

    def then_file1_has_the_expected_content(self):
        with open(self.__extractedfile, 'rb') as f:
            self.assertEquals(b'''file1's known content''', f.read())

    def when_a_directory_is_extracted(self):
        self.__extracteddir = self.new_temp_dir() / 'destination dir'
        bead = m.Archive(self.__bead)
        bead.extract_dir('path/to', self.__extracteddir)
        self.__extractedfile = os.path.join(self.__extracteddir, 'file1')

    def then_directory_has_the_expected_files(self):
        self.assertEquals(
            {'file1', 'file2'},
            set(os.listdir(self.__extracteddir))
        )

    def when_content_hash_is_checked(self):
        bead = m.Archive(self.__bead)
        self.__content_hash = bead.content_hash

    def then_content_hash_is_a_string(self):
        self.assertIsInstance(self.__content_hash, ''.__class__)

    def when_a_nonexistent_directory_is_extracted(self):
        self.__extracteddir = self.new_temp_dir() / 'destination dir'
        bead = m.Archive(self.__bead)
        bead.extract_dir('path/to/nonexistent', self.__extracteddir)

    def then_an_empty_directory_is_created(self):
        self.assertTrue(os.path.isdir(self.__extracteddir))
        self.assertEquals([], os.listdir(self.__extracteddir))