from argparse import ArgumentParser, ArgumentTypeError
from os import cpu_count
from sys import argv


def process_count(arg: str):
    if arg == "max":
        return cpu_count()

    try:
        arg = int(arg)
    except ValueError:
        raise ArgumentTypeError("Could not convert to int")

    if 0 < arg <= cpu_count():
        return arg
    else:
        if not "--pforce" in argv:
            raise ArgumentTypeError(f"Needs to be between 1 and {cpu_count()}")
        else:
            return arg


def parse_args():
    """
    Parse given command line arguments
    """
    parser = ArgumentParser(description="Argument Parser")

    parser.add_argument("--min", type=int, default=1, help="Smallest number to test")

    parser.add_argument(
        "--max", type=int, default=1000000, help="Highest number to test"
    )

    parser.add_argument(
        "-p",
        "--process_count",
        type=process_count,
        default=cpu_count(),
        help="Amout of workers",
    )

    parser.add_argument(
        "--pforce",
        action="store_true",
        help="Allow process_count over max process_count",
    )

    parser.add_argument("--bar", action="store_true", help="Show progress bar")

    parser.add_argument("-o", "--out", help="File to write to")

    parser.add_argument("--no-output", action="store_true", help="Hide output")

    parser.add_argument("--sort", action="store_true", help="Sort primes by number")

    parser.add_argument(
        "--algo-name",
        default="num_based",
        choices=["score_based", "num_based"],
        help="Name of the distribution algorithm",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = vars(parse_args())

    for arg in args:
        print(f"{arg}: {args[arg]}")
