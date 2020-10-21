# vim:fileencoding=utf-8
#  Plugin log para matebot: Logging/debugging
#  Copyleft (C) 2016-2020 Iuri Guilherme, 2017-2020 Matehackers,
#    2018-2019 Velivery, 2019 Greatful, 2019-2020 Fábrica do Futuro
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime, json, logging, socket, sys

## Telepot
class log_str():
  def __init__(self):
    pass
  def debug(message):
    return u'[%s] [DEBUG] %s' % (str(datetime.datetime.now()), message)
  def info(message):
    return u'[%s] [INFO] %s' % (str(datetime.datetime.now()), message)
  def warn(message):
    return u'[%s] [WARN] (?) %s' % (str(datetime.datetime.now()), message)
  def err(message):
    return u'[%s] [ERR] (!) %s' % (str(datetime.datetime.now()), message)
  def cmd(command):
    return u'[%s] [CMD] Executando "%s"' % (str(datetime.datetime.now()), command)
  def rcv(target, message):
    return u'[%s] [RCV] Recebemos "%s" de %s' % (str(datetime.datetime.now()), message, target)
  def send(target, message):
    return u'[%s] [SEND] Enviando "%s" para %s' % (str(datetime.datetime.now()), message, target)

## Aiogram
from aiogram import (
  Dispatcher,
  types,
)

from aiogram.utils.markdown import escape_md
key_error = u"""Mensagem não enviada para grupo de log. Para ativar log em grup\
os de telegram, coloque o bot em um grupo e use o chat_id do grupo no arquivo d\
e configuração."""

async def tecido_logger(texto: str = ''):
  logger = logging.getLogger('tecido')
  logger.setLevel(logging.DEBUG)
  dispatcher = Dispatcher.get_current()
  bot = dispatcher.bot
  ## https://pymotw.com/3/socket/tcp.html
  # socket_echo_client.py
  # Create a TCP/IP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  ## JAMAIS bloquear
  # ~ sock.setblocking(0) ## Talvez bloquear de vez em quando
  # Connect the socket to the port where the server is listening
  server_address = (bot.tecido['host'], bot.tecido['port'])
  logger.info('connecting to {} port {}'.format(*server_address))
  try:
    sock.connect(server_address)
  except ConnectionRefusedError:
    logger.debug(u"""Servidor TextoTecidoPalavras não escutando em {0}:{1}\
""".format(bot.tecido['host'], bot.tecido['port']))
    return 1
  try:
    # Send data
    ## Texto da mensagem passado pelo parâmetro desta função
    message = texto.encode('raw_unicode_escape', 'replace')
    # ~ message = bytes(texto, 'cp860')
    # ~ message = bytearray(texto, 'UTF-8')
    logger.info('sending {!r}'.format(message))
    sock.sendall(message)
    # Look for the response
    # ~ amount_received = 0
    # ~ amount_expected = len(message)
    # ~ while amount_received < amount_expected:
      # ~ data = sock.recv(16)
      # ~ amount_received += len(data)
      # ~ logger.info('received {!r}'.format(data))
  except Exception as e:
    logger.debug(repr(e))
    return 1
  finally:
    logger.info('closing socket')
    sock.close()
    return 0

## TODO: Descobrir tipo de update (era types.Message)
async def info_logger(
  update,
  descriptions: list = ['none'],
):
  dispatcher = Dispatcher.get_current()
  bot = dispatcher.bot
  url = ''
  if hasattr(update, 'chat') and update.chat.type != "private":
    ##url = update.url
    url = update.link('link', as_html = False)
  text = list()
  text.append(
    u" ".join([
      u" ".join([escape_md("#" + d) for d in descriptions]),
      url,
    ])
  )
  text.append('')
  text.append('```')
  text.append(json.dumps(update.to_python(), indent=2))
  text.append('```')
  try:
    await bot.send_message(
      chat_id = bot.users['special']['info'],
      text = '\n'.join(text),
      disable_notification = True,
      parse_mode = "MarkdownV2",
    )
  except KeyError:
    logging.debug(key_error)
  ## TelegramTextoTecidoTabelas
  await tecido_logger(getattr(update, 'text', ''))

async def debug_logger(
  message: types.Message,
  exception: Exception = None,
  descriptions: list = 'error',
):
  dispatcher = Dispatcher.get_current()
  bot = dispatcher.bot
  url = ''
  if hasattr(message, 'chat') and message.chat.type != "private":
    ##url = message.url
    url = message.link('link', as_html = False)
  text = list()
  text.append(
    u" ".join([
      u" ".join([escape_md("#" + d) for d in descriptions]),
      url,
    ])
  )
  text.append('')
  text.append('```')
  text.append(json.dumps(message.to_python(), indent=2))
  text.append('```')
  text.append('')
  text.append('```')
  text.append(json.dumps(repr(exception), indent=2))
  text.append('```')
  try:
    await bot.send_message(
      chat_id = bot.users['special']['debug'],
      text = '\n'.join(text),
      disable_notification = True,
      parse_mode = "MarkdownV2",
    )
  except KeyError:
    logging.debug(key_error)

async def exception_logger(
  exception: Exception = None,
  descriptions: list = 'error',
):
  dispatcher = Dispatcher.get_current()
  bot = dispatcher.bot
  text = list()
  text.append(
    u" ".join([
      u" ".join([escape_md("#" + d) for d in descriptions]),
    ])
  )
  text.append('')
  text.append('```')
  text.append(json.dumps(repr(exception), indent=2))
  text.append('```')
  try:
    await bot.send_message(
      chat_id = bot.users['special']['debug'],
      text = '\n'.join(text),
      disable_notification = True,
      parse_mode = "MarkdownV2",
    )
  except KeyError:
    logging.debug(key_error)
