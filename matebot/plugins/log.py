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

import datetime, json, logging

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

## TODO: Descobrir tipo de update (era types.Message)
async def info_logger(
  update: types.Update,
  descriptions: list = ['none'],
):
  dispatcher = Dispatcher.get_current()
  bot = dispatcher.bot
  url = ''
  if hasattr(update, 'chat') and update.chat.type != "private":
    # ~ url = update.url
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

async def debug_logger(
  error: str = u"Alguma coisa deu errado",
  message: types.Message = None,
  exception: Exception = None,
  descriptions: list = 'error',
):
  dispatcher = Dispatcher.get_current()
  bot = dispatcher.bot
  url = ''
  if hasattr(message, 'chat') and message.chat.type != "private":
    # ~ url = message.url
    url = message.link('link', as_html = False)
  text = list()
  text.append(
    u" ".join([
      u" ".join([escape_md("#" + d) for d in descriptions]),
      url,
    ])
  )
  text.append('')
  if message is not None:
    text.append('```')
    text.append(json.dumps(message.to_python(), indent=2))
    text.append('```')
    text.append('')
  if exception is not None:
    text.append('```')
    text.append(json.dumps(repr(exception), indent=2))
    text.append('```')
    text.append('')
  text.append(escape_md(error))
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
