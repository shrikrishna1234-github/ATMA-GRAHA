import os
import unittest

class TestProjectStructure(unittest.TestCase):

    def test_directories_exist(self):
        """
        Tests that all the required directories exist.
        """
        dirs = [
            'bin',
            'src/core_engine',
            'src/cli_plane',
            'src/integrity_harness',
            'src/cipher_forge',
            'tests'
        ]
        for d in dirs:
            self.assertTrue(os.path.isdir(d), f"Directory {d} does not exist.")

    def test_files_exist(self):
        """
        Tests that all the required files exist.
        """
        files = [
            'README.md',
            'build.sh',
            'bin/atmagraha',
            'src/core_engine/main.cpp',
            'src/cli_plane/main.py',
            'src/integrity_harness/src/lib.rs',
            'src/cipher_forge/main.go',
            'tests/test_placeholder.py'
        ]
        for f in files:
            self.assertTrue(os.path.exists(f), f"File {f} does not exist.")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
