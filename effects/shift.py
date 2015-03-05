import pixel_util
import random
from PIL import ImageChops

def start(image, pixelsize, time):
    global state
    state = 0
    choose_direction()

def update(image, pixelsize, time):
    global scrollh, scrollv, state
    numcycles = 4
    if time > (state + 1) / numcycles:
        state = int(time * numcycles)
        choose_direction()
    t = (time - state / numcycles) * numcycles
    image = pixel_util.shrink(image, pixelsize)
    image = ImageChops.offset(image, int(image.size[0] * t) * scrollh, int(image.size[1] * t) * scrollv)
    image = pixel_util.expand(image, pixelsize)
    return image
    
def choose_direction():
    global scrollh, scrollv
    scrollh = scrollv = 0
    while scrollh == 0 and scrollv == 0:
        scrollh = random.choice((-1, 1, 0, 0))
        scrollv = random.choice((-1, 1, 0, 0))