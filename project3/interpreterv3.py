from intbase import InterpreterBase, ErrorType
from bparser import BParser
from copy import deepcopy, copy

DEFAULT_VALUES = {
    InterpreterBase.INT_DEF: '0',
    InterpreterBase.STRING_DEF: '""',
    InterpreterBase.BOOL_DEF: 'false',
    InterpreterBase.VOID_DEF: InterpreterBase.NULL_DEF,
}

VARIABLE_RESERVED_TYPES = [
    InterpreterBase.INT_DEF,
    InterpreterBase.STRING_DEF,
    InterpreterBase.BOOL_DEF,
    InterpreterBase.NULL_DEF,
]

METHOD_RESERVED_TYPES = [
    InterpreterBase.INT_DEF,
    InterpreterBase.STRING_DEF,
    InterpreterBase.BOOL_DEF,
    InterpreterBase.NULL_DEF,
    InterpreterBase.VOID_DEF,
]


class TYPE_E(Exception):
    """Raised for TYPE errors"""

    def __init__(self, message):
        self.message = message


class NAME_E(Exception):
    """Raised for NAME errors"""

    def __init__(self, message):
        self.message = message


class SYNTAX_E(Exception):
    """Raised for SYNTAX errors"""

    def __init__(self, message):
        self.message = message


class FAULT_E(Exception):
    """Raised for FAULT errors"""

    def __init__(self, message):
        self.message = message


class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)

    def run(self, program):
        try:
            result, parsed_program = BParser.parse(program)
            if result is False:
                raise SYNTAX_E('Program parsed incorrectly')

            self.__track_classes(parsed_program)

            self.__validate_class_types()

            self.get_class(super().MAIN_CLASS_DEF).instantiate().run_method(
                super().MAIN_FUNC_DEF, [], self)
        except TYPE_E as err:
            super().error(ErrorType.TYPE_ERROR, err.message)
        except NAME_E as err:
            super().error(ErrorType.NAME_ERROR, err.message)
        except SYNTAX_E as err:
            super().error(ErrorType.SYNTAX_ERROR, err.message)
        except FAULT_E as err:
            super().error(ErrorType.FAULT_ERROR, err.message)

    def get_class(self, class_name):
        try:
            return self.classes[class_name]
        except KeyError:
            raise TYPE_E("Unknown class {}".format(class_name))

    def __track_classes(self, parsed_program):
        self.classes = {}
        for class_def in parsed_program:
            if (class_def[0] != InterpreterBase.CLASS_DEF and
                    class_def[0] != InterpreterBase.TEMPLATE_CLASS_DEF):
                raise SYNTAX_E('Top level definition must be class or tclass')

            class_name = class_def[1]

            # populate fields and classes
            fields = {}
            methods = {}
            inherits = []

            # don't treat `inherits x` as field or class or syntax error
            check_index = 2
            if class_def[2] == InterpreterBase.INHERITS_DEF:
                check_index = 4
                inherits.append(class_def[3])
            for item in class_def[check_index:]:
                if item[0] == InterpreterBase.FIELD_DEF:
                    if item[2] in fields:
                        raise NAME_E("Duplicate field {}".format(item[2]))

                    # normal initialization
                    if len(item) == 4:
                        fields[item[2]] = Variable(
                            item[1], item[2], item[3], self)
                    # optional value initialization
                    elif len(item) == 3:
                        match item[1]:
                            case InterpreterBase.INT_DEF:
                                value = '0'
                            case InterpreterBase.STRING_DEF:
                                value = '""'
                            case InterpreterBase.BOOL_DEF:
                                value = 'false'
                            case _:  # class name or null
                                value = InterpreterBase.NULL_DEF
                        fields[item[2]] = Variable(
                            item[1], item[2], value, self)
                    else:
                        raise SYNTAX_E("Wrong number of field params")

                elif item[0] == InterpreterBase.METHOD_DEF:
                    if item[2] in methods:
                        raise NAME_E("Duplicate method {}".format(item[2]))

                    methods[item[2]] = Method(item[1], item[2], item[3],
                                              Statement(item[4][0],
                                                        item[4][1:]))

                else:
                    raise SYNTAX_E("Class member must be a field or method")

            if class_name in self.classes:
                raise TYPE_E("Duplicate class {}".format(class_name))

            self.classes[class_name] = Class(self, class_name, fields,
                                             methods, inherits)

    def __validate_class_types(self):
        # make sure fields and methods of a class type have a real class type
        classes = self.classes.values()
        class_names = self.classes.keys()
        for checked_class in classes:
            # validate inheritance list
            parent_inheritance = []
            # (this should only execute one iteration)
            for class_name in checked_class.inherits:
                parent = self.get_class(class_name)
                # check for circular inheritance
                if checked_class.name in parent.inherits:
                    raise TYPE_E("Circular inheritance for classes {} and {}"
                                 .format(checked_class.name, parent.name))

                parent_inheritance = parent.inherits

            # populate inheritance list
            checked_class.inherits += parent_inheritance

            # validate field types
            for field in checked_class.fields.values():
                if (field.var_type not in class_names and
                        field.var_type not in VARIABLE_RESERVED_TYPES):
                    raise TYPE_E("Type mismatch with field {}"
                                 .format(field.name))
            # validate method types
            for method in checked_class.methods.values():
                if (method.return_type not in class_names and
                        method.return_type not in METHOD_RESERVED_TYPES):
                    raise TYPE_E("Type mismatch with method {}"
                                 .format(method.name))

                # method return type passed check, now to check parameters
                for param in method.params:
                    param_type = param[0]
                    param_name = param[1]
                    if (param_type not in class_names and
                            param_type not in VARIABLE_RESERVED_TYPES):
                        raise TYPE_E("Type mismatch with param {}"
                                     .format(param_name))

    def __str__(self):
        return str([str(x) for x in self.classes])


