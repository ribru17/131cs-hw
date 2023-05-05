# 1.

## a)

Here `refCount` should be of type `int *` since we need this data to be shared
across all instances, thus we should only hold an address that can access to
update shared information.

## b)

```cpp
my_shared_ptr(int *ptr) {
    this->ptr = ptr;
    this->refCount = new int(1);
}
```

## c)

```cpp
my_shared_ptr(const my_shared_ptr &other) {
    this->ptr = other.ptr;
    this->refCount = other.refCount;
    (*this->refCount)++;
}
```

## d)

```cpp
~my_shared_ptr() {
    if (--(*this->refCount) == 0) {
        delete this->refCount;
        delete this->ptr;
    }
}
```

## e)

```cpp
my_shared_ptr &operator=(const my_shared_ptr &obj) {
    // don't do anything if we reassign to ourself
    if (&obj == this) {
        return *this;
    }
    // destruct the self
    this->~my_shared_ptr();

    // reinitialize self with the passed in obj, increment reference count
    this->ptr = obj.ptr;
    this->refCount = obj.refCount;
    (*this->refCount)++;
    return *this;
}
```

# 2.

## a)

We don't want to use a garbage collected language because:

a) If we use GC via reference counting, we must forfeit any (potentially
necessary) performance benefits from multithreading as multithreading can be
very problematic when using reference counting (data races in the reference
count). b) If we use mark and compact/sweep, we could be subject to long,
expensive calls to the GC that will cause our runtime to not perform as quick as
necessary and be potentially unpredictable.

## b)

I think Ava is mostly right because reference counting is quicker and more
predictable, though like I said earlier we would not be able to take advantage
of multithreading, and additionally we could suffer memory leaks if our asteroid
detecting program has cyclical references that would not be freed by our GC.

## c)

I would say that he should use C#, since mark-and-compact GC is less prone to
fragmentation since we regroup each block of memory into a contiguous segment,
rather than mark-and-sweep which just clears individual chunks, leaving gaps in
memory.

## d)

Since Go destructors may not run long after an object is unreachable (and may
not run at all!) I would advise Yvonne to implement her own manual socket
cleanup method that doesn't rely on a finalizer/destructor to run.
