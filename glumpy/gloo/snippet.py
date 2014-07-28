# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import re
import copy
from parser import parse


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

    To override this behavior, the keyword "extern" can be used to indicate
    this variable is already defined elsewhere. This declaration will be then
    removed from the final code but the variable will still be accessible
    through the snippet interface.

    Finally, it is also possible to indicate what name is to be used when
    calling a snippet, using keyword arguments (snippet(var="b"))
    """

    # (Transient) internal id counter for automatic snippets naming
    _id_counter = 0

    def __init__(self, code=None, default=None):

        # Original source code
        self._source_code = code

        # Variables and functions name parsed from source code
        self._objects = parse(code)

        # Default function to be called if not given
        self._default = default

        # No args yet
        self._args = []

        # No chained snippet yet
        self._next = None

        # Symbol & alias tables
        self._symbols = {}
        self._aliases = {}

        # Attached programs
        self._programs = []


    def lookup(self, name):
        """ Search for a specific symbol """

        if name in self._symbols.keys():
            return self._symbols[name]
        elif name in self._aliases.keys():
            return self._aliases[name]
        else:
            # return name
            return None


    @property
    def programs(self):
        """ Attached programs """

        return self._programs


    def attach(self, program):
        """ Attach this snippet to a program """

        if program not in self._programs:
            self._programs.append(program)
        for snippet in list(self._args) + [self._next]:
            if isinstance(snippet, Snippet):
                snippet.attach(program)


    def detach(self, program):
        """ Detach this snippet from a program """

        if program in self._programs:
            index = self._programs.indexof(program)
            del self._programs[index]
        for snippet in list(self._args) + [self._next]:
            if isinstance(snippet, Snippet):
                snippet.detach(program)


    @property
    def code(self):
        """ Mangled code """
        Snippet._id_counter = 0

        snippets = self.snippets
        funnames, varnames = [], []
        for snippet in snippets:
            for _,name,_,_ in snippet._objects["functions"]:
                funnames.append(name)
            for name,_ in snippet._objects["uniforms"]:
                varnames.append(name)
            for varname,_ in snippet._objects["attributes"]:
                names.append(name)
            for varname,_ in snippet._objects["varyings"]:
                names.append(name)
        def find_duplicates(l):
            seen = set()
            seen_add = seen.add
            seen_twice = set( x for x in l if x in seen or seen_add(x) )
            return list( seen_twice )

        fdup = find_duplicates(funnames)
        vdup = find_duplicates(varnames)
        code = self._generate_code(fdup, vdup)
        return code


    def _generate_code(self, fdup=[], vdup=[]):
        """ Generate mangled code """

        Snippet._id_counter += 1
        self._id = Snippet._id_counter
        code = self._source_code

        # Functions (always mangled)
        for _,name,_,_ in self._objects["functions"]:
            mangled_name = "%s_%d" % (name,self._id)
            self._symbols[name] = mangled_name
            code = re.sub(r"(?<=[^\w])(%s)(?=\()" % name,
                          lambda _ : mangled_name, code)

        # Variables
        vars = self._objects["uniforms"]     \
               + self._objects["attributes"] \
               + self._objects["varyings"]
        for name,_ in vars:

            mangled_name = None
            if name in self._aliases.keys():
                mangled_name = self._aliases[name]
            elif name in vdup:
                mangled_name = "%s_%d" % (name,self._id)
            if mangled_name:
                self._symbols[name] = mangled_name
                code = re.sub(r"(?<=[^\w])(%s)(?=[^\w])" % name,
                              lambda _ : mangled_name, code)
            else:
                self._symbols[name] = name

        # Get rig of externs
        code = re.sub(r"\s*extern[^;]*;", lambda _ : "", code)

        # Get code from args
        if len(self._args):
            for snippet in self._args:
                if isinstance(snippet, Snippet):
                    code += snippet._generate_code(fdup, vdup)

        # Get code from next snippet
        if self.next:
            operand, snippet = self.next
            if isinstance(snippet, Snippet):
                code += snippet._generate_code(fdup, vdup)

        return code


    @property
    def call(self):
        """ Mangled call """
        # This force code to be built and name mangled
        code = self.code
        return self._generate_call()


    def _generate_call(self):
        """ Generate mangled call """

        if len(self._objects["functions"]):
            if self._default:
                name = self._default
            else:
                _,name,_,_ = self._objects["functions"][0]

            s = self.lookup(name)
            if len(self._args):
                s += " ( " + ", ".join([str(arg) for arg in self._args]) + " )"
            else:
                s += "()"
            if self.next:
                operand, other = self.next
                s += " %s " % operand + str(other)
        else:
            if self._next:
                operand, other = self.next
                s = str(other)
        return s


#    def __getattr__(self, key):
#        for  (rtype, name, args, code) in self._objects["functions"]:
#            if name == key:
#                S = self.copy()
#                S._default = key
#                return S
##                source = "%s %s(%s)\n{%s}\n" % (rtype, name, args, code)
##                return Snippet(source)
#        return object.__getattribute__(self,key)


    def copy(self):
        """ Copy snippet """

        return copy.deepcopy(self)


    @property
    def next(self):
        """ Get next snippet in the chain """

        return self._next


    @property
    def last(self):
        """ Get last snippet in the chain """

        if self.next:
            operand, snippet = self.next
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
            operand, snippet = self.next
            if isinstance(snippet, Snippet):
                all.extend(snippet.snippets)
        return all


    def __call__(self, *args, **kwargs):
        """ __call__(self, *args) <==> self(*args) """

        S = self.copy()
        S._args = args
        for symbol in kwargs.keys():
            S._aliases[symbol] = kwargs[symbol]
        return S

    def __op__(self, operand, other):
        S = self.copy()
        S.last._next = (operand,other)
        return S

    def __add__(self, other):
        return self.__op__("+", other)

    def __sub__(self, other):
        return self.__op__("-", other)

    def __mul__(self, other):
        return self.__op__("*", other)

    def __div__(self, other):
        return self.__op__("/", other)

    def __radd__(self, other):
        return self.__op__("+", other)

    def __rsub__(self, other):
        return self.__op__("-", other)

    def __rmul__(self, other):
        return self.__op__("*", other)

    def __rdiv__(self, other):
        return self.__op__("/", other)

    def __str__(self):
        return self._generate_call()

    def __getitem__(self, key):
        if len(self._programs) == 0:
            raise RuntimeError("Snippet is not attached to a program")

        name = self.lookup(key)
        if name is not None:
            program = self._programs[0]
            return program[name]

        # values = []
        # for program in self._programs:
        #     values.append(program[key])

        # for snippet in self._args:
        #     if isinstance(snippet, Snippet):
        #         for program in snippet._programs:
        #             values.append(program[key])
        #     if self._next:
        #         operand,snippet = self._next
        #         if isinstance(snippet, Snippet):
        #             for program in snippet._programs:
        #                 values.append(self._program[key])
        # if len(values) == 1:
        #     return values[0]
        # else:
        #     return values

    def __setitem__(self, key, value):
        if len(self._programs) == 0:
            raise RuntimeError("Snippet is not attached to a program")

        name = self.lookup(key)
        if name is not None:
            for program in self._programs:
                program[name] = value

        for snippet in self._args:
            if isinstance(snippet, Snippet):
                snippet[key] = value
            if self._next:
                operand,snippet = self._next
                if isinstance(snippet, Snippet):
                    snippet[key] = value




# -----------------------------------------------------------------------------
if __name__ == '__main__':
    scale = """
