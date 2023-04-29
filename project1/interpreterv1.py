from intbase import InterpreterBase, ErrorType
from bparser import BParser


class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)

    def throw_err(type):
        super().error(type)

    def run(self, program):
        result, parsed_program = BParser.parse(program)
        if result is False:
            super().error(ErrorType.SYNTAX_ERROR)
            return

        self.classes = {}
        for class_def in parsed_program:
            if class_def[0] != InterpreterBase.CLASS_DEF:
                super().error(ErrorType.SYNTAX_ERROR)
                return
            class_name = class_def[1]

            # populate fields and classes
            fields = {}
            methods = {}
            for item in class_def[2:]:
                if item[0] == InterpreterBase.FIELD_DEF:
                    if item[1] in fields:
                        super().error(ErrorType.NAME_ERROR,
                                      "Duplicate field {}".format(item[1]))

                    fields[item[1]] = Variable(item[1], item[2])
                elif item[0] == InterpreterBase.METHOD_DEF:
                    if item[1] in methods:
                        super().error(ErrorType.NAME_ERROR,
                                      "Duplicate method {}".format(item[1]))

                    methods[item[1]] = Method(item[1], item[2],
                                              Statement(item[3][0],
                                                        item[3][1:]))
                else:
                    super().error(ErrorType.SYNTAX_ERROR)
                    return

            if class_name in self.classes:
                super().error(ErrorType.NAME_ERROR,
                              "Duplicate class {}".format(class_name))
            self.classes[class_name] = Class(class_name, fields, methods)

        self.get_class(super().MAIN_CLASS_DEF).run_method(
            super().MAIN_FUNC_DEF, super())

    def get_class(self, class_name):
        return self.classes[class_name]

    def __str__(self):
        return str([str(x) for x in self.classes])


class Class():
    def __init__(self, name='', fields={}, methods={}):
        self.name = name
        self.fields = fields
        self.methods = methods

    def run_method(self, method_name, base):
        self.get_method(method_name).run(self.fields, base)

    def get_method(self, method_name):
        return self.methods[method_name]

    def __str__(self):
        return (self.name + ' ' + str([str(x) for x in self.fields]) + ' ' +
                str([str(x) for x in self.methods]))


class Variable():
    def __init__(self, name, value):
        self.name = name
        # use empty list for fields because we cannot
        # initially set a field to a variable
        self.value = Value(value, [])

    def __str__(self):
        return self.name + ' ' + str(self.value)


class Value():
    def __init__(self, value, fields):
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
            except ValueError:  # otherwise it is a variable
                if value[0] != '_' and not value[0].isalpha():
                    InterpreterBase(self).error(ErrorType.SYNTAX_ERROR)

                # assign value from given variable list
                try:
                    self.value = fields[value].value.value
                    self.value_type = fields[value].value.value_type
                except KeyError:
                    # var doesn't exist
                    InterpreterBase(self).error(ErrorType.NAME_ERROR)
                except TypeError:
                    # cannot initialize var with other var!
                    InterpreterBase(self).error(ErrorType.TYPE_ERROR)

    def __str__(self):
        return self.value_type + ' ' + str(self.value)


class Method():
    def __init__(self, name, params, statement):
        self.name = name
        self.params = params
        self.statement = statement

    def run(self, fields, base):
        self.statement.run(fields, base)

    def __str__(self):
        return self.name + ' ' + str(self.params) + ' ' + str(self.statement)


