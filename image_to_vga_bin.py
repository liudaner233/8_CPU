# coding=utf-8
"""Convert an image to the 100 x 100 RGB332 VGA ROM format."""

import argparse
from pathlib import Path
from PIL import Image, ImageOps

def convert(source: Path, output: Path) :
    # Keep the full image visible and use a white background when padding.
    with Image.open(source) as original:
        rgba = original.convert("RGBA")
        background = Image.new("RGBA", rgba.size, "white")
        background.alpha_composite(rgba)
        image = ImageOps.contain(background.convert("RGB"), (100, 100), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (100, 100), "white")
    canvas.paste(image, ((100 - image.width) // 2, (100 - image.height) // 2))

    data = bytearray()
    pixels = []
    rgb = canvas.tobytes()
    for red, green, blue in zip(rgb[0::3], rgb[1::3], rgb[2::3]):
        # RGB332: RRR GGG BB, one byte per pixel, left-to-right and top-to-bottom.
        value = (red & 0xE0) | ((green & 0xE0) >> 3) | (blue >> 6)
        data.append(value)
        pixels.append(((value >> 5) * 255 // 7,
                       ((value >> 2) & 7) * 255 // 7,
                       (value & 3) * 255 // 3))

    data.extend((0, 0))
    output.write_bytes(data)

    print('Compile finished!!!')


def main() :
    folder = Path(__file__).resolve().parent / "VAG"
    folder.mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(description="Generate a 100x100 RGB332 LogicCircuit image ROM")
    parser.add_argument("image", type=Path, help="Source image")
    parser.add_argument("-o", "--output", type=Path, default=folder/'VGA.bin',help='Specify the output filename and path')
    args = parser.parse_args()
    convert(args.image, args.output)


if __name__ == "__main__":
    main()
