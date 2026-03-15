import os
import zipfile
from PIL import Image

def convert_to_webp(input_path):
    img = Image.open(input_path)

    width, height = img.size

    scale = 512 / max(width, height)
    new_width = int(width * scale)
    new_height = int(height * scale)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

    x = (512 - new_width) // 2
    y = (512 - new_height) // 2

    canvas.paste(img, (x, y), img.convert("RGBA"))

    base = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join("stickers", base + ".webp")

    canvas.save(output_path, "webp")
    return output_path


def extract_static(zip_path):
    output = "stickers"
    os.makedirs(output, exist_ok=True)

    files = []

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for name in zip_ref.namelist():
            if name.lower().endswith((".webp", ".png", ".jpeg", ".jpg")): #lowered since webp files can end e.g. with WebP
                zip_ref.extract(name, output)

                in_path = os.path.join(output, name)

                files.append(convert_to_webp(in_path))
        return files



