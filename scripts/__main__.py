from arg_parse import parse_args
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


def get_nums_list(min_num: int, max_num: int, process_count: int, score_based: bool = False) -> list:
    if score_based:
        # Setup nums
        min_num = min_num
        max_num = max_num + 1
        process_count = process_count
        count_of_nums = max_num - min_num

        max_score = 0
        for i in range(count_of_nums + 1):
            max_score += i

        score_per_worker = int(max_score / process_count)
        rest = max_score - ((process_count - 1) * score_per_worker)

        out = []

        num = min_num + 1
        for p_num in range(process_count - 1):
            score = 0
            start = num
            while True:
                score += num
                num += 1
                if score >= score_per_worker:
                    out.append([
                        start,
                        num,
                        score,
                        num - start
                    ])
                    num += 1
                    break
                elif num > max_num:
                    break

        out.append([
            out[-1][1],
            count_of_nums,
            rest,
            count_of_nums - out[-1][1]
        ])

        return out

    else:
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

    print(f"Calculating all primes from {args.min} to {args.max}")
    print(f"Process Count: {args.process_count}")

    queue = Queue()
    primes = []

    nums = get_nums_list(args.min, args.max, args.process_count, args.score_based)
    if nums == None:
        print("Number of workers to high")
        exit(1)
    for num in nums:
        print(num[-1])

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
        print("Sorting list...")
        primes.sort()
    
    if not args.no_output:
        print("Generating out string...")
        string = ""

        for prime_i in tqdm(range(len(primes))):
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

