# vim:fileencoding=utf-8
#  Plugin personalidades para matebot: Robô também é gente?
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

from aiogram import types

from matebot.aio_matebot.controllers.callbacks import (
  error_callback,
  exception_callback,
)

from matebot.plugins.personalidades import (
  default,
  metarec,
  pave,
  pacume,
)

async def gerar_comando(command, bot, message):
  try:
    return await getattr(
      globals()[bot.info.get('personalidade', 'default')], command)(message)
  except Exception as exception:
    await error_callback(message, exception, ['personalidades',
      bot.info.get('personalidade', 'default'), 'gerarComando'])
    try:
      return await getattr(globals()['default'], command)(message)
    except Exception as exception:
      ## Não deveria acontecer
      await error_callback(message, exception, ['personalidades',
        bot.info.get('personalidade', 'default'), 'gerarComando', 'debug'])
      return ''

async def gerar_texto(command, bot, message):
  try:
    return await getattr(globals()[bot.info.get('personalidade', 'default')],
      command)(message)
  except Exception as exception:
    await error_callback(message, exception, ['personalidades',
      bot.info.get('personalidade', 'default'), 'gerarTexto'])
    try:
      return await getattr(globals()['default'], command)(message)
    except Exception as exception:
      ## Não deveria acontecer
      await error_callback(message, exception, ['personalidades',
        bot.info.get('personalidade', 'default'), 'gerarTexto', 'debug'])
      return ''

async def add_handlers(dispatcher):
  try:
    await getattr(globals()[dispatcher.bot.info.get('personalidade',
      'default')], 'add_handlers')(dispatcher)
  except Exception as exception:
    await exception_callback(exception, ['personalidades', 'add_handlers'])
    await getattr(globals()['default'], 'add_handlers')(dispatcher)
