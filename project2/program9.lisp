(class living
       (field string name "jesse")
       (method string foo ((string i)) (return (+ name i)))
       )

(class person inherits living
       (method string bar () (return (call me foo "10")))
       )

(class student inherits person
       (method string foo ((string i)) (return (+ i "5")))
       )

(class main
       (field person s null)
       (method void main ()
               (begin
                 (set s (new student))
                 (print (call s bar))
                 )
               )
       )

# should output "105"
