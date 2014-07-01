#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import re
import numpy as np
import glumpy.gl as gl


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


def remove_comments(code):
    """ Remove C-style comment from GLSL code string """

    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)

    def do_replace(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string

    return regex.sub(do_replace, code)



def get_declarations(code, qualifier = ""):
    variables = []
    re_type = re.compile("""
                         \s*%s                      # Variable qualifier
                         \s+(?P<type>\w+)           # Variable type
                         \s+(?P<names>[\w,\[\] ]+); # Variable name(s)
                         """ % qualifier, re.VERBOSE)

    re_names = re.compile("""
                          (?P<name>\w+)            # Variable name
                          \s*(\[(?P<size>\d+)\])? # Variable size
                          """, re.VERBOSE)
    code = remove_comments(code)

    for match in re.finditer(re_type, code):
        gtype =_gtypes[match.group('type')]
        names = match.group('names')
        for match in re.finditer(re_names, names):
            name = match.group('name')
            size = match.group('size')
            if size is None:
                variables.append((name, gtype))
            else:
                size = int(size)
                if size == 0:
                    raise RuntimeError("Size of a variable array cannot be zero")
                for i in range(size):
                    iname = '%s[%d]' % (name,i)
                    variables.append((iname, gtype))
        return variables

def get_uniforms(code):
    if len(code):
        return get_declarations(code, qualifier = "uniform")
    return []

def get_attributes(code):
    if len(code):
        return get_declarations(code, qualifier = "attribute")
    return []

def get_functions(source):
    functions = []

    regex = re.compile("""
                       \s*(?P<rtype>\w+)    # Function return type
                       \s+(?P<name>[\w]+)   # Function name
                       \s*\((?P<args>.*?)\) # Function arguments
                       \s*\{(?P<code>.*?)\} # Function content
                       """, re.VERBOSE | re.DOTALL)

    code = remove_comments(source)
    for match in re.finditer(regex, source):
        rtype= match.group('rtype')
        name = match.group('name')
        args = match.group('args')
        code = match.group('code')
        functions.append( (rtype, name, args, code) )

    return functions
