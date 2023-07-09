import cv2
import os
from pathlib import Path
import argparse


def add_watermark(image_path, watermark1_path, insta_logo_path, output_path, opacity, scale1, scale2):
    # Read the watermarks and the image
    watermark1 = cv2.imread(str(watermark1_path), -1)
    watermark1 = cv2.cvtColor(watermark1, cv2.COLOR_BGR2BGRA)

    insta_logo = cv2.imread(str(insta_logo_path), -1)
    insta_logo = cv2.cvtColor(insta_logo, cv2.COLOR_BGR2BGRA)

    image = cv2.imread(str(image_path))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

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
    resized_insta_logo = cv2.resize(insta_logo, dim2, interpolation=cv2.INTER_AREA)

    # Add fixed text next to the Instagram logo
    font = cv2.FONT_HERSHEY_SIMPLEX
    insta_text = "@space_shop42"
    text_size, _ = cv2.getTextSize(insta_text, font, 2, 2)
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

    # Save the result
    cv2.imwrite(str(output_path / Path(image_path).name), image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add watermarks to batch of images.')
    parser.add_argument('-i', '--images_path', type=str, required=True,
                        help='The path to the folder containing images.')
    parser.add_argument('-o', '--opacity', type=float, default=0.8,
                        help='The opacity of the watermarks. Default is 0.8.')
    parser.add_argument('-s1', '--scale1', type=int, default=15,
                        help='The scale of the logo ss_watermark as a percentage of the image height. Default is 15.')
    parser.add_argument('-s2', '--scale2', type=int, default=3,
                        help='The scale of the instagram ss_watermark as a percentage of the image height. Default is 3.')

    args = parser.parse_args()

    watermarks_path = Path("img")
    logo_path = watermarks_path / "Space-shop-logo_white.png"
    insta_logo = watermarks_path / "instagram.png"

    images_path = Path(args.images_path)
    output_path = images_path / "watermarked"

    os.makedirs(output_path, exist_ok=True)

    for img_name in os.listdir(str(images_path)):
        if img_name.lower().endswith(".jpg") or img_name.endswith(".png"):
            add_watermark(images_path / img_name, logo_path, insta_logo, output_path,
                          opacity=args.opacity, scale1=args.scale1, scale2=args.scale2)
