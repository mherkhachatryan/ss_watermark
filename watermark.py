import cv2
import os
from pathlib import Path
import argparse
from PIL import Image
import piexif
from tqdm import tqdm
from PIL import ExifTags
import subprocess


def compress_image_with_imagemagick(input_path, output_path, quality):
    subprocess.run(["convert", input_path, "-quality", str(quality), output_path], check=True)


def add_watermark(image_path, watermark1_path, insta_logo_path, output_path, opacity, scale1, scale2, quality):
    # Read the watermarks and the image
    watermark1 = cv2.imread(str(watermark1_path), -1)
    watermark1 = cv2.cvtColor(watermark1, cv2.COLOR_BGR2BGRA)

    insta_logo = cv2.imread(str(insta_logo_path), -1)
    insta_logo = cv2.cvtColor(insta_logo, cv2.COLOR_BGR2BGRA)

    original_image = Image.open(image_path)
    exif_data = piexif.load(original_image.info['exif'])

    image = cv2.imread(str(image_path))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGRA)

    original_image = Image.open(image_path)

    # Resize the first ss_watermark
    height1 = int(image.shape[0] * scale1 / 100)
    width1 = height1
    dim1 = (width1, height1)
    resized_watermark1 = cv2.resize(watermark1, dim1, interpolation=cv2.INTER_AREA)

    # Position of the first ss_watermark
    x1 = 0
    y1 = image.shape[0] - height1

    # Apply the first ss_watermark
    roi1 = image[y1:y1 + height1, x1:x1 + width1].copy()
    mask1 = resized_watermark1[..., 3] > 0
    roi1[mask1] = cv2.addWeighted(roi1, 1 - opacity, resized_watermark1, opacity, 0)[mask1]
    image[y1:y1 + height1, x1:x1 + width1] = roi1

    # Resize and position the Instagram logo
    height2 = int(image.shape[0] * scale2 / 100)
    width2 = height2
    dim2 = (width2, height2)
    resized_insta_logo = cv2.resize(insta_logo, dim2, interpolation=cv2.INTER_CUBIC)

    # Add fixed text next to the Instagram logo
    font = cv2.FONT_HERSHEY_TRIPLEX
    insta_text = "@space_shop42"
    font_scale = 2
    font_thickness = 100
    text_size, _ = cv2.getTextSize(insta_text, font, font_scale, font_thickness)
    text_x = image.shape[1] - text_size[0] - 300
    text_y = image.shape[0] - height2 + text_size[1]

    cv2.putText(image, insta_text, (text_x, text_y), font, 3, (255, 255, 255), 2, cv2.LINE_AA)

    # Calculate position for Instagram logo to be left from text
    x2 = text_x - width2 - 10
    y2 = image.shape[0] - height2 - 50

    # Apply the Instagram logo
    roi2 = image[y2:y2 + height2, x2:x2 + width2].copy()
    mask2 = resized_insta_logo[..., 3] > 0
    roi2[mask2] = cv2.addWeighted(roi2, 1 - opacity, resized_insta_logo, opacity, 0)[mask2]
    image[y2:y2 + height2, x2:x2 + width2] = roi2

    try:
        exif_data = piexif.load(original_image.info['exif'])
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(original_image._getexif().items())

        # Apply the orientation correction to the OpenCV image
        if exif[orientation] == 3:
            image = cv2.rotate(image, cv2.ROTATE_180)
        elif exif[orientation] == 6:
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif exif[orientation] == 8:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    except (AttributeError, KeyError, IndexError):
        # cases: image doesn't have getexif
        pass

    processed_image = Image.fromarray(image)

    if processed_image.mode == 'RGBA':
        processed_image = processed_image.convert('RGB')

    temp_output_path = str(output_path / ("temp_" + Path(image_path).name))
    if temp_output_path.lower().endswith('.jpg') or temp_output_path.lower().endswith('.jpeg'):
        processed_image.save(temp_output_path, quality=quality, exif=piexif.dump(exif_data))
    else:
        processed_image.save(temp_output_path, exif=piexif.dump(exif_data))

    if quality != 100:
        final_output_path = str(output_path / Path(image_path).name)
        compress_image_with_imagemagick(temp_output_path, final_output_path, quality)
        os.remove(temp_output_path)
    else:
        os.rename(temp_output_path, str(output_path / Path(image_path).name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add watermarks to batch of images. Original images won't be affected. A new copy will be created")
    parser.add_argument('-i', '--images_path', type=str, required=True,
                        help='The path to the folder containing images.')
    parser.add_argument('-o', '--opacity', type=float, default=0.8,
                        help='The opacity of the watermarks. Default is 0.8.')
    parser.add_argument('-s1', '--scale1', type=int, default=15,
                        help='The scale of the logo ss_watermark as a percentage of the image height. Default is 15.')
    parser.add_argument('-s2', '--scale2', type=int, default=3,
                        help='The scale of the instagram ss_watermark as a percentage of the image height. Default is 3.')
    parser.add_argument('-q', '--quality', type=int, default=100,
                        help='Quality of the output image as a percentage. Default is 100.')

    args = parser.parse_args()

    watermarks_path = Path("img")
    logo_path = watermarks_path / "Space-shop-logo_white.png"
    insta_logo = watermarks_path / "instagram.png"

    images_path = Path(args.images_path)
    output_path = images_path / "watermarked"

    os.makedirs(output_path, exist_ok=True)

    for img_name in tqdm(os.listdir(str(images_path))):
        if img_name.lower().endswith(".jpg") or img_name.endswith(".png"):
            add_watermark(images_path / img_name, logo_path, insta_logo, output_path,
                          opacity=args.opacity, scale1=args.scale1, scale2=args.scale2, quality=args.quality)
