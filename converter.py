import numpy as np
from PIL import Image
from argparse import ArgumentParser

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


def make_rgba(image):
    img = np.asarray(Image.open(image))
    signature = np.mean(img, axis=2)
    alpha = sigmoid(signature)
    filtered_img = np.dstack((img, alpha))
    img_with_alpha = Image.fromarray(filtered_img.astype('uint8'))
    return img_with_alpha


if __name__ == "__main__":
    out_img = make_rgba(args.in_file)
    out_path = args.out_file
    if out_path is None:
        name = "./marciana.jpg".split("/")[-1].split(".")[0]
        out_path = f"./{name}.png"
    out_img.save(out_path)
