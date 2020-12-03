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
from matebot.aio_matebot.controllers.longpolling import run_polling
from matebot.aio_matebot.controllers.webhook import run_webhook

def run(bot_name):
  bot = MateBot(
    token = config.bots[bot_name]['telegram']['token'] or '',
    config = config,
    name = bot_name,
  )
  dispatcher = Dispatcher(bot)
  try:
    run_webhook(dispatcher)
  except Exception as e:
    logging.warning(u"Webhook não deu certo! Exceção: {}".format(repr(e)))
    run_polling(dispatcher)
  finally:
    logging.info(u"Webhook do Telegram terminou")

async def arun(bot_name):
  bot = MateBot(
    token = config.bots[bot_name]['telegram']['token'] or '',
    config = config,
    name = bot_name,
  )
  dispatcher = Dispatcher(bot)
  try:
    await controllers.arun_webhook(dispatcher)
  except KeyError as e:
    logging.warning(u"""Problema com o arquivo de configuração. Já lerdes o man\
ual? Fizerdes tudo certo? Se tiverdes certeza de que está tudo certo e não func\
iona, pede ajuda no Github, no Telegram, no Discord, enfim...\nChave que não fo\
i encontrada no arquivo de configuração: {}""".format(str(e)))
  except Exception as e:
    logging.warning(u"""Webhook do Telegram não deu certo! Exceção: {}\
""".format(repr(e)))
    raise
  finally:
    logging.info(u"Webhook do Telegram terminou")
