from flask import Flask, render_template, request, send_file
from openai import OpenAI
import os
from werkzeug.utils import secure_filename
import base64
from io import BytesIO

app = Flask(__name__)
client = OpenAI(api_key="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")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None

    if request.method == "POST":
        prompt = request.form.get("prompt")
        file = request.files.get("image")

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            with open(filepath, "rb") as img:
                img_base64 = base64.b64encode(img.read()).decode("utf-8")

            response = client.images.edit(
                model="gpt-image-1",
                prompt=prompt,
                image=img_base64
            )
        else:
            response = client.images.generate(
                model="gpt-image-1",
                prompt=prompt
            )

        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        image_url = "data:image/png;base64," + image_base64

    return render_template("index.html", image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
