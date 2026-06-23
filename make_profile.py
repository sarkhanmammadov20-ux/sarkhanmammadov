from PIL import Image, ImageDraw, ImageFilter
import math
import random

SIZE = 768
random.seed(12)

img = Image.new("RGBA", (SIZE, SIZE), (3, 5, 8, 255))
px = img.load()

for y in range(SIZE):
    for x in range(SIZE):
        dx = (x - SIZE / 2) / (SIZE / 2)
        dy = (y - SIZE / 2) / (SIZE / 2)
        r = math.sqrt(dx * dx + dy * dy)
        side = max(0, 1 - abs(dx))
        upper = max(0, 1 - (y / SIZE))
        light = max(0, 1 - r)
        grain = random.randint(-7, 7)
        base = int(11 + 30 * light + 17 * upper + grain)
        blue = int(16 + 35 * light + 18 * side + grain)
        px[x, y] = (max(0, base - 4), max(0, base), max(0, blue), 255)

draw = ImageDraw.Draw(img, "RGBA")

# Subtle window/key light from above.
for i in range(170):
    alpha = int(42 * (1 - i / 170))
    draw.ellipse((112 + i, 20 + i, SIZE - 112 - i, SIZE - 180 - i), outline=(230, 241, 239, alpha), width=2)

# Head and shoulders as a restrained backlit silhouette.
sil = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
s = ImageDraw.Draw(sil, "RGBA")
s.ellipse((274, 154, 494, 382), fill=(14, 16, 18, 244))
s.rounded_rectangle((218, 360, 550, 720), radius=156, fill=(12, 14, 17, 246))
s.polygon([(282, 382), (486, 382), (528, 704), (236, 704)], fill=(11, 13, 16, 250))
sil = sil.filter(ImageFilter.GaussianBlur(0.55))
img.alpha_composite(sil)

# Rim light and facial plane, kept intentionally anonymous.
rim = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
r = ImageDraw.Draw(rim, "RGBA")
r.arc((262, 144, 502, 392), 206, 338, fill=(220, 237, 235, 84), width=5)
r.arc((270, 152, 510, 400), 198, 332, fill=(78, 154, 164, 45), width=7)
r.ellipse((330, 214, 466, 358), fill=(48, 52, 56, 36))
r.line((384, 192, 384, 646), fill=(255, 255, 255, 10), width=1)
rim = rim.filter(ImageFilter.GaussianBlur(1.3))
img.alpha_composite(rim)

# Optical vignette.
v = Image.new("L", (SIZE, SIZE), 0)
vp = v.load()
for y in range(SIZE):
    for x in range(SIZE):
        dx = (x - SIZE / 2) / (SIZE / 2)
        dy = (y - SIZE / 2) / (SIZE / 2)
        amount = min(255, int(max(0, math.sqrt(dx * dx + dy * dy) - 0.43) * 260))
        vp[x, y] = amount
vignette = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
vignette.putalpha(v.filter(ImageFilter.GaussianBlur(28)))
img = Image.alpha_composite(img, vignette)

mask = Image.new("L", (SIZE, SIZE), 0)
m = ImageDraw.Draw(mask)
m.ellipse((0, 0, SIZE - 1, SIZE - 1), fill=255)
out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
out.alpha_composite(img)
out.putalpha(mask)
out.save("outputs/profile.png")
