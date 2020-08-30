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

import os

### Flask
from flask import Flask
app = Flask(__name__, instance_relative_config = True)
try:
  ## Por padrão ./instance/config.py que deve estar ignorado pelo 
  ## .gitignore. Copiar ./default_config.py para ./instance/config.py 
  ## antes de rodar o flask.
  ## TODO hardcoding 'instance.config.developmentConfig' doesn't seem right
  app.config.from_object('doc.default_config.Config')
  app.config.from_object('.'.join([
    'instance',
    'config',
    ''.join([os.environ['FLASK_ENV'], 'Config']),
  ]))
except Exception as e:
  print(u"Arquivo de configuração não encontrado. Exceção: %s" % (e))
  raise

# ~ ### Logging
# ~ import logging
# ~ # Configure logging
# ~ logging.basicConfig(level=logging.INFO)
# ~ logging.basicConfig(level=logging.DEBUG)

# ~ ### Aiogram
# ~ ## https://docs.aiogram.dev/en/latest/
# ~ from aiogram import (
  # ~ Bot,
  # ~ Dispatcher,
# ~ )

# ~ API_TOKEN = app.config['BOTFATHER']['token']

# ~ # Initialize bot and dispatcher
# ~ bots = list()
# ~ ## Bot único
# ~ bots.append(Bot(token=API_TOKEN))
# ~ ## Múltiplos bots
# ~ for token in app.config['BOTFATHER']['tokens']
  # ~ bots.append(Bot(token=token))

# ~ dispatchers = list()
# ~ for bot in bots:
  # ~ dispatchers.append(Dispatcher(bot))

# ~ ### AIO Matebot
# ~ from matebot.aio_matebot import (
  # ~ models,
  # ~ views,
  # ~ controllers,
# ~ )

# ~ ### Flask Shell
# ~ @app.shell_context_processor
# ~ def make_shell_context():
  # ~ return {
    # ~ 'bot': bots[0],
    # ~ 'dp': dispatchers[0],
  # ~ }

"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = app.config['BOTFATHER']['token']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
  """
  This handler will be called when user sends `/start` or `/help` command
  """
  await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
  with open('data/cats.jpg', 'rb') as photo:
    '''
    # Old fashioned way:
    await bot.send_photo(
        message.chat.id,
        photo,
        caption='Cats are here 😺',
        reply_to_message_id=message.message_id,
    )
    '''

    await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler()
async def echo(message: types.Message):
  # old style:
  # await bot.send_message(message.chat.id, message.text)

  await message.answer(message.text)


executor.start_polling(dp, skip_updates=True)
