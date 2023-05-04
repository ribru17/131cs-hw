from math import sqrt


def nth_fibonacci(n: int) -> int:
    phi = (1 + sqrt(5))/2
    psi = (1 - sqrt(5))/2
    return int((phi**n - psi**n)/sqrt(5))


print(nth_fibonacci(15))

a = False
if a:
    p = 'hi'
else:
    p = 'yo'


print(p)
