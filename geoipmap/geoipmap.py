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

"""
Methods to gather longitude and latitude coordinates given an IP address
using a database (CSV) and plot those points into a worldmap using the
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
__version__ = "1.0.1"
__mantainer__ = "J. A. Corbal"
__email__ = "jacorbal@gmail.com"
__status__ = "Development"


import csv
import math
import matplotlib.patches
import matplotlib.pyplot as plt
from netaddr import IPAddress
from netaddr import IPNetwork
from netaddr import valid_ipv4


def geo_to_pixel(lat, lon, width, height, lon_west, lon_east, lat_south):
    """Converts longitude and latitude to Mercator projection coordinates.

    :param lat: Latitude in degrees
    :type lat: float
    :param lon: Longitude in degrees
    :type lon: float
    :param width: Map width in pixels
    :type width: int
    :param height: Map height in pixels
    :type height: int
    :param lon_west: Longitude of the left side of the map in degrees
    :type lon_west: float
    :param lon_east: Longitude of the right side of the map in degrees
    :type lon_east: float
    :param lat_south: Latitude of the bottom of the map in degrees
    :type lat_south: float
    :return: Pixel coordinates (x,y)
    :rtype: pair
    """
    lat_south_rad = math.radians(lat_south)
    lat_rad = math.radians(lat)
    lon_delta = (lon_east - lon_west)
    map_width = (width / lon_delta) * 360 / (2 * math.pi)
    offset_y = (map_width /
                2 * math.log((1 + math.sin(lat_south_rad)) /
                             (1 - math.sin(lat_south_rad))))

    x = (lon - lon_west) * (width / lon_delta)
    y = height - ((map_width /
                   2 * math.log((1 + math.sin(lat_rad)) /
                                (1 - math.sin(lat_rad)))) - offset_y)

    return (x, y)


def ips_to_pixels(lst_ips_file, csv_nwgeo_file, image, verbose=False):
    """Return a list of pairs (x,y) from a list of IPs.

    This method check the geoposition of the list of IP using a database
    file in the format CSV, then translate their (lon,lat) to the points
    in a plane.

    The "pixels" are in reality circles with a radius determined by the
    aspect ratio of the image so, in the typical ratios, the radius of
    that circle is around seven pixels long.

    :param lst_ips_file: File with a list of IPs, one per line
    :type lst_ips_file: str
    :param csv_nwgeo_file: CSV file with a list of networks and geocoords.
    :type csv_nwgeo_file: str
    :param image: Image where the points will be plotted
    :type image: SimpleImage
    :return: Set of pairs (x,y) associated to the IPs
    :rtype: set

    :see: geo_to_pixel
    """
    with open(csv_nwgeo_file, 'rt') as f:
        reader = csv.reader(f)
        nwgeo = list(reader)  # list([network,latitude,longitude])

    with open(lst_ips_file, 'rt') as f:
        ips = f.readlines()
        ips = [x.strip() for x in ips]  # list(ip)

    if verbose:
        print("Gathering data; this may take a while...")

    pixels = {geo_to_pixel(float(lat), float(lon),
                           image.width, image.height,
                           image.w_deg, image.e_deg, image.s_deg)
              for [nw, lat, lon] in nwgeo
              for ip in ips
              if valid_ipv4(ip) and IPAddress(ip) in IPNetwork(nw)}

    if verbose:
        print("Data gathered!")

    return pixels


def plot_pixels(pixels, image, radius=None):
    """Plot coordinates from a list of pairs (x,y) as circles.

    When not set, the radius of the circle is obtained from the
    resolution of the image, where usually 'width > height' but
    'width ~= height'.  The default radius is the 0.3% of the largest
    dimension of the image, so:

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

    The default image has a resolution of 2058×1746 px, so its radius
    will be 6.174.

    :param pixels: Set of pairs (x,y) to plot
    :type pixels: set
    :param image: Image to draw over
    :type image: SimpleImage
    :param radius: radius in pixels of the circles
    :type radius: float
    """
    if not radius:
        radius = 0.003 * image.width if image.width > image.height \
                                     else 0.003 * image.height

    img = matplotlib.image.imread(image.filepath)
    fig, ax = plt.subplots(1)
#    fig.canvas.window().statusBar().setVisible(False)
    ax.set_aspect('equal')
    ax.imshow(img)

    for x, y in pixels:
        circ = matplotlib.patches.Circle((x, y), radius,
                                         facecolor='red',
                                         edgecolor='black')
        ax.add_patch(circ)

    # Show the image
    plt.axis('off')
#    plt.savefig("plot_" + image.filepath, bbox_inches='tight')
    plt.show()
