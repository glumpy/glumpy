# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
A Shader is a user-defined program designed to run on some stage of a
graphics processor. Its purpose is to execute one of the programmable stages of
the rendering pipeline.

Read more on shaders on `OpenGL Wiki <https://www.opengl.org/wiki/Shader>`_

**Example usage**

  .. code:: python

     vertex = '''
         attribute vec2 position;
         void main (void)
         {
             gl_Position = vec4(0.85*position, 0.0, 1.0);
         } '''
     fragment = '''
         void main(void)
         {
             gl_FragColor = vec4(1.0,1.0,0.0,1.0);
         } '''

     quad = gloo.Program(vertex, fragment, count=4)
     quad['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
"""
import re
import os.path
import numpy as np
from glumpy import gl
from glumpy.log import log
from . snippet import Snippet
from . globject import GLObject
from . parser import (remove_comments, preprocess,
                      get_uniforms, get_attributes, get_hooks)



# ------------------------------------------------------------ Shader class ---
class Shader(GLObject):
    """
    Abstract shader class.

    :param gl.GLEnum target:

       * gl.GL_VERTEX_SHADER
       * gl.GL_FRAGMENT_SHADER
       * gl.GL_GEOMETRY_SHADER

    :param str code: Shader code or a filename containing shader code

    .. note::
    
       If the shader code is actually a filename, the filename must be prefixed
       with ``file:``. Note that you can also get shader code from the library
       module.
    """

    _gtypes = {
        'float':       gl.GL_FLOAT,
        'vec2':        gl.GL_FLOAT_VEC2,
        'vec3':        gl.GL_FLOAT_VEC3,
        'vec4':        gl.GL_FLOAT_VEC4,
        'int':         gl.GL_INT,
        'ivec2':       gl.GL_INT_VEC2,
        'ivec3':       gl.GL_INT_VEC3,
        'ivec4':       gl.GL_INT_VEC4,
        'bool':        gl.GL_BOOL,
        'bvec2':       gl.GL_BOOL_VEC2,
        'bvec3':       gl.GL_BOOL_VEC3,
        'bvec4':       gl.GL_BOOL_VEC4,
        'mat2':        gl.GL_FLOAT_MAT2,
        'mat3':        gl.GL_FLOAT_MAT3,
        'mat4':        gl.GL_FLOAT_MAT4,
        'sampler1D':   gl.GL_SAMPLER_1D,
        'sampler2D':   gl.GL_SAMPLER_2D,
        'samplerCube': gl.GL_SAMPLER_CUBE,
    }


    def __init__(self, target, code):
        """
        Initialize the shader.
        """

        GLObject.__init__(self)
        self._target = target
        self._snippets = {}

        if os.path.isfile(code):
            with open(code, 'rt') as file:
                self._code = preprocess(file.read())
                self._source = os.path.basename(code)
        else:
            self._code = preprocess(code)
            self._source = '<string>'

        self._hooked = self._code
        self._need_update = True
        self._program = None


    def __setitem__(self, name, snippet):
        """
        Set a snippet on the given hook in the source code.
        """

        self._snippets[name] = snippet


    def _replace_hooks(self, name, snippet):

        #re_hook = r"(?P<hook>%s)(\.(?P<subhook>\w+))?" % name
        re_hook = r"(?P<hook>%s)(\.(?P<subhook>[\.\w\!]+))?" % name
        re_args = r"(\((?P<args>[^<>]+)\))?"
        re_hooks = re.compile("\<"+re_hook+re_args+"\>" , re.VERBOSE )
        pattern = "\<" + re_hook + re_args + "\>"

        # snippet is not a Snippet (it should be a string)
        if not isinstance(snippet,Snippet):
            def replace(match):
                hook = match.group('hook')
                subhook = match.group('subhook')
                if subhook:
                    return snippet + '.' + subhook
                return snippet
            self._hooked = re.sub(pattern, replace, self._hooked)
            return

        # Store snippet code for later inclusion
        # self._snippets.append(snippet)

        # Replace expression of type <hook.subhook(args)>
        def replace_with_args(match):
            hook = match.group('hook')
            subhook = match.group('subhook')
            args = match.group('args')

            if subhook and '.' in subhook:
                s = snippet
                for item in subhook.split('.')[:-1]:
                    if isinstance(s[item], Snippet):
                        s = s[item]
                subhook = subhook.split('.')[-1]

                # If the last snippet name endswith "!" this means to call
                # the snippet with given arguments and not the ones stored.
                # If S = A(B(C))("t"):
                #   <S>     -> A(B(C("t")))
                #   <S!>(t) -> A("t")
                override = False
                if subhook[-1] == "!":
                    override = True
                    subhook = subhook[:-1]

                # Do we have a class alias ? We don't return it yet since we
                # need its translation from the symbol table
                if subhook in s.aliases.keys():
                    subhook = s.aliases[subhook]
                # If subhook is a variable (uniform/attribute/varying)
                if subhook in s.globals:
                    return s.globals[subhook]
                return s.mangled_call(subhook, match.group("args"), override=override)

            # If subhook is a variable (uniform/attribute/varying)
            if subhook in snippet.globals:
                return snippet.globals[subhook]
            return snippet.mangled_call(subhook, match.group("args"))


        self._hooked = re.sub(pattern, replace_with_args, self._hooked)


    def reset(self):
        """ Reset shader snippets """

        self._snippets = {}


    @property
    def code(self):
        """ Shader source code (built from original and snippet codes) """

        # Last minute hook settings
        self._hooked = self._code
        for name,snippet in self._snippets.items():
            self._replace_hooks(name,snippet)

        snippet_code = "// --- Snippets code : start --- //\n"
        deps = []
        for snippet in self._snippets.values():
            if isinstance(snippet, Snippet):
                deps.extend(snippet.dependencies)
        for snippet in list(set(deps)):
            snippet_code += snippet.mangled_code()
        snippet_code += "// --- Snippets code : end --- //\n"
        return snippet_code + self._hooked



    def _create(self):
        """ Create the shader """

        log.debug("GPU: Creating shader")

        # Check if we have something to compile
        if not self.code:
            raise RuntimeError("No code has been given")

        # Check that shader object has been created
        if self._handle <= 0:
            self._handle = gl.glCreateShader(self._target)
            if self._handle <= 0:
                raise RuntimeError("Cannot create shader object")


    def _update(self):
        """ Compile the source and checks everything's ok """

        log.debug("GPU: Compiling shader")

        if len(self.hooks):
            hooks = [name for name,snippet in self.hooks]
            error = "Shader has pending hooks (%s), cannot compile" % hooks
            raise RuntimeError(error)

        # Set shader version
        code = "#version 120\n" + self.code
        gl.glShaderSource(self._handle, code)

        # Actual compilation
        gl.glCompileShader(self._handle)
        status = gl.glGetShaderiv(self._handle, gl.GL_COMPILE_STATUS)
        if not status:
            error = gl.glGetShaderInfoLog(self._handle).decode()
            lineno, mesg = self._parse_error(error)
            self._print_error(mesg, lineno-1)
            raise RuntimeError("Shader compilation error")


    def _delete(self):
        """ Delete shader from GPU memory (if it was present). """

        gl.glDeleteShader(self._handle)


    def _parse_error(self, error):
        """
        Parses a single GLSL error and extracts the line number and error
        description.

        Parameters
        ----------
        error : str
            An error string as returned by the compilation process
        """

        # Nvidia
        # 0(7): error C1008: undefined variable "MV"
        # 0(2) : error C0118: macros prefixed with '__' are reserved
        m = re.match(r'(\d+)\((\d+)\)\s*:\s(.*)', error )
        if m: return int(m.group(2)), m.group(3)

        # ATI / Intel
        # ERROR: 0:131: '{' : syntax error parse error
        m = re.match(r'ERROR:\s(\d+):(\d+):\s(.*)', error )
        if m: return int(m.group(2)), m.group(3)

        # Nouveau
        # 0:28(16): error: syntax error, unexpected ')', expecting '('
        m = re.match( r'(\d+):(\d+)\((\d+)\):\s(.*)', error )
        if m: return int(m.group(2)), m.group(4)

        raise ValueError('Unknown GLSL error format:\n{}\n'.format(error))


    def _print_error(self, error, lineno):
        """
        Print error and show the faulty line + some context

        Parameters
        ----------
        error : str
            An error string as returned byt the compilation process

        lineno: int
            Line where error occurs
        """
        lines = self.code.split('\n')
        start = max(0,lineno-3)
        end = min(len(lines),lineno+3)

        print('Error in %s' % (repr(self)))
        print(' -> %s' % error)
        print()
        if start > 0:
            print(' ...')
        for i, line in enumerate(lines[start:end]):
            if (i+start) == lineno:
                print(' %03d %s' % (i+start, line))
            else:
                if len(line):
                    print(' %03d %s' % (i+start,line))
        if end < len(lines):
            print(' ...')
        print()


    @property
    def hooks(self):
        """ Shader hooks (place where snippets can be inserted) """

        # We get hooks from the original code, not the hooked one
        code = remove_comments(self._hooked)
        return get_hooks(code)


    @property
    def uniforms(self):
        """ Shader uniforms obtained from source code """

        code = remove_comments(self.code)
        gtypes = Shader._gtypes
        return [ (n,gtypes[t]) for (n,t) in get_uniforms(code) ]


    @property
    def attributes(self):
        """ Shader attributes obtained from source code """

        code = remove_comments(self.code)
        gtypes = Shader._gtypes
        return [(n,gtypes[t]) for (n,t) in get_attributes(code)]



# ------------------------------------------------------ VertexShader class ---
class VertexShader(Shader):
    """ Vertex shader class """

    def __init__(self, code=None):
        Shader.__init__(self, gl.GL_VERTEX_SHADER, code)

    @property
    def code(self):
        code = super(VertexShader, self).code
        code = "#define _GLUMPY__VERTEX_SHADER__\n" + code
        return code


    def __repr__(self):
        return "Vertex shader %d (%s)" % (self._id, self._source)




class FragmentShader(Shader):
    """ Fragment shader class """


    def __init__(self, code=None):
        Shader.__init__(self, gl.GL_FRAGMENT_SHADER, code)

    @property
    def code(self):
        code = super(FragmentShader, self).code
        code = "#define _GLUMPY__FRAGMENT_SHADER__\n" + code
        return code


    def __repr__(self):
        return "Fragment shader %d (%s)" % (self._id, self._source)



class GeometryShader(Shader):
    """ Geometry shader class.

        :param str code: Shader code or a filename containing shader code
        :param int vertices_out: Number of output vertices
        :param gl.GLEnum input_type:

           * GL_POINTS
           * GL_LINES​, GL_LINE_STRIP​, GL_LINE_LIST
           * GL_LINES_ADJACENCY​, GL_LINE_STRIP_ADJACENCY
           * GL_TRIANGLES​, GL_TRIANGLE_STRIP​, GL_TRIANGLE_FAN
           * GL_TRIANGLES_ADJACENCY​, GL_TRIANGLE_STRIP_ADJACENCY

        :param gl.GLEnum output_type:

           * GL_POINTS, GL_LINES​, GL_LINE_STRIP
           * GL_TRIANGLES​, GL_TRIANGLE_STRIP​, GL_TRIANGLE_FAN
    """


    def __init__(self, code=None, vertices_out=0, input_type=None, output_type=None):
        Shader.__init__(self, gl.GL_GEOMETRY_SHADER_EXT, code)

        self._vertices_out = vertices_out

        # GL_POINTS
        # GL_LINES​, GL_LINE_STRIP​, GL_LINE_LIST
        # GL_LINES_ADJACENCY​, GL_LINE_STRIP_ADJACENCY
        # GL_TRIANGLES​, GL_TRIANGLE_STRIP​, GL_TRIANGLE_FAN
        # GL_TRIANGLES_ADJACENCY​, GL_TRIANGLE_STRIP_ADJACENCY
        self._input_type = input_type

        # GL_POINTS, GL_LINES​, GL_LINE_STRIP
        # GL_TRIANGLES​, GL_TRIANGLE_STRIP​, GL_TRIANGLE_FAN
        self._output_type = output_type

    @property
    def vertices_out(self):
        return self._vertices_out

    @vertices_out.setter
    def vertices_out(self, value):
        self._vertices_out = value

    @property
    def input_type(self):
        """ """
        return self._input_type

    @input_type.setter
    def input_type(self, value):
        self._input_type = value

    @property
    def output_type(self):
        return self._output_type

    @output_type.setter
    def output_type(self, value):
        self._output_type = value

    def __repr__(self):
        return "Geometry shader %d (%s)" % (self._id, self._source)
