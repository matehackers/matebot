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
  Dispatcher,
  executor,
  types,
  filters,
)

## Matebot
from matebot.aio_matebot import (
  config,
)

## Generic Callbacks
from matebot.aio_matebot.controllers.callbacks import (
  message_callback,
  command_callback,
  error_callback,
  any_message_callback,
  any_edited_message_callback,
  any_channel_post_callback,
  any_edited_channel_post_callback,
  any_update_callback,
  any_error_callback,
)

## Filters
from matebot.aio_matebot.controllers.filters import (
  IsReplyToIdFilter,
)

## Plugins
from matebot.plugins import (
  default as plugin_default,
  admin as plugin_admin,
  archive as plugin_archive,
  donate as plugin_donate,
  feedback as plugin_feedback,
  hashes as plugin_hashes,
  mate_matica as plugin_matematica,
  personalidades as plugin_personalidades,
  qr as plugin_qr,
  tropixel as plugin_tropixel,
  welcome as plugin_welcome,
  ytdl as plugin_ytdl,
)

async def add_filters(dispatcher: Dispatcher):
  ### Filters
  dispatcher.filters_factory.bind(IsReplyToIdFilter)

async def add_handlers(dispatcher: Dispatcher):
  ## Plugins de personalidades
  ## Carregados primeiro para sobrescrever todos outros (comportamento aiogram)
  await plugin_personalidades.add_handlers(dispatcher)
  ## Plugins especiais
  if dispatcher.bot.info.get('personalidade') in ['default', 'metarec', 'pave']:
    await plugin_donate.add_handlers(dispatcher)
  ## Plugins mais que especiais
  if dispatcher.bot.info.get('personalidade') in ['default', 'metarec']:
    try:
      await plugin_tropixel.add_handlers(dispatcher)
    except KeyError:
      logging.warning(u"plugin tropixel não configurado")
  ## Plugins gerais
  await plugin_archive.add_handlers(dispatcher)
  await plugin_hashes.add_handlers(dispatcher)
  await plugin_matematica.add_handlers(dispatcher)
  await plugin_qr.add_handlers(dispatcher)
  await plugin_ytdl.add_handlers(dispatcher)
  await plugin_feedback.add_handlers(dispatcher)
  await plugin_admin.add_handlers(dispatcher)
  try:
    await plugin_welcome.add_handlers(dispatcher)
  except KeyError:
    logging.warning(u"plugin welcome não configurado")
  await plugin_default.add_handlers(dispatcher)
  ## Todas updates que não forem tratadas por handlers anteriores
  dispatcher.register_message_handler(
    any_message_callback,
    content_types = types.message.ContentType.ANY,
  )
  dispatcher.register_edited_message_handler(any_edited_message_callback)
  dispatcher.register_channel_post_handler(any_channel_post_callback)
  dispatcher.register_edited_channel_post_handler(
    any_edited_channel_post_callback,
  )
  dispatcher.register_errors_handler(any_error_callback)

# ~ async def on_startup(dispatcher: Dispatcher):
  # ~ await add_filters(dispatcher)
  # ~ await add_handlers(dispatcher)

async def polling_on_startup(dispatcher: Dispatcher):
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

async def polling_on_shutdown(dispatcher: Dispatcher):
  logging.info(u"Tchau!")
  try:
    await dispatcher.bot.send_message(
      chat_id = dispatcher.bot.users['special']['info'],
      text = u"Mãe tá #off",
      disable_notification = True,
    )
  except KeyError:
    logging.debug(u"Já começou não configurando os logs...")
  dispatcher.stop_polling()

async def webhook_on_startup(dispatcher: Dispatcher):
  await dispatcher.bot.set_webhook(dispatcher.bot.url)
  # insert code here to run it after start

async def webhook_on_shutdown(dispatcher: Dispatcher):
  logging.warning(u"Webhook Shutting down...")
  # insert code here to run it before shutdown
  # Remove webhook (not acceptable in some cases)
  await dispatcher.bot.delete_webhook()
  # Close DB connection (if used)
  await dispatcher.storage.close()
  await dispatcher.storage.wait_closed()
  logging.warning(u"Mãe tá #off")

def run_polling(dispatcher: Dispatcher):
  executor.start_polling(
    dispatcher,
    on_startup = polling_on_startup,
    on_shutdown = polling_on_shutdown,
  )

def run_webhook(dispatcher: Dispatcher):
  from aiogram.contrib.middlewares.logging import LoggingMiddleware
  from aiogram.dispatcher.webhook import SendMessage

  # webhook settings
  WEBHOOK_HOST = dispatcher.bot.config.get('webhook', {
    'host': 'https://localhost'}).get('host')
  WEBHOOK_PATH = dispatcher.bot.config.get('webhook', {
    'path': '/webhook'}).get('path')
  WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

  # webserver settings
  WEBAPP_HOST = dispatcher.bot.config.get('webhook', {
    'webapp': 'localhost'}).get('webapp')
  WEBAPP_PORT = dispatcher.bot.config.get('webhook', {
    'port': 3001}).get('port')

  bot = dispatcher.bot
  dispatcher.middleware.setup(LoggingMiddleware())

  @dispatcher.message_handler()
  async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    return SendMessage(message.chat.id, message.text)

  setattr(dispatcher.bot, 'url', WEBHOOK_URL)

  executor.start_webhook(
    dispatcher = dispatcher,
    webhook_path = WEBHOOK_PATH,
    on_startup = webhook_on_startup,
    on_shutdown = webhook_on_shutdown,
    skip_updates = True,
    host = WEBAPP_HOST,
    port = WEBAPP_PORT,
  )
