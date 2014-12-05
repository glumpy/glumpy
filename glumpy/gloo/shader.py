# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import re
import os.path
import numpy as np
from glumpy import gl
from glumpy.log import log
from . snippet import Snippet
from . globject import GLObject
from . parser import (remove_comments, preprocess,
                      get_uniforms, get_attributes, get_hooks)



class Shader(GLObject):
    """Abstract shader class."""

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
    }


    def __init__(self, target, code):
        """
        Initialize the shader and get code if possible.

        Parameters
        ----------

        code: str
            code can be a filename or the actual code
        """

        GLObject.__init__(self)
        self._target = target
        self._code = None
        self._source = None
        self._hooked = None
        self.code = preprocess(code)
        self._program = None


    def __setitem__(self, name, data):
        """ """

        # code = re.sub(r"<(?P<name>[a-zA-Z_]\w+)\((?P<args>[^<>]+)\)>",
        #               "\g<name>(\g<args>)", code)
        # code = re.sub(r"<(?P<name>[a-zA-Z_]\w+)>", "\g<name>", code)

        name = "<%s>" % name
        if isinstance(data,Snippet):
            call = data.call
            code = data.code
            self._hooked = self._hooked.replace(name, call)
            self._hooked = code + self._hooked
        else:
            self._hooked = self._hooked.replace(name, data)


    @property
    def code(self):
        """ Shader source code """
        return self._hooked


    @code.setter
    def code(self, code):
        """ Shader source code """

        if os.path.isfile(code):
            with open(code, 'rt') as file:
                self._code = file.read()
                self._source = os.path.basename(code)
        else:
            self._code   = code
            self._source = '<string>'
        self._hooked = self._code
        self._need_update = True


#    @property
#    def source(self):
#        """ Shader source (string or filename) """
#        return self._source


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
                raise RuntimeErrolr("Cannot create shader object")


    def _update(self):
        """ Compile the source and checks everything's ok """

        log.debug("GPU: Compiling shader")

        if len(self.hooks):
            raise RuntimeError("Shader has pending hooks, cannot compile")

        # Set shader source
        code = "#version 120\n" + self.code
        # code = self.code
        gl.glShaderSource(self._handle, code)

        # Actual compilation
        gl.glCompileShader(self._handle)
        status = gl.glGetShaderiv(self._handle, gl.GL_COMPILE_STATUS)
        if not status:
            error = gl.glGetShaderInfoLog(self._handle)
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
            An error string as returned byt the compilation process
        """

        # Nvidia
        # 0(7): error C1008: undefined variable "MV"
        m = re.match(r'(\d+)\((\d+)\):\s(.*)', error )
        if m: return int(m.group(2)), m.group(3)

        # ATI / Intel
        # ERROR: 0:131: '{' : syntax error parse error
        m = re.match(r'ERROR:\s(\d+):(\d+):\s(.*)', error )
        if m: return int(m.group(2)), m.group(3)

        # Nouveau
        # 0:28(16): error: syntax error, unexpected ')', expecting '('
        m = re.match( r'(\d+):(\d+)\((\d+)\):\s(.*)', error )
        if m: return int(m.group(2)), m.group(4)

        raise ValueError('Unknown GLSL error format')


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

    def __repr__(self):
        return "Vertex shader %d (%s)" % (self._id, self._source)



# ---------------------------------------------------- FragmentShader class ---
class FragmentShader(Shader):
    """ Fragment shader class """


    def __init__(self, code=None):
        Shader.__init__(self, gl.GL_FRAGMENT_SHADER, code)


    def __repr__(self):
        return "Fragment shader %d (%s)" % (self._id, self._source)


# ---------------------------------------------------- GeometryShader class ---
class GeometryShader(Shader):
    """ Geometry shader class """


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
