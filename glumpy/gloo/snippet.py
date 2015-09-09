# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import re
import copy
from . import parser


class Snippet(object):
    """
    A snippet is a piece of GLSL code that can be injected into an another GLSL
    code. It provides the necessary machinery to take care of name collisions,
    external variables and snippet composition (call, +, -, /, *).

    A snippet can declare uniforms, const, attributes and varying using random
    names. However, these names will be later mangled such as to avoid name
    collisions with other snippets and/or main code. This means that any
    snippet variable must be accessed through the snippet (snippet["variable"])
    to be able to change its value within the main program.

    Snippet can be composed together through call::

      A = Snippet(code="...")
      B = Snippet(code="...")
      C = A(B("P"))

    and arithmetic composition::

      A = Snippet(code="...")
      B = Snippet(code="...")
      C = A("P") + B("P")

    """

    # Internal id counter for automatic snippets name mangling
    _id_counter = 1

    # Class aliases
    aliases = { }

    def __init__(self, code=None, default=None, *args, **kwargs):

        # Original source code
        self._source_code = parser.merge_includes(code)

        # Variables and functions name parsed from source code
        self._objects = parser.parse(code)

        # Arguments (other snippets or strings)
        self._args = list(args)

        # No chained snippet yet
        self._next = None

        # No name
        self._name = None

        # No default call
        self._call = None

        # Snippet identification
        self._id = Snippet._id_counter
        Snippet._id_counter += 1

        # Process kwargs (name and call)
        self.process_kwargs(**kwargs)

        # If no name has been given, set a default one
        if self._name is None:
            classname = self.__class__.__name__
            self._name = "%s_%d" % (classname, self._id)

        # Symbol table
        self._symbols = {}
        for (name,dtype) in self._objects["attributes"]:
            self._symbols[name] = "%s_%d" % (name,self._id)
        for (name,dtype) in self._objects["uniforms"]:
            self._symbols[name] = "%s_%d" % (name,self._id)
        for (name,dtype) in self._objects["varyings"]:
            self._symbols[name] = "%s_%d" % (name,self._id)
        for (name,dtype) in self._objects["consts"]:
            self._symbols[name] = "%s_%d" % (name,self._id)
        for (rtype,name,args,code) in self._objects["functions"]:
            self._symbols[name] = "%s_%d" % (name,self._id)

        # Aliases (through kwargs)
        for name,alias in kwargs.items():
            self._symbols[name] = alias

        # Attached programs
        self._programs = []


    def process_kwargs(self, **kwargs):
        """ Process kwargs as given in __init__() or __call__() """

        if "name" in kwargs.keys():
            self._name = kwargs["name"]
            del kwargs["name"]

        if "call" in kwargs.keys():
            self._call = kwargs["call"]
            del kwargs["call"]


    @property
    def name(self):
        """ Name of the snippet """

        return self._name


    @property
    def programs(self):
        """ Currently attached programs """

        return self._programs


    @property
    def objects(self):
        """
        Objects composing this snippet only.

        Object are uniforms, attributes, consts, varying and functions.
        """

        return self._objects


    @property
    def symbols(self):
        """
        Symbol table.
        """

        return self._symbols


    @property
    def locals(self):
        """
        Local symbols.

        Local symbols are defined from the code of this snippet only, not
        taking into account symbols from arguments (call) or next (operators).
        """

        symbols = {}
        objects = self._objects
        for name,dtype in objects["uniforms"]+ objects["attributes"] + objects["varyings"]:
            symbols[name] = self.symbols[name]
        # return self._symbols
        return symbols


    @property
    def globals(self):
        """
        Global symbols.

        Global symbols are defined from all the codes composing this snippet,
        taking into account symbols from arguments (call) and next (operators).
        """

        """ Global symbols """

        symbols = {}
        for snippet in self.snippets:
            symbols.update(snippet.locals)
        return symbols


    @property
    def args(self):
        """ Call arguments """

        return list(self._args)


    @property
    def next(self):
        """ Next snippet in the arihmetic chain. """

        if self._next:
            return self._next[1]
        return None


    @property
    def last(self):
        """ Get last snippet in the arithmetic chain. """

        if self.next:
            snippet = self.next
            if isinstance(snippet, Snippet):
                return snippet.last
        return self


    @property
    def snippets(self):
        """ Get all snippets composing this snippet (including self) """

        all = [self,]
        for snippet in self._args:
            if isinstance(snippet, Snippet):
                all.extend(snippet.snippets)
        if self.next:
            operand, snippet = self._next
            if isinstance(snippet, Snippet):
                all.extend(snippet.snippets)
        return all


    @property
    def is_attached(self):
        """ Whether snippet is attached to a program """
        return len(self._programs) > 0


    def lookup(self, name, deepsearch=True):
        """ Search for a specific symbol """

        if deepsearch:
            for snippet in self.snippets:
                symbols = snippet._symbols
                if name in symbols.keys():
                    return symbols[name]
            return None

        return self.symbols.get(name,None)


    def attach(self, program):
        """ Attach this snippet to a program """

        if program not in self._programs:
            self._programs.append(program)

        for snippet in self.snippets[1:]:
            if isinstance(snippet, Snippet):
                snippet.attach(program)

        # WARN: Do we need to build hooks ?
        # program._build_hooks()
        program._build_uniforms()
        program._build_attributes()


    def detach(self, program):
        """ Detach this snippet from a program """

        if program in self._programs:
            index = self._programs.indexof(program)
            del self._programs[index]
        for snippet in list(self._args) + [self.next]:
            if isinstance(snippet, Snippet):
                snippet.detach(program)


    @property
    def dependencies(self):
        """ Compute snippet dependencies """

        deps = [self]
        for snippet in self._args:
            if isinstance(snippet, Snippet):
                deps.extend(snippet.dependencies)
        if self.next:
            operand, snippet = self._next
            if isinstance(snippet, Snippet):
                deps.extend(snippet.dependencies)

        return list(set(deps))


    @property
    def code(self):
        """ Mangled code """

        code = ""
        for snippet in self.dependencies:
            code += snippet.mangled_code()
        return code


    def mangled_code(self):
        """ Generate mangled code """

        code = self._source_code
        objects = self._objects
        functions = objects["functions"]
        names = objects["uniforms"] + objects["attributes"] + objects["varyings"]
        for _,name,_,_ in functions:
            symbol = self.symbols[name]
            code = re.sub(r"(?<=[^\w])(%s)(?=\()" % name, symbol, code)
        for name, _ in names:
            symbol = self.symbols[name]
            code = re.sub(r"(?<=[^\w])(%s)(?=[^\w])" % name, symbol, code)
        return code


    @property
    def call(self):
        """ Mangled call """

        self.mangled_code()
        return self.mangled_call()


    def mangled_call(self, function=None, arguments=None, isolated=False):
        """ Generate mangled call """

        s = ""

        # Is there a function defined in the snippet ?
        # (It may happen a snippet only has uniforms, like the Viewport snippet)
        # WARN: what about Viewport(Transform) ?
        if len(self._objects["functions"]):

            # Is there a function specified in the shader source ?
            # Such as <transform.forward>
            if function:
                name = function

            # Has a function be specified when building the snippet ?
            # Snippet(..., call="some_function")
            elif self._call is not None:
                name = self._call
            else:
                _,name,_,_ = self._objects["functions"][0]

            s = self.lookup(name, deepsearch=False) or name

            if len(self._args) and isolated is False:
                s += "("
                for i,arg in enumerate(self._args):
                    if isinstance(arg,Snippet):
                        # We do not propagate given function to to other snippets
                        # s += arg.mangled_call(function,arguments)
                        s += arg.mangled_call(None,arguments)
                    else:
                        #  This handle call of the form: transform('.x')
                        if arguments is not None and arg.startswith('.'):
                            s += arguments
                        s += str(arg)

                    if i < (len(self._args)-1):
                        s += ", "
                s += ")"
            else:
                # If an argument has been given, we put it at the end
                # This handles hooks of the form <transform(args)>
                if arguments is not None:
                    s += "(%s)" % arguments
                else:
                    s += "()"
            if self.next:
                operand, other = self._next
                if operand in "+-/*":
                    call = other.mangled_call(function,arguments).strip()
                    if len(call):
                        s += ' ' + operand + ' ' + call

        # No function defined in this snippet, we look for next one
        else:
            if self._next:
                operand, other = self.next
                if operand in "+-/*":
                    s = other.mangled_call(function,arguments)
        return s


    def __call__(self, *args, **kwargs):
        """
        Call with new arguments and keyword arguments.

        IMPORTANT: The returned snippet is `self`, not a copy.
        """

        # Override call arguments
        self._args = args

        # Here we process kwargs as if they were given in __init__()
        self.process_kwargs(**kwargs)

        # Remaining kwargs are aliases
        for name, alias in kwargs.items():
           self._symbols[name] = alias

        return self


    def copy(self, deep=False):
        """ Shallow or deep copy of the snippet """

        if deep:
            snippet = copy.deepcopy(self)
        else:
            snippet = copy.copy(self)
        return snippet


    def __op__(self, operand, other):
        snippet = self.copy()
        snippet.last._next = operand,other
        return snippet

    def __add__(self, other):
        return self.__op__("+", other)

    def __and__(self, other):
        return self.__op__("&", other)

    def __sub__(self, other):
        return self.__op__("-", other)

    def __mul__(self, other):
        return self.__op__("*", other)

    def __div__(self, other):
        return self.__op__("/", other)

    def __radd__(self, other):
        return self.__op__("+", other)

    def __rand__(self, other):
        return self.__op__("&", other)

    def __rsub__(self, other):
        return self.__op__("-", other)

    def __rmul__(self, other):
        return self.__op__("*", other)

    def __rdiv__(self, other):
        return self.__op__("/", other)

    def __rshift__(self, other):
        return self.__op__(";", other)

    def __repr__(self):
        # return self.generate_call()

        # s = self._name
        s = self.__class__.__name__
        s += "("
        if len(self._args):
            s += " "
            for i,snippet in enumerate(self._args):
                s += repr(snippet)
                if i < len(self._args)-1:
                    s+= ", "
            s += " "
        s += ")"
        if self._next:
            s += " %s %s" % self._next

        return s


    def __getitem__(self, key):
        """
        Get an item from:

          1. this snippet
          2. the children (args)
          3. the sibling (next)
          4. the attached programs
        """

        # First we look in all snippets
        for snippet in self.snippets:
            if snippet.name == key:
                return snippet

            if hasattr(snippet, key):
                return getattr(snippet, key)

        # Then we look into all attached program
        if len(self._programs) > 0:
            name = self.lookup(key)
            for program in self._programs:
                try:
                    return program[name]
                except AttributeError:
                    pass

        # No luck, we raise exception
        raise AttributeError


    def __setitem__(self, key, value):
        """
        Set an item in:

          1. this snippet
          2. the children (args)
          3. the sibling (next)
          4. the attached programs
        """

        name = self.lookup(key) or key

        found = False

        # First we look in all snippets for the actual key
        for snippet in self.snippets:
            if hasattr(snippet, name):
                setattr(snippet, name, value)
                found = True


        # Then we look into all attached program
        if len(self._programs) > 0:
            for program in self._programs:
                try:
                    program[name] = value
                except IndexError:
                    pass
                else:
                    found = True

        if not found:
            error = 'Snippet does not have such key ("%s")' % key
            raise IndexError(error)


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    A = Snippet("uniform float a;\nvoid function_A(void) {};\n\n", name = "Snippet_A")
    B = Snippet("uniform float b;\nvoid function_B(void) {};\n\n", name = "Snippet_B")
    C = Snippet("uniform float c;\nvoid function_C(void) {};\n\n", name = "Snippet_C")
    D = A(B("A")) + C()

    print(D["Snippet_A"])
    print(D["Snippet_B"])
    print(D["Snippet_C"])

    print(D.locals)
    print(D.globals)

    print(D["Snippet_A"].locals)
    print(D["Snippet_B"].locals)
    print(D["Snippet_C"].locals)

    # print D.objects
    print(D.symbols)
    # print D

    print(D)
    print([snippet._id for snippet in D.dependencies])

    print()
    print("Call:")
    print(D.call)
    print()
    print("Code:")
    print(D.code)
    print()
