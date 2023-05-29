*KNOWN BUGS*

No proper type checking occurs for templates that have, for example, a field
that references its own type (such as a linked list template) where the field
has a malformed type (e.g. foo@int@int template has a field of type foo@int)
