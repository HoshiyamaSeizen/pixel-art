from PIL import Image
from io import BytesIO
from base64 import b64encode, b64decode
from sys import argv

if __name__ == "__main__":
    with open(argv[1], 'r+') as f:
        base64img, pixel_size, colors = f.readlines()

        index = base64img.find('base64,')
        base64img = base64img[index+7:]

        img = Image.open(BytesIO(b64decode(base64img)))
        img = img.resize(
            (img.width // int(pixel_size), img.height // int(pixel_size)),
            resample=Image.NEAREST
        )
        img = img.convert("P", palette=Image.ADAPTIVE, colors=int(colors)).convert('RGB')
        img = img.resize(
            (img.width * int(pixel_size), img.height * int(pixel_size)),
            resample=Image.NEAREST
        )

        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        base64img = b64encode(buffered.getvalue()).decode("utf-8")

        f.seek(0)
        f.write("data:image/jpeg;base64," + base64img)
        f.truncate()
