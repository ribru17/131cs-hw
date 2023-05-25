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
