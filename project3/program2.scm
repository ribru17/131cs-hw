(class foo
 (method void bar ( ) (print "hello"))
)

(class main
  (method foo f () (return null))
  (method void main () 
    (let ((main x null))
      (set x (call me f))   # main type for x and foo type returned by function f are incompatible
      (print "reached bad")
    )
  )
)

