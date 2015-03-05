import pixel_util, random

def start(image, pixelsize, time):
    pass

def update(image, pixelsize, time):
    image = pixel_util.shrink(image, pixelsize)
    original = image.copy()
    w, h = image.size
    pixels = image.load()
    numswap = int(w * h / 4)
    for i in range(numswap):
        pos1 = (random.randrange(0, w), random.randrange(0, h))
        pos2 = (random.randrange(0, w), random.randrange(0, h))
        temp = pixels[pos1]
        pixels[pos1] = pixels[pos2]
        pixels[pos2] = temp
    image = pixel_util.fade_transition(image, original, time, transtime=.4)
    image = pixel_util.expand(image, pixelsize)
    return image
    