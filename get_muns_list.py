def get_nums_list(max_num, thread_count):
    rest = max_num % (thread_count - 1)
    _max = max_num - rest
    one_element = int(_max / (thread_count - 1))
    nums = []
    for i in range(thread_count - 1):
        nums.append(one_element)
    nums.append(rest)
    return nums


if __name__ == "__main__":
    print(get_nums_list(10000, 8))