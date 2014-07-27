#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import os
import numpy as np
from glumpy.gloo import Snippet
from glumpy.shaders import get_code
from glumpy.app.window.event import EventDispatcher


class Transform(Snippet,EventDispatcher):

    shaderfile = None

    def __init__(self, *args, **kwargs):
        code = get_code(self.__class__.shaderfile)
        Snippet.__init__(self, code)
        EventDispatcher.__init__(self)

        self._args = list(args)
        for symbol in kwargs.keys():
            self._aliases[symbol] = kwargs[symbol]

    def attach(self, program):
        """ A new program is attached """

        Snippet.attach(self,program)
        # WARN: Do we need to build hooks ?
        # program._build_hooks()
        program._build_uniforms()
        program._build_attributes()
        self.dispatch_event("on_attach", program)


    def on_attach(self, program):
        for snippet in self._args + [self._next]:
            if isinstance(snippet, Snippet):
                snippet.dispatch_event("on_attach", program)


    def on_resize(self, width, height):
        for snippet in self._args + [self._next]:
            if isinstance(snippet, Snippet):
                snippet.dispatch_event("on_resize", width, height)


    def on_mouse_drag(self, x, y, dx, dy, button):
        for snippet in self._args + [self._next]:
            if isinstance(snippet, Snippet):
                snippet.dispatch_event("on_mouse_drag", x, y, dx, dy, button)


    def on_mouse_scroll(self, x, y, dx, dy):
        for snippet in self._args + [self._next]:
            if isinstance(snippet, Snippet):
                snippet.dispatch_event("on_mouse_scroll", x, y, dx, dy)


    def on_data(self):
        for snippet in self._args + [self]:
            if isinstance(snippet, Snippet):
                snippet.dispatch_event("on_data")



Transform.register_event_type('on_attach')
Transform.register_event_type('on_resize')
Transform.register_event_type('on_mouse_drag')
Transform.register_event_type('on_mouse_scroll')
