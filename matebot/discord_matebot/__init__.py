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

import logging

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

### Discord MateBot
from matebot.discord_matebot import (
  # ~ models,
  # ~ views,
  controllers,
)
from matebot.discord_matebot.controllers.client import MateClient
from matebot.discord_matebot.controllers.events import add_events

def app(bot_name):
  try:
    client = MateClient(config = config, name = bot_name)
    add_events(client)
    client.run(config.bots[bot_name]['token'] or '')
  except KeyError as exception:
    logging.warning(u"""Problema com o arquivo de configuração. Já lerdes o man\
ual? Fizerdes tudo certo? Se tiverdes certeza de que está tudo certo e não func\
iona, pede ajuda no Github, no Telegram, no Discord, enfim...\nChave que não fo\
i encontrada no arquivo de configuração: {}""".format(str(exception)))
  except Exception as exception:
    logging.warning(u"Deu Errado: {}".format(repr(exception)))
