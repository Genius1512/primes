import math


def score_based(min_num: int, max_num: int, process_count: int) -> list:
    if process_count == 1:
        return [[min_num, max_num]]
    max_num += 1
    count_of_nums = max_num - min_num
    
    max_score = 0
    for score in range(count_of_nums + 1):
        max_score += score

    score_per_worker = math.floor(max_score / process_count)
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
                    num
                ])
                num += 1
                break
            if num > max_num:
                break

    out.append([
        out[-1][1],
        count_of_nums,
    ])

    for i in range(2, process_count):
        divisor = i
        num = math.ceil((out[i - 2][1] - out[i - 2][0]) / divisor)
        out[i - 2][1] -= num
        try:
            out[i - 1][0] -= num
        except IndexError:
            pass

        print(f"{i - 2}: {divisor}/{out[i - 2][1]}/{out[i - 2][1] + num}")

    return out


def num_based(min_num: int, max_num: int, process_count: int) -> list:
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



if __name__ == "__main__":
    score_based(1, 1000, 2)
