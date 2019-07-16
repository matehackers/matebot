# vim:fileencoding=utf-8
#  Plugin qrencode para matebot: Gera qr code a partir de texto.
#  Copyleft (C) 2016-2019 Desobediente Civil, Matehackers, Velivery

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

def cmd_qr(args):
  try:
    response = create_qrcode(' '.join(args['command_list']))
    return {
      'status': True,
      'type': "image",
      'response': response,
      'debug': u"QR code bem sucedido",
      'multi': False,
      'parse_mode': None,
    }
  except Exception as e:
    return {
      'status': False,
      'type': "erro",
      'response':  u"Não consegui gerar um qr code com %s\nOs desenvolvedores devem ter sido avisados já, eu acho." % (str(args['command_list'])),
      'debug': u"QR code erro\nExceção: %s" % (e),
      'multi': False,
      'parse_mode': None,
    }

def create_qrcode(text):
  import os
  import pyqrcode
  import tempfile
  photo = tempfile.mkstemp(suffix='.png')
  qrcode = pyqrcode.create(str(text), version=10)
  qrcode.png(photo[1], scale=6)
  return {
    'photo': photo, 
    'text': str(text),
  }

