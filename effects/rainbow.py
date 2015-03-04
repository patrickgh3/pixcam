import pixel_util
import colorsys
import functools

def start(image, pixelsize, time):
    pass

def update(image, pixelsize, time):
    image = pixel_util.shrink(image, pixelsize)
    original = image.copy()
    pixels = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            color = colorsys.rgb_to_hsv(*pixels[x, y])
            color = colorsys.hsv_to_rgb(time * 3.5, color[1], color[2])
            pixels[x, y] = (int(color[0]), int(color[1]), int(color[2]))
    image = pixel_util.fade_transition(image, original, time)
    image = pixel_util.expand(image, pixelsize)
    return image