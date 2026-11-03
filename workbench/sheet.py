import sys, importlib, os
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw
from lib import C

def render(mods, outdir, words=None):
    os.makedirs(outdir, exist_ok=True)
    made = []
    for m in mods:
        mod = importlib.import_module(m)
        importlib.reload(mod)
        for w, fn in mod.D.items():
            if words and w not in words:
                continue
            c = C(); fn(c); c.save(f"{outdir}/{w}.png"); made.append(w)
    return made

def sheet(outdir, words, path, cols=5, cell=240):
    rows = (len(words) + cols - 1) // cols
    im = Image.new("RGB", (cols * cell, rows * (cell + 16)), "white")
    d = ImageDraw.Draw(im)
    for i, w in enumerate(words):
        x, y = (i % cols) * cell, (i // cols) * (cell + 16)
        p = f"{outdir}/{w}.png"
        if os.path.exists(p):
            im.paste(Image.open(p).resize((cell - 8, cell - 8)), (x + 4, y + 16))
        d.text((x + 6, y + 2), w, fill="red")
    im.save(path)

if __name__ == "__main__":
    out = sys.argv[1]; mods = sys.argv[2].split(","); words = sys.argv[3].split(",") if len(sys.argv) > 3 else None
    made = render(mods, out, words)
    sheet(out, made, out + "_sheet.png")
    print(len(made), out + "_sheet.png")
