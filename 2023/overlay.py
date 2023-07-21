"""
USAGE

BERSERK: python3 overlay.py --input puck.png --pixel-size=1 --top-left 461 -162

Upload the output file, and get the direct link to it
Fill out the tampermonkey script template, and host somewhere like GIST or pastebin

"""
import os
import argparse
import string

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
parser.add_argument("--credits", type=str, default=None,
    help="File path to credits")
parser.add_argument("--script-template", type=str, default=None,
    help="Monkey script template file")
parser.add_argument("--script-name", type=str, nargs='+', default=None,
    help="Monkey script name")
parser.add_argument("--script-version", type=str, default=None,
    help="Version number for this monkey script")
args = parser.parse_args()

CANVAS_SIZE = (1000,1000)
PIXEL_SIZE = args.pixel_size
# adjust for negative coords
# START_COORD = args.top_left
START_COORD = (args.top_left[0]+CANVAS_SIZE[0]//2,args.top_left[1]+CANVAS_SIZE[1]//2)

image_path = args.input
if args.output is None:
    args.output = args.input+".big.png"

# Open ref image
im = Image.open(image_path)
pix = im.load()
image_size = im.size

# Create new image
big = PIL.Image.new('RGBA', (CANVAS_SIZE[0]*3,CANVAS_SIZE[1]*3), (255,255,255,0))
big_map = big.load()

# Copy pixels from ref into new image
for orig_pix_x in range(0, image_size[0]-PIXEL_SIZE+1, PIXEL_SIZE):
    for orig_pix_y in range(0, image_size[1]-PIXEL_SIZE+1, PIXEL_SIZE):
        # Get the color of the pixel in the middle of the reference pixel
        pixel = pix[orig_pix_x+PIXEL_SIZE//2, orig_pix_y+PIXEL_SIZE//2]
        # 3 pixels per pixel in original
        big_x = (((START_COORD[0]+orig_pix_x//PIXEL_SIZE)*3))+1
        big_y = (((START_COORD[1]+orig_pix_y//PIXEL_SIZE)*3))+1
        # print(pixel, big_x, big_y)
        big_map[big_x, big_y] = pixel

# output
with open(args.output, 'wb') as f:
    big.save(f)

# Output the template if requested
if args.script_template is not None:
    with open(args.script_template, 'r') as f:
        template = string.Template(f.read())
    if args.credits:
        with open(args.credits, 'r') as f:
            credits = ', '.join(f.read().splitlines(False)).strip()
    else:
        credits = None
    monkey = template.substitute(
        script_name=' '.join(args.script_name).strip() or '{} overlay'.format(os.path.basename(args.input)),
        overlay_version=args.script_version or '0.1',
        credits=credits or 'unknown'
    )
    # Put template next to overlay
    monkey_path = os.path.join(os.path.dirname(args.output), 'monkey.user.js')
    with open(monkey_path, 'w') as f:
        f.write(monkey)
