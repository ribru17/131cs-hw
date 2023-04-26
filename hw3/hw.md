# 1.

```python
from functools import reduce
def convert_to_decimal(bits):
    exponents = range(len(bits)-1, -1, -1)
    nums = [bit * (2 ** exp) for bit, exp in zip(bits, exponents)]
    return reduce(lambda acc, num: acc + num, nums)
```

# 2.

## a)

```python
def parse_csv(lines):
  return [(y[0], int(y[1])) for y in [x.split(',') for x in lines]]
```

## b)

```python
def unique_characters(sentence):
    return {c for c in sentence}
```

## c)

```python
def squares_dict(lower_bound, upper_bound):
    return {x: x**2 for x in range(lower_bound, upper_bound+1)}
```