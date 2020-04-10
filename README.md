# transparent-png
handy function for converting high-res whiteboard sketches to crisp, transparent PNGs

## Getting running
Super easy: 
* clone this repo
* `cd transparent-png`
* `pip install -r requirements.txt`
* To test: `python converter.py`

You should go from this...

![](https://imgur.com/Ae7YVQa)

to this:

![](https://imgur.com/P5LO9v4)

You can point the converter at any file and manually specify the output file: `python converter.py /tmp/myjpeg.jpg --out_path mypng.png` 

## Tuning the conversion
I use a sigmoid function the looks at how dark a pixel is and, based on that, assigns it an alpha transparency. The sigmoid function is nice because it render a smooth gradient against a mainly transparent background, avoiding the awkward discontinuities that a simple threshold would create. The defaults I picked worked pretty well, but if you'd like to play with them this is the function you'll be adjusting:

![](https://imgur.com/epNzyaz)

`--offset` shifts the curve right and left, and `--steepness` controls how step the gradient is. The larger this number, the closer your approximation to a strict threshold for transparency will be. 
