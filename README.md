# hash_app

A file-based hash bucket application written in Python.

## Run

Install Python 3.8 or later. From the cloned repository directory, create a virtual environment

```sh
python -m venv .venv
```

Activate it with `.venv\Scripts\Activate.ps1` in Windows PowerShell, or `source .venv/bin/activate` on Linux/macOS. Then install and run

```sh
python -m pip install .
hash_app 5 20
```

Use `python3` if needed when creating the environment. Installation includes the xxHash dependency. You can also run `python hash_app.py 5 20` after installation.

The first argument is the number of buckets (`n`), and the second is the maximum Unicode characters per file (`s`). Both must be positive integers. Enter strings one at a time. Press Ctrl+C to quit. Empty lines are skipped, and end-of-input also exits.

## Hashing

The application uses the xxHash algorithm (XXH64, seed 0) through the Python `xxhash` library on the UTF-8 input. The bucket number is `(hash % n) + 1`, giving filenames from `1.txt` to `n.txt`. Collisions are allowed, and strings are stored without separators.

## Overflow files

Files are stored in `buckets/<n>-<s>/`. Each bucket starts with `1.txt`, `2.txt`, and so on.

Overflow files use consecutive names such as `3.txt`, `3.1.txt`, `3.2.txt`. These names form the reference chain. The program finds the last file before writing and creates the next file when the current one is full. Long inputs can span several files. Restarting with the same arguments continues the existing files.

For example, with `n=1` and `s=4`, entering `Hello` and then `World` stores `Hell` in `1.txt`, `oWor` in `1.1.txt`, and `ld` in `1.2.txt`.

## Tests

```sh
python -m unittest -v
```
