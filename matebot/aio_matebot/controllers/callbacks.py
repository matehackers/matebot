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

from aiogram import (
  Dispatcher,
  exceptions,
  types,
)

from matebot.aio_matebot import (
  config,
)

from matebot.plugins.log import (
  debug_logger,
  exception_logger,
  info_logger,
)

async def message_callback(
  message: types.Message,
  descriptions: list = ['message'],
):
  await info_logger(message, descriptions)

async def command_callback(
  message: types.Message,
  descriptions: list = ['command'],
):
  await info_logger(message, ['command'] + descriptions)

async def error_callback(
  message: types.Message,
  exception: Exception = None,
  descriptions: list = ['error'],
):
  await debug_logger(message, exception, descriptions)

async def exception_callback(
  exception: Exception = None,
  descriptions: list = ['error'],
):
  await exception_logger(exception, descriptions)

async def any_message_callback(message: types.Message):
  await info_logger(
    message,
    ['message', message.content_type, message.chat.type],
  )

async def any_edited_message_callback(message: types.Message):
  await info_logger(message, ['edited_message', message.chat.type])

async def any_channel_post_callback(message: types.Message):
  await info_logger(message, ['channel_post'])

async def any_edited_channel_post_callback(message: types.Message):
  await info_logger(message, ['edited_channel_post'],)

async def any_update_callback(update):
  await info_logger(update, ['update'])

async def any_error_callback(update, error):
  if update:
    await debug_logger(update, error, ['error', 'unhandled'])
  else:
    await exception_logger(error, ['error', 'unhandled'])
