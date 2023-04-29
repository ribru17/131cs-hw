from intbase import InterpreterBase, ErrorType
from bparser import BParser


class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)

    def run(self, program):
        result, parsed_program = BParser.parse(program)
        if result is False:
            super().error(ErrorType.SYNTAX_ERROR)
            return


class Variable():
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Value():
    def __init__(self, value_type, value):
        self.value_type = value_type
        self.value = value


class Method():
    def __init__(self, name, params, statements):
        self.name = name
        self.params = params
        self.statements = statements

    def run(self):
        for statement in self.statements:
            statement.run()


class Statement():
    def __init__(self, statement_type, params):
        self.statement_type = statement_type
        self.params = params

    def run(self):
        match self.statement_type:
            case InterpreterBase.BEGIN_DEF:
                print('TODO')
            case InterpreterBase.CALL_DEF:
                print('TODO')
            case InterpreterBase.IF_DEF:
                print('TODO')
            case InterpreterBase.INPUT_INT_DEF:
                print('TODO')
            case InterpreterBase.INPUT_STRING_DEF:
                print('TODO')
            case InterpreterBase.PRINT_DEF:
                print('TODO')
            case InterpreterBase.RETURN_DEF:
                print('TODO')
            case InterpreterBase.SET_DEF:
                print('TODO')
            case InterpreterBase.WHILE_DEF:
                print('TODO')


class Class():
    def __init__(self, name, fields, methods):
        self.name = name
        self.fields = fields
        self.methods = methods


# program = ['(class main',
#            '(method hello_world () (print "hello world!"))',
#            ')']

program = [
    '(class other',
    '(method hi () (print "hi"))',
    ')',
    '(class main',
    '(method hello_world () (print "hello world!"))',
    ')'
]


interpreter = Interpreter()
interpreter.run(program)
