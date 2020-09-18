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

### Personalidade padrão do @mate_obot

from matebot.aio_matebot.controllers.callbacks import (
  command_callback,
  message_callback,
)

async def start(message):
  return u"""Oi oi oi {first_name} {last_name}, me use, me use. O teu id no tel\
egram é {telegram_id}\n\nEu sou uma bot social com múltiplas personalidades pro\
gramada para aprender conforme o ambiente onde estou. Para saber quais comandos\
 estou respondendo, envie /lista\nPara mais informações sobre a minha atual per\
sonalidade, envie /info""".format(
    first_name = message.from_user.first_name,
    last_name = message.from_user.last_name,
    telegram_id = message.from_user.id,
  )

async def welcome(message):
  return u"""Bem vinda(o)(e){members} ao grupo {title}\n\nVerif\
ique a mensagem fixada (se houver) para saber o que está acontecendo e se quise\
r e puder, se apresente. Não parece, mas o pessoal daqui está genuinamente inte\
ressado em te ver escrevendo! Mas sem pressão, pode ser no teu tempo. Qualquer \
coisa, estou à disposição.""".format(
    members = 's' if len(message.new_chat_members) > 1 else ' ' + 
      ', '.join([
        ' '.join([member['first_name'] or '', member['last_name'] or ''])
        for member in message.new_chat_members
      ]),
    title = message.chat.title,
  )

async def info(infos):
  return u"""Eu sou uma MateBot com personalidade padrão configurada para respo\
nder os comandos básicos. O meu código fonte está em {repository} , Quem me adm\
inistra é {admin} , quem me desenvolve é {dev}\nSe quiser acompanhar meu proces\
so de desenvolvimento, tem um canal de notícias {channel}\nTambém tem um grupo \
do telegram onde mais gente interessada no meu desenvolvimento se encontra, o l\
ink de acesso {group}""".format(
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
