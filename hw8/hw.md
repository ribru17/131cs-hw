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
