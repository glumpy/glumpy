# coding: utf-8
"""
Inputhook management for GUI event loop integration.
"""

#-----------------------------------------------------------------------------
#  Copyright (C) 2008-2011  The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

try:
    import ctypes
except ImportError:
    ctypes = None
except SystemError: # IronPython issue, 2/8/2014
    ctypes = None
import os
import sys


#-----------------------------------------------------------------------------
# Utilities
#-----------------------------------------------------------------------------

def _stdin_ready_posix():
    """Return True if there's something to read on stdin (posix version)."""
    infds, outfds, erfds = select.select([sys.stdin],[],[],0)
    return bool(infds)

def _stdin_ready_nt():
    """Return True if there's something to read on stdin (nt version)."""
    return msvcrt.kbhit()

def _stdin_ready_other():
    """Return True, assuming there's something to read on stdin."""
    return True #


def _ignore_CTRL_C_posix():
    """Ignore CTRL+C (SIGINT)."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def _allow_CTRL_C_posix():
    """Take CTRL+C into account (SIGINT)."""
    signal.signal(signal.SIGINT, signal.default_int_handler)

def _ignore_CTRL_C_other():
    """Ignore CTRL+C (not implemented)."""
    pass

def _allow_CTRL_C_other():
    """Take CTRL+C into account (not implemented)."""
    pass

if os.name == 'posix':
    import select
    import signal
    stdin_ready = _stdin_ready_posix
    ignore_CTRL_C = _ignore_CTRL_C_posix
    allow_CTRL_C = _allow_CTRL_C_posix
elif os.name == 'nt':
    import msvcrt
    stdin_ready = _stdin_ready_nt
    ignore_CTRL_C = _ignore_CTRL_C_other
    allow_CTRL_C = _allow_CTRL_C_other
else:
    stdin_ready = _stdin_ready_other
    ignore_CTRL_C = _ignore_CTRL_C_other
    allow_CTRL_C = _allow_CTRL_C_other


#-----------------------------------------------------------------------------
# Main InputHookManager class
#-----------------------------------------------------------------------------


class InputHookManager(object):
    """Manage PyOS_InputHook for different GUI toolkits.

    This class installs various hooks under ``PyOSInputHook`` to handle
    GUI event loop integration.
    """

    def __init__(self):
        if ctypes is None:
            warn("IPython GUI event loop requires ctypes, %gui will not be available")
            return
        self.PYFUNC = ctypes.PYFUNCTYPE(ctypes.c_int)
        self._reset()

    def _reset(self):
        self._callback_pyfunctype = None
        self._callback = None
        self._installed = False

    def get_pyos_inputhook(self):
        """Return the current PyOS_InputHook as a ctypes.c_void_p."""
        return ctypes.c_void_p.in_dll(ctypes.pythonapi,"PyOS_InputHook")

    def get_pyos_inputhook_as_func(self):
        """Return the current PyOS_InputHook as a ctypes.PYFUNCYPE."""
        return self.PYFUNC.in_dll(ctypes.pythonapi,"PyOS_InputHook")

    def set_inputhook(self, callback):
        """Set PyOS_InputHook to callback and return the previous one."""
        # On platforms with 'readline' support, it's all too likely to
        # have a KeyboardInterrupt signal delivered *even before* an
        # initial ``try:`` clause in the callback can be executed, so
        # we need to disable CTRL+C in this situation.
        ignore_CTRL_C()
        self._callback = callback
        self._callback_pyfunctype = self.PYFUNC(callback)
        pyos_inputhook_ptr = self.get_pyos_inputhook()
        original = self.get_pyos_inputhook_as_func()
        pyos_inputhook_ptr.value = \
            ctypes.cast(self._callback_pyfunctype, ctypes.c_void_p).value
        self._installed = True
        return original

    def clear_inputhook(self, app=None):
        """Set PyOS_InputHook to NULL and return the previous one.

        Parameters
        ----------
        app : optional, ignored
          This parameter is allowed only so that clear_inputhook() can be
          called with a similar interface as all the ``enable_*`` methods.  But
          the actual value of the parameter is ignored.  This uniform interface
          makes it easier to have user-level entry points in the main IPython
          app like :meth:`enable_gui`."""
        pyos_inputhook_ptr = self.get_pyos_inputhook()
        original = self.get_pyos_inputhook_as_func()
        pyos_inputhook_ptr.value = ctypes.c_void_p(None).value
        allow_CTRL_C()
        self._reset()
        return original

inputhook_manager = InputHookManager()
