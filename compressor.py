import subprocess


def compress_images(input_path, output_path, quality):
    subprocess.run(["convert", input_path, "-quality", str(quality), output_path], check=True)
