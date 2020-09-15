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

def add_handlers(dispatcher):
  from aiogram import (
    filters,
    types,
  )
  from aiogram.utils.markdown import escape_md
  from matebot.aio_matebot.controllers.callbacks import (
    command_callback,
    message_callback,
  )
  from matebot.plugins.personalidades import (
    gerar_texto,
    gerar_comando,
  )

  ## Tropixel Café / Rede Metareciclagem
  ## Requer que personalidade do bot seja 'metarec'
  @dispatcher.message_handler(
    filters.IDFilter(
      chat_id = dispatcher.bot.users.get('tropixel', -1),
    ),
    content_types = types.ContentTypes.NEW_CHAT_MEMBERS,
  )
  async def welcome_metarec_callback(message: types.Message):
    await message_callback(message, ['welcome', 'metarec', message.chat.type])
    ## Mudar de personalidade temporariamente
    personalidade = dispatcher.bot.info['personalidade']
    dispatcher.bot.info.update(personalidade = 'metarec')
    text = await gerar_texto('welcome', dispatcher.bot, message)
    command = await message.reply(text)
    await command_callback(command, ['welcome', 'metarec', message.chat.type])
    dispatcher.bot.info.update(personalidade = personalidade)

  ## Padrão de boas vindas. Exclui grupos 'omega' pra evitar de mandar mensagem
  ## de boas vindas em grupos onde o bot só é utilizado com os comandos básicos.
  ## Requer que grupos que queiram ativar o plugin de boas vindas sejam
  ## adicionados pelo menos às listas 'delta' ou 'gama'.
  @dispatcher.message_handler(
    filters.IDFilter(
      chat_id = dispatcher.bot.users.get('delta', -1) +
        dispatcher.bot.users.get('gamma', -1),
    ),
    content_types = types.ContentTypes.NEW_CHAT_MEMBERS,
  )
  async def welcome_callback(message: types.Message):
    await message_callback(message, ['welcome', message.chat.type])
    text = await gerar_texto('welcome', dispatcher.bot, message)
    command = await message.reply(text)
    await command_callback(command, ['welcome', message.chat.type])
