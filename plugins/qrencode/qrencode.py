# vim:fileencoding=utf-8
## Generate qr codes from text.
## This uses UNIX qrencode package

import os
import pyqrcode
import tempfile

class qrencode():
  def __init__(self):
    pass
  def svg(self, text):
    photo = tempfile.mkstemp(suffix='.png')
    qrcode = pyqrcode.create(str(text), version=10)
    qrcode.png(photo[1], scale=6)
    return {'photo': photo, 'text': text}

