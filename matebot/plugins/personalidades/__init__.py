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

from matebot.aio_matebot.controllers.callbacks import error_callback

from matebot.plugins.personalidades import (
  default,
  metarec,
  pave,
)

async def gerar_comando(command, bot, message):
  try:
    return await getattr(globals()[bot.info['personalidade']], command)(message)
  except Exception as e:
    await error_callback(['personalidades'], e)
    try:
      return await getattr(globals()['default'], command)(message)
    except Exception as e:
      ## Não deveria acontecer
      await error_callback(['personalidades', 'debug'], e)

async def gerar_texto(command, bot, message):
  try:
    return await getattr(globals()[bot.info['personalidade']], command)(message)
  except Exception as e:
    await error_callback(['personalidades'], e)
    try:
      return await getattr(globals()['default'], command)(message)
    except Exception as e:
      ## Não deveria acontecer
      await error_callback(['personalidades', 'debug'], e)

async def add_handlers(dispatcher):
  try:
    await getattr(globals()[
      dispatcher.bot.info['personalidade']], 'add_handlers')(dispatcher)
  except Exception as e:
    await error_callback(['personalidades'], e)
    await getattr(globals()['default'], 'add_handlers')(dispatcher)
