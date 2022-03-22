from argparse import ArgumentParser, ArgumentTypeError
from os import cpu_count


def p_count(arg: str):
    if arg == "max":
        return cpu_count()
    else:
        try:
            arg = int(arg)
        except ValueError:
            raise ArgumentTypeError("Process Count needs to be either a number or 'max'")

        if arg > cpu_count():
            raise ArgumentTypeError(f"Process Count is above the max of {cpu_count()}")
        elif arg < 1:
            raise ArgumentTypeError(f"Process Count needs to be above zero")

        return arg



def parse_args():
    """
    Parse given command line arguments
    """
    parser = ArgumentParser(
        description="Argument Parser"
    )

    parser.add_argument(
        "--min",
        default=10,
        type=int,
        help="Min number"
    )

    parser.add_argument(
        "--max",
        default=10000000,
        type=int,
        help="Max number"
    )

    parser.add_argument(
        "-p", "--process-count",
        default=cpu_count(),
        type=p_count,
        help="Number of processes"
    )

    parser.add_argument(
        "--bar",
        action="store_true",
        help="Show progress bar"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = vars(parse_args())

    for arg in args:
        print(f"{arg}: {args[arg]}")