// Forward
vec4 forward(vec4 position, vec3 scale)
{
    return vec4( position.xyz * translate, position.w );
}

// Inverse
vec4 inverse(vec4 position, vec3 scale)
{
    return vec4( position.xyz / scale, position.w );
}
"""

    translate = """
// Forward
vec4 forward(vec4 position, vec3 translate)
{
    return vec4( position.xyz + translate, position.w );
}

// Inverse
vec4 inverse(vec4 position, vec3 translate)
{
    return vec4( position.xyz - translate, position.w );
}

"""
    # Scale = Snippet(scale)
    # Translate = Snippet(translate)
    # Position4D = "position"
    # Position3D = "vec4( position.xyz, 1.0)"
    # Position2D = "vec4( position.xy, 0.0, 1.0)"

    # R = Translate(Position3D,"translate") + Scale(Position3D,"scale")
    # print R.code
    # print R.call

    # # print "---"


    translate = """
uniform vec3 translate;

// Forward
vec4 forward(vec4 position)
{
    return vec4( position.xyz + translate, position.w );
}

// Inverse
vec4 inverse(vec4 position)
{
    return vec4( position.xyz - translate, position.w );
}

"""
    scale = """
uniform vec3 scale;

// Forward
vec4 forward(vec4 position)
{
    return vec4( position.xyz * scale, position.w );
}

// Inverse
vec4 inverse(vec4 position)
{
    return vec4( position.xyz / scale, position.w );
}
"""

    Scale = Snippet(scale)
    Translate = Snippet(translate)
    Position4D = "position"
    Position3D = "vec4(position.xyz, 1.0)"
    Position2D = "vec4(position.xy, 0.0, 1.0)"

    R = Translate(Position3D)
    R = Translate.forward(Translate.forward(Position3D))
    # R = Translate.forward(Position3D)
    print R.code
    print R.call
