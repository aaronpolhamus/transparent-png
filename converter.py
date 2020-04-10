from argparse import ArgumentParser
import numpy as np

from multiprocessing import Pool, cpu_count
from PIL import Image

parser = ArgumentParser(
    description="Convert a JPG of a black sketch against a contrasting background into a transparent PNG")

parser.add_argument("--in_file", default="./marciana.jpg")
parser.add_argument("--offset", type=int, default=-60)
parser.add_argument("--steepness", type=float, default=0.25)
parser.add_argument("--out_file", type=str, default=None)
args = parser.parse_args()


def sigmoid(value, offset=args.offset, steepness=args.steepness):
    """Set the transparency of a pixel based on how dark it is. Pixels that aren't pretty close to black should wash out
    """
    return 255 / (1 + np.exp(steepness * (value + offset)))


def apply_parallel(func, argument_tuples_iterator, n_workers=None):
    """See https://stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
    """
    if not n_workers:
        n_workers = cpu_count()

    with Pool(n_workers) as pool:
        results = pool.starmap(func, argument_tuples_iterator)

    return results


def make_rgba(coords, rgb):
    signature = np.mean(rgb)
    alpha = int(sigmoid(signature))
    return coords, rgb + (alpha,)


if __name__ == "__main__":
    im = Image.open(args.in_file)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    width, height = im.size
    arg_tups = list()
    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            arg_tups.append(((x, y), (r, g, b)))

    pixel_values = apply_parallel(make_rgba, arg_tups)
    for pixel_values in pixel_values:
        out.putpixel(pixel_values[0], pixel_values[1])

    name = args.in_file.split("/")[-1].split(".")[0]
    out_path = f"./{name}.png"

    out.save(out_path)
