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

import datetime

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
  group: int = -1,
  description: str = 'None',
):
  dispatcher = Dispatcher.get_current()
  bot = dispatcher.bot
  url = ''
  if hasattr(update, 'chat') \
  and update.chat.type in ['group', 'supergroup', 'channel'] \
  and hasattr(update, 'url'):
    url = update.url
  text = list()
  text.append(u"#{desc} {id} {url}".format(desc = description, id = update.update_id, url = url))
  text.append('')
  text.append(str(update))
  await bot.send_message(
    group,
    '\n'.join(text),
    disable_notification = True,
  )

async def debug_logger(
  update: types.Update,
  group: int = -1,
  error: str = 'None',
  exception: Exception = None,
):
  dispatcher = Dispatcher.get_current()
  bot = dispatcher.bot
  url = ''
  if hasattr(update, 'chat') \
  and update.chat.type in ['group', 'supergroup', 'channel'] \
  and hasattr(update, 'url'):
    url = update.url
  text = list()
  text.append(u"#{error} {url}".format(error = error, url = url))
  text.append('')
  text.append(str(update))
  text.append('')
  text.append(str(exception))
  await bot.send_message(
    group,
    '\n'.join(text),
    disable_notification = True,
  )
