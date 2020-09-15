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
  Dispatcher,
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
  ## Plugins gerais
  plugin_archive.add_handlers(dispatcher)
  plugin_hashes.add_handlers(dispatcher)
  plugin_matematica.add_handlers(dispatcher)
  plugin_qr.add_handlers(dispatcher)
  plugin_ytdl.add_handlers(dispatcher)
  ## Plugins especiais
  if dispatcher.bot.info.get('personalidade') in ['default', 'metarec', 'pave']:
    plugin_donate.add_handlers(dispatcher)
  plugin_feedback.add_handlers(dispatcher)
  plugin_admin.add_handlers(dispatcher)
  ## Plugins mais que especiais
  if dispatcher.bot.info.get('personalidade') in ['default', 'metarec']:
    try:
      plugin_tropixel.add_handlers(dispatcher)
    except KeyError:
      logging.warning(u"plugin tropixel não configurado")
  try:
    plugin_welcome.add_handlers(dispatcher)
  except KeyError:
    logging.warning(u"plugin welcome não configurado")
  plugin_default.add_handlers(dispatcher)
  ## Plugins de personalidades
  await plugin_personalidades.add_handlers(dispatcher)
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

async def on_startup(dispatcher: Dispatcher):
  await add_filters(dispatcher)
  await add_handlers(dispatcher)
