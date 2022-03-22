from arg_parse import parse_args
from console import *

import math
from time import perf_counter
from tqdm import tqdm
from multiprocessing import Process, Queue


def is_prime(num: int, border: int) -> bool:
    if num == 1:
        return False
    elif num == 2:
        return False

    for i in range(2, border):
        if num % i == 0:
            return False

    return True


def get_primes(start: int, end: int, pos=None):
    start = start + 1 if start % 2 == 0 else start
    end = end + 1 if end %2 == 0 else end

    out = []
    if start < 2 < end: out.append(2)
    
    if pos != None:
        for num in tqdm(range(start, end, 2), desc=str(pos + 1), position=pos):
            if is_prime(num, int(end ** 0.5)):
                out.append(num)
    else:
        for num in range(start, end, 2):
            if is_prime(num, int(end ** 0.5)):
                out.append(num)

    return out


def get_nums_list(min_num, max_num, process_count):
    if process_count == 1:
        return [[min_num, max_num]]
    
    count_of_nums = max_num - min_num
    nums_per_worker = math.floor(count_of_nums / process_count)
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
    return lst


def worker(id: int, start: int, end: int, q: Queue):
    q.put(get_primes(start, end, id))


def main():
    """
    Entry point
    """
    args = parse_args()

    queue = Queue()
    primes = []

    nums = get_nums_list(args.min, args.max, args.process_count)
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
        primes.sort()

    if not args.no_output:
        string = ""
        for prime in primes:
            string += str(prime) + "\n"
        string += f"\nCalculated {len(primes)} primes\n"
        string += f"Ran for {end_time - start_time} seconds\n"

        if args.out == None:
            Console.success(string)
        else:
            with open(args.out, "w") as f:
                f.write(string)
    else:
        string = f"""\nCalculated {len(primes)} primes
Ran for {end_time - start_time} seconds"""
        if args.out == None:
            Console.success(string)
        else:
            with open(args.out, "w") as f:
                f.write(string)


if __name__ == "__main__":
    main()


