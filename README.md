# SpaceShop42 Watermark

Small script to add watermark of SpaceShop logo and instagram information to folder of images.
# Installation 
Install `imagemagic` first. Install requirements using `pip install -r requirements.txt`. 

# Instructions

```shell
pip install -r requirements.txt

python watermark.py -i <path to images>

python watermark.py -h # for more options
```

There is to options to run with adding watermark and only compression

For adding watermark, recommended way of running

```shell

python watermark.py -i 'path' -q 70
```

For adding with compression

```shell

python watermark.py -i 'path' -q 90 --compress_only
```
