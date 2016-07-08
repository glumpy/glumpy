# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Variables are entry points in the shader that allow to upload CPU data to
the GPU. For OpenGL ES 2.0, there are mainly two types: uniforms and
attributes. The correspondance betwenn GPU and CPU data types is given in the
table below.

=========== ================== == ================== ==============
GLSL Type   GLSL/GL Type       #  GL elementary type Numpy type
=========== ================== == ================== ==============
float       gl.GL_FLOAT        1  gl.GL_FLOAT        np.float32
vec2        gl.GL_FLOAT_VEC2   2  gl.GL_FLOAT        np.float32
vec3        gl.GL_FLOAT_VEC3   3  gl.GL_FLOAT        np.float32
vec4        gl.GL_FLOAT_VEC4   4  gl.GL_FLOAT        np.float32
int         gl.GL_INT          1  gl.GL_INT          np.int32
ivec2       gl.GL_INT_VEC2     2  gl.GL_INT          np.int32
ivec3       gl.GL_INT_VEC3     3  gl.GL_INT          np.int32
ivec4       gl.GL_INT_VEC4     4  gl.GL_INT          np.int32
bool        gl.GL_BOOL         1  gl.GL_BOOL         np.bool
bvec2       gl.GL_BOOL_VEC2    2  gl.GL_BOOL         np.bool
bvec3       gl.GL_BOOL_VEC3    3  gl.GL_BOOL         np.bool
bvec4       gl.GL_BOOL_VEC4    4  gl.GL_BOOL         np.bool
mat2        gl.GL_FLOAT_MAT2   4  gl.GL_FLOAT        np.float32
mat3        gl.GL_FLOAT_MAT3   9  gl.GL_FLOAT        np.float32
mat4        gl.GL_FLOAT_MAT4   16 gl.GL_FLOAT        np.float32
sampler1D   gl.GL_SAMPLER_1D   1  gl.GL_UNSIGNED_INT np.uint32
sampler2D   gl.GL_SAMPLER_2D   1  gl.GL_UNSIGNED_INT np.uint32
samplerCube gl.GL_SAMPLER_CUBE 1  gl.GL_UNSIGNED_INT np.uint32
=========== ================== == ================== ==============

.. note:: 

   Most of the time, you don't need to directly manipulate such variables
   since they are created automatically when shader code is parsed.

**Example usage**

  .. code::

     vertex = '''
         attribute vec3 position;
         void main (void)
         {
             gl_Position = vec4(position, 1.0);
         } '''
     fragment = '''
         uniform vec4 color;
         void main(void)
         {
             gl_FragColor = color;
         } '''
     program = gloo.Program(vertex, fragment, count=4)
     # program["position"] type is Attribute
     # program["color"] type is Uniform
