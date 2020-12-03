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

from discord import (
  # ~ Client,
  TextChannel,
)

from discord.ext.commands import Bot

async def listar_canais(bot: Bot):
  logging.info(u"Lista de servidores onde estamos operando:")
  for guild in bot.guilds:
    logging.info(u"{0} ({1}). Webhooks: {2}".format(
      guild.name,
      guild.id,
      await guild.webhooks(),
    ))
  logging.info(u"Lista de canais de texto aos quais temos acesso:")
  for channel in bot.get_all_channels():
    if type(channel) is TextChannel:
      logging.info(u"{0} ({2}) do servidor {1} ({4}). Webhooks: {3}".format(
        channel.name,
        channel.guild.name,
        channel.id,
        await channel.webhooks(),
        channel.guild.id,
      ))

async def add_webhooks(bot: Bot):
  webhook_name = bot.config_name
  webhooks = list()
  for channel in bot.get_all_channels():
    if type(channel) is TextChannel:
      our_webhooks = [webhook for webhook in await channel.webhooks() if \
        webhook.name == webhook_name]
      if our_webhooks != []:
        logging.info(u"Acrescentado Webhook do canal {}...".format(
          channel.name))
        webhooks.append(our_webhooks[0])
      else:
        logging.info(u"Criando Webhook para canal {}...".format(channel.name))
        webhooks.append(await channel.create_webhook(name = webhook_name))
  logging.info(u"Lista de webhooks: {}".format([repr(webhook) for webhook \
    in webhooks]))
  setattr(bot, 'config_webhooks', webhooks)

def add_events(bot: Bot):
  @bot.listen('on_ready')
  async def start():
    # ~ await listar_canais(bot)
    await add_webhooks(bot)
    asyncio.get_event_loop().stop()

  @bot.listen('on_message')
  async def log(message):
    logging.info(u"""Mensagem de {author} no canal #{channel} do servidor {guil\
d}: {content}""".format(
        author = message.author or '',
        channel = message.channel or '',
        guild = message.guild or '',
        content = message.content or '',
      )
    )
