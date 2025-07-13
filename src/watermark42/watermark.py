import os
from pathlib import Path
import argparse
from tqdm import tqdm
import sys

from _watermark import add_watermark
from compressor import compress_images
import warnings

warnings.filterwarnings("ignore")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("../..")

    return os.path.join(base_path, relative_path)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Add watermarks to batch of images. Original images won't be affected. A new copy will be created")
    parser.add_argument('-i', '--images_path', type=str,
                        help='The path to the folder containing images.')
    parser.add_argument('-o', '--opacity', type=float, default=0.8,
                        help='The opacity of the watermarks. Default is 0.8.')
    parser.add_argument('-s1', '--scale1', type=int, default=10,
                        help='The scale of the logo ss_watermark as a percentage of the image height. Default is 10.')
    parser.add_argument('-s2', '--scale2', type=int, default=3,
                        help='The scale of the instagram ss_watermark as a percentage of the image height. Default is 3.')
    parser.add_argument('-q', '--quality', type=int, default=70,
                        help='Quality of the output image as a percentage. Default is 100.')
    parser.add_argument('--compress_only', action='store_true',
                        help='Only compress the images, do not add a watermark.')

    # Ignore unknown arguments
    args, unknown = parser.parse_known_args()
    if unknown:
        print(f"Warning: Unknown arguments ignored: {unknown}")
    return args


def main():
    args = parse_arguments()

    # If running as executable and no images_path provided, use the executable's directory
    if getattr(sys, 'frozen', False) and not args.images_path:
        images_path = Path(os.path.dirname(sys.executable))
    else:
        images_path = Path(args.images_path) if args.images_path else Path.cwd()

    watermarks_path = Path(resource_path("../../assets/img"))
    logo_path = watermarks_path / "Space_42_logo.png"
    insta_logo = watermarks_path / "instagram.png"

    output_path_watermarked = images_path / "watermarked"
    output_path_compressed_only = images_path / "compressed"

    os.makedirs(output_path_watermarked, exist_ok=True)
    os.makedirs(output_path_compressed_only, exist_ok=True)

    for img_name in tqdm(os.listdir(str(images_path))):
        if img_name.lower().endswith((".jpg", ".png")):
            if args.compress_only:
                compress_images(images_path / img_name, output_path_compressed_only / img_name, args.quality)
            else:
                add_watermark(images_path / img_name, logo_path, insta_logo, output_path_watermarked,
                              opacity=args.opacity, scale1=args.scale1, scale2=args.scale2, quality=args.quality)

    print("Processing complete. Check the 'watermarked' or 'compressed' folder for output.")


if __name__ == "__main__":
    main()
