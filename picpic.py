#!usr/bin/env python3
# -*-coding=utf-8-*-

from PIL import Image
import sys


def main():
    # infile = sys.argv[1]
    infile = "huaji.png"
    try:
        im = Image.open(infile)
        print(im.size, im.mode)
    except IOError:
        print("Fail: Cannot open file")
        sys.exit(0)

    sz = 64
    print("resizing...")
    im = im.resize((sz, sz))

    if im.mode != "RGB":
        im = im.convert("RGB")

    bands = im.split()
    big_bands = []
    for i in [0, 1, 2]:
        tmp = bands[i].point(lambda x: (x - 128) // 2 + 128)
        lookup = [tmp.point(lambda x: x + d) for d in range(-64, 64)]

        tmp = tmp.load()
        big_tmp = Image.new("L", (sz * sz, sz * sz))
        for x in range(64):
            for y in range(64):
                big_tmp.paste(lookup[tmp[x, y] - 64], (x * 64, y * 64))

        big_bands.append(big_tmp)

    big_im = Image.merge("RGB", tuple(big_bands))
    big_im.save("output.png", "PNG")


if __name__ == "__main__":
    main()
