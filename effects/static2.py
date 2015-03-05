import pixel_util, random, itertools

def start(image, pixelsize, time):
    global coords
    image = pixel_util.shrink(image, pixelsize)
    w, h = image.size
    coords = list(itertools.product(range(w), range(h)))
    random.shuffle(coords)
    coords = list(zip(coords[::2], coords[1::2]))
    
def update(image, pixelsize, time):
    global coords
    if time < .4:
        index = int(time / .4 * len(coords))
        swapcoords = coords[:index]
    elif time > 1 - .4:
        index = int((time - (1 - .4)) / .4 * len(coords))
        swapcoords = coords[index:]
    else:
        swapcoords = coords
        
    image = pixel_util.shrink(image, pixelsize)
    pixels = image.load()
    for pos in swapcoords:
        temp = pixels[pos[0]]
        pixels[pos[0]] = pixels[pos[1]]
        pixels[pos[1]] = temp
    image = pixel_util.expand(image, pixelsize)
    return image