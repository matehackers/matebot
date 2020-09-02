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
# ~ logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

### Config
from instance.config import Config

### Aiogram
## https://docs.aiogram.dev/en/latest/
from aiogram import (
  Bot,
  Dispatcher,
  executor,
)

# ~ ### AIO Matebot
from matebot.aio_matebot import (
  models,
  views,
  controllers,
)

async def on_startup(dispatcher: Dispatcher):
  controllers.add_handlers(dispatcher)
  bot = dispatcher.bot
  print(u"Deu Certo, nosso id é {}".format(str(bot.id)))

async def on_shutdown(dispatcher: Dispatcher):
  dispatcher.stop_polling()
  print(u"Tchau!")

def run(bot):
  config = Config()
  bot = Bot(token=config.tokens[bot])
  dispatcher = Dispatcher(bot)
  executor.start_polling(
    dispatcher,
    on_startup = on_startup,
    on_shutdown = on_shutdown,
  )
  dispatcher.stop_polling()

## TODO Não uso mais Quart nem Flask
### Quart
# ~ import os
# ~ import hypercorn.asyncio
# ~ from quart import Quart
# ~ app = Quart(__name__, instance_relative_config = True)
# ~ try:
  # ~ ## Por padrão ./instance/config.py que deve estar ignorado pelo 
  # ~ ## .gitignore. Copiar ./default_config.py para ./instance/config.py 
  # ~ ## antes de rodar o flask.
  # ~ ## TODO hardcoding 'instance.config.developmentConfig' doesn't seem right
  # ~ app.config.from_object('doc.default_config.Config')
  # ~ app.config.from_object('.'.join([
    # ~ 'instance',
    # ~ 'config',
    # ~ ''.join([os.environ['QUART_ENV'], 'Config']),
  # ~ ]))
# ~ except Exception as e:
  # ~ print(u"Arquivo de configuração não encontrado. Exceção: %s" % (e))
  # ~ raise
## Quart Shell
# ~ @app.shell_context_processor
# ~ def make_shell_context():
  # ~ return {
    # ~ 'bot': bots[0],
    # ~ 'dp': dispatchers[0],
  # ~ }
