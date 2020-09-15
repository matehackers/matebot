# vim:fileencoding=utf-8
#  Plugin tropixel para matebot: Comandos para o Tropixel Café @tropixelcafe
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

async def add_handlers(dispatcher):
  from aiogram import (
    filters,
    types,
  )  
  from matebot.aio_matebot.controllers.callbacks import (
    command_callback,
    message_callback,
  )
  from matebot.plugins.personalidades import (
    gerar_texto,
  )

  ## Tropixel Café / Rede Metareciclagem
  @dispatcher.message_handler(
    filters.IDFilter(
      chat_id = dispatcher.bot.users.get('tropixel', -1),
    ),
    content_types = types.ContentTypes.NEW_CHAT_MEMBERS,
  )
  async def welcome_tropixel_callback(message: types.Message):
    await message_callback(message, ['welcome', 'tropixel', message.chat.type])
    text = await gerar_texto('tropixel', dispatcher.bot, message)
    command = await message.reply(text)
    await command_callback(command, ['welcome', 'tropixel', message.chat.type])

  ## Link para o Boteco Tropixel
  @dispatcher.message_handler(
    filters.IDFilter(
      chat_id = dispatcher.bot.users.get('tropixel', -1),
    ),
    commands = ['boteco'],
  )
  async def tropixel_boteco_callback(message):
    await message_callback(message, ['tropixel', 'boteco', message.chat.type])
    command = await message.reply(
      u"Link para o boteco: {}".format(
        dispatcher.bot.info.get(
          'tropixel', dict(boteco = u"Não sei"),
        ).get('boteco', u"Não sei"),
      ),
      disable_web_page_preview = True,
      disable_notification = True,
    )
    await command_callback(command, ['tropixel', 'boteco', message.chat.type])

  ## Link para a Rede Tropixel
  @dispatcher.message_handler(
    filters.IDFilter(
      chat_id = dispatcher.bot.users.get('tropixel', -1),
    ),
    commands = ['forum', 'rede', 'site', 'wiki'],
  )
  async def tropixel_site_callback(message):
    await message_callback(message, ['tropixel', 'site', message.chat.type])
    command = await message.reply(
      u"Link para o site/rede/forum/wiki: {}".format(
          dispatcher.bot.info.get(
          'tropixel', dict(site = u"Não sei"),
        ).get('site', u"Não sei"),
      ),
      disable_web_page_preview = True,
      disable_notification = True,
    )
    await command_callback(command, ['tropixel', 'site', message.chat.type])
