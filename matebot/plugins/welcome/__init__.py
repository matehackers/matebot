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
  from matebot.aio_matebot.controllers.callbacks import command_callback
  from matebot.plugins.personalidades import gerar_texto

  ## Tropixel Café / Rede Metareciclagem
  @dispatcher.message_handler(
    filters.IDFilter(
      chat_id = dispatcher.bot.users['tropixel'],
    ),
    content_types = types.ContentTypes.NEW_CHAT_MEMBERS,
  )
  async def metarec_callback(message: types.Message):
    ## Mudar de personalidade temporariamente
    personalidade = dispatcher.bot.info['personalidade']
    dispatcher.bot.info.update(personalidade = 'metarec')
    text = await gerar_texto('welcome', dispatcher.bot, message)
    command = await message.reply(text)
    await command_callback(command, 'welcome')
    dispatcher.bot.info.update(personalidade = personalidade)

  ## Saúda com trollada
  ## Requer que personalidade do bot seja 'pave'
  @dispatcher.message_handler(
    filters.IDFilter(
      ## Somente grupos configurados pra receber novas pessoas com pegadinha
      chat_id = dispatcher.bot.users['pegadinha'],
    ),
    content_types = types.ContentTypes.NEW_CHAT_MEMBERS,
  )
  async def pegadinha_callback(message: types.Message):
    ## Mudar de personalidade temporariamente
    personalidade = dispatcher.bot.info['personalidade']
    dispatcher.bot.info.update(personalidade = 'pave')
    text = await gerar_texto('pegadinha', dispatcher.bot, message)
    command = await message.reply(text)
    await command_callback(command, 'pegadinha')
    dispatcher.bot.info.update(personalidade = personalidade)

  ## Padrão de boas vindas. Exclui grupos 'omega' pra evitar de mandar mensagem
  ## de boas vindas em grupos onde o bot só é utilizado com os comandos básicos.
  ## Requer que grupos que queiram ativar o plugin de boas vindas sejam
  ## adicionados pelo menos à lista 'epsilon'.
  @dispatcher.message_handler(
    filters.IDFilter(
      chat_id = dispatcher.bot.users['epsilon'] + 
        dispatcher.bot.users['delta'] + dispatcher.bot.users['gamma'],
    ),
    content_types = types.ContentTypes.NEW_CHAT_MEMBERS,
  )
  async def welcome_callback(message: types.Message):
    text = await gerar_texto('welcome', dispatcher.bot, message)
    command = await message.reply(text)
    await command_callback(command, 'welcome')
