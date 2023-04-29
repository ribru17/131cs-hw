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

        self.classes = []
        for class_def in parsed_program:
            if class_def[0] != InterpreterBase.CLASS_DEF:
                print("BAD")
                return
            class_name = class_def[1]
            fields = []
            methods = []
            for item in class_def[2:]:
                if item[0] == InterpreterBase.FIELD_DEF:
                    fields.append(Variable(item[1], item[2]))
                elif item[0] == InterpreterBase.METHOD_DEF:
                    methods.append(Method())


class Variable():
    def __init__(self, name, value):
        self.name = name
        self.value = Value(value)


class Value():
    def __init__(self, value):
        if value == InterpreterBase.TRUE_DEF:
            self.value = True
            self.value_type = InterpreterBase.BOOL_DEF
        elif value == InterpreterBase.FALSE_DEF:
            self.value = False
            self.value_type = InterpreterBase.BOOL_DEF
        elif value == InterpreterBase.NULL_DEF:
            self.value_type = InterpreterBase.VOID_DEF
            self.value = None
        elif value[0] == value[-1] == '"':
            self.value_type = InterpreterBase.STRING_DEF
            self.value = value.strip('"')
        else:
            try:
                self.value = int(value)
                self.value_type = InterpreterBase.INT_DEF
            except ValueError:
                print('BAD VALUE')
                return


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
    '(field hif 4)',
    '(field hit 5)',
    '(method hi () (begin',
    '(print "hi")',
    '(print "hi")',
    '))',
    ')',
    '(class main',
    '(method hello_world () (print "hello world!"))',
    ')'
]


# interpreter = Interpreter()
# interpreter.run(program)
success, parsed_program = BParser.parse(program)
print(parsed_program)
# try:
#     print(int('1b23'))
# except ValueError:
#     print('bad')
