import math
from threading import Thread
from multiprocessing import Process, Manager
from rich.progress import Progress

from console import *
from arg_parse import parse_args


def is_prime(num: int) -> bool:
    """
    Check if num is prime
    """
    if num == 1:
        return False
    elif num == 2:
        return True

    for i in range(1, math.ceil(num ** 0.5)):
        if i == 1:
            continue
        
        if num % i == 0:
            return False

    return True


def get_nums_list(min_num: int, max_num: int, process_count: int):
    if process_count == 1:
        return [
            [min_num, max_num]
        ]
    
    count_of_nums = max_num - min_num
    nums_per_worker = math.floor(count_of_nums / 8)
    rest = count_of_nums - ((process_count - 1) * nums_per_worker)

    lst = []
    start = min_num
    for i in range(process_count - 1):
        lst.append([
           start + 1,
           start + nums_per_worker
        ])
        start += nums_per_worker
    lst.append([
        max_num - rest,
        max_num
    ])
    return lst


def worker(start: int, end: int, primes):
    start = start + 1 if start % 2 == 0 else start
    end   = end   + 1 if end   % 2 == 0 else end
    
    for num in range(start, end, 2):
        if is_prime(num):
            primes.append(num)


def show_progress(primes, total):
    with Progress() as progress:
        task = progress.add_task("Calculating primes", total=total)
        while True:
            progress.update(len(primes))


def main():
    """
    Entry point
    """
    args = parse_args()

    manager = Manager()
    primes = manager.list()
    
    processes = []
    nums_list = get_nums_list(args.min, args.max, args.process_count)

    for i in range(args.process_count):
        processes.append(
            Process(
                target=worker,
                args=(
                        nums_list[i][0],
                        nums_list[i][1],
                        primes
                )
            )
        )

    if args.bar:
        updater = Thread(
            target=show_progress,
            args=(primes, args.max - args.min),
            daemon=True
        )
        updater.start()

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print(primes.sort())


if __name__ == "__main__":
    main()
