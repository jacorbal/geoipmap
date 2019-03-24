#!/usr/bin/env python
# vim: set ft=python fenc=utf8 fo=tcqrj1n:

# GEOIPMAP :: World map plotting of locations associated to IPs
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

"""
Methods to gather longitude and latitude coordinates given an IP address
using a database (CSV) and plot those points into a world map using the
Mercator projection.

Required:
  * List of IPs (one IP per line)
  * Geolocalization database in the format of a CSV with the following
    columns: 'network,latitude,longitude', where latitude and longitude
    are floating point degrees.
  * Map image.  If the properties change, those changes must be
    addressed in this file.
"""

__author__ = "J. A. Corbal"
__copyright__ = "Copyright (C) 2019, J. A. Corbal"
__license__ = "BSD 2-Clause"
__version__ = "1.2.0"
__mantainer__ = "J. A. Corbal"
__email__ = "jacorbal@gmail.com"
__status__ = "Development"


import csv
import math
import matplotlib.patches
import matplotlib.pyplot as plt
import multiprocessing
from netaddr import IPAddress
from netaddr import IPNetwork
from netaddr import valid_ipv4
import threading


class GeoIpMap(object):
    """GeoIpMap class.  Get the data, calculate and plot.

    This class instantiates objects capable of the following methods:

      1. Get list of IPs and database of IPs and geocoordinates
      2. Convert IP addresses to pixels: `ips_to_pixels`
      3. Plot the pixels in a image: `plot`

    In order to perform this actions, three files are needed:

      * `ips_file`.  A list of the IPs to plot, one per line
      * `geodb_file`.  A CSV file with columns: 'netmask,lat,lon'
      * Image file.  Contained indirectly in the `img` object

    ..note:: Right now, the files must be formatted with no comments.

    This class returns the `_pixels` set attribute when invoked for
    printing, containing the pairs (`x`, `y`) to be drawn in the map.
    """

    def __init__(self, ips_file, geodb_file, img,
                 method='multiprocessing',  num_workers=4,
                 num_splits=10, verbose=False):
        """Initializes the GeoIPMap object.

        If the method is 'threads', then the method for finding the IPs
        in the table with be done by the `threading` module (by the
        applying `__ips_to_pixels_threading`); otherwise it will use the
        `multiprocessing` module (using `__ips_to_pixels_multiprocessing`).
        If `num_splits` is less or equal to one, none of those methods
        will be used, and the table search is done in the "classical
        way" (with `__ips_to_pixels_raw`).

        When using `method=threading`, the argument `num_splits`
        indicate in how many chunks the list is divided in order to make
        better comparisons.  This variable is nonfunctional when using
        the multiprocessing method.

        When using `method!=threading` (i.e., `method=multiprocessing`),
        the argument `num_workers` indicate how many workers are being
        used in the calculation.  This variable is nonfunctional when
        using the threading method.

        When using `method=raw`, then no multiprocessing or threading is
        performed.

        :param iplist_file: IP list file, one IP per line
        :type iplist_file: str
        :param geodb_file: Netmask, latitude and longitude CSV database
        :type geodb_file: str
        :param img: Image object with information to plot
        :type img: GeoImage
        :param num_splits: Splits of `geodb_file` for reading (threading)
        :type num_splits: int
        :param num_workers: Number of workers when multiprocessing
        :type num_workers: int
        :param verbose: When true, print information on screen
        :type verbose: bool
        """
        self._pixels = set()
        self._img = img
        self._method = method
        self._verbose = verbose
        self.__set_num_splits(num_splits)
        self.__set_num_workers(num_workers)
        self.__set_geodb(geodb_file)
        self.__set_ips(ips_file)

    def __get_num_splits(self):
        return self._num_splits

    def __get_num_workers(self):
        return self._num_workers

    def __get_geodb(self):
        return self._geodb

    def __get_ips(self):
        return self._ips

    def __set_geodb(self, geodb_file):
        if (self._verbose):
            print('Unpacking', geodb_file)
        with open(geodb_file, 'rt') as f:
            reader = csv.reader(f)
            self._geodb = list(reader)

    def __set_ips(self, ips_file):
        if (self._verbose):
            print('Unpacking', ips_file)
        with open(ips_file, 'rt') as f:
            self._ips = f.readlines()
            self._ips = [x.strip() for x in self._ips]

    def __set_num_splits(self, num_splits):
        """Sets the number of splits the threading function can do."""
        if num_splits < 0:
            self._num_splits = 0
