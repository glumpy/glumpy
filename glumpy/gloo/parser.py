#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import re
import numpy as np
import OpenGL.GL as gl


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
    """ Extract declarations of type:

        qualifier type name[,name,...];
    """

    if not len(code):
        return []

    variables = []
    if qualifier:
        re_type = re.compile("""
                             %s                               # Variable qualifier
                             \s+(?P<type>\w+)                 # Variable type
                             \s+(?P<names>[\w,\[\]\n =\.$]+); # Variable name(s)
                             """ % qualifier, re.VERBOSE)
    else:
        re_type = re.compile("""
                             \s*(?P<type>\w+)         # Variable type
                             \s+(?P<names>[\w\[\] ]+) # Variable name(s)
                             """, re.VERBOSE)

    re_names = re.compile("""
                          (?P<name>\w+)           # Variable name
                          \s*(\[(?P<size>\d+)\])? # Variable size
                          (\s*[^,]+)?
                          """, re.VERBOSE)

    for match in re.finditer(re_type, code):
        vtype = match.group('type')
        names = match.group('names')
        for match in re.finditer(re_names, names):
            name = match.group('name')
            size = match.group('size')
            if size is None:
                variables.append((name, vtype))
            else:
                size = int(size)
                if size == 0:
                    raise RuntimeError("Size of a variable array cannot be zero")
                for i in range(size):
                    iname = '%s[%d]' % (name,i)
                    variables.append((iname, vtype))
    return variables

def get_hooks(code):
    hooks = []
    re_hooks = re.compile("\<(?P<hook>\w+)\>", re.VERBOSE)
    for match in re.finditer(re_hooks, code):
        hooks.append(match.group('hook'))
    return hooks

def get_args(code):
    return get_declarations(code, qualifier = "")

def get_externs(code):
    return get_declarations(code, qualifier = "extern")

def get_consts(code):
    return get_declarations(code, qualifier = "const")

def get_uniforms(code):
    return get_declarations(code, qualifier = "uniform")

def get_attributes(code):
    return get_declarations(code, qualifier = "attribute")

def get_varyings(code):
    return get_declarations(code, qualifier = "varying")

def get_functions(code):
    functions = []
    regex = re.compile("""
                       \s*(?P<type>\w+)    # Function return type
                       \s+(?P<name>[\w]+)   # Function name
                       \s*\((?P<args>.*?)\) # Function arguments
                       \s*\{(?P<code>.*?)\} # Function content
                       """, re.VERBOSE | re.DOTALL)

    for match in re.finditer(regex, code):
        rtype = match.group('type')
        name = match.group('name')
        args = match.group('args')
        fcode = match.group('code')
        functions.append( (rtype, name, args, fcode) )

    return functions

def parse(code):
    if code:
        code = remove_comments(code)
    externs   = get_externs(code) if code else []
    consts    = get_consts(code) if code else []
    uniforms  = get_uniforms(code) if code else []
    attributes= get_attributes(code) if code else []
    varyings  = get_varyings(code) if code else []
    hooks     = get_hooks(code) if code else []
    functions = get_functions(code) if code else []

    return { 'externs'   : externs,   'consts'    : consts,
             'uniforms'  : uniforms,  'attributes': attributes,
             'varyings'  : varyings,  'hooks'     : hooks,
             'functions' : functions }


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    code = """
    # version 120

    extern float extern_a[2] /* comment */,
                 extern_b,   /* comment */
                 extern_c    /* comment */;

    const float const_a = <hook_1>;
    const float const_b = 2.0, const_c = 3.0;

    uniform float uniform_a;
    uniform float uniform_b;
    uniform float uniform_c[2];
    uniform float <hook_2>;

    attribute float attribute_a[2] , attribute_b , attribute_c;

    varying float varying_a[2];
    varying vec4 varying_b;
    varying mat4 varying_c;

    <hook_3>;

    void
    function_a(int a, int b, int c)
    {
        float a = 1;
    }

    void function_b(int a, int b, int c) {}
    """

    p = parse(code)

    for key in p.keys():
        print key
        if key not in["functions", "hooks"]:
            for (name,vtype) in p[key]:
                print " - %s (%s)"%  (name,vtype)
            print
        elif key == "hooks":
            for name in p[key]:
                print " - %s " % name
            print
        else:
            for (rtype,name,args,func) in p[key]:
                print " - %s %s (%s) { ... }"%  (rtype, name, args)
            print
