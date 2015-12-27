# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import re
import numpy as np

from glumpy import gl
from glumpy.log import log
from glumpy import library
from . snippet import Snippet
from . globject import GLObject
from . buffer import VertexBuffer, IndexBuffer
from . shader import VertexShader, FragmentShader, GeometryShader
from . variable import gl_typeinfo, Uniform, Attribute



# ----------------------------------------------------------- Program class ---
class Program(GLObject):
    """
    A Program is an object to which shaders can be attached and linked to create
    a shader program.

    :param str|None vertex:
      Vertex shader object (as code or filename)
    :param str|None fragment:
      Fragment shader object (as code or filename)
    :param str|None geometry:
      Geometry shader object (as code or filename)
    :param int count:
      Optional. Number of vertices this program will use. This can be
      specified to initialize a VertexBuffer during program initialization.

    .. warning::

       If a shader is given as a string and contains a ``{``, glumpy considers
       the string to be actual code. Else, glumpy will try to locate the file
       in the library (``glumpy/library``).

    The actual compilation of a program is a complex operation since include
    msut be resolved and hooks must be inserted at the proper place.
    """

    # ---------------------------------
    def __init__(self, vertex=None, fragment=None, geometry=None, count=0):
        """
        Initialize the program and optionnaly buffer.
        """

        GLObject.__init__(self)
        self._count = count
        self._buffer = None
        self._vertex =  None
        self._fragment = None
        self._geometry = None
        
        if vertex is not None:
            if isinstance(vertex, str):
                if not '{' in vertex:
                    vertex = library.get(vertex)
                self._vertex = VertexShader(vertex)
            elif isinstance(vertex,VertexShader):
                self._vertex = vertex
            else:
                log.error("vertex must be a string or a VertexShader")

        if fragment is not None:
            if isinstance(fragment, str):
                if not '{' in fragment:
                    fragment = library.get(fragment)
                self._fragment = FragmentShader(fragment)
            elif isinstance(fragment, FragmentShader):
                self._fragment = fragment
            else:
                log.error("fragment must be a string or a FragmentShader")

        if geometry is not None:
            if isinstance(geometry, str):
                if not '{' in geometry:
                    geometry = library.get(geometry)
                self._geometry = GeometryShader(geometry)
            elif isinstance(geometry, GeometryShader):
                self._geometry = geometry
            else:
                log.error("geometry must be a string or a GeometryShader")
                

        self._uniforms = {}
        self._attributes = {}

        # Build hooks, uniforms and attributes
        self._build_hooks()
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


    @property
    def vertex(self):
        """ Vertex shader object """
        return self._vertex


    @property
    def fragment(self):
        """ Fragment shader object """
        return self._fragment

    
    @property
    def geometry(self):
        """ Geometry shader object """
        return self._geometry


    @property
    def hooks(self):
        """
        Hook names collected from vertex, fragment and geometry shaders.


        Hooks are placeholder in a shader source code where shader snippet can
        be inserted.

        Example:

        .. code:: C

           attribute vec3 position;
           void main () {
               gl_Position = <transform>(position); # "transform" is a hook
           }
        """

        return tuple(self._vert_hooks.keys()) + \
               tuple(self._frag_hooks.keys()) + \
               tuple(self._geom_hooks.keys())


    def _setup(self):
        """ Setup the program by resolving all pending hooks. """
        pass


    def _create(self):
        """
        Build (link) the program and checks everything's ok.

        A GL context must be available to be able to build (link)
        """

        log.debug("GPU: Creating program")

        # Check if program has been created
        if self._handle <= 0:
            self._handle = gl.glCreateProgram()
            if not self._handle:
                raise ValueError("Cannot create program object")

        self._build_shaders(self._handle)

        log.debug("GPU: Linking program")

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


    def _build_shaders(self, program):
        """ Build and attach shaders """

        # Check if we have at least something to attach
        if not self._vertex:
            raise ValueError("No vertex shader has been given")
        if not self._fragment:
            raise ValueError("No fragment shader has been given")

        log.debug("GPU: Attaching shaders to program")

        # Attach shaders
        attached = gl.glGetAttachedShaders(program)
        shaders = [self._vertex, self._fragment]
        if self._geometry is not None:
            shaders.append(self._geometry)

        for shader in shaders:
            if shader.need_update:
                if shader.handle in attached:
                    gl.glDetachShader(program, shader.handle)
                shader.activate()
                if isinstance(shader, GeometryShader):
                    if shader.vertices_out is not None:
                        gl.glProgramParameteriEXT(self._handle,
                                                  gl.GL_GEOMETRY_VERTICES_OUT_EXT,
                                                  shader.vertices_out)
                    if shader.input_type is not None:
                        gl.glProgramParameteriEXT(self._handle,
                                                  gl.GL_GEOMETRY_INPUT_TYPE_EXT,
                                                  shader.input_type)
                    if shader.output_type is not None:
                        gl.glProgramParameteriEXT(self._handle,
                                                  gl.GL_GEOMETRY_OUTPUT_TYPE_EXT,
                                                  shader.output_type)
                gl.glAttachShader(program, shader.handle)
                shader._program = self


    def _build_hooks(self):
        """ Build hooks """

        self._vert_hooks = {}
        self._frag_hooks = {}
        self._geom_hooks = {}

        if self._vertex is not None:
            for (hook,subhook) in self._vertex.hooks:
                self._vert_hooks[hook] = None
        if self._fragment is not None:
            for (hook,subhook) in self._fragment.hooks:
                self._frag_hooks[hook] = None
        if self._geometry is not None:
            for (hook,subhook) in self._geometry.hooks:
                self._geom_hooks[hook] = None



    def _build_uniforms(self):
        """ Build the uniform objects """

        # We might rebuild the program because of snippets but we must
        # keep already bound uniforms

        count = 0
        for (name,gtype) in self.all_uniforms:
            if name not in self._uniforms.keys():
                uniform = Uniform(self, name, gtype)
            else:
                uniform = self._uniforms[name]
            gtype = uniform.gtype
            if gtype in (gl.GL_SAMPLER_1D, gl.GL_SAMPLER_2D, gl.GL_SAMPLER_CUBE):
                uniform._texture_unit = count
                count += 1
            self._uniforms[name] = uniform
        self._need_update = True


    def _build_attributes(self):
        """ Build the attribute objects """

        # We might rebuild the program because of snippets but we must
        # keep already bound attributes

        dtype = []
        for (name,gtype) in self.all_attributes:
            if name not in self._attributes.keys():
                attribute = Attribute(self, name, gtype)
            else:
                attribute = self._attributes[name]

            self._attributes[name] = attribute
            dtype.append(attribute.dtype)


    def bind(self, data):
        """
        Bind a vertex buffer to the program, matching buffer record names with
        program attributes.

        Several buffers can be bound but the size of the different buffers must
        match.
        """

        if isinstance(data, VertexBuffer):
            for name in data.dtype.names:
                if name in self._attributes.keys():
                    self._attributes[name].set_data(data.ravel()[name])


    def __setitem__(self, name, data):

        vhooks = self._vert_hooks.keys()
        fhooks = self._frag_hooks.keys()

        if name in tuple(vhooks) + tuple(fhooks):
            snippet = data

            if name in vhooks:
                self._vertex[name] = snippet
                self._vert_hooks[name] = snippet
            if name in fhooks:
                self._fragment[name] = snippet
                self._frag_hooks[name] = snippet

            if isinstance(data, Snippet):
                snippet.attach(self)

            self._build_uniforms()
            self._build_attributes()
            self._need_update = True

        # if name in self._hooks.keys():
        #     shader, snippet = self._hooks[name]
        #     snippet = data
        #     shader[name] = snippet
        #     self._hooks[name] = shader, snippet
        #     if isinstance(data, Snippet):
        #         snippet.attach(self)
        #     self._build_uniforms()
        #     self._build_attributes()
        #     self._need_update = True

        elif name in self._uniforms.keys():
            self._uniforms[name].set_data(data)
        elif name in self._attributes.keys():
            self._attributes[name].set_data(data)
        else:
            raise IndexError("Unknown item (no corresponding hook, uniform or attribute)")


    def __getitem__(self, name):
        if name in self._vert_hooks.keys():
            return self._vert_hooks[name]
        elif name in self._frag_hooks.keys():
            return self._frag_hooks[name]
