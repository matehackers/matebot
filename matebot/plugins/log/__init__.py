# vim:fileencoding=utf-8
#  Plugin log para matebot: Logging/debugging
#  Copyleft (C) 2016-2020 Iuri Guilherme, 2017-2020 Matehackers,
#    2018-2019 Velivery, 2019 Greatful, 2020 Fábrica do Futuro
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

import datetime, json

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

async def update_logger(
  update: types.Update,
  descriptions: list = ['none'],
):
  dispatcher = Dispatcher.get_current()
  bot = dispatcher.bot
  url = ''
  if hasattr(update, 'chat') and update.chat.type != "private":
    url = update.url
  text = list()
  text.append(u" ".join([u" ".join(["#" + d for d in descriptions]), str(url)]))
  text.append('')
  text.append(json.dumps(update.to_python(), indent=2))
  await bot.send_message(
    bot.users['special']['log'],
    '\n'.join(text),
    disable_notification = True,
  )

async def info_logger(
  update: types.Update,
  descriptions: list = ['none'],
  info: str = "None",
):
  dispatcher = Dispatcher.get_current()
  bot = dispatcher.bot
  url = ''
  if hasattr(update, 'chat') and update.chat.type != "private":
    url = update.url
  text = list()
  text.append(u" ".join([u" ".join(["#" + d for d in descriptions]), str(url)]))
  text.append('')
  text.append(info)
  await bot.send_message(
    bot.users['special']['info'],
    '\n'.join(text),
    disable_notification = True,
  )

async def debug_logger(
  update: types.Update,
  error: str = 'none',
  exception: Exception = None,
):
  dispatcher = Dispatcher.get_current()
  bot = dispatcher.bot
  url = ''
  if hasattr(update, 'chat') and update.chat.type != "private":
    url = update.url
  text = list()
  text.append(u" ".join(["#" + str(error), str(url)]))
  text.append('')
  text.append(json.dumps(update.to_python(), indent=2))
  text.append('')
  text.append(u"Exception: {exception}".format(exception = exception))
  await bot.send_message(
    bot.users['special']['debug'],
    '\n'.join(text),
    disable_notification = True,
  )
