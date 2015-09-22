# The MIT License (MIT)
#
# Copyright (c) 2014 Zulko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# File from the MoviePy project - released under licence MIT
# See https://github.com/Zulko/moviepy

"""
Configuration of MoviePy


This file enables you to specify a configuration for MoviePy. In
particular you can enter the path to the FFMPEG and ImageMagick
binaries.

These changes must be done BEFORE installing MoviePy: first make the changes,
then install MoviePy with

    [sudo] python setup.py install

Note that you can also change the path to the binaries AFTER installation, but
only for one script at a time, as follows:

>>> import moviepy.config as cf
>>> cf.change_settings({"FFMPEG_BINARY": "some/new/path/to/ffmpeg"})
>>> print( cf.get_setting("FFMPEG_BINARY") )  # prints the current setting


Instructions
--------------

FFMPEG_BINARY
    Normally you can leave this one to its default ('ffmpeg-imageio') at which
    case image-io will download the right ffmpeg binary (at first use) and then
    always use that binary.
    The second option is 'auto-detect', in this case ffmpeg will be whatever
    binary is found on the computer generally 'ffmpeg' (on linux) or 'ffmpeg.exe'
    (on windows).
    Third option: If you want to use a binary at a special location on you disk,
    enter it like that:

    FFMPEG_BINARY = r"path/to/ffmpeg" # on linux
    FFMPEG_BINARY = r"path\to\ffmpeg.exe" # on windows

    Warning: the 'r' before the path is important, especially on Windows.


IMAGEMAGICK_BINARY
    For linux users, 'convert' should be fine.
    For Windows users, you must specify the path to the ImageMagick
    'convert' binary. For instance:

    IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-6.8.8-Q16\convert.exe"

"""

FFMPEG_BINARY = 'ffmpeg'
IMAGEMAGICK_BINARY = 'auto-detect'
