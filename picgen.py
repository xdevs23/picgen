#!/usr/bin/env python3

import numpy as np
from PIL import Image
import random
import sys
import math
import argparse
from scipy.ndimage import gaussian_filter

def main():
    boringMode = "boring"
    fancyMode = "fancy"

    xInputSize = 32
    yInputSize = 32
    xOutputSize = 2048
    yOutputSize = 2048
    colorsPerPixel = 3 # rgb, no alpha, 8 bit per color, 24 bit color per pixel
    mode = fancyMode
    enableBlur = False
    blurSigma = 3
    saveTo = None
    openInViewer = True

    parser = argparse.ArgumentParser(description='Generate a random image')
    parser.add_argument('--gen-size',
    help='Size of image to generate (not the actual output resolution) (default: %sx%s)' % (xInputSize, yInputSize))
    parser.add_argument('--resolution',
    help='Output resolution (default: %sx%s)' % (xOutputSize, yOutputSize))
    parser.add_argument('--mode',
    help='Pattern/Mode (available: boring, fancy) (default: %s)' % mode)
    parser.add_argument('--blur', help="Specify to enable", action='store_true')
    parser.add_argument('--blur-radius', type=int, help="Blur radius (only has effect if --blur is set) (default: %s)" % blurSigma)
    parser.add_argument('--save-to', help="Save image to the specified file, otherwise open in default viewer")
    parser.add_argument('--open-in-viewer', help="Open image in viewer regardless of the --save-to argument", action="store_true")

    args = parser.parse_args()

    if args.gen_size is not None:
    split = str.split(args.gen_size, 'x')
    xInputSize = int(split[0])
    yInputSize = int(split[1])

    if args.resolution is not None:
    split = str.split(args.resolution, 'x')
    xOutputSize = int(split[0])
    yOutputSize = int(split[1])

    if args.mode is not None: mode = args.mode
    if args.blur is not None: enableBlur = args.blur
    if args.blur_radius is not None: blurSigma = args.blur_radius

    saveTo = args.save_to
    openInViewer = saveTo is None or args.open_in_viewer

    print()
    print("Input size: %s x %s" % (xInputSize, yInputSize))
    print("Output size: %s x %s" % (xOutputSize, yOutputSize))
    print("Colors per pixel: %s" % colorsPerPixel)
    print("Mode: %s" % mode)
    print("Blur: %s, radius: %s" % (enableBlur, blurSigma))
    if openInViewer: print("Image will be opened in default viewer")
    if saveTo is not None: print("Image will be saved to %s" % saveTo)
    print()

    # Create a y,x,d array of 8 bit unsigned integers
    downscale = np.zeros( (yInputSize, xInputSize, colorsPerPixel), dtype=np.uint8 )

    for y in range(len(downscale)):
    sys.stdout.write("\rGenerating %s out of %s" % (y + 1, len(downscale)))
    sys.stdout.flush()
    if mode == fancyMode:
    for x in range(len(downscale[y])):
    downscale[y,x] = [random.randint(1,4) * 64 - 20, random.randint(1,4) * 64 - 20, random.randint(1,4) * 64 - 20]
    elif mode == boringMode:
    for x in range(len(downscale[y])):
    downscale[y,x] = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]

    print()

    data = downscale

    if xInputSize != xOutputSize or yInputSize != yOutputSize:
    data = np.zeros( (yOutputSize, xOutputSize, colorsPerPixel), dtype=np.uint8 )
    print("Upscaling...")

    upscaleFactorX = len(data[0]) / len(downscale[0])
    upscaleFactorY = len(data) / len(downscale)

    print("  Upscale factor X: %s" % upscaleFactorX)
    print("  Upscale factor Y: %s" % upscaleFactorY)

    for y in range(len(data)):
    sys.stdout.write("\rUpscaling %s out of %s" % (y + 1, len(data)))
    sys.stdout.flush()
    for x in range(len(data[y])):
    yIx = math.floor(y / upscaleFactorY)
    # Check if we're still in bounds
    if yIx > len(downscale): break
    xIx = math.floor(x / upscaleFactorX)
    # Check if we're still in bounds
    if xIx > len(downscale[yIx]): break
    data[y,x] = downscale[yIx][xIx]

    print()

    if enableBlur:
    print("Applying blur...")
    # Separate r, g, b
    b, g, r = data[:, :, 0], data[:, :, 1], data[:, :, 2]

    # Blur it
    r = gaussian_filter(r, sigma=blurSigma)
    g = gaussian_filter(g, sigma=blurSigma)
    b = gaussian_filter(b, sigma=blurSigma)

    # Put it back together
    data[..., 0] = b
    data[..., 1] = g
    data[..., 2] = r

    print()

    print("Constructing final image")
    image = Image.fromarray(data)
    print("Done")
    print()

    if openInViewer:
    print("Opening image")
    image.show() # View in default viewer

    if saveTo is not None:
    print("Saving image")
    image.save(saveTo) # Save to filesystem
    print("Saved")

    print()


if __name__ == "__main__":
    main()
else:
    raise RuntimeError("Use picgen as a script only")