"""
import ctypes
import numpy as np

from glumpy import gl
from glumpy.log import log
from glumpy.gloo.globject import GLObject
from glumpy.gloo.buffer import VertexBuffer
from glumpy.gloo.texture import TextureCube
from glumpy.gloo.texture import Texture1D, Texture2D
from glumpy.gloo.texture import TextureFloat1D, TextureFloat2D


# ------------------------------------------------------------- gl_typeinfo ---
gl_typeinfo = {
    gl.GL_FLOAT        : ( 1, gl.GL_FLOAT,        np.float32),
    gl.GL_FLOAT_VEC2   : ( 2, gl.GL_FLOAT,        np.float32),
    gl.GL_FLOAT_VEC3   : ( 3, gl.GL_FLOAT,        np.float32),
    gl.GL_FLOAT_VEC4   : ( 4, gl.GL_FLOAT,        np.float32),
    gl.GL_INT          : ( 1, gl.GL_INT,          np.int32),
    gl.GL_INT_VEC2     : ( 2, gl.GL_INT,          np.int32),
    gl.GL_INT_VEC3     : ( 3, gl.GL_INT,          np.int32),
    gl.GL_INT_VEC4     : ( 4, gl.GL_INT,          np.int32),
    gl.GL_BOOL         : ( 1, gl.GL_BOOL,         np.bool),
    gl.GL_BOOL_VEC2    : ( 2, gl.GL_BOOL,         np.bool),
    gl.GL_BOOL_VEC3    : ( 3, gl.GL_BOOL,         np.bool),
    gl.GL_BOOL_VEC4    : ( 4, gl.GL_BOOL,         np.bool),
    gl.GL_FLOAT_MAT2   : ( 4, gl.GL_FLOAT,        np.float32),
    gl.GL_FLOAT_MAT3   : ( 9, gl.GL_FLOAT,        np.float32),
    gl.GL_FLOAT_MAT4   : (16, gl.GL_FLOAT,        np.float32),
    gl.GL_SAMPLER_1D   : ( 1, gl.GL_UNSIGNED_INT, np.uint32),
    gl.GL_SAMPLER_2D   : ( 1, gl.GL_UNSIGNED_INT, np.uint32),
    gl.GL_SAMPLER_CUBE : ( 1, gl.GL_UNSIGNED_INT, np.uint32)
}



# ---------------------------------------------------------- Variable class ---
class Variable(GLObject):
    """ A variable is an interface between a program and data """

    def __init__(self, program, name, gtype):
        """ Initialize the data into default state """

        # Make sure variable type is allowed (for ES 2.0 shader)
        if gtype not in [gl.GL_FLOAT,      gl.GL_FLOAT_VEC2,
                         gl.GL_FLOAT_VEC3, gl.GL_FLOAT_VEC4,
                         gl.GL_INT,        gl.GL_BOOL,
                         gl.GL_FLOAT_MAT2, gl.GL_FLOAT_MAT3,
                         gl.GL_FLOAT_MAT4, gl.GL_SAMPLER_1D,
                         gl.GL_SAMPLER_2D, gl.GL_SAMPLER_CUBE]:
            raise TypeError("Unknown variable type")

        GLObject.__init__(self)

        # Program this variable belongs to
        self._program = program

        # Name of this variable in the program
        self._name = name

        # Build dtype
        size, _, base = gl_typeinfo[gtype]
        self._dtype = (name,base,size)

        # GL type
        self._gtype = gtype

        # CPU data
        self._data = None

        # Whether this variable is active
        self._active = True


    @property
    def name(self):
        """ Variable name """

        return self._name


    @property
    def program(self):
        """ Program this variable belongs to """

        return self._program


    @property
    def gtype(self):
        """ Type of the underlying variable (as a GL constant) """

        return self._gtype

    @property
    def dtype(self):
        """ Equivalent dtype of the variable """

        return self._dtype


    @property
    def active(self):
        """ Whether this variable is active in the program """
        return self._active


    @active.setter
    def active(self, active):
        """ Whether this variable is active in the program """
        self._active = active


    @property
    def data(self):
        """ CPU data """

        return self._data



# ----------------------------------------------------------- Uniform class ---
class Uniform(Variable):
    """ A Uniform represents a program uniform variable. """

    _ufunctions = {
        gl.GL_FLOAT:        gl.glUniform1fv,
        gl.GL_FLOAT_VEC2:   gl.glUniform2fv,
        gl.GL_FLOAT_VEC3:   gl.glUniform3fv,
        gl.GL_FLOAT_VEC4:   gl.glUniform4fv,
        gl.GL_INT:          gl.glUniform1iv,
        gl.GL_BOOL:         gl.glUniform1iv,
        gl.GL_FLOAT_MAT2:   gl.glUniformMatrix2fv,
        gl.GL_FLOAT_MAT3:   gl.glUniformMatrix3fv,
        gl.GL_FLOAT_MAT4:   gl.glUniformMatrix4fv,
        gl.GL_SAMPLER_1D:   gl.glUniform1i,
        gl.GL_SAMPLER_2D:   gl.glUniform1i,
        gl.GL_SAMPLER_CUBE: gl.glUniform1i
    }


    def __init__(self, program, name, gtype):
        """ Initialize the input into default state """

        Variable.__init__(self, program, name, gtype)
        size, _, dtype = gl_typeinfo[self._gtype]
        self._data = np.zeros(size, dtype)
        self._ufunction = Uniform._ufunctions[self._gtype]
        self._texture_unit = -1


    def set_data(self, data):
        """ Assign new data to the variable (deferred operation) """

        # Textures need special handling
        if self._gtype == gl.GL_SAMPLER_1D:

            if isinstance(data, Texture1D):
                self._data = data

            elif isinstance(self._data, Texture1D):
                self._data.set_data(data)

            # Automatic texture creation if required
            else:
                data = np.array(data,copy=False)
                if data.dtype in [np.float16, np.float32, np.float64]:
                    self._data = data.astype(np.float32).view(Texture1D)
                else:
                    self._data = data.view(Texture1D)

        elif self._gtype == gl.GL_SAMPLER_2D:
            if isinstance(data, Texture2D):
                self._data = data
            elif isinstance(self._data, Texture2D):
                #self._data.set_data(data)
                self._data[...] = data.reshape(self._data.shape)

            # Automatic texture creation if required
            else:
                data = np.array(data,copy=False)
                if data.dtype in [np.float16, np.float32, np.float64]:
                    self._data = data.astype(np.float32).view(Texture2D)
                else:
                    self._data = data.view(Texture2D)

        elif self._gtype == gl.GL_SAMPLER_CUBE:
            if isinstance(data, TextureCube):
                self._data = data
            elif isinstance(self._data, TextureCube):
                self._data[...] = data.reshape(self._data.shape)

            # Automatic texture creation if required
            else:
                data = np.array(data,copy=False)
                if data.dtype in [np.float16, np.float32, np.float64]:
                    self._data = data.astype(np.float32).view(TextureCube)
                else:
                    self._data = data.view(TextureCube)

        else:
            self._data[...] = np.array(data,copy=False).ravel()

        self._need_update = True


    def _activate(self):
        if self._gtype in (gl.GL_SAMPLER_1D, gl.GL_SAMPLER_2D, gl.GL_SAMPLER_CUBE):
            if self.data is not None:
                log.debug("GPU: Active texture is %d" % self._texture_unit)
                gl.glActiveTexture(gl.GL_TEXTURE0 + self._texture_unit)
                self.data.activate()

    def _update(self):

        # Check active status (mandatory)
        if not self._active:
            raise RuntimeError("Uniform variable is not active")

        # WARNING : Uniform are supposed to keep their value between program
        #           activation/deactivation (from the GL documentation). It has
        #           been tested on some machines but if it is not the case on
        #           every machine, we can expect nasty bugs from this early
        #           return

        # Matrices (need a transpose argument)
        if self._gtype in (gl.GL_FLOAT_MAT2, gl.GL_FLOAT_MAT3, gl.GL_FLOAT_MAT4):
            # OpenGL ES 2.0 does not support transpose
            transpose = False
            self._ufunction(self._handle, 1, transpose, self._data)

        # Textures (need to get texture count)
        elif self._gtype in (gl.GL_SAMPLER_1D, gl.GL_SAMPLER_2D, gl.GL_SAMPLER_CUBE):
            # texture = self.data
            log.debug("GPU: Activactin texture %d" % self._texture_unit)
            # gl.glActiveTexture(gl.GL_TEXTURE0 + self._unit)
            # gl.glBindTexture(texture.target, texture.handle)
            gl.glUniform1i(self._handle, self._texture_unit)

        # Regular uniform
        else:
            self._ufunction(self._handle, 1, self._data)


    def _create(self):
        """ Create uniform on GPU (get handle) """

        self._handle = gl.glGetUniformLocation(self._program.handle, self._name)




# --------------------------------------------------------- Attribute class ---
class Attribute(Variable):
    """ An Attribute represents a program attribute variable """

    _afunctions = {
        gl.GL_FLOAT:      gl.glVertexAttrib1f,
        gl.GL_FLOAT_VEC2: gl.glVertexAttrib2f,
        gl.GL_FLOAT_VEC3: gl.glVertexAttrib3f,
        gl.GL_FLOAT_VEC4: gl.glVertexAttrib4f
    }

    def __init__(self, program, name, gtype):
        """ Initialize the input into default state """

        Variable.__init__(self, program, name, gtype)

        # Number of elements this attribute links to (in the attached buffer)
        self._size = 0

        # Whether this attribure is generic
        self._generic = False



    def set_data(self, data):
        """ Assign new data to the variable (deferred operation) """

        isnumeric = isinstance(data, (float, int))

        # New vertex buffer
        if isinstance(data, VertexBuffer):
            self._data = data

        # We already have a vertex buffer
        elif isinstance(self._data, VertexBuffer):
            self._data[...] = data

        # Data is a tuple with size <= 4, we assume this designates a generate
        # vertex attribute.
        elif (isnumeric or (isinstance(data, (tuple, list)) and
                            len(data) in (1, 2, 3, 4) and
                            isinstance(data[0], (float, int)))):
            # Let numpy convert the data for us
            _, _, dtype = gl_typeinfo[self._gtype]
            self._data = np.array(data).astype(dtype)
            self._generic = True
            self._need_update = True
            self._afunction = Attribute._afunctions[self._gtype]
            return

        # For array-like, we need to build a proper VertexBuffer to be able to
        # upload it later to GPU memory.
        else: #lif not isinstance(data, VertexBuffer):
            name,base,count = self.dtype
            data = np.array(data,dtype=base,copy=False)
            data = data.ravel().view([self.dtype])
            # WARNING : transform data with the right type
            # data = np.array(data,copy=False)
            self._data = data.view(VertexBuffer)

        self._generic = False


    def _activate(self):
        if isinstance(self.data,VertexBuffer):
            self.data.activate()
            size, gtype, dtype = gl_typeinfo[self._gtype]
            stride = self.data.stride
            offset = ctypes.c_void_p(self.data.offset)
            gl.glEnableVertexAttribArray(self.handle)
            gl.glVertexAttribPointer(self.handle, size, gtype, gl.GL_FALSE, stride, offset)


    def _deactivate(self):
        if isinstance(self.data,VertexBuffer):
            self.data.deactivate()
            if self.handle > 0:
                gl.glDisableVertexAttribArray(self.handle)


    def _update(self):
        """ Actual upload of data to GPU memory  """

        log.debug("GPU: Updating %s" % self.name)

        # Check active status (mandatory)
#        if not self._active:
#            raise RuntimeError("Attribute variable is not active")
#        if self._data is None:
#            raise RuntimeError("Attribute variable data is not set")

        # Generic vertex attribute (all vertices receive the same value)
        if self._generic:
            if self._handle >= 0:
                gl.glDisableVertexAttribArray(self._handle)
                self._afunction(self._handle, *self._data)

        # Regular vertex buffer
        elif self.handle >= 0:
            #if self._need_update:
            #    self.data._update()
            #    self._need_update = False

            # Get relevant information from gl_typeinfo
            size, gtype, dtype = gl_typeinfo[self._gtype]
            stride = self.data.stride

            # Make offset a pointer, or it will be interpreted as a small array
            offset = ctypes.c_void_p(self.data.offset)
            gl.glEnableVertexAttribArray(self.handle)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.data.handle)
            gl.glVertexAttribPointer(self.handle, size, gtype,  gl.GL_FALSE, stride, offset)


    def _create(self):
        """ Create attribute on GPU (get handle) """

        self._handle = gl.glGetAttribLocation(self._program.handle, self.name)


    @property
    def size(self):
        """ Size of the underlying vertex buffer """

        if self._data is None:
            return 0
        return self._data.size

    def __len__(self):
        """ Length of the underlying vertex buffer """

        if self._data is None:
            return 0
        return len(self._data)
