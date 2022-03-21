from argparse import ArgumentParser, ArgumentTypeError
from os import cpu_count


def max_number(num: str):
    try:
        num = int(num)
    except ValueError:
        raise ArgumentTypeError("Could not convert to number")

    if num < 10:
        raise ArgumentTypeError("Needs to be bigger than 10")

    return num


def process_count(num: str):
    try:
        num = int(num)
    except ValueError:
        raise ArgumentTypeError("Could not convert to number")

    if 0 < num <= cpu_count():
        return num
    else:
        raise ArgumentTypeError("To small or to big: 0 < num < cpu_count")


def parse_args():
    """
    Parse given command line arguments
    """
    parser = ArgumentParser(
        description="Argument Parser"
    )

    parser.add_argument(
        "-m", "--max",
        type=max_number,
        default=1000000,
        help="Max number"
    )

    parser.add_argument(
        "-p", "--process-count",
        type=process_count,
        default=cpu_count(),
        help="Process count"
    )

    parser.add_argument(
        "-b", "--bar",
        action="store_true",
        default=False,
        help="Show progress bar or not"
    )

    parser.add_argument(
        "-o", "--out",
        default=None,
        help="Out file"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = vars(parse_args())

    for arg in args:
        print(f"{arg}: {args[arg]}")
