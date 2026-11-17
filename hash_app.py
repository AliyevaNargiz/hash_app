import argparse
from pathlib import Path
from zlib import crc32


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def bucket_path(directory, bucket, overflow):
    if overflow == 0:
        return directory / f"{bucket}.txt"
    return directory / f"{bucket}.{overflow}.txt"


def append_text(directory, bucket, capacity, text):
    overflow = 0
    while bucket_path(directory, bucket, overflow + 1).is_file():
        overflow += 1
    path = bucket_path(directory, bucket, overflow)
    available = max(0, capacity - len(path.read_text(encoding="utf-8")))

    written = []
    offset = 0
    while offset < len(text):
        if available == 0:
            overflow += 1
            path = bucket_path(directory, bucket, overflow)
            available = capacity
        end = min(offset + available, len(text))
        with path.open("a", encoding="utf-8", newline="") as file:
            file.write(text[offset:end])
        written.append(path.name)
        offset = end
        available = 0
    return written


def main():
    parser = argparse.ArgumentParser(prog="hash_app")
    parser.add_argument("n", type=positive_int, help="number of buckets")
    parser.add_argument("s", type=positive_int, help="capacity in characters")
    args = parser.parse_args()

    directory = Path("buckets") / f"{args.n}-{args.s}"
    directory.mkdir(parents=True, exist_ok=True)
    for bucket in range(1, args.n + 1):
        bucket_path(directory, bucket, 0).touch(exist_ok=True)

    try:
        while True:
            text = input("Please enter the string: ")
            if text == "":
                continue
            bucket = crc32(text.encode("utf-8")) % args.n + 1
            written = append_text(directory, bucket, args.s, text)
            print(f"{text} added to {', '.join(written)}")
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    main()
