# 1.

## a)

- Interface `A` has no supertypes
- Interface `B` has a supertype of `A`
- Interface `C` has a supertype of `A`
- Class `D` has a supertype of `A`, `B`, and `C`
- Class `E` has a supertype of `A` and `C`
- Class `F` has a supertype of `A`, `B`, `C`, and `D`
- Class `G` has a supertype of `A` and `B`

## b)

The `foo` function can be given classes `D`, `F`, and `G` since they all
implement `B`.

## c)

This will not work because `A` is not guaranteed to implement all the methods of
`C`, since `C` is a subtype of `A` and not the other way around.

# 3.

- Inheritance
  - Objects derive from base classes and inherit their base implementation of
    certain methods. These methods can be overridden if needed.
- Subtype polymorphism
  - Objects derive from interfaces that define which methods must be
    implemented. Nothing is inherited since the interfaces themselves provide
    only definitions (not implementations) so these methods must still be
    implemented by the derived class.
- Dynamic dispatch
  - This is a method of finding which function to call when a given class (given
    as a parameter for instance) could potentially have derived members whose
    methods should be prioritized over the base class methods. Inheritance and
    subtype polymorphism often make use of dynamic dispatch.

# 4.

We cannot use subtype polymorphism in a dynamically-typed language because
subtype polymorphism involves contracts that certain classes will implement
certain methods, thus implementing the interface as a whole. This doesn't make
sense in dynamically-typed programming languages because we wouldn't specify
variables or parameters as an interface type because they would not be given a
type at all (at compile time): subtype polymorphism is redundant and not
necessary since we will always use duck typing to check whether methods exist in
a class anyway.

We can, however, use dynamic dispatch in dynamically-typed languages. This is
because we always need to check (at runtime) for possible methods that exist in
the base class of a given derived class, as no such information is stored prior
to runtime. So dynamically-typed languages must use duck typing to call methods,
which makes use of dynamic dispatch.
