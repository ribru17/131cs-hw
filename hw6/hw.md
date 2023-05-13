# 1.

## a)

With pass by value, this program would print:

```
baz
bar
1
```

## b)

With pass by reference, this program would print:

```
baz
bar
4
```

## c)

With pass by object reference, this program would print:

```
baz
bar
1
```

## d)

With pass by need, this program would print:

```
bar
1
```

# 2.

A benefit of the `Optional` approach is improved programmer experience: you know
that the function returns an optional based on the function signature. This
enables the LSP to give you more intelligent autocompletion and error / type
checking. With the second option, you only know that an `int` is returned from
the function: you don't know if the function returns `-1`, throws an exception,
or does anything different when/if the value is not found. You would have to
spend time looking at the function logic to determine this behavior. Users of
the `Optional` method must only handle two cases: the `Optional` contains a
value or the `Optional` contains `nullptr`. Users of the exception throwing
method may assume the value given back is always valid, so long as they have a
catcher around the function just in case it is not. This is more dangerous
because the `Optional` value must always be "unboxed" from the `struct`, meaning
the programmer must always consciously be aware that their return value being
vaild is not guaranteed. With the exception method, the value given back is
always an `int` that, according to intuition (and your LSP) can always be used
normally where any other `int` can be used, so it can be easy to call the
function and accidentally forget that you need to set up a catcher for it just
in case. I would say that given all of this the `Optional` is more suitable for
this use case, as it seems most idiomatic given that the function has only two
possible states: "has it" and "doesn't have it".

# 3.

## a)

```
catch 2
I'm done!
that's what I say
Really done!
```

## b)

```
catch 1
hurray!
I'm done!
that's what I say
Really done!
```

## c)

```
catch 1
hurray!
I'm done!
that's what I say
Really done!
```

## d)

```
catch 3
Really done!
```

## e)

```
hurray!
I'm done!
that's what I say
Really done!
```
