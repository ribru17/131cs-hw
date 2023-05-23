# 1.

## a)

The template approach is nice because everything is generated at compile time,
and thus it leads to faster runtime performance. This would affect compilation
time, however, as well as code size, since templates generate a version of the
code for each type needed. Templates also have clear errors since they apply to
statically-typed programming languages.

## b)

The generics approach is good because it creates less code (types are
substituted at runtime) and thus helps to reduce compilation time. This could
perhaps negatively affect runtime compared to the template approach, however I
think this would be negligible. Errors are also still clear as this approach
also applies to statically-typed languages.

## c)

The duck typing approach is used for dynamically-typed languages, since no types
are checked until runtime, specifically not until the very moment a method /
property is needed. Since this creates more of a runtime it is a bit slower than
the previous two methods, but it is nice for simplicity as you don't need to be
as thorough in ensuring types if you, say, just want to write a quick and dirty
Python program. It is also nice because not much extra code is needed to get
this implementation working. Due to the less strict nature, however, duck typing
is inherently more error-prone, and errors are usually less readable.

# 2.

Dynamically-typed languages can't support parametric polymorphism because they
don't need to. No types are kept track of at compile time (and there usually is
no "compile time"), meaning that the only way to validate whether a property or
method exists on a certain object is for the program to check that right before
it is accessed at runtime, throwing an error if it is not (i.e., duck typing).

# 3.

I think you could create something similar to duck typing by essentially making
each class inherit from some master generic definition that defines each method,
but by default makes them throw some sort of type error. Then if any class wants
to actually implement these functions, it will do so and these derived versions
will be called and no type errors thrown if they are implemented. In that way
each function gets its method called regularly, unless it was not implemented in
which case a type error is thrown (like duck typing). The only difference is
that only defined methods can be called: duck typing allows you to call any made
up method that doesn't exist anywhere (to you demise) while the hacky generic
approach will only allow to call those methods specified in the hypothetical
master generic specification.
