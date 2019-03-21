#!/usr/bin/env python
# vim: set ft=python fenc=utf8 fo=tcqrj1n:

# GEOIPMAP :: Worldmap plotting of locations associated to IPs
# Copyright (C) 2019, J. A. Corbal <jacorbal@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Just a image class, more like a container for image information"""

__author__ = "J. A. Corbal"
__copyright__ = "Copyright (C) 2019, J. A. Corbal"
__license__ = "BSD 2-Clause"
__version__ = "1.0.1"
__mantainer__ = "J. A. Corbal"
__email__ = "jacorbal@gmail.com"
__status__ = "Development"


class GeoImage(object):
    """Image class (more like a struct)."""
    def __init__(self, filepath, width, height,
                 w_deg=-180, e_deg=180, s_deg=-89.9):
        """Geo image data:

        :param filepath: Path to the image
        :type filepath: str
        :param width: Width in pixels
        :type width: int
        :param height: Height in pixels
        :type height: int
        :param w_deg: Most fore west position in degrees
        :type w_deg: float
        :param e_deg: Most fore east position in degrees
        :type e_deg: float
        :param s_deg: Most fore south position in degrees
        :type s_deg: float
        """
        self.__set_filepath(filepath)
        self.__set_width(width)
        self.__set_height(height)
        self.__set_w_deg(w_deg)
        self.__set_e_deg(e_deg)
        self.__set_s_deg(s_deg)

    def __get_filepath(self):
        return self._filepath

    def __set_filepath(self, filepath):
        if filepath:
            self._filepath = filepath

    def __get_width(self):
        return self._width

    def __get_height(self):
        return self._height

    def __get_w_deg(self):
        return self._w_deg

    def __get_e_deg(self):
        return self._e_deg

    def __get_s_deg(self):
        return self._s_deg

    def __set_width(self, width):
        if (width > 0):
            self._width = width

    def __set_height(self, height):
        if (height > 0):
            self._height = height

    def __set_w_deg(self, w_deg):
        self._w_deg = w_deg

    def __set_e_deg(self, e_deg):
        self._e_deg = e_deg

    def __set_s_deg(self, s_deg):
        self._s_deg = s_deg

    filepath = property(__get_filepath, __set_filepath)
    width = property(__get_width, __set_width)
    height = property(__get_height, __set_height)
    w_deg = property(__get_w_deg, __set_w_deg)
    e_deg = property(__get_e_deg, __set_e_deg)
    s_deg = property(__get_s_deg, __set_s_deg)
