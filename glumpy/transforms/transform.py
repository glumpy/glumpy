#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import os
import numpy as np
from glumpy.gloo import parser
from glumpy.app.window.event import EventDispatcher


class Transform(EventDispatcher):

    # Internal id counter to name transforms
    _idcount = 0

    def __init__(self, source_file=None):

        # Unique transform identifier used for name mangling
        Transform._idcount += 1
        self._id = Transform._idcount

        # No program attached yet
        self._programs = []

        if source_file is None:
            self._source_file = None
            self._source_code = ""
        else:
            directory = os.path.dirname(os.path.realpath(__file__))
            self._source_file = os.path.join(directory,source_file)
            self._source_code = open(self._source_file).read()

        # Default symbol table
        self._table = { "forward" : "forward_%d" % self._id,
                        "inverse" : "inverse_%d" % self._id }
        self._values = {}

        # Get uniform delarations
        for name,gtype in parser.get_uniforms(self._source_code):
            self._table[name] = "%s_%d" % (name, self._id)
            self._values[name] = None

        # Generate mangled code (no name collision with other transforms)
        code = self._source_code
        for i, j in self._table.iteritems():
            code = code.replace(i,j)
        self._mangle_code = code

        # No other transforms yet
        self._next = None


    def __getitem__(self, key):
        if key in self._values.keys():
            return self._values[key]


    def __setitem__(self, key, value):
        if key in self._values.keys():
            self._values[key] = value
            self.update(key)

    def update(self, key):
        if key in self._values.keys():
            for program in self._programs:
                program[self.lookup(key)] = self._values[key]

    def on_resize(self, width, height):
        if self._next:
            self._next.dispatch_event("on_resize", width, height)

    def on_mouse_drag(self, x, y, dx, dy, button):
        if self._next:
            self._next.dispatch_event("on_mouse_drag", x, y, dx, dy, button)

    def on_mouse_scroll(self, x, y, dx, dy):
        if self._next:
            self_next.dispatch_event("on_mouse_scroll", x, y, dx, dy)

    def on_data(self):
        if self._next:
            self_next.dispatch_event("on_data")


    def last(self):
        """ Get last transform from the whole transfrom chain """
        if self._next:
            return self._next.last()
        return self

    def __add__(self, transform):
        """ Append a transform to this one """

        self.last()._next = transform
        return self

    def lookup(self, name):
        """ Lookup in the symbol table for a specific symbol """
        return self._table[name]

    @property
    def next(self):
        return self._next

    @property
    def programs(self):
        return self._programs

    def attach(self, program):
        if program in self._programs:
            return

        self._programs.append(program)

        # Update variables in program
        for symbol in self._table.keys():
            if symbol not in ["forward", "inverse"] and hasattr(self, symbol):
                for program in self._programs:
                    program[self.lookup(symbol)] = self._values[symbol]

        # Update variables in next transforms
        if self.next:
            self.next.attach(program)

    def detach(self, program):
        programs = self._programs
        if program in programs:
            del programs[programs.index(program)]


    @property
    def code(self):
        """ Compositon of all transformation (funcs + call) """

        funcs = ""
        call = (
            """\n"""
            """// -----------------------------\n"""
            """// Final composed transformation\n"""
            """// -----------------------------\n"""
            """vec4 transform(vec4 position) {\n"""
            """    return """)
        transform = self
        n = 0
        while transform:
            funcs += transform._mangle_code
            call += transform._table["forward"] + "( "
            transform = transform._next
            n += 1

        call += "position"
        call += " )" * n + ";"
        call += "\n}"

        return funcs + call


Transform.register_event_type('on_data')
Transform.register_event_type('on_resize')
Transform.register_event_type('on_mouse_drag')
Transform.register_event_type('on_mouse_scroll')
