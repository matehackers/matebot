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

import asyncio, logging

### Config
try:
  from instance.config import Config
  config = Config()
except Exception as e:
  print(u"""Arquivo de configuração não encontrado ou mal formado. Leia o manua\
l.\n{}""".format(str(e)))
  raise

### discord.py
## https://discord.com/developers/docs/intro
## https://discordpy.readthedocs.io/en/latest/
import discord
from discord import errors

### Discord MateBot
from matebot.discord_matebot import (
  # ~ models,
  # ~ views,
  controllers,
)
from matebot.discord_matebot.controllers.clients import (
  MateClient,
  MateBot,
)
from matebot.discord_matebot.controllers.events import (
  add_events,
  add_webhooks,
)

def app(bot_name):
  try:
    # ~ client = MateClient(config = config, name = bot_name)
    # ~ add_events(client)
    # ~ client.run(config.bots[bot_name]['token'] or '')
    bot = MateBot(command_prefix="!", config = config, name = bot_name)
    logging.info(u"Terminou a configuração do bot")
    # ~ loop = asyncio.get_event_loop()
    # ~ try:
      # ~ loop.run_forever(bot.start(config.bots[bot_name]['token'] or ''))
    # ~ except KeyboardInterrupt:
      # ~ pass
    # ~ finally:
      # ~ loop.run_until_complete(bot.logout())
      # ~ loop.close()
    bot.run(config.bots[bot_name]['discord']['token'] or '')
  except KeyError as exception:
    logging.warning(u"""Problema com o arquivo de configuração. Já lerdes o man\
ual? Fizerdes tudo certo? Se tiverdes certeza de que está tudo certo e não func\
iona, pede ajuda no Github, no Telegram, no Discord, enfim...\nChave que não fo\
i encontrada no arquivo de configuração: {}""".format(str(exception)))
  except Exception as exception:
    logging.warning(u"Deu Errado: {}".format(repr(exception)))
    raise
  try:
    webhooks = bot.config_webhooks
    pass
  except KeyboardInterrupt:
    logging.warning(u"Encerrando...")
  except Exception as exception:
    logging.warning(u"Deu Errado: {}".format(repr(exception)))
    raise


async def run(bot_name):
  try:
    bot = MateBot(command_prefix="!", config = config, name = bot_name)
    await bot.start(config.bots[bot_name]['discord']['token'] or '')
    # ~ loop = asyncio.get_event_loop()
    # ~ try:
      # ~ loop.run_forever(bot.start(config.bots[bot_name]['token'] or ''))
    # ~ except KeyboardInterrupt:
      # ~ pass
    # ~ finally:
      # ~ loop.run_until_complete(bot.logout())
      # ~ loop.close()
  except KeyError as e:
    logging.warning(u"""Problema com o arquivo de configuração. Já lerdes o man\
ual? Fizerdes tudo certo? Se tiverdes certeza de que está tudo certo e não func\
iona, pede ajuda no Github, no Telegram, no Discord, enfim...\nChave que não fo\
i encontrada no arquivo de configuração: {}""".format(str(e)))
  except Exception as e:
    logging.warning(u"Deu Errado: {}".format(repr(e)))
    raise
  try:
    webhooks = bot.config_webhooks
    logging.info(u"Webhooks do Discord: {}".format(['{} de {}'.format(
      webhook.channel, webhook.guild) for webhook in webhooks]))
  except Exception as exception:
    logging.warning(u"Deu Errado: {}".format(repr(exception)))
    raise
