# hash_app

`hash_app` is a command-line program that stores text in file-based hash buckets. It uses Python 3.8 or later and the standard library.

## Run

From the repository directory, run:

```sh
python hash_app.py 5 20
```

Use `python3` instead if that is your Python command. Both arguments must be positive integers. The first is the number of buckets, `n`. The second is the maximum characters per file, `s`. Type a string and press Enter. Use Ctrl+C to quit. End-of-input also stops the program, so input can be piped in. Empty lines are skipped.

## Hashing

The program computes CRC-32 with the standard-library function `zlib.crc32` on the input's UTF-8 bytes. It uses `(hash % n) + 1` to select one of the buckets numbered 1 through `n`. Different strings can land in the same bucket.

## Files and overflow

Each configuration stores its files in `buckets/<n>-<s>/` under the current working directory. The primary files are `1.txt` through `n.txt`. Each file holds up to `s` Unicode code points. The program appends text without adding separators.

The filenames link each bucket to its overflow chain. For bucket 3, the order is `3.txt`, `3.1.txt`, `3.2.txt`, and so on. Appends start in the last file in that chain. When it fills, the next numbered file is created as soon as there is more text to write. One input can span multiple files.

For example, with `n=1` and `s=4`, entering `Hello` and then `World` produces `Hell` in `1.txt`, `oWor` in `1.1.txt`, and `ld` in `1.2.txt`.

For each input, the program follows the numbered filenames to the last file and reads its length to see how much space is left. Restarting with the same arguments resumes the existing chains. Use one process per configuration directory at a time.
