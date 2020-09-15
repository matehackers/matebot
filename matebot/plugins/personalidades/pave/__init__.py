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

### Personalidade do Tiozão do Pavê @tiozao_bot

from aiogram import (
  Dispatcher,
  filters,
)

from matebot.aio_matebot.controllers.callbacks import (
  command_callback,
  message_callback,
)

## TODO Sentenças impróprias para publicar no Github por razões diversas
try:
  from instance import random_texts_pave as random_texts
except:
  from matebot.plugins.personalidades.pave import random_texts

async def start(message):
  return random_texts.start(message)

async def welcome(message):
  bot = Dispatcher.get_current().bot
  admin = message.from_user.first_name
  if message.chat.type in ['group', 'supergroup']:
    admin = [member.user for member in await bot.get_chat_administrators(
      message.chat.id) if member.status == 'creator'][0].first_name or u"@admin"
  return random_texts.welcome(message, bot, admin)

async def info():
  return u"""Eu sou um bot com personalidade de tiozão do pavê (termo moderno p\
oliticamente correto: "humor boomer") configurado e desenvolvido para ser imper\
tinente, sarcástico, ignorante, agressivo e sem noção. A tua opinião em relação\
 à minha atitude influencia no meu comportamento que nunca vai ser pra te agrad\
ar. Para enviar sugestões ou relatar problemas para o pessoal que faz manutençã\
o, use o comando /feedback por exemplo /feedback Obrigado pelo bot!"""

## Pegadinha
async def pegadinha1(message):
  return await message.reply_photo(open('files/pegadinha1.jpg', 'rb'))
async def pegadinha2(message):
  return await message.reply_photo(open('files/pegadinha2.png', 'rb'))
async def pegadinha3(message):
  return await message.reply_animation(open('files/pegadinha3.mp4', 'rb'))
async def pegadinha4(message):
  bot = Dispatcher.get_current().bot
  return await message.reply(
    u"é {}, pa pa pa".format(bot.get_chat_members_count(message.chat.id)),
  )
async def pegadinha(message):
  return await random.choice([
    pegadinha1,
    pegadinha2,
    pegadinha3,
    pegadinha4,
  ])(message)

async def add_handlers(dispatcher):
  ## Piadas sem graça
  # ~ @dispatcher.message_handler(
    # ~ commands = ['piada'],
  # ~ )
  # ~ async def piada_callback(message):
    # ~ await message_callback(message, ['piada',
      # ~ dispatcher.bot.get('personalidade', 'pave'), message.chat.type])
    # ~ command = await message.reply(random_texts.piadas())
    # ~ await command_callback(command, ['piada',
      # ~ dispatcher.bot.get('personalidade', 'pave'), message.chat.type])

  ## Versículos bíblicos fora de contexto
  @dispatcher.message_handler(
    commands = ['versiculo'],
  )
  async def versiculo_callback(message):
    await message_callback(message, ['versiculo', message.chat.type])
    command = await message.reply(
      random_texts.versiculos_md(),
      parse_mode = "MarkdownV2",
    )
    await command_callback(command, ['versiculo', message.chat.type])

  ## /info
  @dispatcher.message_handler(
    commands = ['info'],
  )
  async def info_callback(message):
    await message_callback(
      message,
      ['info', dispatcher.bot.get('personalidade', 'pave'), message.chat.type],
    )
    command = await message.reply(await info())
    await command_callback(
      command,
      ['info', dispatcher.bot.get('personalidade', 'pave'), message.chat.type],
    )

  ## Responde toda referência a bebidas
  @dispatcher.message_handler(
    filters.Regexp('({})'.format('|'.join(random_texts.bebidas()))),
  )
  async def resposta_bebida_callback(message):
    await message_callback(message, ['resposta', 'bebida', message.chat.type])
    command = await message.reply(random_texts.respostas_bebida())
    await command_callback(command, ['resposta', 'bebida', message.chat.type])

  ## Responde mensagens que são respostas a mensagens deste bot
  ## Reponde com patada
  @dispatcher.message_handler(is_reply_to_id = dispatcher.bot.id)
  async def resposta_ignorante_callback(message):
    await message_callback(
      message,
      ['resposta', 'ignorante', message.chat.type],
    )
    admin = message.from_user.first_name
    if message.chat.type in ['group', 'supergroup']:
      admin = [member.user for member in \
        await dispatcher.bot.get_chat_administrators(
        message.chat.id) if member.status == 'creator'][0].first_name \
        or u"@admin"
    command = await message.reply(random_texts.respostas_ignorante(admin))
    await command_callback(command, ['resposta' 'ignorante', message.chat.type])
