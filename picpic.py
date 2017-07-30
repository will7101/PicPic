#!usr/bin/env python3
# -*-coding=utf-8-*-

from PIL import Image
import getopt
import sys
import os


def usage():
    print("usage: %s [-h] [-x width] [-y height] [-a alpha] <filename>" % sys.argv[0])


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hx:y:a:")
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    if ("-h", "") in opts:
        usage()
        sys.exit(0)

    try:
        infile = args[0]
        im = Image.open(infile)
        print(im.size, im.mode)
    except IndexError as err:
        print(err)
        usage()
        sys.exit(-1)
    except IOError as err:
        print(err)
        print("Error: cannot open file")
        sys.exit(-1)

    im = im.convert("RGBA")

    width = 64
    height = 64
    alpha = 0.5

    for o, a in opts:
        if o == "-x":
            width = int(a)
        if o == "-y":
            height = int(a)
        elif o == "-a":
            alpha = float(a)

    if not (0 < width <= 256 and 0 < height <= 256 and 0.0 <= alpha <= 1.0):
        print("Error: out of range")
        sys.exit(-1)

    print("resizing...")
    sz = min(width, height)
    pixel = im.resize((sz, sz), Image.LANCZOS)
    im = im.resize((width, height), Image.LANCZOS)

    layer0 = im.resize((width * sz, height * sz), Image.NEAREST)
    layer1 = Image.new(im.mode, layer0.size)

    for x in range(width):
        for y in range(height):
            layer1.paste(pixel, (x * sz, y * sz))

    print("merging...")
    output = Image.blend(layer0, layer1, alpha)

    outfile = os.path.splitext(infile)[0] + "_picpic.png"
    output.save(outfile, "PNG")
    print("done.")


if __name__ == "__main__":
    main()