#        elif num_splits > 200:
#            self._num_splits = 200
        else:
            self._num_splits = num_splits

    def __set_num_workers(self, num_workers):
        """Sets the number of workers for multiprocessing."""
        if num_workers < 0:
            self._num_workers = 0
        else:
            self._num_workers = num_workers

    def __del_ips(self):
        del self._ips

    def __del_geodb(self):
        del self._geodb

    def geo_to_pixel(self, lat, lon):
        """Converts longitude and latitude to Mercator proj. coords.

        :param lat: Latitude in degrees
        :type lat: float
        :param lon: Longitude in degrees
        :type lon: float
        :return: Pixel coordinates (`x`, `y`)
        :rtype: pair
        """
        lat_south_rad = math.radians(self._img.s_deg)
        lat_rad = math.radians(lat)
        lon_delta = (self._img.e_deg - self._img.w_deg)
        map_width = (self._img.width / lon_delta) * 360 / (2 * math.pi)
        offset_y = (map_width /
                    2 * math.log((1 + math.sin(lat_south_rad)) /
                                 (1 - math.sin(lat_south_rad))))

        x = (lon - self._img.w_deg) * (self._img.width / lon_delta)
        y = self._img.height - \
            ((map_width / 2 * math.log((1 + math.sin(lat_rad)) /
                                       (1 - math.sin(lat_rad)))) -
             offset_y)

        return (x, y)

    def __ips_to_pixels_raw(self):
        """Return a list of pairs (`x`, `y`) from a list of IPs.

        ..note:: This method is very heavy; just for debugging.
                 The original purpose of this method was to test the
                 program, but other methods are
                 `__ips_to_pixels_threading` and
                 `__ips_to_pixels_multiprocessing`.

        This method check the geoposition of the list of IP using a
        database file in the format CSV, then translate their
        (`lon`, `lat`) to the points in a plane.

        :see: self.geo_to_pixel
        """
        if self._verbose:
            print("Gathering data; this may take a while...")

        self._pixels = {self.geo_to_pixel(float(lat), float(lon))
                        for [nw, lat, lon] in self._geodb
                        for ip in self._ips
                        if valid_ipv4(ip) and
                        IPAddress(ip) in IPNetwork(nw)}

        if self._verbose:
            print("Data gathered!")

    def __match_geodb(self, start=None, end=None):
        """Private method to get the pixels for an IP.

        This method check the geoposition of the list of IP using a
        database file in the format CSV, then translate their
        (`lon`, `lat`) to the points in a plane.  But instead of
        searching in the whole database, it looks within a range defined
        by [`start`, `end`].  It `start` and/or `end` are `None`, then
        it will be considered repectively the beginning and the end of
        the list.

        :param start: Where to start in the CSV database
        :type start: int
        :param end: Where to end
        :type start: int
        """
        for nw, lat, lon in self._geodb[start:end]:
            for ip in self._ips:
                if valid_ipv4(ip) and IPAddress(ip) in IPNetwork(nw):
                    self._pixels.add(self.geo_to_pixel(float(lat),
                                                       float(lon)))

    def __ips_to_pixels_threading(self):
        """Splits the load of `__match_geodb` to run collectively.

        This is the threading version of `ips_to_pixels`

        ..see:: self.__ips_to_pixels_raw
        """
        if self._verbose:
            print("Threading; gathering data; this may take a while...")

        split_size = len(self._geodb) // self._num_splits
        threads = []
        for i in range(self._num_splits):
            start = i * split_size
            end = None if i + 1 == self._num_splits \
                else (i + 1) * split_size
            threads.append(
                threading.Thread(target=self.__match_geodb,
                                 args=(start, end)))
            threads[-1].start()

        for t in threads:
            t.join()

        if self._verbose:
            print("Data gathered!")

    def __ips_to_pixels_multiprocessing(self):
        """Splits the load of `__match_geodb` to run collectively.

        This is the multiprocessing version of `ips_to_pixels`

        ..see:: self.__ips_to_pixels_raw
        """
        if self._verbose:
            print("Multiprocessing; gathering data; this may take a while...")

        workers = []
        for i in range(self._num_workers):
            workers.append(multiprocessing.Process(target=self.__match_geodb))
            workers[-1].start()

        for worker in workers:
            worker.join()

        if self._verbose:
            print("Data gathered!")

    def ips_to_pixels(self):
        """Sets the default method for translating IPs to pixels.

        Depending on the class attribute `self._num_splits`, it chooses
        a method with threading/multiprocessing or without them.

        When the number of workers is one (or less), instead of
        multiprocessing the calculations, those are made by the *raw*
        method.  The same happens when using the threading method using
        one split of the data.
        """
        if self._num_splits <= 1 or self._num_workers <= 1 or \
           self._method == 'raw':
            self.__ips_to_pixels_raw()
        else:
            if self._method == 'threading':
                self.__ips_to_pixels_threading()
            else:
                self.__ips_to_pixels_multiprocessing()

    def plot(self, radius=None):
        """Plot coordinates from a list of pairs (`x`, `y`) as circles.

        When not set, the radius of the circle is obtained from the
        resolution of the image, where usually 'width > height' but
        'width ~= height'.  The default radius is the 0.3% of the
        largest dimension of the image, so:

                ============ ========
                 Resolution   Radius
                ============ ========
                  800×600      2.400
                 1024×768      3.072
                 1280×1024     3.840
                 1920×1080     5.760
                 3840×2160    11.520
                 7680×4320    23.040
                ============ ========

        The default image has a resolution of 2058×1746 pixels, so its
        radius will be 6.174.

        :param radius: radius in pixels of the circles
        :type radius: float
        """
        if not radius:
            radius = 0.003 * self._img.width \
                if self._img.width > self._img.height \
                else 0.003 * self._img.height

        img = matplotlib.image.imread(self._img.filepath)
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.imshow(img)

        for x, y in self._pixels:
            circ = matplotlib.patches.Circle((x, y), radius,
                                             facecolor='red',
                                             edgecolor='black')
            ax.add_patch(circ)

        # Show the image
        plt.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        if self._verbose:
            print('Plotting')
        plt.show()

    # Properties
    num_splits = property(__get_num_splits, __set_num_splits)
    num_workers = property(__get_num_workers, __set_num_workers)
    ips = property(__get_ips, __set_ips, __del_ips)
    geodb = property(__get_geodb, __set_geodb, __del_geodb)

    # Class printing
    def __repr__(self):
        return self._pixels

    def __str__(self):
        return self._pixels
