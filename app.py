#!/usr/bin/env python
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
## Do jeito mais difícil para o mais fácil:
##  1) ./start.py
##  2) python3 start.py
##  3) pipenv run start.py aiogram matebot
##  4) pipenv run matebot
##  5) Ler o README.md ;)

import asyncio, logging, subprocess, sys

### Logging
logging.basicConfig(level=logging.INFO)
# ~ logging.basicConfig(level=logging.DEBUG)

try:
  from matebot import aio_matebot as telegram_bot
except Exception as e:
  telegram_bot = None
  logging.debug(repr(e))

try:
  from matebot import discord_matebot as discord_bot
except Exception as e:
  discord_bot = None
  logging.debug(repr(e))

try:
  from matebot.ptb_matebot import app as flask_bot
except Exception as e:
  flask_bot = None
  logging.debug(repr(e))

try:
  from matebot.tp_matebot import bot as telepot_bot
except Exception as e:
  telepot_bot = None
  logging.debug(repr(e))

async def bouncer(bot):
  ## FIXME
  try:
    asyncio.gather(
      telegram_bot.arun(bot),
      discord_bot.run(bot),
    )
  except KeyboardInterrupt:
    logging.info(u"Encerrando...")
  except Exception as e:
    logging.debug(u"Deu errado: {}".format(repr(e)))
    raise
  finally:
    logging.info(u"Terminou o loop do bouncer")

if __name__ == "__main__":
  mode = 'bouncer'
  bot = 'matebot'
  port = 5000
  ## TODO fazer validação de verdade
  if len(sys.argv) > 1:
    mode = sys.argv[1]
    logging.info(u"Modo de operação: {}".format(str(mode)))
    if len(sys.argv) > 2:
      bot = sys.argv[2]
      logging.info(u"""Usando token do bot "{}" do arquivo de configuração.\
""".format(bot))
      if len(sys.argv) > 3:
        port = sys.argv[3]
        logging.info(u"Alterando porta para {}".format(port))
      else:
        logging.info(u"Porta não informada, usando padrão {}".format(port))
    else:
      logging.warning(u"Nome do bot não informado, {} presumido".format(bot))
  else:
    logging.warning(u"""Modo de operação não informado, {} presumido.\
""".format(mode))
    logging.warning(u"Nome do bot não informado, {} presumido".format(bot))
  if mode == 'bouncer':
    ## FIXME
    # ~ asyncio.run(bouncer(bot))
    logging.warning(u"Bouncer não está funcionando, revertendo para aiogram")
    telegram_bot.run(bot)
  elif mode == 'aiogram':
    telegram_bot.run(bot)
  elif mode == 'discord':
    discord_bot.app(bot)
  elif mode == 'flask':
    flask_bot.run(port=port)
  elif mode == 'telepot':
    telepot_bot(mode, bot)
  else:
    logging.warning(u"""Não entendi nada, não consegui iniciar. Leia o manual p\
or favor.""")
