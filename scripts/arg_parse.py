from argparse import ArgumentParser


def parse_args():
    """
    Parse given command line arguments
    """
    parser = ArgumentParser(
        description="Argument Parser"
    )

    # add arguments here

    return parser.parse_args()


if __name__ == "__main__":
    args = vars(parse_args())

    for arg in args:
        print(f"{arg}: {args[arg]}")
