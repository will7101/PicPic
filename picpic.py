#!usr/bin/env python3
# -*-coding=utf-8-*-

from PIL import Image
import sys

file_name = "huaji.png"
try:
    im = Image.open(file_name)
    # print(im.size)
except IOError:
    print("Cannot open file!")
    sys.exit(0)

out = im.resize((64, 64))

out.save("out.png", "PNG")
