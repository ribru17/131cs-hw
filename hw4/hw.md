# 1.

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

# 2.

## a)

This language is dynamically typed because we initially have the variable
`user_id` holding a value that is a string and then later we convert it to an
integer, meaning that the type of the variable changes during runtime (or really
it means that the variable does not have a type and that it holds a value whose
type changes at runtime).

## b)

This language seems to use a scoping strategy where variables are not bound to
their block scope (e.g. if they are defined in an `if` statement they can be
accessed outside of that statement) but rather variables are bound to their
function scope (they can only be used in the function they are defined in). This
is somewhat similar to languages I've used before but slightly different in that
I would've expected the `x = 1` line to either set a global variable `x` or
perhaps mutate the previous definition of `x` (if it was still in scope after
being defined in the previous function).

## c)

This language uses block scoping strategies and defines closures within curly
brackets. Variables can be shadowed and redeclared in nested scopes. This is
similar to other languages I've used in that variables are scoped to the block
they are defined in. It is maybe slightly different in that it can define a
closure/block without any real reason (i.e. the closure in the example is not
part of a conditional statement or loop or something).

## d)
