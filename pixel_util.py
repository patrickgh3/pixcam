from PIL import Image, ImageTk
import math

def pixelize(image, pixelsize):
    
    #image = image.resize((int(image.size[0] / pixelsize), int(image.size[1] / pixelsize)), Image.NEAREST)
    #image = image.resize((int(image.size[0] * pixelsize), int(image.size[1] * pixelsize)), Image.NEAREST)
    
    image = shrink(image, pixelsize)
    image = expand(image, pixelsize)
    
    #padimage = Image.new('RGB', (camwidth, camheight), 0x000000)
    #padimage.paste(image, (int((camwidth - image.size[0]) / 2), int((camheight - image.size[1]) / 2)))
    #padimage = padimage.resize((int(padimage.size[0] * width / camwidth), int(padimage.size[1] * height / camheight)), Image.NEAREST)
    return image
    
def shrink(image, pixelsize):
    return image.resize((int(image.size[0] / pixelsize), int(image.size[1] / pixelsize)), Image.NEAREST)
    
def expand(image, pixelsize):
    return image.resize((int(image.size[0] * pixelsize), int(image.size[1] * pixelsize)), Image.NEAREST)
    
def fade_transition(image, original, time):
    return Image.blend(image, original, abs(time - 0.5) * 8 - 3)