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
                super().error(ErrorType.SYNTAX_ERROR)
                return
            class_name = class_def[1]
            fields = []
            methods = []
            for item in class_def[2:]:
                if item[0] == InterpreterBase.FIELD_DEF:
                    fields.append(Variable(item[1], item[2]))
                elif item[0] == InterpreterBase.METHOD_DEF:
                    methods.append(
                        Method(item[1], item[2],
                               Statement(item[3][0], item[3][1:])))
                else:
                    super().error(ErrorType.SYNTAX_ERROR)
                    return
            self.classes.append(Class(class_name, fields, methods))

        self.__get_class(super().MAIN_CLASS_DEF).run_method(
            super().MAIN_FUNC_DEF)

    def __get_class(self, class_name):
        for class_def in self.classes:
            if class_def.name == class_name:
                return class_def

        return None


class Class():
    def __init__(self, name, fields, methods):
        self.name = name
        self.fields = fields
        self.methods = methods

    def run_method(self, method_name):
        self.__get_method(method_name).run()

    def __get_method(self, method_name):
        for method in self.methods:
            if method.name == method_name:
                return method

        return None

    def __str__(self):
        return (self.name + ' ' + str([str(x) for x in self.fields]) + ' ' +
                str([str(x) for x in self.methods]))


class Variable():
    def __init__(self, name, value):
        self.name = name
        self.value = Value(value)

    def __str__(self):
        return self.name + ' ' + str(self.value)


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
                InterpreterBase(self).error(ErrorType.SYNTAX_ERROR)
                return

    def __str__(self):
        return self.value_type + ' ' + str(self.value)


class Method():
    def __init__(self, name, params, statement):
        self.name = name
        self.params = params
        self.statement = statement

    def run(self):
        self.statement.run()

    def __str__(self):
        return self.name + ' ' + str(self.params) + ' ' + str(self.statement)


class Statement():
    def __init__(self, statement_type, params):
        self.statement_type = statement_type
        self.params = params

    def run(self):
        match self.statement_type:
            case InterpreterBase.BEGIN_DEF:
                print('TODO')
                print(self.params)
            case InterpreterBase.CALL_DEF:
                print('TODO')
            case InterpreterBase.IF_DEF:
                print('TODO')
            case InterpreterBase.INPUT_INT_DEF:
                print('TODO')
            case InterpreterBase.INPUT_STRING_DEF:
                print('TODO')
            case InterpreterBase.PRINT_DEF:
                value = self.__run_expression(self.params[0])
                if value.value_type == InterpreterBase.BOOL_DEF:
                    value = (InterpreterBase.TRUE_DEF if value.value
                             else InterpreterBase.FALSE_DEF)
                else:
                    value = value.value
                InterpreterBase(self).output(value)
            case InterpreterBase.RETURN_DEF:
                print('TODO')
            case InterpreterBase.SET_DEF:
                print('TODO')
            case InterpreterBase.WHILE_DEF:
                print('TODO')
            case _:
                InterpreterBase(self).error(ErrorType.SYNTAX_ERROR)

    def __run_expression(self, expr):
        if isinstance(expr, list):
            operator = expr[0]
            match operator:
                case '+':
                    lhs = self.__run_expression(expr[1])
                    rhs = self.__run_expression(expr[2])

                    if (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(lhs.value + rhs.value))
                    elif (lhs.value_type == InterpreterBase.STRING_DEF and
                          rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value('"{}"'.format(lhs.value + rhs.value))
                    else:
                        InterpreterBase(self).error(ErrorType.TYPE_ERROR)
                case '-' | '*' | '/' | '%':
                    lhs = self.__run_expression(expr[1])
                    rhs = self.__run_expression(expr[2])

                    if not (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        InterpreterBase(self).error(ErrorType.TYPE_ERROR)

                    return Value(str(int(
                        eval(str(self.__run_expression(expr[1]).value) +
                             operator +
                             str(self.__run_expression(expr[2]).value)))))
                case '<' | '<=' | '>' | '>=':
                    lhs = self.__run_expression(expr[1])
                    rhs = self.__run_expression(expr[2])

                    if (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower())
                    elif (lhs.value_type == InterpreterBase.STRING_DEF and
                            rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value(str(eval(
                            '"{}"{}"{}"'.format(lhs.value,
                                                operator, rhs.value))).lower())
                    else:
                        InterpreterBase(self).error(ErrorType.TYPE_ERROR)
                case '==' | '!=':
                    # TODO: should be able to compare null and object
                    lhs = self.__run_expression(expr[1])
                    rhs = self.__run_expression(expr[2])

                    if (lhs.value_type == InterpreterBase.STRING_DEF and
                            rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value(str(eval(
                            '"{}"{}"{}"'.format(lhs.value,
                                                operator, rhs.value))).lower())
                    # elif isinstance(lhs.value, None) and isinstance(rhs.value, str):
                    #     return Value(eval('"{}"{}"{}"'.format(lhs.value, operator, rhs.value)))
                    elif (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(eval(str(lhs.value) + operator + str(rhs.value))).lower())
                    else:
                        InterpreterBase(self).error(ErrorType.TYPE_ERROR)
        else:
            return Value(expr)


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
    # '(method main () (print (+ 99 80)))',
    # '(method main () (print (+ "hi" " there")))',
    # '(method main () (print (> "zi" "there")))',
    # '(method main () (print (> 99 -100)))',
    # '(method main () (print (> 99 true)))',
    # '(method main () (print (== "99" "990")))',
    '(method main () (print (!= 991 991)))',
    # '(method main () (print (+ 1 (* (- 99 96) (/ 900 100)))))',  # 28
    # '(method main () (print (+ 1 (* (- 99 "hi") (/ 900 100)))))',
    # '(method main () (print "hello world"))',
    # '    (method main () (begin',
    # '        (set guy (new other))',
    # '        (call guy hi)',
    # '    ))',
    ')'


]


interpreter = Interpreter()
interpreter.run(program)

# print(Value('null'))

# success, parsed_program = BParser.parse(program)
# print(parsed_program)

# try:
#     print(int('1b23'))
# except ValueError:
#     print('bad')
# mydict = {}
# print(mydict['hello'] or 'not here')
