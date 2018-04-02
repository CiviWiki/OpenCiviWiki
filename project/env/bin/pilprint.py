#!/var/www/OpenCiviWiki/project/env/bin/python
#
# The Python Imaging Library.
# $Id$
#
# print image files to postscript printer
#
# History:
# 0.1   1996-04-20 fl   Created
# 0.2   1996-10-04 fl   Use draft mode when converting.
# 0.3   2003-05-06 fl   Fixed a typo or two.
#

from __future__ import print_function
import getopt
import os
import sys
import subprocess

VERSION = "pilprint 0.3/2003-05-05"

from PIL import Image
from PIL import PSDraw

letter = (1.0*72, 1.0*72, 7.5*72, 10.0*72)


def description(filepath, image):
    title = os.path.splitext(os.path.split(filepath)[1])[0]
    format = " (%dx%d "
    if image.format:
        format = " (" + image.format + " %dx%d "
    return title + format % image.size + image.mode + ")"

if len(sys.argv) == 1:
    print("PIL Print 0.3/2003-05-05 -- print image files")
    print("Usage: pilprint files...")
    print("Options:")
    print("  -c            colour printer (default is monochrome)")
    print("  -d            debug (show available drivers)")
    print("  -p            print via lpr (default is stdout)")
    print("  -P <printer>  same as -p but use given printer")
    sys.exit(1)

try:
    opt, argv = getopt.getopt(sys.argv[1:], "cdpP:")
except getopt.error as v:
    print(v)
    sys.exit(1)

printerArgs = []  # print to stdout
monochrome = 1    # reduce file size for most common case

for o, a in opt:
    if o == "-d":
        # debug: show available drivers
        Image.init()
        print(Image.ID)
        sys.exit(1)
    elif o == "-c":
        # colour printer
        monochrome = 0
    elif o == "-p":
        # default printer channel
        printerArgs = ["lpr"]
    elif o == "-P":
        # printer channel
        printerArgs = ["lpr", "-P%s" % a]

for filepath in argv:
    try:

        im = Image.open(filepath)

        title = description(filepath, im)

        if monochrome and im.mode not in ["1", "L"]:
            im.draft("L", im.size)
            im = im.convert("L")

        if printerArgs:
            p = subprocess.Popen(printerArgs, stdin=subprocess.PIPE)
            fp = p.stdin
        else:
            fp = sys.stdout

        ps = PSDraw.PSDraw(fp)

        ps.begin_document()
        ps.setfont("Helvetica-Narrow-Bold", 18)
        ps.text((letter[0], letter[3]+24), title)
        ps.setfont("Helvetica-Narrow-Bold", 8)
        ps.text((letter[0], letter[1]-30), VERSION)
        ps.image(letter, im)
        ps.end_document()

        if printerArgs:
            fp.close()

    except:
        print("cannot print image", end=' ')
        print("(%s:%s)" % (sys.exc_info()[0], sys.exc_info()[1]))
