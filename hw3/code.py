from functools import reduce


def convert_to_decimal(bits):
    exponents = range(len(bits)-1, -1, -1)
    nums = [bit * (2 ** exp) for bit, exp in zip(bits, exponents)]
    return reduce(lambda acc, num: acc + num, nums)


def parse_csv(lines):
    return [(y[0], int(y[1])) for y in [x.split(',') for x in lines]]


def unique_characters(sentence):
    return {c for c in sentence}


def squares_dict(lower_bound, upper_bound):
    return {x: x**2 for x in range(lower_bound, upper_bound+1)}


def strip_characters(sentence, chars_to_remove):
    return "".join([x for x in sentence if x not in chars_to_remove])


class Duck:
    def __init__(self):
        pass  # Empty initializer


class Squid:
    def __init__(self):
        pass

    def quack(self):
        print("Squid")


class Dack(Duck):
    def __init__(self):
        pass


def is_duck_a(duck):
    try:
        duck.quack()
        return True
    except:
        return False


def is_duck_b(duck):
    return isinstance(duck, Duck)


def largest_sum(nums, k):
    if k < 0 or k > len(nums):
        raise ValueError
    elif k == 0:
        return 0

    max_sum = None
    for i in range(len(nums)-k+1):
        sum = 0
        for num in nums[i:i+k]:
            sum += num
        if max_sum is None or sum > max_sum:
            max_sum = sum
    return max_sum
