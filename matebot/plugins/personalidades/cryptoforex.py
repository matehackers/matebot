# vim:fileencoding=utf-8
#  Plugin personalidades para matebot: Robô também é gente?
#  Copyleft (C) 2020-2021 Iuri Guilherme, 2020-2021 Matehackers,
#   2020-2021 Fábrica do Futuro
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

### Personalidade investidora forex do @cryptoforexbot

from matebot.aio_matebot.controllers.callbacks import (
  command_callback,
  message_callback,
)

async def start(message):
  return u"""Oi oi oi {first_name} {last_name}, me use, me use. O teu id no te\
legram é {telegram_id}""".format(
    first_name = message.from_user.first_name,
    last_name = message.from_user.last_name,
    telegram_id = message.from_user.id,
  )

async def help(message):
  return u"""
Crypto Forex Bot help

This bot convert values in some cryptocurrencies to fiat/crypto currencies.



To see the price info for a cryptocurrency, use /price <coin>
Example: /price ETH



To convert values, use /conv <value> <from> <to>
Where <value> must be a valid real number (commas will be ignored);
<from> may be a coinmarketcap id or a cryptocurrency symbol;
<to> may be any fiat or cryptocurrency symbol supported by coinmarketcap;

Example: /conv 1 BTC USD

To see a list of available commands, type /lista
"""

async def welcome(message):
  return u"""Bem vinda(o) {members} ao grupo {title}\n\nVerifique a mensagem f\
ixada (se houver) para saber o que está acontecendo e quais são as regras do g\
rupo. Qualquer coisa, estou à disposição. Mas não acostuma que é de graça...\
""".format(
    members = 's' if len(message.new_chat_members) > 1 else ' ' + 
      ', '.join([
        ' '.join([member['first_name'] or '', member['last_name'] or ''])
        for member in message.new_chat_members
      ]),
    title = message.chat.title,
  )

async def info(infos):
  return u"""Eu sou uma MateBot com personalidade de investidora forex configu\
rada para converter valores de criptomoedas, entre outros comandos relacionado\
s ao criptomercado. O meu código fonte está em {repository} , Quem me administ\
ra é {admin} , quem me desenvolve é {dev}\nSe quiser acompanhar meu processo d\
e desenvolvimento, tem um canal de notícias {channel}\nTambém tem um grupo do \
telegram onde mais gente interessada no meu desenvolvimento se encontra, o lin\
k de acesso {group}""".format(
    repository = infos.get('repository', u"algum lugar"),
    admin = infos.get('admin', u"Ninguém"),
    dev = infos.get('dev', u"Alguém"),
    channel = infos.get('channel', u"que eu não sei."),
    group = infos.get('group', u"eu não sei."),
  )

async def add_handlers(dispatcher):
  ## Comando /info padrão
  @dispatcher.message_handler(
    commands = ['info'],
  )
  async def info_callback(message):
    await message_callback(message, ['info', message.chat.type])
    command = await message.reply(await info(dispatcher.bot.info))
    await command_callback(command, ['info', message.chat.type])
