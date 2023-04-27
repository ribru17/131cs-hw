from intbase import InterpreterBase
from bparser import BParser


class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)

    def run(self, program):
        result, parsed_program = BParser.parse(program)
        if result is True:
            print(parsed_program)
        else:
            print('Parsing failed. There must have been a \
mismatched parenthesis.')


class Variable():
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Value():
    def __init__(self, value_type, value):
        self.value_type = value_type
        self.value = value


class Function():
    def __init__(self, name, params, statements):
        self.name = name
        self.params = params
        self.statements = statements


class Statement():
    def __init__(self, statement_type):
        self.statement_type = statement_type


class ClassDefinition():
    def __init__(self, name, fields, methods):
        self.name = name
        self.fields = fields
        self.methods = methods


program = ['(class main',
           '(method hello_world () (print "hello world!"))',
           ')']

interpreter = Interpreter()
interpreter.run(program)