class Statement():
    def __init__(self, statement_type, params):
        self.statement_type = statement_type
        self.params = params

    def run(self, vars, base):
        match self.statement_type:
            case InterpreterBase.BEGIN_DEF:
                for statement in self.params:
                    Statement(statement[0], statement[1:]).run(vars, base)
            case InterpreterBase.CALL_DEF:
                print('TODO')
            case InterpreterBase.IF_DEF:
                condition = self.__run_expression(self.params[0], vars, base)
                if condition.value_type != InterpreterBase.BOOL_DEF:
                    base.error(ErrorType.TYPE_ERROR)
                    # base.error(
                    #     ErrorType.TYPE_ERROR, "non-boolean if condition")

                if condition.value is True:
                    Statement(self.params[1][0],
                              self.params[1][1:]).run(vars, base)
                else:
                    if len(self.params) < 3:
                        return
                    elif len(self.params) == 3:
                        Statement(self.params[2][0],
                                  self.params[2][1:]).run(vars, base)
                    else:
                        base.error(
                            ErrorType.SYNTAX_ERROR, "Too many `if` branches")

            case InterpreterBase.INPUT_INT_DEF:
                input = base.get_input()
                try:
                    vars[self.params[0]].value = Value(input, vars)
                except KeyError:
                    base.error(
                        ErrorType.NAME_ERROR,
                        "Unknown variable {}".format(self.params[0]))
            case InterpreterBase.INPUT_STRING_DEF:
                input = base.get_input()
                try:
                    vars[self.params[0]].value = Value(
                        '"{}"'.format(input), vars)
                except KeyError:
                    base.error(
                        ErrorType.NAME_ERROR,
                        "Unknown variable {}".format(self.params[0]))
            case InterpreterBase.PRINT_DEF:
                out_string = ''
                for param in self.params:
                    value = self.__run_expression(param, vars, base)
                    if value.value_type == InterpreterBase.BOOL_DEF:
                        value = (InterpreterBase.TRUE_DEF if value.value
                                 else InterpreterBase.FALSE_DEF)
                    else:
                        value = value.value
                    out_string += str(value)

                base.output(out_string)
            case InterpreterBase.RETURN_DEF:
                print('TODO')
            case InterpreterBase.SET_DEF:
                vars[self.params[0]].value = self.__run_expression(
                    self.params[1], vars, base)
            case InterpreterBase.WHILE_DEF:
                condition = self.__run_expression(self.params[0], vars, base)
                if condition.value_type != InterpreterBase.BOOL_DEF:
                    base.error(
                        ErrorType.TYPE_ERROR, "Non-boolean while condition")
                while condition.value is True:
                    Statement(self.params[1][0],
                              self.params[1][1:]).run(vars, base)
                    condition = self.__run_expression(
                        self.params[0], vars, base)
            case _:
                base.error(ErrorType.SYNTAX_ERROR)

    def __run_expression(self, expr, vars, base):
        if isinstance(expr, list):
            operator = expr[0]
            match operator:
                case '+':
                    lhs = self.__run_expression(expr[1], vars, base)
                    rhs = self.__run_expression(expr[2], vars, base)

                    if (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(lhs.value + rhs.value), vars)
                    elif (lhs.value_type == InterpreterBase.STRING_DEF and
                          rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value('"{}"'.format(lhs.value + rhs.value),
                                     vars)
                    else:
                        base.error(ErrorType.TYPE_ERROR)
                case '-' | '*' | '/' | '%':
                    lhs = self.__run_expression(expr[1], vars, base)
                    rhs = self.__run_expression(expr[2], vars, base)

                    if not (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        base.error(ErrorType.TYPE_ERROR)

                    return Value(str(int(
                        eval(str(lhs.value) +
                             operator +
                             str(rhs.value)))), vars)
                case '<' | '<=' | '>' | '>=':
                    lhs = self.__run_expression(expr[1], vars, base)
                    rhs = self.__run_expression(expr[2], vars, base)

                    if (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(), vars)
                    elif (lhs.value_type == InterpreterBase.STRING_DEF and
                            rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value(str(eval(
                            '"{}"{}"{}"'.format(lhs.value,
                                                operator, rhs.value))).lower(),
                                     vars)
                    else:
                        base.error(ErrorType.TYPE_ERROR)
                case '==' | '!=':
                    # TODO: should be able to compare null and object
                    lhs = self.__run_expression(expr[1], vars, base)
                    rhs = self.__run_expression(expr[2], vars, base)

                    if (lhs.value_type == InterpreterBase.STRING_DEF and
                            rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value(str(eval(
                            '"{}"{}"{}"'.format(lhs.value,
                                                operator, rhs.value))).lower(),
                                     vars)
                    elif (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(), vars)
                    elif (lhs.value_type == InterpreterBase.BOOL_DEF and
                            rhs.value_type == InterpreterBase.BOOL_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(), vars)
                    else:
                        base.error(ErrorType.TYPE_ERROR)
                case '&' | '|':
                    lhs = self.__run_expression(expr[1], vars, base)
                    rhs = self.__run_expression(expr[2], vars, base)

                    if (lhs.value_type == InterpreterBase.BOOL_DEF and
                            rhs.value_type == InterpreterBase.BOOL_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(), vars)
                    else:
                        base.error(ErrorType.TYPE_ERROR)
                case '!':
                    lhs = self.__run_expression(expr[1], vars, base)
                    if lhs.value_type == InterpreterBase.BOOL_DEF:
                        return Value(str(not lhs.value).lower(), vars)
                    else:
                        base.error(ErrorType.TYPE_ERROR)

        else:
            return Value(expr, vars)


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
    # '(method main () (print (!= false false)))',
    # '(method main () (print (! false)))',
    '(field myfield 92)',
    '(field strfild "helo")',
    '(field x 100)',
    # '(field strfild "helo")',
    # '(field myfield2 "strfild")',
    '(method main () (begin',
    '(print (+ strfild " ther"))',
    '(print myfield)',
    '(print (+ 9 9))',
    '(print (/ myfield 9))',
    '(print (/ 1000 9))',
    '(print (% 1000 9))',
    '(print myfield)',
    '(set myfield 1000)',
    '(print myfield)',
    # '(if (+ 9 (+ 1 8)) (print "hi") (if false (print "yo") (print "hmm")) )',
    '(if (!= 9 (+ 1 8)) (print "hi") (if false (print "yo") (print "hmm")) )',
    '(print (* myfield 2))',
    # '(print myfield2)',
    # '(begin (print "INNER") (print "AGAIN"))',
    # '(inputs myfield)',
    # '(print (+ myfield "5"))',
    # '           (inputi x)	 ',
    '           (while (> x 0) ',
    '             (begin',
    # '               (print x)',
    '               (print "x is " x " " true " that")',
    '               (set x (/ x 2))',
    '             ) ',
    '           )',

    # '(inputi myfield)',
    # '(print (+ myfield 5))',
    '(print "end")))',
    ')'


]


interpreter = Interpreter()
interpreter.run(program)

# print(1 is True)

# success, parsed_program = BParser.parse(program)
# print(parsed_program)
