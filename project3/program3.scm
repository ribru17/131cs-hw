(class main
 (field string hi "yoo")
 (field int inty 5)
 (method string ligma () (throw "ah"))
 (method string foo ((string sup))
   (begin
     (print "hello")
     #(throw "I ran into a problem!")
     (throw (+ sup " bye"))
     (print "goodbye")
   )
 )

 (method void bar ()
   (begin
     (print "hi")
     #(return (call me foo (call me ligma)) )
     (return (call me foo "yo"))
     (print "bye")
   )
 )

 (method void main ()
  (begin
    (try
	  # try running the a statement that may generate an exception
       (call me bar)      	  
       # only run the following statement if an exception occurs
       (print "I got this exception: " exception)  
       #(print "uh oh")
    )
    #(throw "bad")
    (print "reached the end")
  )
 )
)
