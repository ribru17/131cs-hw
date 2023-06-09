from intbase import InterpreterBase, ErrorType
from bparser import BParser
from copy import deepcopy


class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)

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

                    fields[item[1]] = Variable(item[1], item[2], super())
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
                super().error(ErrorType.TYPE_ERROR,
                              "Duplicate class {}".format(class_name))
            self.classes[class_name] = Class(class_name, fields, methods)

        self.get_class(super().MAIN_CLASS_DEF).instantiate().run_method(
            super().MAIN_FUNC_DEF, [], super(), self)

    def get_class(self, class_name):
        try:
            return self.classes[class_name]
        except KeyError:
            super().error(ErrorType.TYPE_ERROR,
                          "Unknown class {}".format(class_name))

    def __str__(self):
        return str([str(x) for x in self.classes])


class Class():
    def __init__(self, name='', fields={}, methods={}):
        self.name = name
        self.fields = fields
        self.methods = methods

    def instantiate(self):
        return ClassInstance(self.name, self.fields, self.methods)

    def __str__(self):
        return (self.name + ' ' + str({'{}:{}'.format(key, val.value) for
                                       (key, val) in self.fields.items()}) +
                ' ' + str({'{}:{}'.format(key, val) for (key, val)
                           in self.methods.items()}))


class ClassInstance():
    def __init__(self, name, fields, methods):
        self.name = deepcopy(name)
        self.fields = deepcopy(fields)
        self.methods = deepcopy(methods)

    def run_method(self, method_name, params, base, intr):
        try:
            return self.get_method(method_name).run(self.fields,
                                                    params, base, intr, self)
        except KeyError:
            base.error(ErrorType.NAME_ERROR,
                       "Unknown method {}".format(method_name))

    def get_method(self, method_name):
        return self.methods[method_name]

    def __str__(self):
        return '<Class instance of {}>'.format(self.name)


class Variable():
    def __init__(self, name, value, base):
        self.name = name
        if isinstance(value, Value):
            self.value = value
        else:
            # use empty list for fields because we cannot
            # initially set a field to a variable
            self.value = Value(value, [], base)

    def __str__(self):
        return self.name + ' ' + str(self.value)


class Value():
    def __init__(self, value, fields, base):
        if value == InterpreterBase.TRUE_DEF:
            self.value = True
            self.value_type = InterpreterBase.BOOL_DEF
        elif value == InterpreterBase.FALSE_DEF:
            self.value = False
            self.value_type = InterpreterBase.BOOL_DEF
        elif value == InterpreterBase.NULL_DEF:
            self.value_type = InterpreterBase.VOID_DEF
            self.value = None
        elif isinstance(value, ClassInstance):
            self.value_type = InterpreterBase.CLASS_DEF
            self.value = value
        elif value[0] == value[-1] == '"':
            self.value_type = InterpreterBase.STRING_DEF
            self.value = value.strip('"')
        else:
            try:
                self.value = int(value)
                self.value_type = InterpreterBase.INT_DEF
            except ValueError:  # otherwise it is a variable
                if value[0] != '_' and not value[0].isalpha():
                    base.error(ErrorType.SYNTAX_ERROR)

                # assign value from given variable list
                try:
                    self.value = fields[value].value.value
                    self.value_type = fields[value].value.value_type
                except KeyError:
                    # var doesn't exist
                    base.error(
                        ErrorType.NAME_ERROR,
                        "Unknown variable {}".format(value))
                except TypeError:
                    # cannot initialize var with other var!
                    base.error(
                        ErrorType.TYPE_ERROR,
                        "Field must be initialized with a constant")

    def __str__(self):
        return self.value_type + ' ' + str(self.value)


class Method():
    def __init__(self, name, params, statement):
        self.name = name
        self.params = params
        self.statement = statement

    def run(self, fields, params, base, intr, me):
        if len(params) != len(self.params):
            base.error(ErrorType.TYPE_ERROR,
                       'Wrong number of arguments for {}'.format(self.name))
        scope = fields | {k: Variable(k, v, base) for (
            k, v) in list(zip(self.params, params))}

        return self.statement.run(scope, base, intr, me)[0]

    def __str__(self):
        return self.name + ' ' + str(self.params) + ' ' + str(self.statement)


