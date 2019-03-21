# GeoIPMap

  * **Version:** 1.0.1 (2019-03-21)
  * **Requires:** `python-matplotlib`, `python-netaddr`.

This program plots the geographical coordinates of IPs (v4) using a database
(CSV) in a worldmap using the Mercator projection.

All needed data it's contained in the folder `data/`, although through
arguments you can specify another files.  The usage of the main entry
is:

        -i <IPLIST>, --iplist <IPLIST>
                            File of IPs to plot, one per line
        -g <GEODB>, --geodb <GEODB>
                            CSV document with columns: network, lat, lon
        -f <IMAGEFILE>, --imagefile <IMAGEFILE>
                            Template image path to plot over
        -W WIDTH, --width WIDTH
                            Width in pixels of the image file
        -H HEIGHT, --height HEIGHT
                            Height in pixels of the image file
        -l LEFT, --left LEFT
                            Degrees most to the left in the image
        -r RIGHT, --right RIGHT
                            Degrees most to the right in the image
        -b BOTTOM, --bottom BOTTOM
                            Degrees most to the bottom in the image

You can see this options anytime by using the `-h` or `--help` argument.
The default values for the options `-l`, `-r`, and `-b` are calibrated
for the [Mercator
map](https://upload.wikimedia.org/wikipedia/commons/f/f4/Mercator_projection_SW.jpg)
with resolution of 2058×1746 pixels you can find in Wikipedia.

Three files are required for this program to work:

  * **Image file.**  This is a worldmap image in the Mercator
    projection.  The file properties such as `width`, `length`, and the
    degrees of left, right, and bottom boundaries depicted may be
    entered through the command line, as well as the filename.
    When changing the image, you have to adjust three points specified
    in degrees, the point most to the left (by default is -180 degrees), 
    the point most to the right (by default is 180 degrees), and the
    point most to the south.  It shouldn't be greater than -90 degrees
    (although if you have a map where the most fore south point is at -90
    degrees, you should use an approximation, such as -89.99 degrees).

    The default map for the configured settings is the one you can find
    in Wikipedia for the article: [Mercator
    Projection](https://en.wikipedia.org/wiki/Mercator_projection), but
    in the size of 2058×1746 pixels.

  * **IP list.**  A file of the IPs you want to plot in a map.  There
    have to be IP addresses, not in subnet notation or netmasks, one
    per line.  By default, the file used will be `data/ips.lst`.  For
    example:

        ...
        77.247.181.162
        198.98.56.149
        185.220.100.252
        162.247.74.202
        195.176.3.19
        145.239.91.37
        185.220.101.54
        51.15.125.181
        ...

  * **Geocoordinates database.**  A CSV file containing the following
    columns, without comments (may be this will be solved in a future
    version): `netmask, latitude, longitude`.  The default CVS file used
    is `data/geoip_ipv4.csv`.  For example:

        ...
        73.185.104.0/23,37.8209,-121.2827
        73.185.106.0/23,38.6106,-121.2789
        73.185.108.0/23,38.5879,-121.4053
        73.185.110.0/23,38.6711,-121.1495
        73.185.112.0/23,36.3170,-119.3087
        73.185.114.0/23,38.1345,-120.4516
        73.185.116.0/23,39.1663,-121.5105
        ...

## Usage

Using few options:

  1. Download the Mercator map (2058×1746 pixels) from Wikipedia
    <https://upload.wikimedia.org/wikipedia/commons/f/f4/Mercator_projection_SW.jpg>
    and save it in the `data` folder under the name of
    `worldmap_raw.jpg`.

  2. Put a file containing the IPs you want to plot (one per line) in
     the map in the folder `data` under the name of `ips.lst`.

  3. Create a CVS database with the columns: `netmask latitude
     longitude`.  See below.


## Generating a CVS database

The CSV database of 'network, longitude, latitude' is not included due
its weight, but it can be constructed easily.

  1. Download from [MaxMind](https://dev.maxmind.com) the GeoLite2 City
     database in CVS format.  You'll find it at:
  <https://geolite.maxmind.com/download/geoip/database/GeoLite2-City-CSV.zip>.

  2. Uncompress that file and work with the
     `GeoLite2-City-Blocks-IPv4.csv` file.  It's a very huge file and
     has much more information that the needed for this program to run.

  3. Create a new document using the following command:

        $ awk -F',' '{print $1","$8","$9}' GeoLite2-City-Blocks-IPv4.csv >geoip_ipv4.csv

     Put the file in the `data` directory with that name.

## Using custom files

The only requirement is the format of the files and the projection used
in the map.  You can use different filenames specifying them in the
option arguments:

Instead `python main.py`, you may use:

        $ python main.py -i <my_iplist> -g <my_geodb> -f <my_image> -b -80

When changing the image, you have to specify, at least, the degrees more
to the south the map displays (and in some cases, the points more to the
west and/or to the right when the map is not calibrated in the range
[-180,180] for degrees of longitude.

## License

This program is under the BSD 2-Clause license.  This license has also
been called the "Simplified BSD License" and the "FreeBSD License".

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

      1. Redistributions of source code must retain the above copyright
         notice, this list of conditions and the following disclaimer.

      2. Redistributions in binary form must reproduce the above
         copyright notice, this list of conditions and the following
         disclaimer in the documentation and/or other materials provided
         with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.

The BSD 2-clause license allows you almost unlimited freedom with the
software so long as you include the BSD copyright notice in it (found in
the `LICENSE` file).

Under this license, you may:

  * use the software for commercial use;
  * modify the software and create derivatives;
  * distribute original or modified works;
  * place warranty on the software licensed.

You must:

  * include copyright
  * include the full text of license in modified software.

More information about the license:
<https://en.wikipedia.org/wiki/BSD_licenses#2-clause>.


---

J. A. Corbal, 2019.

