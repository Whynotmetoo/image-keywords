import pyexiv2
from typing import List
import os

def write_meta(title: str, keywords: List[str], image_path: str):
    # load image
    image = pyexiv2.Image(image_path)

    # set title
    image.modify_xmp({'Xmp.dc.description': {f'lang=x-default': title}})
    image.modify_exif({'Exif.Image.ImageDescription': title})
    image.modify_iptc({'Iptc.Application2.Caption': title})

    # set keywords
    image.modify_iptc({'Iptc.Application2.Keywords': keywords})
    image.modify_exif({'Exif.Photo.UserComment': f'charset=Ascii {{"c":"{keywords}"}}'})

    # save
    image.close()


def active_write_data(image_path: str):
    image = pyexiv2.Image(image_path)

     # get xmp data
    xmp = image.read_xmp()
    # get iptc data
    iptc = image.read_iptc()
    # get exif data
    exif = image.read_exif()
    print(f"xmp data: {xmp}\n")
    print(f"iptc data: {iptc}\n")
    print(f"exif data: {exif}\n")


if __name__ == "__main__":
    # replace it with your path
    image_directory = os.path.join(os.path.dirname(__file__), 'test/Vibrant Abstract Visualization of a Human Brain Signifying Intelligence and Creativity.jpg')
    active_write_data(image_directory)