class Statement():
    def __init__(self, statement_type, params):
        self.statement_type = statement_type
        self.params = params

    def run(self, vars, base, intr, me):
        match self.statement_type:
            case InterpreterBase.BEGIN_DEF:
                for statement in self.params:
                    result, returned = Statement(statement[0],
                                                 statement[1:]).run(
                        vars, base, intr, me)
                    if returned is not None:
                        return result, returned

                return Value(InterpreterBase.NULL_DEF, vars, base), None
            case InterpreterBase.CALL_DEF:
                if self.params[0] == InterpreterBase.ME_DEF:
                    me.run_method(
                        self.params[1], [self.__run_expression(
                            x, vars, base, intr, me)
                            for x in self.params[2:]],
                        base, intr)
                else:
                    obj = self.__run_expression(self.params[0],
                                                vars, base, intr, me)
                    if isinstance(obj.value, type(None)):
                        base.error(ErrorType.FAULT_ERROR,
                                   "Tried to dereference null object")
                    if obj.value_type != InterpreterBase.CLASS_DEF:
                        base.error(ErrorType.TYPE_ERROR,
                                   "Can only call methods on class object")
                    obj.value.run_method(
                        self.params[1], [self.__run_expression(
                            x, vars, base, intr, me)
                            for x in self.params[2:]],
                        base, intr)
                return Value(InterpreterBase.NULL_DEF, vars, base), None
            case InterpreterBase.IF_DEF:
                condition = self.__run_expression(
                    self.params[0], vars, base, intr, me)
                if condition.value_type != InterpreterBase.BOOL_DEF:
                    base.error(ErrorType.TYPE_ERROR,
                               "non-boolean if condition")

                if condition.value is True:
                    return Statement(self.params[1][0],
                                     self.params[1][1:]).run(
                        vars, base, intr, me)
                else:
                    if len(self.params) < 3:
                        return Value(InterpreterBase.NULL_DEF,
                                     vars, base), None
                    elif len(self.params) == 3:
                        return Statement(self.params[2][0],
                                         self.params[2][1:]).run(
                            vars, base, intr, me)
                    else:
                        base.error(
                            ErrorType.SYNTAX_ERROR, "Too many `if` branches")

            case InterpreterBase.INPUT_INT_DEF:
                input = base.get_input()
                try:
                    vars[self.params[0]].value = Value(input, vars, base)
                    return Value(InterpreterBase.NULL_DEF, vars, base), None
                except KeyError:
                    base.error(
                        ErrorType.NAME_ERROR,
                        "Unknown variable {}".format(self.params[0]))
            case InterpreterBase.INPUT_STRING_DEF:
                input = base.get_input()
                try:
                    vars[self.params[0]].value = Value(
                        '"{}"'.format(input), vars, base)
                    return Value(InterpreterBase.NULL_DEF, vars, base), None
                except KeyError:
                    base.error(
                        ErrorType.NAME_ERROR,
                        "Unknown variable {}".format(self.params[0]))
            case InterpreterBase.PRINT_DEF:
                out_string = ''
                for param in self.params:
                    value = self.__run_expression(param, vars, base, intr, me)
                    if value.value_type == InterpreterBase.BOOL_DEF:
                        value = (InterpreterBase.TRUE_DEF if value.value
                                 else InterpreterBase.FALSE_DEF)
                    else:
                        value = value.value
                    out_string += str(value)

                base.output(out_string)
                return Value(InterpreterBase.NULL_DEF, vars, base), None
            case InterpreterBase.RETURN_DEF:
                if len(self.params) == 0:
                    return Value(InterpreterBase.NULL_DEF,
                                 vars, base), InterpreterBase.RETURN_DEF

                return self.__run_expression(self.params[0],
                                             vars, base, intr,
                                             me), InterpreterBase.RETURN_DEF
            case InterpreterBase.SET_DEF:
                try:
                    vars[self.params[0]].value = self.__run_expression(
                        self.params[1], vars, base, intr, me)
                    return Value(InterpreterBase.NULL_DEF, vars, base), None
                except KeyError:
                    base.error(ErrorType.NAME_ERROR,
                               "Unknown variable {}".format(self.params[0]))
            case InterpreterBase.WHILE_DEF:
                condition = self.__run_expression(
                    self.params[0], vars, base, intr, me)
                if condition.value_type != InterpreterBase.BOOL_DEF:
                    base.error(
                        ErrorType.TYPE_ERROR, "Non-boolean while condition")
                while condition.value is True:
                    for statement in self.params[1:]:
                        result, returned = Statement(statement[0],
                                                     statement[1:]).run(
                            vars, base, intr, me)
                        if returned is not None:
                            return result, returned
                    condition = self.__run_expression(
                        self.params[0], vars, base, intr, me)
                return Value(InterpreterBase.NULL_DEF, vars, base), None
            case other:
                base.error(ErrorType.SYNTAX_ERROR,
                           "Unknown statement {}".format(other))

    def __run_expression(self, expr, vars, base, intr, me):
        if isinstance(expr, list):
            operator = expr[0]
            match operator:
                case '+':
                    lhs = self.__run_expression(expr[1], vars, base, intr, me)
                    rhs = self.__run_expression(expr[2], vars, base, intr, me)

                    if (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(lhs.value + rhs.value), vars, base)
                    elif (lhs.value_type == InterpreterBase.STRING_DEF and
                          rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value('"{}"'.format(lhs.value + rhs.value),
                                     vars, base)
                    else:
                        base.error(ErrorType.TYPE_ERROR,
                                   "Can only add two ints or two strings")
                case '-' | '*' | '/' | '%':
                    lhs = self.__run_expression(expr[1], vars, base, intr, me)
                    rhs = self.__run_expression(expr[2], vars, base, intr, me)

                    if not (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        base.error(ErrorType.TYPE_ERROR,
                                   "Must perform this operation on two ints")

                    return Value(str(int(
                        eval(str(lhs.value) +
                             operator +
                             str(rhs.value)))), vars, base)
                case '<' | '<=' | '>' | '>=':
                    lhs = self.__run_expression(expr[1], vars, base, intr, me)
                    rhs = self.__run_expression(expr[2], vars, base, intr, me)

                    if (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(),
                                     vars, base)
                    elif (lhs.value_type == InterpreterBase.STRING_DEF and
                            rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value(str(eval(
                            '"{}"{}"{}"'.format(lhs.value,
                                                operator, rhs.value))).lower(),
                                     vars, base)
                    else:
                        base.error(
                            ErrorType.TYPE_ERROR,
                            "Must perform this operation\
                            on two ints or two strings")
                case '==' | '!=':
                    lhs = self.__run_expression(expr[1], vars, base, intr, me)
                    rhs = self.__run_expression(expr[2], vars, base, intr, me)

                    if (lhs.value_type == InterpreterBase.STRING_DEF and
                            rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value(str(eval(
                            '"{}"{}"{}"'.format(lhs.value,
                                                operator, rhs.value))).lower(),
                                     vars, base)
                    elif (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(),
                                     vars, base)
                    elif (lhs.value_type == InterpreterBase.BOOL_DEF and
                            rhs.value_type == InterpreterBase.BOOL_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(),
                                     vars, base)
                    elif ((lhs.value_type == InterpreterBase.VOID_DEF or
                            lhs.value_type == InterpreterBase.CLASS_DEF) and
                            (lhs.value_type == InterpreterBase.VOID_DEF or
                                lhs.value_type == InterpreterBase.CLASS_DEF)):
                        if operator == '==':
                            return Value(str(lhs.value == rhs.value).lower(),
                                         vars, base)
                        else:
                            return Value(str(lhs.value != rhs.value).lower(),
                                         vars, base)
                    else:
                        base.error(ErrorType.TYPE_ERROR,
                                   "Incompatible types for equality operation")
                case '&' | '|':
                    lhs = self.__run_expression(expr[1], vars, base, intr, me)
                    rhs = self.__run_expression(expr[2], vars, base, intr, me)

                    if (lhs.value_type == InterpreterBase.BOOL_DEF and
                            rhs.value_type == InterpreterBase.BOOL_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(),
                                     vars, base)
                    else:
                        base.error(ErrorType.TYPE_ERROR,
                                   "Both operands must be booleans")
                case '!':
                    lhs = self.__run_expression(expr[1], vars, base, intr, me)
                    if lhs.value_type == InterpreterBase.BOOL_DEF:
                        return Value(str(not lhs.value).lower(), vars, base)
                    else:
                        base.error(ErrorType.TYPE_ERROR,
                                   "Can only perform `not` on a boolean")
                case InterpreterBase.NEW_DEF:
                    class_name = expr[1]
                    new_instance = intr.get_class(class_name).instantiate()
                    return Value(new_instance, vars, base)
                case InterpreterBase.CALL_DEF:
                    if expr[1] == InterpreterBase.ME_DEF:
                        return me.run_method(
                            expr[2], [self.__run_expression(
                                x, vars, base, intr, me)
                                for x in expr[3:]],
                            base, intr)
                    else:
                        obj = self.__run_expression(
                            expr[1], vars, base, intr, me)
                        if isinstance(obj.value, type(None)):
                            base.error(ErrorType.FAULT_ERROR,
                                       "Tried to dereference null object")
                        if obj.value_type != InterpreterBase.CLASS_DEF:
                            base.error(ErrorType.TYPE_ERROR,
                                       "Can only call methods on class object")
                        return obj.value.run_method(
                            expr[2], [self.__run_expression(
                                x, vars, base, intr, me)
                                for x in expr[3:]],
                            base, intr)
                case other:
                    base.error(ErrorType.SYNTAX_ERROR,
                               "Unknown operator {}".format(other))

        else:
            return Value(expr, vars, base)


if __name__ == '__main__':
    with open('program.txt') as program_file:
        program = program_file.readlines()

    interpreter = Interpreter()
    interpreter.run(program)
