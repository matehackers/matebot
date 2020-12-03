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

## Aiogram
from aiogram import (
  Bot,
  # ~ Dispatcher,
  executor,
  types,
  filters,
)
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import (
  Executor,
  start_webhook,
)

## Matebot
from matebot.aio_matebot import (
  config,
)
from matebot.aio_matebot.controllers import (
  add_filters,
  add_handlers,
)

async def webhook_on_startup(dispatcher: Dispatcher):
  certificate = None
  try:
    certificate = open('instance/matebot.pem', 'r')
  except Exception as e:
    logging.warning(u"""Certificado não encontrado ou não consegui abrir.\nExce\
ção: {0}""".format(repr(e)))
  await dispatcher.bot.set_webhook(
    url = dispatcher.bot.url,
    certificate = certificate,
  )
  await add_filters(dispatcher)
  await add_handlers(dispatcher)
  logging.info(u"Deu Certo, nosso id é {}".format(str(dispatcher.bot.id)))
  try:
    await dispatcher.bot.send_message(
      chat_id = dispatcher.bot.users['special']['info'],
      text = u"Mãe tá #on",
      disable_notification = True,
    )
  except KeyError:
    logging.debug(u"Já começou não configurando os logs...")

async def webhook_on_shutdown(dispatcher: Dispatcher):
  logging.info(u"Tchau!")
  try:
    await dispatcher.bot.send_message(
      chat_id = dispatcher.bot.users['special']['info'],
      text = u"Mãe tá #off",
      disable_notification = True,
    )
  except KeyError:
    logging.debug(u"Já começou não configurando os logs...")
  await dispatcher.bot.delete_webhook()
  # ~ await dispatcher.storage.close()
  # ~ await dispatcher.storage.wait_closed()
  logging.warning(u"Mãe tá #off")


def run_webhook(dispatcher: Dispatcher):
  from aiogram.contrib.middlewares.logging import LoggingMiddleware

  # webhook settings
  WEBHOOK_HOST = getattr(dispatcher.bot, 'webhook').get('host')
  WEBHOOK_PORT = getattr(dispatcher.bot, 'webhook').get('port')
  WEBHOOK_LOCALHOST = getattr(dispatcher.bot, 'webhook').get('localhost')
  WEBHOOK_LOCALPORT = getattr(dispatcher.bot, 'webhook').get('localport')
  WEBHOOK_PATH = getattr(dispatcher.bot, 'webhook').get('path')
  WEBHOOK_URL = "https://{0}:{2}/{1}".format(
    WEBHOOK_HOST,
    WEBHOOK_PATH,
    WEBHOOK_PORT,
  )
  setattr(dispatcher.bot, 'url', WEBHOOK_URL)

  dispatcher.middleware.setup(LoggingMiddleware())

  # ~ from aiogram.dispatcher.webhook import SendMessage
  # ~ @dispatcher.message_handler()
  # ~ async def echo_callback(message: types.Message):
    # ~ # Regular request
    # ~ await dispatcher.bot.send_message(message.chat.id, message.text)

    # ~ # or reply INTO webhook
    # ~ return SendMessage(message.chat.id, message.text)

  ## FIXME Falta mandar o certificado como parâmetro
  start_webhook(
    dispatcher = dispatcher,
    webhook_path = "/" + WEBHOOK_PATH,
    on_startup = webhook_on_startup,
    on_shutdown = webhook_on_shutdown,
    skip_updates = False,
    host = WEBHOOK_LOCALHOST,
    port = WEBHOOK_LOCALPORT,
  )

async def arun_webhook(dispatcher: Dispatcher):
  from aiogram.contrib.middlewares.logging import LoggingMiddleware

  # webhook settings
  WEBHOOK_HOST = getattr(dispatcher.bot, 'webhook').get('host')
  WEBHOOK_PORT = getattr(dispatcher.bot, 'webhook').get('port')
  WEBHOOK_LOCALHOST = getattr(dispatcher.bot, 'webhook').get('localhost')
  WEBHOOK_LOCALPORT = getattr(dispatcher.bot, 'webhook').get('localport')
  WEBHOOK_PATH = getattr(dispatcher.bot, 'webhook').get('path')
  WEBHOOK_URL = "https://{0}:{2}/{1}".format(
    WEBHOOK_HOST,
    WEBHOOK_PATH,
    WEBHOOK_PORT,
  )
  setattr(dispatcher.bot, 'url', WEBHOOK_URL)

  dispatcher.middleware.setup(LoggingMiddleware())

  # ~ from aiogram.dispatcher.webhook import SendMessage
  # ~ @dispatcher.message_handler()
  # ~ async def echo_callback(message: types.Message):
    # ~ # Regular request
    # ~ await dispatcher.bot.send_message(message.chat.id, message.text)

    # ~ # or reply INTO webhook
    # ~ return SendMessage(message.chat.id, message.text)

  ## FIXME Falta mandar o certificado como parâmetro
  start_webhook(
    dispatcher = dispatcher,
    webhook_path = "/" + WEBHOOK_PATH,
    on_startup = webhook_on_startup,
    on_shutdown = webhook_on_shutdown,
    skip_updates = False,
    host = WEBHOOK_LOCALHOST,
    port = WEBHOOK_LOCALPORT,
  )
