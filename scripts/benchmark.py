from main import get_nums_list, worker
from os import cpu_count
from multiprocessing import Process, Queue
from time import perf_counter


def main():
    tests_count = 20
    min_num, max_num = 1, 10000000

    sb_times = []
    nb_times = []
    for alg in ["score_based", "num_based"]:
        print(f"Testing {alg}")
        for i in range(tests_count):
            print(f"Test n. {i}")
            primes = []
            queue = Queue()
            processes = []
            nums = get_nums_list(alg)(min_num, max_num, cpu_count())

            for i in range(cpu_count()):
                processes.append(
                    Process(target=worker, args=(None, nums[i][0], nums[i][1], queue))
                )

            start_time = perf_counter()

            for p in processes:
                p.start()
            for p in processes:
                primes += queue.get()
            for p in processes:
                p.join()

            end_time = perf_counter()
            if alg == "score_based":
                sb_times.append(end_time - start_time)
            else:
                nb_times.append(end_time - start_time)

    sb_avg = 0
    for time in sb_times:
        sb_avg += time
    sb_avg /= tests_count

    nb_avg = 0
    for time in nb_times:
        nb_avg += time
    nb_avg /= tests_count

    print(f"Score based avg: {sb_avg}")
    print(f"Num based avg: {nb_avg}")


if __name__ == "__main__":
    main()
