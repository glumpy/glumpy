#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Transform

Transforms are specific snippet that can handle and propagate events such that
they are able to react to window event.

A Transform can be connected to the following events:

 * attach
 * resize
 * mouse_scroll
 * mouse_grab
 * mouse_press
 * mouse_release
"""
import os
import numpy as np
from glumpy.gloo import Snippet
from glumpy.app.window.event import EventDispatcher


class Transform(Snippet,EventDispatcher):

    @classmethod
    def get(cls, key, kwargs):
        """ Return a given parameter from the kwargs and remove it """
        if  key in kwargs.keys():
            value = kwargs[key]
            del kwargs[key]
            return value
        return None


    def __init__(self, code, *args, **kwargs):
        Snippet.__init__(self, code, None, *args, **kwargs)
        EventDispatcher.__init__(self)
        self._window = None


    def attach(self, program):
        """ Attach the transform to a program """

        Snippet.attach(self,program)
        self.dispatch_event("on_attach", program)


    def on_attach(self, program):
        for snippet in list(self._args):
            if isinstance(snippet, Snippet):
                snippet.dispatch_event("on_attach", program)
        if self._next:
            operator, snippet = self._next
            snippet.dispatch_event("on_attach", program)

    def on_resize(self, width, height):
        for snippet in list(self._args):
            if isinstance(snippet, Snippet):
                snippet.dispatch_event("on_resize", width, height)
        if self._next:
            operator, snippet = self._next
            snippet.dispatch_event("on_resize", width, height)


    def on_mouse_drag(self, x, y, dx, dy, button):
        for snippet in list(self._args):
            if isinstance(snippet, Snippet):
                snippet.dispatch_event("on_mouse_drag", x, y, dx, dy, button)
        if self._next:
            operator, snippet = self._next
            snippet.dispatch_event("on_mouse_drag", x, y, dx, dy, button)


    def on_mouse_scroll(self, x, y, dx, dy):
        for snippet in list(self._args):
            if isinstance(snippet, Snippet):
                snippet.dispatch_event("on_mouse_scroll", x, y, dx, dy)
        if self._next:
            operator, snippet = self._next
            snippet.dispatch_event("on_mouse_scroll", x, y, dx, dy)


    # def on_data(self):
    #     for snippet in self._args:
    #         if isinstance(snippet, Snippet):
    #             snippet.dispatch_event("on_data")
    #     if self._next:
    #         operator, snippet = self._next
    #         snippet.dispatch_event("on_data")



Transform.register_event_type('on_attach')
Transform.register_event_type('on_resize')
Transform.register_event_type('on_mouse_drag')
Transform.register_event_type('on_mouse_scroll')
Transform.register_event_type('on_mouse_press')
Transform.register_event_type('on_mouse_release')
