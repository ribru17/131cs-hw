(class noder
    (method void hi () (print "HI"))
)
(class yo
    (method void hi () (print "HI"))
    (method yo getme () (return me))
     (method void f ((string x)) (print x))
)
(class foo inherits yo
 (method void f ((int x)) (print (+ 1 x)))
)
(class bar inherits foo
 (method bar getme () (return))
)

(class main
 (field bar b null)
 (field yo y null)
 (field noder n null)
 (field int inty 2)
 (field string str "")
 (method void bro ((int q)) (print q))
 (method bar create () (print "created"))
 (method noder create2 () (print "created"))
 (method yo create3 () (print "created"))
 (method foo test () (return (new foo)))
 (method void main ()
   (begin
      #(set b (call me create))
      #(set y (call me create))
      #(set b (call me create2))
      #(set b (new yo))
      #(call b hi)
      #(inputs str)
      #(print (+ "HELLO " str))
      #(print "yo")
      #(set b (new bar))
      #(call b f "hey")
      #(print (== (call me create2) (call me create)))
      #(print (== (call me create) (call me create2) ))
      #(print (==  (new yo) (call me create2) ))
      #(print (==  (call me create3) (call me create)))
   )
 )
)
