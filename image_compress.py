from PIL import Image
import os

def compress_image(image_path, max_size=(512, 512), quality=40):
    """
    compress the file while keey the ratio
    :param image_path: image path
    :param max_size: maximum width and height
    :param quality: quality
    :return: path for compressed file
    """
    # open file
    with Image.open(image_path) as img:
        # get original size
        original_width, original_height = img.size
        # calculate the scale ration
        ratio = min(max_size[0]/original_width, max_size[1]/original_height)
        
        # if need to compress
        if ratio < 1:
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            # compress
            img_resized = img.resize((new_width, new_height), Image.LANCZOS)
            # create path for compressed file
            file_name, file_ext = os.path.splitext(image_path)
            compressed_path = f"{file_name}_compressed{file_ext}"
            # save compressed file
            img_resized.save(compressed_path, optimize=True, quality=quality)
            return compressed_path
        
        # if no need to compress, just save
        else:
            file_name, file_ext = os.path.splitext(image_path)
            compressed_path = f"{file_name}_compressed{file_ext}"
            img.save(compressed_path, optimize=True, quality=quality)
            return compressed_path