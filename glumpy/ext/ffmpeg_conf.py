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
Configuration MoviePy


This file enables you to specify a configuration for MoviePy. In
particular you can enter the path to the FFMPEG and ImageMagick
binaries.

Instructions
--------------


FFMPEG_BINARY
    Normally you can leave this one to its default (None) and MoviePy
    will detect automatically the right name, which will be either
    'ffmpeg' (on linux) or 'ffmpeg.exe' (on windows). If you want to
    use a binary at a special location on you disk, enter it like that:

    FFMPEG_BINARY = r"path/to/ffmpeg(.exe)"

    Warning: the 'r' before the path is important, especially on Windows.


IMAGEMAGICK_BINARY
    For linux users, 'convert' should be fine.
    For Windows users, you must specify the path to the ImageMagick
    'convert' binary. For instance:

    IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-6.8.8-Q16\convert.exe"

You can run this file to check that FFMPEG has been detected.
"""

FFMPEG_BINARY = None
IMAGEMAGICK_BINARY = 'convert'



# =====================================================================
# CODE. Don't write anything below this line !

import subprocess as sp

def try_cmd(cmd):
        try:
            proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
            proc.communicate()
        except:
            return False
        else:
            return True


if FFMPEG_BINARY is None:

    if try_cmd(['ffmpeg']):
        FFMPEG_BINARY = 'ffmpeg'
    elif try_cmd(['ffmpeg.exe']):
        FFMPEG_BINARY = 'ffmpeg.exe'
    else:
        raise IOError("FFMPEG binary not found. Try installing MoviePy"
                      " manually and specify the path to the binary in"
                      " the file conf.py")

if __name__ == "__main__":
    if try_cmd([FFMPEG_BINARY]):
        print( "MoviePy : ffmpeg successfully found." )
    else:
        print( "MoviePy : can't find ffmpeg." )
