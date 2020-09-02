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

from aiogram import (
  exceptions,
  types,
)

from matebot.aio_matebot import (
  bot,
  config,
)

async def update_logger(
  message: types.Message,
  update_type: str = 'none',
):
  url = ''
  if message.chat.type in ['group', 'supergroup', 'channel']:
    url = message.url
  text = list()
  text.append(u"#{u_type} {url}".format(u_type = update_type, url = url))
  text.append('')
  text.append(str(message))
  await bot.send_message(
    config.groups['admin']['caos'],
    '\n'.join(text),
    disable_notification = True,
  )

async def debug_logger(
  message: types.Message,
  error: str = 'None',
  exception: str = 'None',
):
  url = ''
  if message.chat.type in ['group', 'supergroup', 'channel']:
    url = message.url
  text = list()
  text.append(u"#{error} {url}".format(error = error, url = url))
  text.append('')
  text.append(str(message))
  text.append('')
  text.append(exception)
  await bot.send_message(
    config.groups['admin']['debug'],
    '\n'.join(text),
    disable_notification = True,
  )

async def send_message(
  chat_id: int,
  text: str,
  parse_mode: str = None,
  disable_web_page_preview: bool = True,
  disable_notification: bool = True,
  reply_to_message_id: int = None,
  reply_markup = None,
):
  try:
    await bot.send_message(
      chat_id = chat_id,
      text = text,
      disable_notification = disable_notification,
      reply_to_message_id = reply_to_message_id,
      reply_markup = reply_markup,
    )
  except exceptions.BotBlocked:
    await debug_logger(
      message,
      'BotBlocked',
      None,
    )
  except exceptions.ChatNotFound:
    await debug_logger(
      message,
      'ChatNotFound',
      None,
    )
  except exceptions.RetryAfter as e:
    await asyncio.sleep(e.timeout)
    return await send_message(user_id, text)  # Recursive call
    await debug_logger(
      message,
      'RetryAfter',
      str(e),
    )
  except exceptions.UserDeactivated:
    await debug_logger(
      message,
      'UserDeactivated',
      None,
    )
  except exceptions.TelegramAPIError:
    await debug_logger(
      message,
      'TelegramAPIError',
      None,
    )
  except Exception as e:
    await debug_logger(
      message,
      'NotTelegram',
      str(e),
    )

async def any_message_callback(message: types.Message):
  await update_logger(message, 'message')

async def any_edited_message_callback(message: types.Message):
  await update_logger(message, 'edited_message')

async def any_channel_post_callback(message: types.Message):
  await update_logger(message, 'channel_post')

async def any_edited_channel_post_callback(message: types.Message):
  await update_logger(message, 'edited_channel_post')

async def any_error_callback(message: types.Message):
  await debug_logger(message, 'error')
