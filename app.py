from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw
import numpy as np
import io
import random
import hashlib

app = Flask(__name__)

def generate_image(prompt):
    seed = int(hashlib.sha256(prompt.encode()).hexdigest(), 16) % (10**8)
    random.seed(seed)
    np.random.seed(seed)

    width, height = 512, 512

    noise = np.random.rand(height, width, 3) * 255
    noise = noise.astype(np.uint8)

    img = Image.fromarray(noise)
    draw = ImageDraw.Draw(img)

    # Stars
    for _ in range(400):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 2)
        draw.ellipse((x, y, x+size, y+size), fill=(255, 255, 255))

    # Glow nebula
    for _ in range(6):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(80, 200)
        color = tuple(np.random.randint(50, 255, size=3))
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color)

    return img

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        img = generate_image(prompt)

        img_io = io.BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
