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

import asyncio, logging

from aiogram import (
  Bot,
  exceptions,
  types,
)

from matebot.aio_matebot.controllers.callbacks import (
  exception_callback,
)

## TODO Tratar todas as exceções
## https://github.com/aiogram/aiogram/blob/dev-2.x/aiogram/utils/exceptions.py

## TODO Tratar todos métodos que enviam types.Message
## https://github.com/aiogram/aiogram/blob/dev-2.x/aiogram/bot/bot.py

class MateBot(Bot):
  def __init__(self, *args, **kwargs):
    ## Tratando as configurações
    config = kwargs.get('config')
    name = kwargs.get('name', 'matebot')
    setattr(self, 'info',
      config.bots[name]['info'] or config.default_bot['info'])
    setattr(self, 'plugins',
      config.bots[name]['plugins'] or config.default_bot['plugins'])
    setattr(self, 'users',
      config.bots[name]['users'] or config.default_bot['users'])
    kwargs.pop('config', None)
    kwargs.pop('name', None)
    super().__init__(*args, **kwargs)

  async def send_message(self, *args, **kwargs):
    try:
      return await super().send_message(*args, **kwargs)
    except exceptions.RetryAfter as exception:
      logging.warning(u"Flood control: Aguardando {} segundos...".format(
        exception.timeout))
      await asyncio.sleep(exception.timeout)
      return await self.send_message(*args, **kwargs)
    except exceptions.BotBlocked as exception:
      await exception_callback(
        exception,
        ['sendMessage', 'BotBlocked'],
      )
    except exceptions.ChatNotFound as exception:
      await exception_callback(
        exception,
        ['sendMessage', 'ChatNotFound'],
      )
      message = kwargs.get('message')
    except exceptions.UserDeactivated as exception:
      await exception_callback(
        exception,
        ['sendMessage', 'UserDeactivated'],
      )
      message = kwargs.get('message')
    except exceptions.TelegramAPIError as exception:
      await exception_callback(
        exception,
        ['sendMessage', 'TelegramAPIError'],
      )
      message = kwargs.get('message')
    except exceptions.TerminatedByOtherGetUpdates as exception:
      logging.warning(repr(exception))
    except Exception as exception:
      await exception_callback(
        exception,
        ['sendMessage', 'NotTelegram'],
      )
    return None

  async def send_photo(self, *args, **kwargs):
    try:
      return await super().send_photo(*args, **kwargs)
    except exceptions.RetryAfter as exception:
      logging.warning(u"Flood control: Aguardando {} segundos...".format(
        exception.timeout))
      await asyncio.sleep(exception.timeout)
      return await self.send_photo(*args, **kwargs)
    except exceptions.BotBlocked as exception:
      await exception_callback(
        exception,
        ['sendPhoto', 'BotBlocked'],
      )
    except exceptions.ChatNotFound as exception:
      await exception_callback(
        exception,
        ['sendPhoto', 'ChatNotFound'],
      )
      message = kwargs.get('message')
    except exceptions.UserDeactivated as exception:
      await exception_callback(
        exception,
        ['sendPhoto', 'UserDeactivated'],
      )
      message = kwargs.get('message')
    except exceptions.TelegramAPIError as exception:
      await exception_callback(
        exception,
        ['sendPhoto', 'TelegramAPIError'],
      )
      message = kwargs.get('message')
    except exceptions.TerminatedByOtherGetUpdates as exception:
      logging.warning(repr(exception))
    except Exception as exception:
      await exception_callback(
        exception,
        ['sendPhoto', 'NotTelegram'],
      )
    return None

  async def send_video(self, *args, **kwargs):
    try:
      return await super().send_video(*args, **kwargs)
    except exceptions.RetryAfter as exception:
      logging.warning(u"Flood control: Aguardando {} segundos...".format(
        exception.timeout))
      await asyncio.sleep(exception.timeout)
      return await self.send_video(*args, **kwargs)
    except exceptions.BotBlocked as exception:
      await exception_callback(
        exception,
        ['sendVideo', 'BotBlocked'],
      )
    except exceptions.ChatNotFound as exception:
      await exception_callback(
        exception,
        ['sendVideo', 'ChatNotFound'],
      )
      message = kwargs.get('message')
    except exceptions.UserDeactivated as exception:
      await exception_callback(
        exception,
        ['sendVideo', 'UserDeactivated'],
      )
      message = kwargs.get('message')
    except exceptions.TelegramAPIError as exception:
      await exception_callback(
        exception,
        ['sendVideo', 'TelegramAPIError'],
      )
      message = kwargs.get('message')
    except exceptions.TerminatedByOtherGetUpdates as exception:
      logging.warning(repr(exception))
    except Exception as exception:
      await exception_callback(
        exception,
        ['sendVideo', 'NotTelegram'],
      )
    return None

  async def send_animation(self, *args, **kwargs):
    try:
      return await super().send_animation(*args, **kwargs)
    except exceptions.RetryAfter as exception:
      logging.warning(u"Flood control: Aguardando {} segundos...".format(
        exception.timeout))
      await asyncio.sleep(exception.timeout)
      return await self.send_message(*args, **kwargs)
    except exceptions.BotBlocked as exception:
      await exception_callback(
        exception,
        ['sendAnimation', 'BotBlocked'],
      )
    except exceptions.ChatNotFound as exception:
      await exception_callback(
        exception,
        ['sendAnimation', 'ChatNotFound'],
      )
      message = kwargs.get('message')
    except exceptions.UserDeactivated as exception:
      await exception_callback(
        exception,
        ['sendAnimation', 'UserDeactivated'],
      )
      message = kwargs.get('message')
    except exceptions.TelegramAPIError as exception:
      await exception_callback(
        exception,
        ['sendAnimation', 'TelegramAPIError'],
      )
      message = kwargs.get('message')
    except exceptions.TerminatedByOtherGetUpdates as exception:
      logging.warning(repr(exception))
    except Exception as exception:
      await exception_callback(
        exception,
        ['sendAnimation', 'NotTelegram'],
      )
    return None
