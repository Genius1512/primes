from sys import argv
from multiprocessing import Process, Queue
from os import cpu_count
from time import perf_counter


def is_prime(num, border):
    if num == 1:
        return False

    for i in range(2, border):
        if num == i:
            continue

        if num % i == 0:
            return False
    return True


def get_primes(start: int, end: int) -> list:
    start = start + 1 if start % 2 == 0 else start
    end = end + 1 if end % 2 == 0 else end

    out = []
    if start < 2 < end: out.append(2)

    for num in range(start, end, 2):
        if is_prime(num, int(end ** 0.5)):
            out.append(num)
    
    return out


def get_nums_list(max_num, process_count):
    if process_count == 1:
        return [max_num]

    rest = max_num % (process_count - 1)
    _max = max_num - rest
    one_element = int(_max / (process_count - 1))
    nums = []
    for _ in range(process_count - 1):
        nums.append(one_element)
    nums.append(rest)
    return nums


def handler(queue, start: int, end: int):
    queue.put(get_primes(start, end))


def main(args):
    try:
        max_num = int(args[1])
    except IndexError:
        max_num = 100000

    try:
        process_count = args[2]
        if process_count == "max":
            process_count = cpu_count()
        else:
            process_count = int(process_count)
    except IndexError:
        process_count = 4

    print("Processes: " + str(process_count))
    print("Max number: " + str(max_num))

    queue = Queue()
    primes = []

    nums = get_nums_list(max_num, process_count)
    biggest = 0

    processes: list[Process] = []
    for i in range(process_count):
        processes.append(Process(
            target=handler,
            args=(queue, biggest + 1, biggest + nums[i])
        ))
        biggest += nums[i]

    start_time = perf_counter()

    for p in processes:
        p.start()
    for p in processes:
        primes += queue.get()
    for p in processes:
        p.join()

    end_time = perf_counter()

    for prime in primes:
        print(prime)

    print(f"""Finished in {end_time - start_time} seconds
Generated {len(primes)} prime numbers""")


if __name__ == "__main__":
    main(argv)
