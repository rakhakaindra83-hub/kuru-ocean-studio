from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math, random, subprocess

root = Path(__file__).parent
w, h, fps, seconds = 960, 540, 24, 8
random.seed(17)
particles = [(random.randrange(w), random.randrange(h), random.uniform(0, math.tau), random.choice((1, 1, 1, 2)), random.choice((1, 2, 3))) for _ in range(75)]
base = Image.new('RGB', (w, h))
draw = ImageDraw.Draw(base)
for y in range(h):
    draw.line((0, y, w, y), fill=(2, int(12 + 13 * (1-y/h)), int(24 + 16 * (1-y/h))))
proc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pixel_format', 'rgb24', '-video_size', f'{w}x{h}', '-framerate', str(fps), '-i', '-', '-an', '-c:v', 'libx264', '-crf', '25', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(root/'assets/deep-ocean.mp4')], stdin=subprocess.PIPE)
for frame in range(fps*seconds):
    t = frame/(fps*seconds)*math.tau
    rays = Image.new('RGB', (w,h), (0,0,0))
    d = ImageDraw.Draw(rays)
    for i in range(4):
        x = 490+i*100+30*math.sin(t+i)
        d.polygon([(x, -60), (x+15,-60), (x-130, h), (x-270,h)], fill=(2,10,15))
    from PIL import ImageChops
    image = ImageChops.add(base, rays.filter(ImageFilter.GaussianBlur(30)))
    glow = Image.new('RGB', (w,h), (0,0,0))
    gd = ImageDraw.Draw(glow)
    dots = []
    for x,y,phase,r,speed in particles:
        px = x+9*math.sin(t+phase)
        py = y+6*math.cos(t+phase)
        light = .15+.85*((1+math.sin(t*speed+phase))/2)**3
        color = tuple(int(v*light) for v in (95,195,210))
        gd.ellipse((px-r*3,py-r*3,px+r*3,py+r*3),fill=color)
        dots.append((px,py,r,color))
    image = ImageChops.add(image, glow.filter(ImageFilter.GaussianBlur(5)))
    d = ImageDraw.Draw(image)
    for x,y,r,c in dots:
        d.ellipse((x-r,y-r,x+r,y+r),fill=c)
    if frame == 0:
        image.save(root/'assets/deep-ocean-poster.jpg', quality=90)
    proc.stdin.write(image.tobytes())
proc.stdin.close()
assert proc.wait() == 0
print('Created 8-second seamless deep-ocean video:', (root/'assets/deep-ocean.mp4').stat().st_size, 'bytes')
