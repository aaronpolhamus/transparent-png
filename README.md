# transparent-png
handy function for converting high-res whiteboard sketches to crisp, transparent background PNGs. Thanks for the wicked-awesome Marciana drawing, Monica ;) 

## Getting running
Super easy: 
* clone this repo
* `cd transparent-png`
* `pip install -r requirements.txt`
* To test: `python converter.py`

You should go from this...

![Imgur](https://i.imgur.com/Ae7YVQa.jpg)

to this:

![Imgur](https://i.imgur.com/P5LO9v4.png)

You can point the converter at any file and manually specify the output file: `python converter.py --in_file /tmp/myjpeg.jpg --out_file mypng.png` 

Here's a more fully-feature version. This works best on whiteboard sketches where the target colors are very consistent, but the visual effect is cool nonetheless: 

```
python converter.py --in_file ./balloons-over-bagan.jpg --out_file ./balloons.png --targets 182 109 58 121 29 39 103 118 77 --steepness 0.25 --offset 40
```
Takes you from this...

![Imgur](https://i.imgur.com/MSvj2Nu.jpg)

to this:

![Imgur](https://i.imgur.com/rJsuazt.png)

## Tuning the conversion
I use a sigmoid function the looks at how dark a pixel is and, based on that, assigns it an alpha transparency. The sigmoid function is nice because it renders a smooth gradient against a transparent background, avoiding the awkward discontinuities that a simple threshold would create. The defaults I picked worked pretty well, but if you'd like to play with them this is the function you'll be adjusting:

![Imgur](https://i.imgur.com/epNzyaz.png)

`--offset` shifts the curve right and left, and `--steepness` controls the steepness of the transparency gradient. The larger this number, the closer your approximation to a strict threshold for transparency will be. 

