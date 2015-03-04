import pixel_util
import random
import time

class Flake:
    def __init__(self, x, y, colorpos, target=None):
        self.x = x
        self.y = y
        self.colorpos = colorpos
        self.target = target
        self.velocity = 0
        self.accel = 0.05

def start(image, pixelsize, t):
    global bed, bed2, flakes, count, state, time, spawncount
    bed = []
    bed2 = []
    flakes = []
    count = 0
    state = 1
    time = t
    spawncount = 0

def update(image, pixelsize, t):
    global bed, flakes, count, w, h, state, bed2, time, spawncount, lasttime
    image = pixel_util.shrink(image, pixelsize)
    count += 1
    if count < 20: return pixel_util.expand(image, pixelsize)
    if bed == []:
        w, h = image.size
        bed = [h] * w
        lasttime = t
        
    spawncount += w * h * (t - lasttime) * 2.5
    lasttime = t
    if state == 1:
        while spawncount > 0 and sum(bed) > 0:
            random_column_execute(lambda x: flakes.append(Flake(x=x, y=bed[x], colorpos=(x, bed[x]))))
            spawncount -= 1
        for f in flakes:
            f.velocity += f.accel
            f.y += f.velocity
            if int(f.y) >= h:
                flakes.remove(f)
        if sum(bed) == 0 and len(flakes) == 0:
            state = 2
            bed = [h] * w
            bed2 = [h] * w
            spawncount = 0
    elif state == 2:
        while spawncount > 0 and sum(bed) > 0:
            random_column_execute(lambda x: flakes.append(Flake(x=x, y=-1, colorpos=(x, bed[x]), target=bed[x])))
            spawncount -= 1
        for f in flakes:
            f.velocity += f.accel
            f.y += f.velocity
            if int(f.y) >= f.target:
                flakes.remove(f)
                bed2[f.x] -= 1
        if sum(bed) == 0 and sum(bed2) == 0:
            pass
            #bed = [h] * w
            #flakes = []
            #state = 1
    
    pixels = image.load()
    imagecopy = image.copy()
    if state == 1:
        for x, col in enumerate(bed):
            for y in range(h - col):
                #print(w, h, x, h - 1 - y)
                pixels[x, h - 1 - y] = (0, 0, 0)
    elif state == 2:
        for x, col in enumerate(bed2):
            for y in range(col):
                pixels[x, y] = (0, 0, 0)
    for f in flakes:
        if f.y < 0: continue
        if f.x >= w or int(f.y) >= h:
            flakes.remove(f)
            continue
        #print(w, h, f.x, int(f.y))
        pixels[f.x, int(f.y)] = imagecopy.getpixel(f.colorpos)
    
    image = pixel_util.expand(image, pixelsize)
    return image
    
def random_column_execute(func):
    while 1:
        x = random.randrange(0, w)
        if bed[x] > 0:
            bed[x] -= 1
            func(x)
            break