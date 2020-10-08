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

import logging

### Config
try:
  from instance.config import Config
  config = Config()
except Exception as e:
  logging.warning("""Arquivo de configuração não encontrado ou mal formado. Lei\
a o manual.\n{}""".format(str(e)))
  raise

### Aiogram
## https://docs.aiogram.dev/en/latest/
from aiogram import (
  Dispatcher,
)

### AIO Matebot
from matebot.aio_matebot import (
  models,
  views,
  controllers,
)
from matebot.aio_matebot.controllers.bot import MateBot

def run(bot_name):
  bot = MateBot(
    token = config.bots[bot_name]['token'] or '',
    config = config,
    name = bot_name,
  )
  dispatcher = Dispatcher(bot)
  try:
    controllers.run_webhook(dispatcher)
  except Exception as e:
    logging.warning(u"Webhook não deu certo! Exceção: {}".format(repr(e))
    controllers.run_polling(dispatcher)
