"""This script file can place a transparent filter over an image based on an arbitrary number of colors. To use this
functionality in triplets of RGB codes with simple space separation. To select red, green, and blue, for example, you
would pass --targets 255 0 0 0 255 0 0 0 255. By default it the converter selects only the color black for filtering.
"""

from argparse import ArgumentParser
from itertools import zip_longest

import numpy as np
from PIL import Image

parser = ArgumentParser(
    description="Convert a JPG of a black sketch against a contrasting background into a transparent PNG")

parser.add_argument("--in_file", default="./marciana.jpg")
parser.add_argument("--targets", nargs="+", type=int, default=[0, 0, 0])
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


if __name__ == "__main__":
    if not len(args.targets) % 3 == 0:
        raise ValueError("--targets must receive RGB triplets of 3 numbers each. Use 0 to indicate a missing color")
    targets = [item for item in grouper(3, args.targets)]
    img = np.asarray(Image.open(args.in_file))
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
