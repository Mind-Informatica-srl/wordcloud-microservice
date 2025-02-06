import io
from PIL import Image


def overlayimages(image1, image2):
    # Ensure both images have the same size
    image2 = image2.resize(image1.size)

    # Overlay images
    combined_image = Image.alpha_composite(image1.convert('RGBA'), image2.convert('RGBA'))

    # Save to a bytes buffer
    img_byte_arr = io.BytesIO()
    combined_image.save(img_byte_arr, format='svg')
    img_byte_arr.seek(0)

    return img_byte_arr