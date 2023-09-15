from PIL import Image,JpegImagePlugin


Image.register_extension(JpegImagePlugin.JpegImageFile.format, ".abcd")