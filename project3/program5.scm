(tclass node (field_type othertype)
    (field node@field_type@othertype next null)
    (field field_type value)
    (method void set_val ((field_type v)) (set value v))
    (method field_type get_val () (return value))
    (method void set_next((node@field_type@othertype n)) (set next n))
    (method node@field_type get_next() (return next))
    # this should error ^^^
  )

  (class main
    (method void main ()
      (let ((node@int@int x null))
        (set x (new node@int))
        (call x set_val 5)
        (print (call x get_val))
      )
    )
  )
