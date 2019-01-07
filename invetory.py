import qrcode
import brother_ql

from PIL import Image, ImageDraw, ImageFont

# from brother_ql.raster import BrotherQLRaster
# from brother_ql.devicedependent import models, label_type_specs, ENDLESS_LABEL, DIE_CUT_LABEL, ROUND_DIE_CUT_LABEL
# from brother_ql import BrotherQLError, BrotherQLUnsupportedCmd, BrotherQLUnknownModel
from brother_ql.backends import backend_factory
# from brother_ql.reader import interpret_response

title_text: str = 'Cameras'
list_text: str = "Wifi Outdoor \nWifi Indoor \nOther"
base_url: str = 'https://nc.torchtarget.biz/apps/files/?dir=/Inventory/'
qr_url: str = base_url + title_text
print(qr_url)

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=4,
    border=4,
)
mypath: str = "tmp3.bmp"
mypath2: str = "tmp3.bin"

qr.add_data(qr_url)
qr.make(fit=True)
img = qr.make_image()
print(img.size[1], img.size[0])
x = img.size[1]
y = img.size[0]

newImage = Image.new('L', (x * 2, int(y + y // 4 + 1)), "white")
titleImage = Image.new('L', (x * 2, int(y // 4 + 1)), "white")
textImage = Image.new('L', (x, y), "white")
draw = ImageDraw.Draw(textImage)
draw.multiline_text((0, 10), list_text)
textImage.save("tmp2.bmp")

draw = ImageDraw.Draw(titleImage)
font = ImageFont.truetype("arial.ttf", int(y / 5))
draw.text((0, 0), title_text, font=font)
titleImage.save("tmp4.bmp")

newImage.paste(titleImage, (0, 0))
newImage.paste(img, (0, int(y // 4 + 1)))
newImage.save("tmp1.bmp")
newImage.paste(textImage, (x, int(y // 4 + 1)))
newImage.save("tmp3.bmp")

# 29x90 Codes 306x 991
qlr = brother_ql.BrotherQLRaster('QL-700')
qlr.exception_on_warning = True
brother_ql.create_label(qlr, newImage, '62')
fo = open(mypath2, 'wb')
fo.write(qlr.data)
fo.close()

be = backend_factory('pyusb')
list_available_devices = be['list_available_devices']
BrotherQLBackend = be['backend_class']

ad = list_available_devices()
for printer in ad:
    print("HERE")
    print(ad)
    print(printer['identifier'])

string_descr = ad[0]['identifier']
print("Selecting first device %s" % string_descr)
printer = BrotherQLBackend(string_descr)
printer.write(qlr.data)
