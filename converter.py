"""This script file can place a transparent filter over an image based on an arbitrary number of colors. To use this
functionality in triplets of RGB codes with simple space separation. To select red, green, and blue, for example, you
would pass --targets 255 0 0 0 255 0 0 0 255. By default the converter selects only the color black for filtering.

Passing the --interactive flag as true provide a handy way to get your RGB codes by manually selecting pixels rather
than typing in a long list of values. This can be helpful for wen you have an image with a lot of light/dark contrasts.
When using this approach, try putting --offset and --steepness on stricter settings and selecting a broader range for
increased conversion quality.
"""

from argparse import ArgumentParser
from itertools import zip_longest

import cv2
import numpy as np
from PIL import Image

parser = ArgumentParser(
    description="Convert a JPG of a black sketch against a contrasting background into a transparent PNG")

parser.add_argument("--in_file", default="./marciana.jpg")
parser.add_argument("--targets", nargs="+", type=int, default=[0, 0, 0])
parser.add_argument("--interactive", type=bool, default=False)
parser.add_argument("--offset", type=int, default=60)
parser.add_argument("--steepness", type=float, default=0.25)
parser.add_argument("--out_file", type=str, default="./marciana.png")
args = parser.parse_args()


def sigmoid(value, offset=args.offset, steepness=args.steepness):
    """Set the transparency of a pixel based on how dark it is. Pixels that aren't pretty close to black should wash out
    """
    return 255/(1 + np.exp(steepness * (value - offset)))


def grouper(n, iterable):
    """https://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n"""
    rgbs = [iter(iterable)] * n
    return zip_longest(*rgbs)


def pick_rgb(event, x, y, flags, param):
    """https://stackoverflow.com/questions/56787999/python-opencv-realtime-get-rgb-values-when-mouse-is-clicked"""
    if event == cv2.EVENT_LBUTTONDOWN:
        # A bit hacky, but we'll be overwriting an array from an outer scope, as well as referencing the image from
        # outer scope as well
        bgr = cv2_img[y, x]
        targets.append(tuple(np.flip(bgr)))


if __name__ == "__main__":
    if not len(args.targets) % 3 == 0:
        raise ValueError("--targets must receive RGB triplets of 3 numbers each. Use 0 to indicate a missing color")
    targets = [item for item in grouper(3, args.targets)]
    img = np.asarray(Image.open(args.in_file))

    if args.interactive:
        cv2_img = cv2.imread(args.in_file)
        cv2.namedWindow('pick_rgb')
        cv2.setMouseCallback('pick_rgb', pick_rgb)
        targets = list()
        while True:
            cv2.imshow('pick_rgb', cv2_img)
            if cv2.waitKey(1) == 27:
                break
        cv2.destroyAllWindows()
        cv2.waitKey(1)

    w, h, _ = img.shape
    alphas = np.empty((w, h, len(targets)), dtype=int)
    for i, target in enumerate(targets):
        print(f"Generating mask for RGB target {target}")
        target_array = np.full(img.shape, target, dtype=int)
        diffs_array = img - target_array
        dist_array = np.sqrt(np.sum(diffs_array**2, axis=2))
        alphas[:, :, i] = sigmoid(dist_array)

    alpha_mask = np.max(alphas, axis=2)
    filtered_img = np.dstack((img, alpha_mask))
    out_img = Image.fromarray(filtered_img.astype('uint8'))
    out_img.save(args.out_file)
