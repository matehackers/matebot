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

def add_handlers(dispatcher):
  from aiogram import (
    Dispatcher,
    filters,
  )  
  from matebot.aio_matebot.controllers.callbacks import command_callback

  ## Link para o Boteco Tropixel
  @dispatcher.message_handler(
    filters.IDFilter(
      chat_id = Dispatcher.get_current().bot.users['tropixel'],
    ),
    commands = ['boteco'],
  )
  async def tropixel_boteco_callback(message):
    command = await message.reply(
      u"Link para o boteco: {}".format(
        Dispatcher.get_current().bot.info['tropixel']['boteco'] or u"Não sei",
      ),
      disable_web_page_preview = True,
      disable_notification = True,
    )
    await command_callback(command, 'tropixelBoteco')

  ## Link para a Rede Tropixel
  @dispatcher.message_handler(
    filters.IDFilter(
      chat_id = Dispatcher.get_current().bot.users['tropixel'],
    ),
    commands = ['forum', 'rede', 'site', 'wiki'],
  )
  async def tropixel_site_callback(message):
    command = await message.reply(
      u"Link para o site/rede/forum/wiki: {}".format(
        Dispatcher.get_current().bot.info['tropixel']['site'] or u"Não sei",
      ),
      disable_web_page_preview = True,
      disable_notification = True,
    )
    await command_callback(command, 'tropixelSite')
