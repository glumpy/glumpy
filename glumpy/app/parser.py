# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Default argument parser for any glumpy program.
"""
import argparse
import glumpy.defaults


# Default parser
__parser__ = None


def get_default():
    """ Get the default parser. """

    global __parser__

    if __parser__ is None:
        __parser__ = argparse.ArgumentParser()
        set_default_options(__parser__)
    return __parser__



def get_options():
    """ Parse and retrun command line options. """

    options, unknown = get_default().parse_known_args()
    return options


def set_default_options(parser):
    """ Set parser default options. """

    # Backend option
    parser.add_argument("--backend", "-b",
                        default = glumpy.defaults.backend(),
                        choices = ('glfw', 'sdl2', 'qt5', 'pyside',
                                   'pyglet', 'sdl',  'freeglut', 'osxglut'),
                        help="Backend to use, one of ")

    # Record
    parser.add_argument("--record",
                        action='store_true',
                        help='Record a movie (default is "movie.mp4")')

    # Interactive mode
    parser.add_argument("--interactive", "-i",
                        action='store_true',
                        help="Interactive mode")

    # Framerate option
    parser.add_argument("--framerate", "-f",
                        default=60,
                        type=int,
                        help="Framerate in frames/second")

    # Display framerate option
    parser.add_argument("--display-fps",
                        action='store_true',
                        help="Display framerate in the console")

    # Framerate option
    parser.add_argument("--debug", "-d",
                        action='store_true',
                        help="Verbose debug mode")

    # Window size
    parser.add_argument("--size", "-s",
                        default = "",
                        type=str,
                        help="Window size")

    # Window position
    parser.add_argument("--position", "-p",
                        default = "",
                        type=str,
                        help="Window position")

    # Single buffer
    parser.add_argument("--single-buffer",
                        action='store_true',
                        help="Single buffer mode")

    # Stereo mode
    parser.add_argument("--stereo",
                        action='store_true',
                        help="Stereo mode")

    # vertical synchronization
    parser.add_argument("--vsync",
                        default=False,
                        type=bool,
                        help="Enable/disable vertical synchronization")

    # sRGB mode
    parser.add_argument("--srgb",
                        action='store_true',
                        help="sRGB mode (gamma correction)")

    # Depth buffer size
    parser.add_argument("--depth-size",
                        default=16,
                        type=int,
                        help="Depth buffer size")

    # Stencil buffer size
    parser.add_argument("--stencil-size",
                        default=0,
                        type=int,
                        help="Stencil buffer size")

    # GL API
    parser.add_argument("--gl-api",
                        default="GL",
                        choices=["GL","ES"],
                        help="GL API")

    # GL profile
    parser.add_argument("--gl-profile",
                        default="none",
                        choices=["none","core", "compatibility"],
                        help="GL context profile (only relevant for GL > 3.0)")

    # GL version
    parser.add_argument("--gl-version",
                        default="2.1",
                        help="GL version")
