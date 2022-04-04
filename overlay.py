"""
USAGE

BERSERK: python3 overlay.py --pixel-size=1 --top-left 594 194 --input Berserk-ProtectAllies-0.9.png
BLOODBORN: python3 overlay.py --pixel-size=8 --top-left 921 1435 --input bloodborne-0.1.png

Upload the output file, and get the direct link to it
Fill out the tampermonkey script template, and host somewhere like GIST

"""

import argparse

import sys
import PIL
from PIL import ImageColor
from PIL import Image, UnidentifiedImageError

# args
parser = argparse.ArgumentParser()
parser.add_argument("--pixel-size", type=int, default=1,
    help="Width of pixels in input image that correspond to a single r/place pixel. e.g. If each pixel in your reference image is 8x8, pass --pixel-size=8")
parser.add_argument("--top-left", nargs=2, type=int, required=True,
    help="Coords of top left corner of your image")
parser.add_argument("--input", type=str, required=True,
    help="File path to input reference image")
parser.add_argument("--output", type=str, default=None,
    help="File path to output overlay image")
args = parser.parse_args()

PIXEL_SIZE = args.pixel_size
START_COORD = args.top_left
image_path = args.input
if args.output is None:
    args.output = args.input+".big.png"

# Open ref image
im = Image.open(image_path)
pix = im.load()
image_size = im.size

# Create new image
big = PIL.Image.new('RGBA', (6000,6000), (255,255,255,0))
big_map = big.load()

# Copy pixels from ref into new image
for orig_pix_x in range(0, image_size[0]-PIXEL_SIZE+1, PIXEL_SIZE):
    for orig_pix_y in range(0, image_size[1]-PIXEL_SIZE+1, PIXEL_SIZE):
        # Get the color of the pixel in the middle of the reference pixel
        pixel = pix[orig_pix_x+PIXEL_SIZE//2, orig_pix_y+PIXEL_SIZE//2]
        # 3 pixels per pixel in original
        big_map[(((START_COORD[0]+orig_pix_x//PIXEL_SIZE)*3))+1, (((START_COORD[1]+orig_pix_y//PIXEL_SIZE)*3))+1] = pixel

# output
with open(args.output, 'wb') as f:
    big.save(f)

