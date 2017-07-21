#!usr/bin/env python3
# -*-coding=utf-8-*-

from PIL import Image
import getopt
import sys
import os


def usage():
    print("usage: %s [-s size] [-a alpha] <file name>" % sys.argv[0])


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:a:")
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

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

    sz = 64
    alpha = 0.5

    for o, a in opts:
        if o == "-s":
            sz = int(a)
        elif o == "-a":
            alpha = float(a)

    if not (0 < sz <= 256 and 0.0 <= alpha <= 1.0):
        print("Error: out of range")
        sys.exit(-1)

    print("resizing...")
    im = im.resize((sz, sz))

    layer0 = im.resize((sz * sz, sz * sz), Image.NEAREST)
    layer1 = Image.new(im.mode, (sz * sz, sz * sz))

    for x in range(sz):
        for y in range(sz):
            layer1.paste(im, (x * sz, y * sz))

    print("merging...")
    output = Image.blend(layer0, layer1, alpha)

    outfile = os.path.splitext(infile)[0] + "_picpic.png"
    output.save(outfile, "PNG")
    print("done.")


if __name__ == "__main__":
    main()
