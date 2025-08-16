from write_meta import write_meta
from fetch_meta import generate_image_metadata
from image_compress import compress_image

import os

def process_image_directory(directory):
    """
    :param directory: path for images
    """
    metadata_file_path = os.path.join(directory, 'image_metadata.txt')
    with open(metadata_file_path, 'w') as file:
        pass  # empty the file
    
    with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
        # iteration
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(directory, filename)
                
                # compress
                compressed_image_path = compress_image(image_path)
                print(os.path.getsize(compressed_image_path))
                
                # generate meta data
                metadata = generate_image_metadata(compressed_image_path)
                
                if metadata:
                    # rename
                    new_filename = f"{metadata['title']}{os.path.splitext(filename)[1]}"
                    new_image_path = os.path.join(directory, new_filename)
                    os.rename(image_path, new_image_path)
                    
                    # write meta data
                    keywords = [item.strip() for item in metadata['keywords'].split(",")]
                    write_meta(metadata['title'], keywords, new_image_path)
                    metadata_file.write(f"Image: {new_filename}\n")
                    metadata_file.write(f"Title: {metadata['title']}\n")
                    metadata_file.write(f"Keywords: {metadata['keywords']}\n\n")
                    
                    print(f"Processed: {filename} -> {new_filename}\n")
                
                # delete compressed file
                if os.path.exists(compressed_image_path) and compressed_image_path != new_image_path:
                    os.remove(compressed_image_path)

if __name__ == "__main__":
    # replace it with your path
    image_directory = os.path.join(os.path.dirname(__file__), 'Aug-2025')
    process_image_directory(image_directory)