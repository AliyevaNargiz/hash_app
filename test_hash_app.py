import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from zlib import crc32


APP = Path(__file__).with_name("hash_app.py").resolve()


class HashAppTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.buckets = self.directory / "buckets" / "1-4"

    def run_app(self, inputs):
        subprocess.run(
            [sys.executable, "-X", "utf8", str(APP), "1", "4"],
            cwd=self.directory,
            input=inputs,
            encoding="utf-8",
            capture_output=True,
            check=True,
        )

    def bucket_contents(self):
        return {
            path.name: path.read_text(encoding="utf-8")
            for path in self.buckets.glob("*.txt")
        }

    def test_overflow_preserves_order_and_character_limit(self):
        self.run_app("Hello\nWörld\n")
        self.assertEqual(
            self.bucket_contents(),
            {"1.txt": "Hell", "1.1.txt": "oWör", "1.2.txt": "ld"},
        )

    def test_restart_continues_at_last_overflow_file(self):
        self.run_app("Hello\n")
        self.run_app("World\n")
        self.assertEqual(
            self.bucket_contents(),
            {"1.txt": "Hell", "1.1.txt": "oWor", "1.2.txt": "ld"},
        )

    def test_multiple_buckets(self):
        inputs = ["Hello", "World", "Test", "  "]
        subprocess.run(
            [sys.executable, str(APP), "5", "20"],
            cwd=self.directory,
            input="\n".join(inputs) + "\n",
            encoding="utf-8",
            capture_output=True,
            check=True,
        )
        expected = {f"{bucket}.txt": "" for bucket in range(1, 6)}
        for text in inputs:
            bucket = crc32(text.encode("utf-8")) % 5 + 1
            expected[f"{bucket}.txt"] += text
        directory = self.directory / "buckets" / "5-20"
        actual = {
            path.name: path.read_text(encoding="utf-8")
            for path in directory.glob("*.txt")
        }
        self.assertEqual(actual, expected)

    def test_invalid_arguments(self):
        for arguments in [[], ["0", "4"], ["1", "-1"], ["x", "4"]]:
            with self.subTest(arguments=arguments):
                result = subprocess.run(
                    [sys.executable, str(APP), *arguments],
                    cwd=self.directory,
                    capture_output=True,
                )
                self.assertEqual(result.returncode, 2)
        self.assertFalse((self.directory / "buckets").exists())


if __name__ == "__main__":
    unittest.main()
