import math
from pathlib import Path

import numpy as np

from meme_generator_whataboringguy.point_generator import foo_random
from PIL import Image


def calculate_image_size(width, height, N, alpha=0.3):
    radius = min(width, height) / 2
    area_circle = math.pi * radius**2
    total_image_area = alpha * area_circle
    s = int(math.sqrt(total_image_area / N))
    return s


if __name__ == "__main__":
    width = 500
    height = 500
    alpha = 0.3

    dir_root = Path(__file__).parent.parent.parent

    directory_path = dir_root / "images_download_aa"
    image_paths = list(directory_path.glob("*.png"))
    N = len(image_paths)
    points = foo_random(N, 0.7 / np.sqrt(N))
    s = calculate_image_size(width, height, N, alpha)
    canvas = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    for img_path, (x_unit, y_unit) in zip(image_paths, points):
        img = Image.open(img_path).convert("RGBA")
        aspect_ratio = img.width / img.height
        if aspect_ratio > 1:  # Wider than tall
            new_width = int(s * aspect_ratio)
            new_height = s
        else:  # Taller than wide or square
            new_width = s
            new_height = int(s / aspect_ratio)
        img_resized = img.resize((new_width, new_height))
        x_canvas = (x_unit + 1) * (width / 2)
        y_canvas = (y_unit + 1) * (height / 2)
        x_paste = x_canvas - s / 2
        y_paste = y_canvas - s / 2
        x_paste = max(0, min(x_paste, width - s))
        y_paste = max(0, min(y_paste, height - s))
        canvas.paste(img_resized, (int(x_paste), int(y_paste)), img_resized)

    base_image = Image.open(dir_root / "images_base" / "base.png")
    canvas_resized = canvas.resize(
        (int(base_image.width * 0.6), int(base_image.height * 0.6))
    )
    base_image.paste(
        canvas_resized, (base_image.width - canvas_resized.width, 0), canvas_resized
    )
    base_image.save("final_output.png")
    print("Final composite image successfully saved as 'final_output.png'.")