class Class():
    def __init__(self, intr, name='', fields={}, methods={}, inherits=[]):
        self.intr = intr
        self.name = name
        self.fields = fields
        self.methods = methods
        self.inherits = inherits

    def instantiate(self):
        try:
            parent = self.intr.get_class(self.inherits[0])
            parent = parent.instantiate()
        except IndexError:
            parent = None

        return ClassInstance(self.name, self.fields, self.methods,
                             self.inherits, parent)

    def __str__(self):
        return (self.name + ' ' + str({'{}:{}'.format(key, val.value) for
                                       (key, val) in self.fields.items()}) +
                ' ' + str({'{}:{}'.format(key, val) for (key, val)
                           in self.methods.items()}))


class ClassInstance():
    def __init__(self, name, fields, methods, inherits, parent):
        self.name = deepcopy(name)
        self.fields = deepcopy(fields)
        self.methods = deepcopy(methods)
        self.inherits = deepcopy(inherits)
        self.parent = parent

    def run_method(self, method_name, params, intr, me=None):
        if me is None:
            me = self
        method, container = self.get_method(method_name)
        try:
            return method.run(container.fields, params, intr, me)
        except NAME_E:
            if self.parent is None:
                raise NAME_E("No matching function definition found for {}"
                             .format(method.name))
            else:
                return self.parent.run_method(method_name, params, intr, me)

    def get_method(self, method_name):
        """
        Returns (`method`, `pointer to container class`)
        """
        try:
            return self.methods[method_name], self
        except KeyError:
            if self.parent is None:
                raise NAME_E("Unknown method {}".format(method_name))
            else:
                return self.parent.get_method(method_name)

    def __str__(self):
        return '<Class instance of {}>'.format(self.name)


