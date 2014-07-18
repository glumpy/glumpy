# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import re
import numpy as np

from glumpy import gl
from glumpy.log import log
from glumpy.gloo.globject import GLObject
from glumpy.gloo.buffer import VertexBuffer, IndexBuffer
from glumpy.gloo.shader import VertexShader, FragmentShader, GeometryShader
from glumpy.gloo.variable import gl_typeinfo, Uniform, Attribute


# Patch: pythonize the glGetActiveAttrib
import ctypes
gl._glGetActiveAttrib = gl.glGetActiveAttrib
def glGetActiveAttrib(program, index):
    # Prepare
    bufsize = 32
    length = ctypes.c_int()
    size = ctypes.c_int()
    type = ctypes.c_int()
    name = ctypes.create_string_buffer(bufsize)
    # Call
    gl._glGetActiveAttrib(program, index,
                          bufsize, ctypes.byref(length), ctypes.byref(size),
                          ctypes.byref(type), name)
    # Return Python objects
    return name.value, size.value, type.value
gl.glGetActiveAttrib = glGetActiveAttrib




# ----------------------------------------------------------- Program class ---
class Program(GLObject):
    """
    A program is an object to which shaders can be attached and linked to create
    the program.
    """

    # ---------------------------------
    def __init__(self, verts=None, frags=None, geoms=None, count=0):
        """
        Initialize the program and register shaders to be linked.

        Parameters
        ----------

        verts : str, VertexShader, or list
            The vertex shader(s) to be used by this program

        frags : str, FragmentShader, or list
            The fragment shader(s) to be used by this program

        geoms : str, GeometryShader, or list
            The geometry shader(s) to be used by this program

        count : int (optional)
            Number of vertices this program will use. This can be given to
            initialize a VertexBuffer during Program initialization.

        Note
        ----

        If several vertex/fragment/geometry shaders are specified, only one can
        contain the main function respectively.
        """

        GLObject.__init__(self)
        self._count = count
        self._buffer = None


        # Get all vertex shaders
        self._verts = []
        if isinstance(verts, (str, VertexShader)):
            verts = [verts]
        elif isinstance(verts, (type(None), tuple, list)):
            verts = verts or []
        else:
            raise ValueError('Vert must be str, VertexShader or list')
        # Apply
        for shader in verts:
            if isinstance(shader, str):
                self._verts.append(VertexShader(shader))
            elif isinstance(shader, VertexShader):
                if shader not in self._verts:
                    self._verts.append(shader)
            else:
                T = type(shader)
                raise ValueError('Cannot make a VertexShader of %r.' % T)

        # Get all fragment shaders
        self._frags = []
        if isinstance(frags, (str, FragmentShader)):
            frags = [frags]
        elif isinstance(frags, (type(None), tuple, list)):
            frags = frags or []
        else:
            raise ValueError('frags must be str, FragmentShader or list')
        # Apply
        for shader in frags:
            if isinstance(shader, str):
                self._frags.append(FragmentShader(shader))
            elif isinstance(shader, FragmentShader):
                if shader not in self._frags:
                    self._frags.append(shader)
            else:
                T = type(shader)
                raise ValueError('Cannot make a FragmentShader out of %r.' % T)

        # Get all geoms shaders
        self._geoms = []
        if isinstance(geoms, (str, GeometryShader)):
            geoms = [geoms]
        elif isinstance(geoms, (type(None), tuple, list)):
            geoms = geoms or []
        else:
            raise ValueError('geoms must be str, GeometryShader or list')
        # Apply
        for shader in geoms:
            if isinstance(shader, str):
                self._geoms.append(GeometryShader(shader))
            elif isinstance(shader, GeometryShader):
                if shader not in self._geoms:
                    self._geoms.append(shader)
            else:
                T = type(shader)
                raise ValueError('Cannot make a GeometryShader out of %r.' % T)

        # Build uniforms and attributes
        self._build_uniforms()
        self._build_attributes()


        # Build associated structured vertex buffer if count is given
        if self._count > 0:
            dtype = []
            for attribute in self._attributes.values():
                dtype.append(attribute.dtype)
            self._buffer = np.zeros(self._count, dtype=dtype).view(VertexBuffer)
            self.bind(self._buffer)


    def __len__(self):
        if self._buffer is not None:
            return len(self._buffer)
        else:
            return None


    def attach(self, shaders):
        """ Attach one or several vertex/fragment shaders to the program.

        Parameters
        ----------

        shaders : VertexShader or FragmentShaders or list
            Shaders to attach
        """

        if isinstance(shaders, (VertexShader, FragmentShader)):
            shaders = [shaders]
        for shader in shaders:
            if isinstance(shader, VertexShader):
                self._verts.append(shader)
            elif isinstance(shader, FragmentShader):
                self._frags.append(shader)
            else:
                log.warn("Unknown shader type")

        # Ensure uniqueness of shaders
        self._verts = list(set(self._verts))
        self._frags = list(set(self._frags))

        self._need_create = True
        self._need_update = True

        # Build uniforms and attributes
        self._build_uniforms()
        self._build_attributes()



    def detach(self, shaders):
        """Detach one or several vertex/fragment shaders from the program.

        Parameters
        ----------

        shaders : VertexShader or FragmentShaders or list
            Shaders to detach

        Note
        ----

        We don't need to defer attach/detach shaders since shader deletion
        takes care of that.
        """

        if type(shaders) in [VertexShader, FragmentShader]:
            shaders = [shaders]
        for shader in shaders:
            if isinstance(shader, VertexShader):
                if shader in self._verts:
                    self._verts.remove(shader)
                else:
                    raise ValueError("Shader is not attached to the program")
            elif isinstance(shader, FragmentShader):
                if shader in self._frags:
                    self._frags.remove(shader)
                else:
                    raise ValueError("Shader is not attached to the program")
        self._need_update = True

        # Build uniforms and attributes
        self._build_uniforms()
        self._build_attributes()


    def _create(self):
        """
        Build (link) the program and checks everything's ok.

        A GL context must be available to be able to build (link)
        """

        # Check if we have something to link
        if not self._verts:
            raise ValueError("No vertex shader has been given")
        if not self._frags:
            raise ValueError("No fragment shader has been given")

        # Check if program has been created
        if self._handle <= 0:
            self._handle = gl.glCreateProgram()
            if not self._handle:
                raise ValueError("Cannot create program object")

        # Detach any attached shaders
        attached = gl.glGetAttachedShaders(self._handle)
        for handle in attached:
            gl.glDetachShader(self._handle, handle)

        # Attach vertex shaders
        for shader in self._verts:
            shader.activate()
            gl.glAttachShader(self._handle, shader.handle)

        # Attach fragment shaders
        for shader in self._frags:
            shader.activate()
            gl.glAttachShader(self._handle, shader.handle)

        # Attach geometry shaders
        for shader in self._geoms:
            shader.activate()
            gl.glProgramParameteriEXT(self._handle,
                                      gl.GL_GEOMETRY_VERTICES_OUT_EXT,
                                      shader.vertices_out)
            gl.glProgramParameteriEXT(self._handle,
                                      gl.GL_GEOMETRY_INPUT_TYPE_EXT,
                                      shader.input_type)
            gl.glProgramParameteriEXT(self._handle,
                                      gl.GL_GEOMETRY_OUTPUT_TYPE_EXT,
                                      shader.output_type)
            gl.glAttachShader(self._handle, shader.handle)

        log.debug("GPU: Creating program")

        # Link the program
        gl.glLinkProgram(self._handle)
        if not gl.glGetProgramiv(self._handle, gl.GL_LINK_STATUS):
            print(gl.glGetProgramInfoLog(self._handle))
            raise ValueError('Linking error')

        # Activate uniforms
        active_uniforms = [name for (name,gtype) in self.active_uniforms]
        for uniform in self._uniforms.values():
            if uniform.name in active_uniforms:
                uniform.active = True
            else:
                uniform.active = False

        # Activate attributes
        active_attributes = [name for (name,gtype) in self.active_attributes]
        for attribute in self._attributes.values():
            if attribute.name in active_attributes:
                attribute.active = True
            else:
                attribute.active = False


    def _build_uniforms(self):
        """ Build the uniform objects """

        self._uniforms = {}
        count = 0
        for (name,gtype) in self.all_uniforms:
            uniform = Uniform(self, name, gtype)
            if gtype in (gl.GL_SAMPLER_1D, gl.GL_SAMPLER_2D):
                uniform._texture_unit = count
                count += 1
            self._uniforms[name] = uniform
        self._need_update = True


    def _build_attributes(self):
        """ Build the attribute objects """

        self._attributes = {}

        dtype = []
        for (name,gtype) in self.all_attributes:
            attribute = Attribute(self, name, gtype)
            self._attributes[name] = attribute
            dtype.append(attribute.dtype)


    def bind(self, data):
        """ """
        if isinstance(data, VertexBuffer):
            for name in data.dtype.names:
                if name in self._attributes.keys():
                    self._attributes[name].set_data(data[name])


    def __setitem__(self, name, data):
        if name in self._uniforms.keys():
            self._uniforms[name].set_data(data)
        elif name in self._attributes.keys():
            self._attributes[name].set_data(data)
        else:
            raise ValueError("Unknown uniform or attribute")


    def __getitem__(self, name):
        if name in self._uniforms.keys():
            return self._uniforms[name].data
        elif name in self._attributes.keys():
            return self._attributes[name].data
        else:
            raise IndexError("Unknown uniform or attribute")



    def _activate(self):
        """Activate the program as part of current rendering state."""

        log.debug("GPU: Activating program (id=%d)" % self._id)
        gl.glUseProgram(self.handle)

        for uniform in self._uniforms.values():
            if uniform.active:
                uniform.activate()

        for attribute in self._attributes.values():
            if attribute.active:
                attribute.activate()


    def _deactivate(self):
        """Deactivate the program."""

        gl.glUseProgram(0)

        for uniform in self._uniforms.values():
            uniform.deactivate()
        for attribute in self._attributes.values():
            attribute.deactivate()
        log.debug("GPU: Deactivating program (id=%d)" % self._id)


    def _get_all_uniforms(self):
        """Extract uniforms from shaders code """

        uniforms = []
        for shader in self._verts:
            uniforms.extend(shader.uniforms)
        for shader in self._frags:
            uniforms.extend(shader.uniforms)
        for shader in self._geoms:
            uniforms.extend(shader.uniforms)
        uniforms = list(set(uniforms))
        return uniforms
    all_uniforms = property(_get_all_uniforms,
        doc = """ Program uniforms obtained from shaders code """)


    def _get_active_uniforms(self):
        """ Extract active uniforms from GPU """

        count = gl.glGetProgramiv(self.handle, gl.GL_ACTIVE_UNIFORMS)

        # This match a name of the form "name[size]" (= array)
        regex = re.compile("""(?P<name>\w+)\s*(\[(?P<size>\d+)\])\s*""")
        uniforms = []
        for i in range(count):
            name, size, gtype = gl.glGetActiveUniform(self.handle, i)
            # This checks if the uniform is an array
            # Name will be something like xxx[0] instead of xxx
            m = regex.match(name)
            # When uniform is an array, size corresponds to the highest used index
            if m:
                name = m.group('name')
                if size >= 1:
                    for i in range(size):
                        name = '%s[%d]' % (m.group('name'),i)
                        uniforms.append((name, gtype))
            else:
                uniforms.append((name, gtype))

        return uniforms
    active_uniforms = property(_get_active_uniforms,
        doc = "Program active uniforms obtained from GPU")



    def _get_inactive_uniforms(self):
        """ Extract inactive uniforms from GPU """

        active_uniforms = self.active_uniforms
        inactive_uniforms = self.all_uniforms
        for uniform in active_uniforms:
            if uniform in inactive_uniforms:
                inactive_uniforms.remove(uniform)
        return inactive_uniforms
    inactive_uniforms = property(_get_inactive_uniforms,
        doc = "Program inactive uniforms obtained from GPU")



    def _get_all_attributes(self):
        """ Extract attributes from shaders code """

        attributes= []
        for shader in self._verts:
            attributes.extend(shader.attributes)
        # No attribute in fragment shaders
        attributes = list(set(attributes))
        return attributes
    all_attributes = property(_get_all_attributes,
        doc = "Program attributes obtained from shaders code")



    def _get_active_attributes(self):
        """ Extract active attributes from GPU """

        count = gl.glGetProgramiv(self.handle, gl.GL_ACTIVE_ATTRIBUTES)
        attributes = []

        # This match a name of the form "name[size]" (= array)
        regex = re.compile("""(?P<name>\w+)\s*(\[(?P<size>\d+)\])""")

        for i in range(count):
            name, size, gtype = gl.glGetActiveAttrib(self.handle, i)

            # This checks if the attribute is an array
            # Name will be something like xxx[0] instead of xxx
            m = regex.match(name)
            # When attribute is an array, size corresponds to the highest used index
            if m:
                name = m.group('name')
                if size >= 1:
                    for i in range(size):
                        name = '%s[%d]' % (m.group('name'),i)
                        attributes.append((name, gtype))
            else:
                attributes.append((name, gtype))
        return attributes
    active_attributes = property(_get_active_attributes,
        doc = "Program active attributes obtained from GPU")



    def _get_inactive_attributes(self):
        """ Extract inactive attributes from GPU """

        active_attributes = self.active_attributes
        inactive_attributes = self.all_attributes
        for attribute in active_attributes:
            if attribute in inactive_attributes:
                inacative_attributes.remove(attribute)
        return inactive_attributes
    inactive_attributes = property(_get_inactive_attributes,
        doc = "Program inactive attributes obtained from GPU")


    @property
    def shaders(self):
        """ List of shaders currently attached to this program """

        shaders = []
        shaders.extend(self._verts)
        shaders.extend(self._frags)
        shaders.extend(self._geoms)
        return shaders



    def draw(self, mode = gl.GL_TRIANGLES, indices=None): #first=0, count=None):
        """ Draw the attribute arrays in the specified mode.

        Parameters
        ----------
        mode : GL_ENUM
            GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP,
            GL_TRIANGLES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN

        first : int
            The starting vertex index in the vertex array. Default 0.

        count : int
            The number of vertices to draw. Default all.
        """

        self.activate()
        attributes = self._attributes.values()

        # Get buffer size first attribute
        # We need more tests here
        #  - do we have at least 1 attribute ?
        #  - does all attributes report same count ?
        # count = (count or attributes[0].size) - first

        if isinstance(indices, IndexBuffer):
            indices.activate()
            gltypes = { np.dtype(np.uint8) : gl.GL_UNSIGNED_BYTE,
                        np.dtype(np.uint16): gl.GL_UNSIGNED_SHORT,
                        np.dtype(np.uint32): gl.GL_UNSIGNED_INT }
            gl.glDrawElements(mode, indices.size, gltypes[indices.dtype], None)
            indices.deactivate()
        else:
            first = 0
            # count = (self._count or attributes[0].size) - first
            count = len(attributes[0])
            gl.glDrawArrays(mode, first, count)

        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, 0 )
        self.deactivate()
