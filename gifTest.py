from PIL import Image, ImageSequence
import sys, os

filename = sys.argv[1]
im = Image.open(filename)
# original_duration = im.info['duration']
frames = [frame.copy() for frame in ImageSequence.Iterator(im)]    
frames.reverse()

from images2gif import writeGif
writeGif("giftest", frames, dither=0)