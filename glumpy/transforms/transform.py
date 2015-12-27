# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import os
import numpy as np
from glumpy.gloo import Snippet
from glumpy.app.window.event import EventDispatcher


class Transform(Snippet,EventDispatcher):
    """
    Transform

    Transforms are snippets that can handle and propagate events such that they
    are able to react to window event.

    A Transform can be connected to the following events:

    * ``on_attach``
    * ``on_resize``
    * ``on_mouse_scroll``
    * ``on_mouse_grab``
    * ``on_mouse_press``
    * ``on_mouse_release``
    """

    aliases = { }

    @classmethod
    def _get_kwarg(cls, key, kwargs, default=None):
        """ Return a given parameter from the kwargs and remove it """
        if  key in kwargs.keys():
            value = kwargs[key]
            del kwargs[key]
            return value
        return default


    def __init__(self, code, *args, **kwargs):
        Snippet.__init__(self, code, None, *args, **kwargs)
        EventDispatcher.__init__(self)
        self._window = None


    def __getitem__(self, key):
        """ Override getitem to enforce aliases """

        key = self.__class__.aliases.get(key, key)
        return Snippet.__getitem__(self, key)


    def __setitem__(self, key, value):
        """ Override getitem to enforce aliases """

        key = self.__class__.aliases.get(key, key)
        Snippet.__setitem__(self, key, value)




    def attach(self, program):
        """ Attach the transform to a program """

        if program not in self._programs:
            self._programs.append(program)
        program._build_uniforms()
        program._build_attributes()

        for snippet in self.snippets[1:]:
            snippet.attach(program)

        self.dispatch_event("on_attach", program)


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