class Variable():
    def __init__(self, var_type, name, value, intr):
        self.name = name
        self.var_type = var_type
        self.set_value(value, intr)

    def set_value(self, value, intr):
        if isinstance(value, Value):
            self.value = value
        else:
            # use empty dict for fields because we cannot
            # initially set a field to a variable
            self.value = Value(value, {})

        # checks for all cases except invalid class (to be checked in run)
        var_type = self.var_type
        if var_type == InterpreterBase.VOID_DEF:
            raise TYPE_E("Invalid variable type {}".format(var_type))
        elif var_type == InterpreterBase.NULL_DEF:
            var_type = InterpreterBase.VOID_DEF
        if self.value.value_type != var_type:
            # error if wrong class type
            if self.value.value_type == InterpreterBase.CLASS_DEF:
                if (self.value.value.name != var_type and
                        var_type not in self.value.value.inherits):
                    raise TYPE_E("Type mismatch with variable {}"
                                 .format(self.name))
            # error if types don't match and value is not an object nor null
            elif self.value.value_type != InterpreterBase.VOID_DEF:
                raise TYPE_E("Type mismatch with variable {}"
                             .format(self.name))
            # `null` can only be assigned to object or null type
            elif var_type in [InterpreterBase.INT_DEF,
                              InterpreterBase.BOOL_DEF,
                              InterpreterBase.STRING_DEF,]:
                raise TYPE_E("Type mismatch with variable {}"
                             .format(self.name))
            # cannot assign `null` from a class to an incompatible class
            elif (self.value.classname is not None and self.value.classname !=
                    var_type and var_type not in intr.get_class(
                        self.value.classname).inherits):
                raise TYPE_E("Type mismatch with variable {}"
                             .format(self.name))

    def __str__(self):
        return self.name + ' ' + str(self.value)


class Value():
    def __init__(self, value, fields, classname=None, is_exception=None):
        self.classname = classname
        self.is_exception = is_exception
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
                    raise SYNTAX_E("Invalid variable name")

                # assign value from given variable list
                try:
                    self.value = fields[value].value.value
                    self.value_type = fields[value].value.value_type
                except KeyError:
                    # var doesn't exist
                    raise NAME_E("Unknown variable {}".format(value))
                except TypeError:
                    # cannot initialize var with other var!
                    raise TYPE_E("Field must be initialized with a constant")

    def __str__(self):
        return self.value_type + ' ' + str(self.value)


class Method():
    def __init__(self, return_type, name, params, statement):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.statement = statement

    def __run_and_check(self, scope, intr, me):
        return_value, return_trap = self.statement.run(
            scope, intr, me)

        # exception was uncaught in method
        if return_trap == InterpreterBase.THROW_DEF:
            return return_value
        # void functions cannot return a value
        if self.return_type == InterpreterBase.VOID_DEF:
            if (return_trap is not None and
                    return_trap is not InterpreterBase.VOID_DEF):
                raise TYPE_E("Void function cannot return a value")
            else:
                return Value(DEFAULT_VALUES[InterpreterBase.VOID_DEF],
                             {})
        # if statement has incorrect return value, throw an error
        if (return_value.value_type != InterpreterBase.VOID_DEF and
                return_value.value_type != self.return_type):
            # unless it the return type class or derives from it
            if return_value.value_type == InterpreterBase.CLASS_DEF:
                if (self.return_type != return_value.value.name and
                        self.return_type not in return_value.value.inherits):
                    raise TYPE_E("Invalid return type for {}"
                                 .format(self.name))
            else:
                raise TYPE_E("Invalid return type for {}".format(self.name))

        # null function always must return null
        if self.return_type == InterpreterBase.NULL_DEF:
            return return_value

        # if it explicitly returned
        if return_trap is not None:
            # if of form `return` and not `return x`
            if return_trap == InterpreterBase.VOID_DEF:
                return self.__return_wrapper()
            else:
                # only perform type conversions for booleans?
                # this weird behavior follows the barista implementation
                if self.return_type == InterpreterBase.BOOL_DEF:
                    return Value(InterpreterBase.FALSE_DEF, {})
                return return_value
        else:
            return self.__return_wrapper()

    def __return_wrapper(self):
        try:  # returning a primitive?
            default_val = DEFAULT_VALUES[self.return_type]
            return Value(default_val, {})
        except KeyError:  # returning a class
            return Value(InterpreterBase.NULL_DEF, {}, self.return_type)

    def run(self, fields, arguments, intr, me):
        """Returns the `Value` of the called method"""
        # check duplicate params
        seen_params = set()
        for [ptype, pname] in self.params:
            if pname in seen_params:
                raise NAME_E("Duplicate parameter {}".format(pname))
            else:
                seen_params.add(pname)
        # check incorrect number of arguments
        if len(arguments) != len(self.params):
            raise NAME_E("Wrong number of arguments for {}".format(self.name))

        # check incorrect number of arguments or wrong arg types
        try:
            scope = fields | {k[1]: Variable(k[0], k[1], v, intr) for (
                k, v) in list(zip(self.params, arguments))}
            # ~~^ `k` is [var_type, var_name]
        except TYPE_E:
            raise NAME_E("Invalid argument types for {}".format(self.name))

        return self.__run_and_check(scope, intr, me)

    def __str__(self):
        return self.name + ' ' + str(self.params) + ' ' + str(self.statement)


