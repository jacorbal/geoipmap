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

import argparse
from geoipmap import GeoImage
from geoipmap import GeoIpMap


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--iplist', default='data/ips.lst',
                        help="File of IPs to plot, one per line")
    parser.add_argument('-g', '--geodb', default='data/geoip_ipv4.csv',
                        help="CSV document with columns: 'network,lat,lon'")
    parser.add_argument('-f', '--imagefile', default='data/worldmap_raw.jpg',
                        help="Path for the template image to plot over")
    parser.add_argument('-W', '--width', default='2058',
                        help="Width in pixels of the image file")
    parser.add_argument('-H', '--height', default='1746',
                        help="Height in pixels of the image file")
    parser.add_argument('-l', '--left', default='-180',
                        help="Degrees most to the left in the image")
    parser.add_argument('-r', '--right', default='180',
                        help="Degrees most to the right in the image")
    parser.add_argument('-b', '--bottom', default='-82',
                        help="Degrees most to the bottom in the image")
    parser.add_argument('-n', '--nsplits', default='0',
                        help="Splits for reading 'geodb' file (threading)")
    args = parser.parse_args()

    img = GeoImage(args.imagefile,
                   width=int(args.width),
                   height=int(args.height),
                   w_deg=float(args.left),
                   e_deg=float(args.right),
                   s_deg=float(args.bottom))
    geo = GeoIpMap(args.iplist, args.geodb, img,
                   num_splits=int(args.nsplits),
                   verbose=True)
    geo.ips_to_pixels()
    geo.plot()
