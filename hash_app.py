import argparse
from pathlib import Path
from zlib import crc32


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main():
    parser = argparse.ArgumentParser(prog="hash_app")
    parser.add_argument("n", type=positive_int, help="number of buckets")
    parser.add_argument("s", type=positive_int, help="capacity in characters")
    args = parser.parse_args()

    directory = Path("buckets") / f"{args.n}-{args.s}"
    directory.mkdir(parents=True, exist_ok=True)
    for bucket in range(1, args.n + 1):
        (directory / f"{bucket}.txt").touch(exist_ok=True)

    try:
        while True:
            text = input("Please enter the string: ")
            bucket = crc32(text.encode("utf-8")) % args.n + 1
            path = directory / f"{bucket}.txt"
            with path.open("a", encoding="utf-8", newline="") as file:
                file.write(text)
            print(f"{text} added to {path.name}")
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    main()
