# 1.

Operations are done left-to-right. Those in parentheses are prioritized first,
then `AND` expressions then `OR` expressions. If an expression is part of a
disjunction (`OR`) and it evaluates to `true`, then break out early since we
know it to be true. If an expression is part of a conjunction (`AND`), and
evaluates to `false`, break out early as we know the value to be false.

# 2.

## a)

```python
    def __iter__(self):
        return self.generate_iter()

    def generate_iter(self):
        # find valid buckets
        for bucket in self.array:
            current_node = bucket
            # check all nodes of the current bucket
            while current_node is not None:
                yield current_node.value
                current_node = current_node.next
```

## b)

```python
class HashTable:
    def __iter__(self):
        return self.HTIterator(self.array)

    class HTIterator:
        def __init__(self, array):
            self.array = array
            self.curr_bucket = 0
            self.curr_node = self.array[self.curr_bucket]

        def __next__(self):
            # find next valid bucket
            while self.curr_node is None:
                self.curr_bucket += 1
                if self.curr_bucket >= len(self.array):
                    raise StopIteration
                self.curr_node = self.array[self.curr_bucket]

            # check all nodes of current bucket
            val = self.curr_node.value
            self.curr_node = self.curr_node.next
            return val
```

## c)

```python
myht = HashTable(20)
myht.insert(25)
myht.insert(47)
myht.insert(99)
myht.insert(1)
myht.insert(21)

for i in myht:
    print(i)

# PRINTS:
# 21
# 1
# 25
# 47
# 99
```

## d)

```python
myht_iter = myht.__iter__()

while True:
    try:
        val = myht_iter.__next__()
        print(val)
    except StopIteration:
        break
```

## e)

```python
def forEach(self, func):
    for i in self:
        func(i)
```

# 3.

## a)

`green`

## b)

`false`

## c)

`tomato` then `beet`

## d)

This will just list all facts in the order they are given, i.e.:

```
Q = celery,
R = green
Q = tomato,
R = red
Q = persimmon,
R = orange
Q = beet,
R = red
Q = lettuce,
R = green
```

# 4.

## a)

`likes_red(Q) :- likes(Q, F), color(F, red), food(F).`

## b)

`likes_foods_of_colors_that_menachen_likes(Q) :- likes(Q, F), food(F), color(F, C), likes(menachen, P), food(P), color(P, C).`