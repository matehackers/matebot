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
  types,
)

async def send_welcome(message: types.Message):
  """
  This handler will be called when user sends `/start` or `/help` command
  """
  await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

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

async def echo(message: types.Message):
  # old style:
  # await bot.send_message(message.chat.id, message.text)

  await message.answer(message.text)

def add_handlers(dispatcher: Dispatcher):
  dispatcher.register_message_handler(send_welcome, commands=['start', 'help'])
  dispatcher.register_message_handler(cats, regexp='(^cat[s]?$|puss)')
  dispatcher.register_message_handler(echo)
