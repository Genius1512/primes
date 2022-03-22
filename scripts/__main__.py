from arg_parse import parse_args
from console import *

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
    if start <= 2 <= end: out.append(2)

    if start % 2 == 0:
        start += 1

    if pos == None:
        for num in range(start, end + 1, 2):
            if is_prime(num):
                out.append(num)
    
    else:
        for num in tqdm(range(start, end + 1, 2), desc=f"{pos + 1} ", position=pos, unit="Primes"):
            if is_prime(num):
                out.append(num)

    return out


def get_nums_list(min_num, max_num, process_count):
    if process_count == 1:
        return [[min_num, max_num]]
    
    count_of_nums = max_num - min_num
    nums_per_worker = math.floor(count_of_nums / process_count)
    if nums_per_worker <= 1:
        return None

    rest = count_of_nums - (nums_per_worker * (process_count - 1)) + 1

    start = min_num
    lst = []
    for i in range(process_count - 1):
        lst.append([
            start + 1,
            start + nums_per_worker
        ])
        start += nums_per_worker
    lst.append([
        max_num - rest + 2,
        max_num
    ])
    Console.print(lst)
    return lst


def worker(id: int, start: int, end: int, q: Queue):
    q.put(get_primes(start, end, id))


def main():
    """
    Entry point
    """
    args = parse_args()

    Console.success(f"Calculating all primes from {args.min} to {args.max}")
    Console.success(f"Process Count: {args.process_count}")

    queue = Queue()
    primes = []

    nums = get_nums_list(args.min, args.max, args.process_count)
    if nums == None:
        Console.error("Number of workers to high")
        exit(1)

    processes: list[Process] = []
    for i in range(args.process_count):
        if not args.bar:
            id = None
        else:
            id = i

        processes.append(Process(
            target=worker,
            args=(id, nums[i][0], nums[i][1], queue)
        ))

    start_time = perf_counter()

    for p in processes:
        p.start()
    for p in processes:
        primes += queue.get()
    for p in processes:
        p.join()

    end_time = perf_counter()
    
    if args.sort:
        Console.print("Sorting list...")
        primes.sort()
    
    Console.print("Generating out string...")
    if not args.no_output:
        string = ""

        for prime in primes:
            string += f"{prime}\n"

        string += f"""\nCalculated {len(primes)} Primes
Ran for {end_time - start_time} seconds"""
    
    else:
        string = f"""\nCalculated {len(primes)} Primes
Ran for {end_time - start_time} seconds"""
        
    if args.out == None:
        Console.print(string)

    else:
        with open(args.out, "w") as f:
            f.write(string)
        Console.print(f"Wrote to {args.out}")


if __name__ == "__main__":
    main()

