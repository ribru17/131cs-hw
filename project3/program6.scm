(class person 
  (field string name "jane")
  (method void say_something () (print name " says hi"))
)

(class student inherits person
  (method void say_something ()
    (begin
     (print "first")
     (call super say_something)
     (print "second")
    )
  )
)

(class main
  (field person p null)
  (method void foo ((student s))
    (call s say_something))
  (method void main () 
    (begin 
      (set p (new student))
      (call me foo p)
    )
  )
)


