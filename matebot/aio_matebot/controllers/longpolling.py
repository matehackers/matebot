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
  executor,
  types,
  filters,
)
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import (
  Executor,
  start_webhook,
)
from matebot.aio_matebot.controllers import (
  add_filters,
  add_handlers,
)

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

def run_polling(dispatcher: Dispatcher):
  executor.start_polling(
    dispatcher,
    on_startup = polling_on_startup,
    on_shutdown = polling_on_shutdown,
  )
