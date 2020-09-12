# -*- coding: utf-8 -*-
#
#  Matebot
#  
#  Copyleft 2012-2020 Iuri Guilherme <https://github.com/iuriguilherme>,
#     Matehackers <https://github.com/matehackers>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import json

### Logging
import logging
logging.basicConfig(level=logging.INFO)
# ~ logging.basicConfig(level=logging.DEBUG)

### Config
try:
  from instance.config import Config
  config = Config()
except Exception as e:
  print(u"Arquivo de configuração não encontrado ou mal formado. Leia o manual.\
    \n{}".format(str(e)))
  raise

### Aiogram
## https://docs.aiogram.dev/en/latest/
from aiogram import (
  Bot,
  Dispatcher,
  executor,
  exceptions,
)

# ~ ### AIO Matebot
from matebot.aio_matebot import (
  models,
  views,
  controllers,
)

async def on_startup(dispatcher: Dispatcher):
  await controllers.add_handlers(dispatcher)
  bot = dispatcher.bot
  print(u"Deu Certo, nosso id é {}".format(str(bot.id)))

async def on_shutdown(dispatcher: Dispatcher):
  dispatcher.stop_polling()
  print(u"Tchau!")

def run(bot_name):
  bot = Bot(token = config.bots[bot_name]['token'])
  setattr(bot, 'info', config.bots[bot_name]['info'])
  setattr(bot, 'plugins', config.bots[bot_name]['plugins'])
  setattr(bot, 'users', config.bots[bot_name]['users'])
  dispatcher = Dispatcher(bot)
  executor.start_polling(
    dispatcher,
    on_startup = on_startup,
    on_shutdown = on_shutdown,
  )
  dispatcher.stop_polling()
