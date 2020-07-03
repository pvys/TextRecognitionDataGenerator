import cv2
import math
import os
import random as rnd
import numpy as np

from PIL import Image, ImageDraw, ImageFilter


def gaussian_noise(height, width):
    """
        Create a background with Gaussian noise (to mimic paper)
    """

    # We create an all white image
    image = np.ones((height, width)) * 255

    # We add gaussian noise
    cv2.randn(image, 235, 10)

    return image


def plain_white(height, width):
    """
        Create a plain white background
    """

    return np.ones((height, width)) * 255

def quasicrystal(height, width):
    """
        Create a background with quasicrystal (https://en.wikipedia.org/wiki/Quasicrystal)
    """

    image = Image.new("L", (width, height))
    pixels = image.load()

    frequency = rnd.random() * 30 + 20  # frequency
    phase = rnd.random() * 2 * math.pi  # phase
    rotation_count = rnd.randint(10, 20)  # of rotations

    for kw in range(width):
        y = float(kw) / (width - 1) * 4 * math.pi - 2 * math.pi
        for kh in range(height):
            x = float(kh) / (height - 1) * 4 * math.pi - 2 * math.pi
            z = 0.0
            for i in range(rotation_count):
                r = math.hypot(x, y)
                a = math.atan2(y, x) + i * math.pi * 2.0 / rotation_count
                z += math.cos(r * math.sin(a) * frequency + phase)
            c = int(255 - round(255 * z / rotation_count))
            pixels[kw, kh] = c  # grayscale
    return image.convert("RGBA")


def image(height, width, image_path):
    """
        Create a background with a image
    """
    pic = cv2.imread(image_path)

    if pic.shape[1] < width:
        pic = cv2.resize(pic, dsize=(width, int(pic.shape[0] * (width / pic.shape[1]))), interpolation=cv2.INTER_AREA)
    if pic.shape[0] < height:
        pic = cv2.resize(pic, dsize=( int(pic.shape[1] * (height / pic.shape[0])), height), interpolation=cv2.INTER_AREA)
    if pic.shape[1] == width:
        x = 0
    else:
        x = rnd.randint(0, pic.shape[1] - width)
    if pic.shape[0] == height:
        y = 0
    else:
        y = rnd.randint(0, pic.shape[0] - height)

    return pic[y: y + height, x: x + width]
