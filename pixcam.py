from jaraco.video import capture
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.messagebox
import time, os, pkgutil, random
import effects, pixel_util

class Effect:
    def __init__(self, name, duration, module):
        self.name = name
        self.duration = duration
        self.module = module
        
def stop_effect():
    global effect, effectspacing, starttime
    effect = None
    starttime = time.time() + random.uniform(*effectspacing)
        
def load_config():
    global effects, effectorder, effectspacing
    mod_durations = {}
    with open('effect_config.txt') as f:
        section = 'asdf'
        for line in f:  
            if line[0:3] == '---':
                section = line.split('---')[1]
                continue
            key, value = line[:-1].split(':')
            if section == 'global':
                if key == 'spacing':
                    effectspacing = list(map(lambda x: float(x), value.split('-')))
                elif key == 'order':
                    effectorder = value
            if section == 'effect durations':
                mod_durations[key] = float(value)
    
    # https://lextoumbourou.com/blog/posts/dynamically-loading-modules-and-classes-in-python/
    effects = []
    path = os.path.join(os.path.dirname(__file__), 'effects')
    for loader, mod_name, ispkg in pkgutil.iter_modules(path=['effects']):
        loaded_mod = __import__(path + "." + mod_name, fromlist=[mod_name])
        if mod_name in mod_durations:
            effects.append(Effect(mod_name, mod_durations[mod_name], loaded_mod))
    stop_effect()
            
load_config()

def animate():
    global effect, effects, effectorder, effectspacing, pixelsize, starttime
    if effect and time.time() > starttime + effect.duration:
        stop_effect()
    elif not effect and time.time() > starttime:
        starttime = time.time()
        if effectorder == 'random':
            effect = random.choice(effects)
        else:
            exit('not supported!')
        effect.module.start(None, None, effect.duration)
            
    image = cam.get_image()
    pixels = lambda dir, dim: int(crop[dir] * dim)
    image = image.crop((pixels('left', camwidth), pixels('top', camheight), camwidth - pixels('right', camwidth), camheight - pixels('bottom', camheight)))
    image = image.resize((int(image.size[0] * width / camwidth), int(image.size[1] * height / camheight)), Image.NEAREST)
    if effect:
        image = effect.module.update(image, pixelsize, (time.time() - starttime) / effect.duration)
    else:
        image = pixel_util.pixelize(image, pixelsize)
    
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo
    label.after(1, animate)

def mousepress(event):
    global m1down, m2down, pressx, pressy, pixelsize, presspixelsize, crop, presscrop, cropindex
    if event.num == 1:
        if m2down: return
        m1down = True
    elif event.num == 3:
        if m1down: return
        m2down = True
    pressx = event.x
    pressy = event.y
    presspixelsize = pixelsize
    cropindex = getcardinal(event.x, event.y)
    presscrop = crop[cropindex]
    
def mouserelease(event):
    global m1down, m2down
    if event.num == 1:
        m1down = False
    elif event.num == 3:
        m2down = False

def mouse1drag(event):
    global m2down, pressx, pixelsize, presspixelsize
    if m2down: return
    pixelsize = calcint(presspixelsize, (event.x - pressx), 0.05, 1, 70)
    stop_effect()

def mouse2drag(event):
    global m1down, presscrop, pressx, pressy, crop, cropindex, width, height
    if m1down: return
    fun = lambda dx, ymax: calcint(presscrop, dx, 1, 0, ymax)
    if cropindex == 'top':
        val = max(min(presscrop + (event.y - pressy) / height, .4), 0)
    if cropindex == 'bottom':
        val = max(min(presscrop - (event.y - pressy) / height, .4), 0)
    if cropindex == 'left':
        val = max(min(presscrop + (event.x - pressx) / width, .4), 0)
    if cropindex == 'right':
        val = max(min(presscrop - (event.x - pressx) / width, .4), 0)
    crop[cropindex] = val
    stop_effect()

def calcint(y0, dx, slope, ymin, ymax):
    return int(max(min(y0 + dx * slope, ymax), ymin))

def getcardinal(x, y):
    global width, height
    aboveneg = y < x * height / width
    abovepos = y < -x * height / width + height
    if abovepos and aboveneg: return 'top'
    elif not abovepos and not aboveneg: return 'bottom'
    elif abovepos and not aboveneg: return 'left'
    elif not abovepos and aboveneg: return 'right'

def showhelp():
    tkinter.messagebox.showinfo('Help', '''Adjust pixelation - Left click, drag horizontally.
Crop - Right click by an edge, drag toward center.
Resize - Resize the window normally.
Hide / show border - H key.
Hide / show menu bar - M key.''')

def showabout():
    tkinter.messagebox.showinfo('About', 'Pixcam\n\nPatrick Traynor\n\nMade both because I would use it, and it would be fun to make; a nice combination.')
    
def snap():
    root.geometry('%ix%i' % (width, height))

def createmenu():
    global root, menubar, topmost
    menubar = tk.Menu(root)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label='Toggle top level - ' + ('On' if topmost else 'Off'), command=toggle_topmost)
    helpmenu.add_command(label='Reload config', command=load_config)
    helpmenu.add_command(label='Snap', command=snap)
    helpmenu.add_command(label='Help', command=showhelp)
    helpmenu.add_command(label='About', command=showabout)
    menubar.add_cascade(label='Hello', menu=helpmenu)
    root.config(menu=menubar)
    
def toggle_topmost():
    global topmost
    topmost = not topmost
    root.wm_attributes('-topmost', topmost)
    menubar.delete(1)
    createmenu()
    
def keypress(event):
    global hidden, menubar, menuhidden
    if event.char == 'h':
        hidden = not hidden
        root.overrideredirect(hidden)
    elif event.char == 'm':
        menuhidden = not menuhidden
        if menuhidden:
            menubar.delete(1)
        else:
            createmenu()

def on_resize(event):
    global width, height
    width, height = event.width, event.height
    if width > height * camwidth / camheight:
        width = height * camwidth / camheight
    else:
        height = width * camheight / camwidth
    stop_effect()
    
m1down = False
m2down = False
pixelsize = 15
crop = { 'top': 0, 'bottom': 0, 'left': 0, 'right': 0 }
displaymode = 'pad'

cam = capture.Device(0, 0)
camwidth, camheight = cam.get_image().size
width, height = camwidth / 3, camheight / 3

root = tk.Tk()
root.wm_title('pixcam')
img = tk.Image('photo', file='icon.png')
root.tk.call('wm','iconphoto',root._w,img)
hidden = False
menuhidden = False
topmost = True

root.wm_attributes('-topmost', 1)
createmenu()

label = tk.Label(root, borderwidth=0, bg='black')
label.bind("<ButtonPress-1>", mousepress)
label.bind("<ButtonPress-3>", mousepress)
label.bind("<ButtonRelease-1>", mouserelease)
label.bind("<ButtonRelease-3>", mouserelease)
label.bind("<B1-Motion>", mouse1drag)
label.bind("<B3-Motion>", mouse2drag)
label.bind("<Configure>", on_resize)
root.bind_all("<Key>", keypress)
label.pack(fill=tk.BOTH, expand=tk.YES)
animate()

snap()
root.mainloop()