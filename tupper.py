#!/usr/bin/env python3

"""Plot text using Tupper's formula.

Example usage:
  $ python3 tupper.py "Hello, World!" -o hello_world.png
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


SIZE = (106, 17)


def tupper(x: int, y: int) -> bool:
  """Tupper's self-referential formula."""
  return 0.5 < ((y // 17) // (2 ** (17 * x + y % 17))) % 2


def plot_text(text: str, size: int = 7) -> int:
  """Plot the given text using Tupper's formula.

  Args:
    text: The text to plot.
    size: The font size.

  Returns:
    The computed k value.
  """
  font = ImageFont.load_default(size=size)

  image = Image.new("1", SIZE, color=0)
  draw = ImageDraw.Draw(image)
  draw.text((SIZE[0] // 2, SIZE[1] // 2), text, font=font, spacing=-1, fill=1, anchor="mm")

  binary_matrix = np.array(image, dtype=int)
  for row in binary_matrix:
    print("".join(str(x) for x in row))

  binary_matrix_flat = binary_matrix[:, ::-1].flatten("F")

  k = 0
  for bit in binary_matrix_flat:
    k = (k << 1) | int(bit)
  k *= 17

  return k


def save_tupper_to_image(k: int, path: Path) -> None:
  """Save the plot of Tupper's formula for the given k value to an image.

  Args:
    k: The k value representing the text.
    path: The path to save the image.
  """
  fig, ax = plt.subplots(figsize=(SIZE[0] / 10, SIZE[1] / 10))
  for y in range(SIZE[1]):
    for x in range(SIZE[0]):
      if tupper(x, y + k):
        ax.plot(x, y, "ks", markersize=1)

  ax.set_aspect("equal")
  ax.set_xlim(-1, SIZE[0] + 1)
  ax.set_ylim(-1, SIZE[1] + 1)
  ax.axis("off")

  fig.savefig(path, dpi=300)
  plt.close()


if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(
    prog="tupper",
    description="Plot text using Tupper's formula.",
  )
  parser.add_argument("-s", "--size", type=int, help="Font size.", default=7)
  parser.add_argument("-o", "--output", type=Path, help="Output file. If not provided, the plot will not be saved.")
  parser.add_argument("-v", "--verbose", action="store_true", help="Print k value.", default=False)
  parser.add_argument("text", type=str, help="Text to plot.")
  args = parser.parse_args()

  text = args.text.strip()

  k = plot_text(args.text, args.size)

  if args.verbose:
    print("\n---")
    print(f"{k = } (# digits: {math.ceil(math.log10(k + 1))})")

  if args.output:
    save_tupper_to_image(k, args.output)
