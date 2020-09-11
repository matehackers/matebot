# vim:fileencoding=utf-8
#  Plugin welcome para matebot: Boas vindas a pessoas que entram em grupos
#  Copyleft (C) 2020 Iuri Guilherme, 2020 Matehackers
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random

async def pegadinha1(message):
  return await message.reply_photo(open('files/pegadinha1.jpg', 'rb'))

async def pegadinha2(message):
  return await message.reply_photo(open('files/pegadinha2.png', 'rb'))

async def pegadinha3(message):
  return await message.reply_animation(open('files/pegadinha3.mp4', 'rb'))

def add_handlers(dispatcher):
  from matebot.aio_matebot.controllers.callbacks import (
    command_callback,
    error_callback,
  )
  from aiogram import types
  from aiogram.utils.markdown import escape_md

  ## Saúda com trollada
  @dispatcher.message_handler(
    content_types=types.ContentTypes.NEW_CHAT_MEMBERS,
  )
  async def pegadinha_callback(message):
    command = await random.choice([
      # ~ pegadinha1,
      # ~ pegadinha2,
      pegadinha3,
    ])(message)
    await command_callback(command, 'pegadinha')
