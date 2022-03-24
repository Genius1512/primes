from arg_parse import parse_args
import nums_list_algorithms as nla

# from console import *

import math
from sys import exit
from time import perf_counter
from tqdm import tqdm
from multiprocessing import Process, Queue


def is_prime(num: int) -> bool:
    if num == 1:
        return False
    elif num == 2:
        return False

    for i in range(2, math.ceil(num ** 0.5) + 1):
        if num % i == 0:
            return False

    return True


def get_primes(start: int, end: int, pos=None):
    out = []
    if start <= 2 <= end:
        out.append(2)

    if start % 2 == 0:
        start += 1

    if pos == None:
        for num in range(start, end + 1, 2):
            if is_prime(num):
                out.append(num)

    else:
        for num in tqdm(
            range(start, end + 1, 2), desc=f"{pos + 1} ", position=pos, unit="Primes"
        ):
            if is_prime(num):
                out.append(num)

    return out


def get_nums_list(algorithm_name: str):
    dct = {"score_based": nla.score_based, "num_based": nla.num_based}

    return dct[algorithm_name]


def worker(id: int, start: int, end: int, q: Queue):
    q.put(get_primes(start, end, id))


def main():
    """
    Entry point
    """
    args = parse_args()

    print(f"Calculating all primes from {args.min} to {args.max}")
    print(f"Process Count: {args.process_count}")

    queue = Queue()
    primes = []

    nums = get_nums_list(args.algo_name)(args.min, args.max, args.process_count)
    if nums == None:
        print("Number of workers to high")
        exit(1)

    processes: list[Process] = []
    for i in range(args.process_count):
        if not args.bar:
            id = None
        else:
            id = i

        processes.append(
            Process(target=worker, args=(id, nums[i][0], nums[i][1], queue))
        )

    start_time = perf_counter()

    print("Starting")
    for p in processes:
        p.start()
    for p in processes:
        primes += queue.get()
    for p in processes:
        p.join()

    end_time = perf_counter()

    if args.sort:
        print("Sorting list...")
        primes.sort()

    if not args.no_output:
        string = ""

        for prime_i in tqdm(range(len(primes)), desc="Generating out string..."):
            string += f"{primes[prime_i]}\n"

        string += f"""\nCalculated {len(primes)} Primes
Ran for {end_time - start_time} seconds"""

    else:
        string = f"""\nCalculated {len(primes)} Primes
Ran for {end_time - start_time} seconds"""

    if args.out == None:
        print(string)

    else:
        with open(args.out, "w") as f:
            f.write(string)
            print(f"Wrote to {args.out}")


if __name__ == "__main__":
    main()
