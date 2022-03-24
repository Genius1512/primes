from arg_parse import parse_args

import math
from multiprocessing import Process, Queue
from threading import Thread
from time import perf_counter
from rich import print


# globals
primes: list[int] = []
last_num: int = 0


def manager(inp: Queue, out: Queue, max_num: int):
    global primes
    global last_num

    while True:
        if last_num >= max_num:
            print("Manager done")
            out.put(-1)
            break
        
        out.put(last_num + 1)
        last_num += 1
        
        prime = inp.get()
        if prime != -1:
            primes.append(prime)


def worker(inp: Queue, out: Queue):
    while True:
        num = inp.get()
        if num == -1:
            print("Worker done")
            break
        if is_prime(num):
            out.put(num)
        else:
            out.put(-1)


def main():
    """
    Entry point
    """
    args = parse_args()

    print(f"""Calculating primes from {args.min} - {args.max}
Workers count: {args.process_count}""")

    # Vars setup
    last_num = args.min 

    managers: list[Thread] = []
    workers: list[Process] = []

    for i in range(args.process_count):
        manager_inp = Queue(1)
        manager_out = Queue(1)

        managers.append(Thread(
            target=manager,
            args=(manager_inp, manager_out, args.max)
        ))
        workers.append(Process(
            target=worker,
            args=(manager_out, manager_inp)
        ))

    start_time = perf_counter()

    for i in range(args.process_count):
        managers[i].start()
        workers[i].start()

    for i in range(args.process_count):
        managers[i].join()
        workers[i].join()

    end_time = perf_counter()

    print(f"""Done.
Calculated {len(primes)} primes
Ran for {end_time - start_time} seconds""")
    primes.sort()
    print(primes)


def is_prime(num: int) -> bool:
    if num == 1:
        return False
    elif num == 2:
        return True

    for i in range(2, math.ceil(num ** 0.5) + 1):
        if num % i == 0:
            return False

    return True


if __name__ == "__main__":
    main()
