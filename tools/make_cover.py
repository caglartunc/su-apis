import sys
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
src, out = sys.argv[1], sys.argv[2]
top, block, ncol = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
W, H = 1920, 800
rng = np.random.default_rng(7)

im = Image.open(src).convert("RGB")
w, h = im.size; ch = int(w * H / W)
photo = im.crop((0, top, w, top + ch)).resize((W, H), Image.LANCZOS)

sw, sh = W // block, H // block
# flatten regions first (cel-shaded look), then vivid colours
g = photo.resize((sw * 2, sh * 2), Image.LANCZOS).filter(ImageFilter.MedianFilter(3))
g = ImageEnhance.Color(g).enhance(1.45)
g = ImageEnhance.Contrast(g).enhance(1.3)
g = ImageEnhance.Brightness(g).enhance(1.05)
small = g.resize((sw, sh), Image.BOX)
s = np.asarray(small, dtype=float); s = s * np.array([0.95, 0.99, 1.06]); small = Image.fromarray(np.clip(s, 0, 255).astype(np.uint8))
q = small.quantize(colors=ncol, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
pal = np.array(q.getpalette()[:ncol * 3]).reshape(-1, 3)
idx = np.asarray(q)
arr = pal[idx].astype(float)

# sprite-style dark outlines where neighbouring colours differ strongly
lum = arr @ np.array([0.3, 0.59, 0.11])
gx = np.abs(np.diff(lum, axis=1, append=lum[:, -1:])); gy = np.abs(np.diff(lum, axis=0, append=lum[-1:, :]))
edge = np.maximum(gx, gy) > 42
arr[edge] = arr[edge] * 0.35 + np.array([20, 18, 40]) * 0.65

# simple 2-tone dither only in the sky band (top rows, low texture) for a retro gradient
CLOUD = ["....####......",
         "..########....",
         ".###########..",
         "##############",
         ".############.",
         "..ssssssssss.."]
def cloud(cx, cy):
    for r, line in enumerate(CLOUD):
        for c, ch in enumerate(line):
            y, x = cy + r, cx + c
            if 0 <= y < arr.shape[0] and 0 <= x < arr.shape[1] and ch != ".":
                arr[y, x] = (255, 255, 255) if ch == "#" else (196, 222, 250)
            # dark outline around the cloud
    for r in range(-1, len(CLOUD) + 1):
        for c in range(-1, len(CLOUD[0]) + 1):
            inside = 0 <= r < len(CLOUD) and 0 <= c < len(CLOUD[0]) and CLOUD[r][c] != "."
            if inside: continue
            near = any(0 <= r + dr < len(CLOUD) and 0 <= c + dc < len(CLOUD[0]) and CLOUD[r + dr][c + dc] != "."
                       for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)))
            y, x = cy + r, cx + c
            if near and 0 <= y < arr.shape[0] and 0 <= x < arr.shape[1]:
                arr[y, x] = (60, 92, 150)
cloud(int(sw * 0.70), 2)
cloud(int(sw * 0.88), 6)
pix = Image.fromarray(arr.astype(np.uint8)).resize((W, H), Image.NEAREST)

# compose: real photo left -> game art right, with a blocky "loading" dissolve
B = block * 2
cols, rows = W // B + 1, H // B + 1
xs = (np.arange(cols) * B + B / 2) / W
t = np.clip((xs - 0.44) / 0.16, 0, 1)
mask = (rng.random((rows, cols)) < t[None, :]).astype(np.uint8) * 255
mask = Image.fromarray(mask).resize((cols * B, rows * B), Image.NEAREST).crop((0, 0, W, H))
Image.composite(pix, photo, mask).save(out, quality=90, optimize=True, progressive=True)
print("saved", out)