#        if name in self._hooks.keys():
#            return self._hooks[name][1]
        elif name in self._uniforms.keys():
            return self._uniforms[name].data
        elif name in self._attributes.keys():
            return self._attributes[name].data
        else:
            raise IndexError("Unknown item (no corresponding hook, uniform or attribute)")

    # def keys(self):
    #     """ Uniforme and attribute names """

    #     return self._uniforms.keys() + self._attributes.keys()


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


    @property
    def all_uniforms(self):
        """
        List of all uniform parsed from shaders source (read only).
        """

        uniforms = []
        shaders = [self._vertex, self._fragment]
        if self._geometry is not None:
            shaders.append(self._geometry)

        for shader in shaders:
            uniforms.extend(shader.uniforms)
        uniforms = list(set(uniforms))
        return uniforms


    @property
    def active_uniforms(self):
        """
        List of active uniform requested from GPU (read only).

        .. note:: 

           An inactive uniform is a uniform that has been declared but that is
           not actually used in the shader.

           Example:

           .. code::

              uniform vec3 color;     # Inactive
              void main() {
                  gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
              }
        """

        count = gl.glGetProgramiv(self.handle, gl.GL_ACTIVE_UNIFORMS)

        # This match a name of the form "name[size]" (= array)
        regex = re.compile("""(?P<name>\w+)\s*(\[(?P<size>\d+)\])\s*""")
        uniforms = []
        for i in range(count):
            name, size, gtype = gl.glGetActiveUniform(self.handle, i)
            name = name.decode()
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


    @property
    def inactive_uniforms(self):
        """
        List of inactive uniforms requested from GPU (read only).

        .. note:: 

           An inactive uniform is a uniform that has been declared but that is
           not actually used in the shader.

           Example:

           .. code::

              uniform vec3 color;     # Inactive
              void main() {
                  gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
              }
        """

        active_uniforms = self.active_uniforms
        inactive_uniforms = self.all_uniforms
        for uniform in active_uniforms:
            if uniform in inactive_uniforms:
                inactive_uniforms.remove(uniform)
        return inactive_uniforms

    @property
    def all_attributes(self):
        """
        List of all attributes parsed from shaders source (read only).
        """

        attributes= []
        attributes.extend(self._vertex.attributes)
        attributes = list(set(attributes))
        return attributes


    @property
    def active_attributes(self):
        """
        List of active attributes requested from GPU (read only).

        .. note:: 

           An inactive attribute is an attribute that has been declared
           but that is not actually used in the shader.

           Example:

           .. code::

              attribute vec3 normal;    # Inactive
              attribute vec3 position;  # Active
              void main() {
                  gl_Position = vec4(position, 1.0);
              }
        """

        count = gl.glGetProgramiv(self.handle, gl.GL_ACTIVE_ATTRIBUTES)
        attributes = []

        # This match a name of the form "name[size]" (= array)
        regex = re.compile("""(?P<name>\w+)\s*(\[(?P<size>\d+)\])""")

        for i in range(count):
            name, size, gtype = gl.glGetActiveAttrib(self.handle, i)
            name = name.decode()

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


    @property
    def inactive_attributes(self):
        """
        List of inactive attributes requested from GPU (read only).

        .. note:: 

           An inactive attribute is an attribute that has been declared
           but that is not actually used in the shader.

           Example:

           .. code::

              attribute vec3 normal;    # Inactive
              attribute vec3 position;  # Active
              void main() {
                  gl_Position = vec4(position, 1.0);
              }
        """

        active_attributes = self.active_attributes
        inactive_attributes = self.all_attributes
        for attribute in active_attributes:
            if attribute in inactive_attributes:
                inactive_attributes.remove(attribute)
        return inactive_attributes


    def draw(self, mode = gl.GL_TRIANGLES, indices=None): #first=0, count=None):
        """ Draw using the specified mode & indices.

        :param gl.GLEnum mode: 
          One of
            * GL_POINTS
            * GL_LINES
            * GL_LINE_STRIP
            * GL_LINE_LOOP,
            * GL_TRIANGLES
            * GL_TRIANGLE_STRIP
            * GL_TRIANGLE_FAN

        :param IndexBuffer|None indices:
            Vertex indices to be drawn. If none given, everything is drawn.
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
            count = len(tuple(attributes)[0])
            gl.glDrawArrays(mode, first, count)

        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, 0 )
        self.deactivate()