class Statement():
    def __init__(self, statement_type, params):
        self.statement_type = statement_type
        self.params = params

    def run(self, vars, intr, me):
        """
        Returns `(val, return_trap)` where `val` is the value returned from
        the statement and `return_trap` is `None` if no value is explicitly
        returned
        """
        match self.statement_type:
            case InterpreterBase.BEGIN_DEF:
                for statement in self.params:
                    result, returned = Statement(statement[0],
                                                 statement[1:]).run(
                        vars, intr, me)
                    if returned is not None:
                        return result, returned

                return Value(InterpreterBase.NULL_DEF, vars), None
            case InterpreterBase.CALL_DEF:
                if self.params[0] == InterpreterBase.ME_DEF:
                    expressions = []
                    for x in self.params[2:]:
                        exp = self.__run_expression(x, vars, intr, me)
                        if exp.is_exception:
                            return exp, InterpreterBase.THROW_DEF
                        expressions.append(exp)
                    ret_val = me.run_method(self.params[1], expressions, intr)
                elif self.params[0] == InterpreterBase.SUPER_DEF:
                    expressions = []
                    for x in self.params[2:]:
                        exp = self.__run_expression(x, vars, intr, me)
                        if exp.is_exception:
                            return exp, InterpreterBase.THROW_DEF
                        expressions.append(exp)
                    ret_val = me.parent.run_method(
                        self.params[1], expressions, intr)
                else:
                    obj = self.__run_expression(self.params[0],
                                                vars, intr, me)
                    if obj.is_exception:
                        return obj, InterpreterBase.THROW_DEF
                    if isinstance(obj.value, type(None)):
                        raise FAULT_E("Tried to dereference null object")
                    if obj.value_type != InterpreterBase.CLASS_DEF:
                        raise TYPE_E("Can only call methods on class object")
                    expressions = []
                    for x in self.params[2:]:
                        exp = self.__run_expression(x, vars, intr, me)
                        if exp.is_exception:
                            return exp, InterpreterBase.THROW_DEF
                        expressions.append(exp)
                    ret_val = obj.value.run_method(
                        self.params[1], expressions, intr)
                if ret_val.is_exception is True:
                    return ret_val, InterpreterBase.THROW_DEF
                return Value(InterpreterBase.NULL_DEF, vars), None
            case InterpreterBase.IF_DEF:
                condition = self.__run_expression(
                    self.params[0], vars, intr, me)
                if condition.is_exception:
                    return condition, InterpreterBase.THROW_DEF
                if condition.value_type != InterpreterBase.BOOL_DEF:
                    raise TYPE_E("Non-boolean if condition")

                if condition.value is True:
                    return Statement(self.params[1][0],
                                     self.params[1][1:]).run(
                        vars, intr, me)
                else:
                    if len(self.params) < 3:
                        return Value(InterpreterBase.NULL_DEF,
                                     vars), None
                    elif len(self.params) == 3:
                        return Statement(self.params[2][0],
                                         self.params[2][1:]).run(
                            vars, intr, me)
                    else:
                        raise SYNTAX_E("Too many `if` branches")

            case InterpreterBase.INPUT_INT_DEF:
                input = intr.get_input()
                try:
                    vars[self.params[0]].value = Value(input, vars)
                    return Value(InterpreterBase.NULL_DEF, vars), None
                except KeyError:
                    raise NAME_E("Unknown variable {}".format(self.params[0]))
            case InterpreterBase.INPUT_STRING_DEF:
                input = intr.get_input()
                try:
                    vars[self.params[0]].value = Value(
                        '"{}"'.format(input), vars)
                    return Value(InterpreterBase.NULL_DEF, vars), None
                except KeyError:
                    raise NAME_E("Unknown variable {}".format(self.params[0]))
            case InterpreterBase.PRINT_DEF:
                out_string = ''
                for param in self.params:
                    value = self.__run_expression(param, vars, intr, me)
                    if value.is_exception:
                        return value, InterpreterBase.THROW_DEF
                    if value.value_type == InterpreterBase.BOOL_DEF:
                        value = (InterpreterBase.TRUE_DEF if value.value
                                 else InterpreterBase.FALSE_DEF)
                    else:
                        value = value.value
                    out_string += str(value)

                intr.output(out_string)
                return Value(InterpreterBase.NULL_DEF, vars), None
            case InterpreterBase.RETURN_DEF:
                if len(self.params) == 0:
                    return Value(InterpreterBase.NULL_DEF,
                                 vars), InterpreterBase.VOID_DEF

                value = self.__run_expression(self.params[0],
                                              vars, intr,
                                              me)
                if value.is_exception:
                    return value, InterpreterBase.THROW_DEF
                return value, InterpreterBase.RETURN_DEF
            case InterpreterBase.SET_DEF:
                try:
                    new_value = self.__run_expression(
                        self.params[1], vars, intr, me)
                    if new_value.is_exception:
                        return new_value, InterpreterBase.THROW_DEF
                    vars[self.params[0]].set_value(new_value, intr)
                    return Value(InterpreterBase.NULL_DEF, vars), None
                except KeyError:
                    raise NAME_E("Unknown variable {}".format(self.params[0]))
            case InterpreterBase.WHILE_DEF:
                condition = self.__run_expression(
                    self.params[0], vars, intr, me)
                if condition.is_exception:
                    return condition, InterpreterBase.THROW_DEF
                if condition.value_type != InterpreterBase.BOOL_DEF:
                    raise TYPE_E("Non-boolean while condition")
                while condition.value is True:
                    for statement in self.params[1:]:
                        result, returned = Statement(statement[0],
                                                     statement[1:]).run(
                            vars, intr, me)
                        if returned is not None:
                            return result, returned
                    condition = self.__run_expression(
                        self.params[0], vars, intr, me)
                    if condition.is_exception:
                        return condition, InterpreterBase.THROW_DEF
                return Value(InterpreterBase.NULL_DEF, vars), None
            case InterpreterBase.LET_DEF:
                # populate the let block variable scope
                temp_vars = {}
                for var in self.params[0]:
                    if var[1] in temp_vars.keys():
                        raise NAME_E("Duplicate let var {}".format(var[1]))
                    # initialize normally
                    if len(var) == 3:
                        temp_vars[var[1]] = Variable(
                            var[0], var[1], var[2], intr)
                    # initialize with default value
                    elif len(var) == 2:
                        match var[0]:
                            case InterpreterBase.INT_DEF:
                                value = '0'
                            case InterpreterBase.STRING_DEF:
                                value = '""'
                            case InterpreterBase.BOOL_DEF:
                                value = 'false'
                            case _:  # class name or null
                                value = InterpreterBase.NULL_DEF
                        temp_vars[var[1]] = Variable(
                            var[0], var[1], value, intr)

                    # error if type for new variable is not valid
                    if var[0] not in VARIABLE_RESERVED_TYPES:
                        intr.get_class(var[0])

                # combine scopes
                newvars = copy(vars)
                newvars |= temp_vars

                # run each statement with the new scope
                for statement in self.params[1:]:
                    result, returned = Statement(statement[0],
                                                 statement[1:]).run(
                        newvars, intr, me)
                    if returned is not None:
                        return result, returned
                return Value(InterpreterBase.NULL_DEF, newvars), None
            case InterpreterBase.THROW_DEF:
                return (Value(self.params[0], vars, is_exception=True),
                        InterpreterBase.THROW_DEF)
            case InterpreterBase.TRY_DEF:
                try_statement = self.params[0]
                except_statement = self.params[1]
                result, return_trap = Statement(
                    try_statement[0], try_statement[1:]).run(vars, intr, me)
                if return_trap == InterpreterBase.THROW_DEF:
                    vars_with_except = copy(vars)
                    except_var = Variable(
                        InterpreterBase.STRING_DEF,
                        InterpreterBase.EXCEPTION_VARIABLE_DEF, result, intr)
                    vars_with_except |= {
                        InterpreterBase.EXCEPTION_VARIABLE_DEF: except_var}
                    Statement(except_statement[0], except_statement[1:]).run(
                        vars_with_except, intr, me)
                return Value(InterpreterBase.NULL_DEF, vars), None
            case other:
                raise SYNTAX_E("Unknown statement {}".format(other))

    def __run_expression(self, expr, vars, intr, me):
        if isinstance(expr, list):
            operator = expr[0]
            match operator:
                case '+':
                    lhs = self.__run_expression(expr[1], vars, intr, me)
                    rhs = self.__run_expression(expr[2], vars, intr, me)

                    if (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(lhs.value + rhs.value), vars)
                    elif (lhs.value_type == InterpreterBase.STRING_DEF and
                          rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value('"{}"'.format(lhs.value + rhs.value),
                                     vars)
                    else:
                        raise TYPE_E("Can only add two ints or two strings")
                case '-' | '*' | '/' | '%':
                    lhs = self.__run_expression(expr[1], vars, intr, me)
                    rhs = self.__run_expression(expr[2], vars, intr, me)

                    if not (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        raise TYPE_E("Must perform arithmetic on two ints")

                    return Value(str(int(
                        eval(str(lhs.value) +
                             operator +
                             str(rhs.value)))), vars)
                case '<' | '<=' | '>' | '>=':
                    lhs = self.__run_expression(expr[1], vars, intr, me)
                    rhs = self.__run_expression(expr[2], vars, intr, me)

                    if (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(),
                                     vars)
                    elif (lhs.value_type == InterpreterBase.STRING_DEF and
                            rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value(str(eval(
                            '"{}"{}"{}"'.format(lhs.value,
                                                operator, rhs.value))).lower(),
                                     vars)
                    else:
                        raise TYPE_E("Can only use the notion of greater than\
                                     or less than on strings and ints")
                case '==' | '!=':
                    lhs = self.__run_expression(expr[1], vars, intr, me)
                    rhs = self.__run_expression(expr[2], vars, intr, me)

                    if (lhs.value_type == InterpreterBase.STRING_DEF and
                            rhs.value_type == InterpreterBase.STRING_DEF):
                        return Value(str(eval(
                            '"{}"{}"{}"'.format(lhs.value,
                                                operator, rhs.value))).lower(),
                                     vars)
                    elif (lhs.value_type == InterpreterBase.INT_DEF and
                            rhs.value_type == InterpreterBase.INT_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(),
                                     vars)
                    elif (lhs.value_type == InterpreterBase.BOOL_DEF and
                            rhs.value_type == InterpreterBase.BOOL_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(),
                                     vars)
                    elif ((lhs.value_type == InterpreterBase.VOID_DEF or
                            lhs.value_type == InterpreterBase.CLASS_DEF) and
                            (lhs.value_type == InterpreterBase.VOID_DEF or
                                lhs.value_type == InterpreterBase.CLASS_DEF)):
                        if (lhs.value_type == rhs.value_type ==
                                InterpreterBase.CLASS_DEF):
                            if (lhs.value.name != rhs.value.name and
                                lhs.value.name
                                    not in rhs.value.inherits and
                                    rhs.value.name not in lhs.value.inherits):
                                raise TYPE_E(
                                    "Incompatible types for equality operation"
                                )
                        if (lhs.value_type == InterpreterBase.CLASS_DEF and
                                rhs.value_type == InterpreterBase.VOID_DEF):
                            if (rhs.classname is not None and rhs.classname not
                                    in lhs.value.inherits and rhs.classname !=
                                    lhs.value.name and lhs.value.name not in
                                    intr.get_class(rhs.classname).inherits):
                                raise TYPE_E(
                                    "Incompatible types for equality operation"
                                )
                        if (rhs.value_type == InterpreterBase.CLASS_DEF and
                                lhs.value_type == InterpreterBase.VOID_DEF):
                            if (lhs.classname is not None and lhs.classname not
                                    in rhs.value.inherits and lhs.classname !=
                                    rhs.value.name and rhs.value.name not in
                                    intr.get_class(lhs.classname).inherits):
                                raise TYPE_E(
                                    "Incompatible types for equality operation"
                                )
                        if (rhs.value_type == lhs.value_type ==
                                InterpreterBase.VOID_DEF):
                            if (lhs.classname is not None and rhs.classname is
                                    not None and lhs.classname != rhs.classname
                                    and lhs.classname not in intr
                                    .get_class(rhs.classname).inherits and
                                    rhs.classname not in intr
                                    .get_class(lhs.classname).inherits):
                                raise TYPE_E(
                                    "Incompatible types for equality operation"
                                )
                        if operator == '==':
                            return Value(str(lhs.value == rhs.value).lower(),
                                         vars)
                        else:
                            return Value(str(lhs.value != rhs.value).lower(),
                                         vars)
                    else:
                        raise TYPE_E(
                            "Incompatible types for equality operation")
                case '&' | '|':
                    lhs = self.__run_expression(expr[1], vars, intr, me)
                    rhs = self.__run_expression(expr[2], vars, intr, me)

                    if (lhs.value_type == InterpreterBase.BOOL_DEF and
                            rhs.value_type == InterpreterBase.BOOL_DEF):
                        return Value(str(eval(str(lhs.value) + operator +
                                              str(rhs.value))).lower(),
                                     vars)
                    else:
                        raise TYPE_E("Both operands must be booleans")
                case '!':
                    lhs = self.__run_expression(expr[1], vars, intr, me)
                    if lhs.value_type == InterpreterBase.BOOL_DEF:
                        return Value(str(not lhs.value).lower(), vars)
                    else:
                        raise TYPE_E("Can only perform `not` on a boolean")
                case InterpreterBase.NEW_DEF:
                    class_name = expr[1]
                    new_instance = intr.get_class(class_name).instantiate()
                    return Value(new_instance, vars)
                case InterpreterBase.CALL_DEF:
                    if expr[1] == InterpreterBase.ME_DEF:
                        expressions = []
                        for x in expr[3:]:
                            exp = self.__run_expression(x, vars, intr, me)
                            if exp.is_exception:
                                return exp
                            expressions.append(exp)
                        return me.run_method(expr[2], expressions, intr)
                    elif expr[1] == InterpreterBase.SUPER_DEF:
                        expressions = []
                        for x in expr[3:]:
                            exp = self.__run_expression(x, vars, intr, me)
                            if exp.is_exception:
                                return exp
                            expressions.append(exp)
                        return me.parent.run_method(expr[2], expressions, intr)
                    else:
                        obj = self.__run_expression(
                            expr[1], vars, intr, me)
                        if obj.is_exception:
                            return obj
                        if isinstance(obj.value, type(None)):
                            raise FAULT_E("Tried to dereference null object")
                        if obj.value_type != InterpreterBase.CLASS_DEF:
                            raise TYPE_E(
                                "Can only call methods on class object")
                        expressions = []
                        for x in expr[3:]:
                            exp = self.__run_expression(x, vars, intr, me)
                            if exp.is_exception:
                                return exp
                            expressions.append(exp)
                        return obj.value.run_method(expr[2], expressions, intr)
                case other:
                    raise SYNTAX_E("Unknown operator {}".format(other))

        elif expr == InterpreterBase.ME_DEF:
            return Value(me, vars)
        else:
            return Value(expr, vars)


if __name__ == '__main__':
    with open('program3.scm') as program_file:
        program = program_file.readlines()

    interpreter = Interpreter()
    interpreter.run(program)
