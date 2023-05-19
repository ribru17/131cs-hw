*KNOWN BUGS*

`null` is essentially untyped meaning that you can take a `null` returned
value from a function with a return type of some class, and assign it to any
other class regardless of whether the intended return type is or extends that
class.
