# GeoIPMap

This program plots the geographical coordinates of IPs (v4) using a
database (CSV) in a world map using the Mercator projection.

  * **Version:** 1.2.0 (2019-03-24)
  * **Requires:** [`matplotlib`](https://matplotlib.org/),
                  [`netaddr`](https://pypi.org/project/netaddr).


## Installing dependencies

Many Linux distributions already have a package manager that allows to
download this dependencies.

  * Debian:

        $ sudo apt-get install python-matplotlib
        $ sudo apt-get install python-netaddr

  * Gentoo:

        $ sudo emerge -a matplotlib
        $ sudo emerge -a netaddr

  * Arch Linux:

        $ sudo pacman -S python-matplotlib
        $ sudo pacman -S python-netaddr

If that's not the case, you can always install them by using the `pip`
tool.

        $ python -m pip install -U matplotlib
        $ python -m pip install -U netaddr

Make the necesary changes depending on the default version of Python of
your system, (e.g., use `python3` instead of `python`).

## Basics

All needed data could be conveniently contained in the folder `data/`,
although through arguments you can specify another files or path.  The
usage of the main entry is:

        -i <IPLIST>, --iplist <IPLIST>
                            File of IPs to plot, one per line
        -g <GEODB>, --geodb <GEODB>
                            CSV document with columns: 'network,lat,lon'
        -f <IMAGEFILE>, --imagefile <IMAGEFILE>
                            Path for the template image to plot over
        -W <WIDTH>, --width <WIDTH>
                            Width in pixels of the image file
        -H <HEIGHT>, --height <HEIGHT>
                            Height in pixels of the image file
        -l <LEFT>, --left <LEFT>
                            Degrees most to the left in the image
        -r <RIGHT>, --right <RIGHT>
                            Degrees most to the right in the image
        -b <BOTTOM>, --bottom <BOTTOM>
                            Degrees most to the bottom in the image
        -n <NSPLITS>, --nsplits <NSPLITS>
                            Splits for reading 'geodb' file (threading)

You can see this options anytime by using the `-h` or `--help` argument.
The default values for the options `-l`, `-r`, and `-b` are calibrated
for the Mercator map with resolution of 2058×1746 pixels you can find in
Wikipedia, as explained below.

Three files are required for this program to work:

  * **Image file.**  This is a world map image in the Mercator
    projection.  The file properties such as `width`, `length`, and the
    degrees of left, right, and bottom boundaries depicted may be
    entered through the command line, as well as the filename.  When
    changing the image, you have to adjust three points specified in
    degrees, the point most to the left (by default is -180°), the point
    most to the right (by default is 180°), and the point most to the
    south.  It shouldn't be greater than -90°, although if you have a
    map where the most fore south point is exactly at -90°, you should
    use an approximation, such as -89.99, or a division by zero may
    happen because the linear scale becomes infinitely large at the
    poles in this projection.

    The default map for the configured settings is the one you can find
    in Wikipedia for the article: "[Mercator
    Projection](https://en.wikipedia.org/wiki/Mercator_projection)", but
    in the size of 2058×1746 pixels.  It's set between 82°S and 82°N,
    *i.e.*, with latitudes in the range [-82, 82].

    You can download and use a different map, or the same map in a
    different resolution, but you'll have to specify the dimensions and
    other parameters through the command line when invoking the program.

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
    version): `netmask, latitude, longitude`.  The default CSV file used
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

## Quick usage

  1. Download the Mercator map (2058×1746 pixels) from Wikipedia:
    <https://upload.wikimedia.org/wikipedia/commons/f/f4/Mercator_projection_SW.jpg>
    and save it in the `data` folder under the name of
    `worldmap_raw.jpg`.

  2. Put a file containing the IPs you want to plot (one per line) in
     the map in the folder `data` under the name of `ips.lst`.

  3. Create a CSV database with the columns:
     `netmask,latitude,longitude` and save it in the folder `data`under
     the name `geoip_ipv4.csv`.  See below.


## Generating a CSV database

The CSV database of 'network, longitude, latitude' is not included due
its weight, but it can be constructed easily.

  1. Download from [MaxMind](https://dev.maxmind.com) the GeoLite2 City
     database in CSV format.  You'll find it at:
  <https://geolite.maxmind.com/download/geoip/database/GeoLite2-City-CSV.zip>.

  2. Uncompress that file and work with the
     `GeoLite2-City-Blocks-IPv4.csv` file.  It's a very huge file and
     has much more information that the needed for this program to run.

  3. Create a new document using the following command:

        `$ awk -F',' '{print $1","$8","$9}' GeoLite2-City-Blocks-IPv4.csv >geoip_ipv4.csv`

     Put the output file in the `data` directory with the name
     `geoip_ipv4.csv`.

## Using custom files

The only requirement is the format of the files and the projection used
in the map.  You can use different filenames specifying them in the
option arguments:

Instead `python main.py`, you may use:

        $ python main.py -i <my_iplist> -g <my_geodb> -f <my_image> -b -80

When changing the image, you have to specify, at least, the degrees more
to the south the map displays (and in some cases, the points more to the
west and/or to the right when the map is not calibrated in between 180°W
and 180°E, *i.e.*, the range [-180, 180], for degrees of longitude.


## Output and display

This is an example of the output provided by this program using
`matplotlib`.  This image is a zoomed detail.

<!-- ![Output example](images/output_example.png) -->
![Output detail example](images/output_example_detail.png
    "Output detail example")

The red dots indicate each one of the locations of the IPs in the file
`ips.lst`.  The radius of this circle is calculated automatically in the
function `plot_pixels` (in the `geoipmap.py` file).

The automatic calculation provides a way to draw the circles with a size
in relation to the image size.  The computation is performed by getting
the biggest dimension of the image, and set the radius to a 0.3% of this
length, so, for the most common resolutions:

| Resolution  | Radius |
|:-----------:|-------:|
|   800×600   |  2.400 |
|  1024×768   |  3.072 |
|  1280×1024  |  3.840 |
|  1920×1080  |  5.760 |
|  3840×2160  | 11.520 |
|  7680×4320  | 23.040 |

The default image detailed above has a resolution of 2058×1746 pixels,
so its radius will be 6.174 pixels.

This default behaviour can be altered by invoking the `plot_pixels`
function with an extra argument indicating the float value of the radius
in pixels.

        # Automatic radius
        geo.plot()

        # User defined radius
        geo.plot(radius=10)

This function is invoked in the main entry, at the end of the file
`main.py`.

**NOTE.**  This method will be probably changed in the future to a much
better approximation.


## Multiprocessing and threading

See the [benchmarks](benchmark.md) document.


---

J. A. Corbal, 2019-2020.

