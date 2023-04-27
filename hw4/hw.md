# 1

## a)

`Fractional` is a supertype of `Float`. `Int` and `Integer` are subtypes of the
`Integral` type and `Int` is also a subtype of `Integer` since `Int` is bounded
to a certain amount of bits while `Integer` is unbounded. All of these are
subclasses of `Num`.

## b)

In Haskell, `div` and `mod` are only allowed for members of the `Integral`
supertype (in other words, integer variants like `Int` and `Integral`). This is
because they perform integer operations like truncated division and modulo.
`(+)` is under no such constraints and is thus implemented for all subtypes of
`Num`, including fractional (floating point) numbers.

## c)

In C++, `float` is a supertype of `const float` since it allows all of the same
operations as float, as well as the addition assignment operation which a
`const float` does not allow since it must remain constant. The same
relationship holds for `int` and `const int`. `const float` and `const int` are
unrelated (so it follows that `float` and `int` are unrelated as well.)
