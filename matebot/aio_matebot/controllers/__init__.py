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

async def add_handlers(dispatcher: Dispatcher):
  from matebot.plugins import (
    telegram as plugin_telegram,
    admin as plugin_admin,
    feedback as plugin_feedback,
    archive as plugin_archive,
    qr as plugin_qr,
    donate as plugin_donate,
    hashes as plugin_hashes,
    mate_matica as plugin_matematica,
    tropixel as plugin_tropixel,
    ytdl as plugin_ytdl,
    welcome as plugin_welcome,
    personalidades as plugin_personalidades,
  )
  plugin_telegram.add_handlers(dispatcher)
  plugin_admin.add_handlers(dispatcher)
  plugin_feedback.add_handlers(dispatcher)
  plugin_archive.add_handlers(dispatcher)
  plugin_qr.add_handlers(dispatcher)
  plugin_donate.add_handlers(dispatcher)
  plugin_hashes.add_handlers(dispatcher)
  plugin_matematica.add_handlers(dispatcher)
  plugin_ytdl.add_handlers(dispatcher)
  await plugin_personalidades.add_handlers(dispatcher)
  try:
    plugin_tropixel.add_handlers(dispatcher)
  except KeyError:
    logging.warning(u"plugin tropixel não configurado")
  try:
    plugin_welcome.add_handlers(dispatcher)
  except KeyError:
    logging.warning(u"plugin welcome não configurado")

  ## Todas updates que não forem tratadas por handlers anteriores
  dispatcher.register_message_handler(
    any_message_callback,
    content_types = types.message.ContentType.ANY,
  )
  dispatcher.register_edited_message_handler(any_edited_message_callback)
  dispatcher.register_channel_post_handler(any_channel_post_callback)
  dispatcher.register_edited_channel_post_handler(any_edited_channel_post_callback)
  dispatcher.register_errors_handler(any_error_callback)
