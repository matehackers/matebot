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

import random

async def start(message):
  return random.choice([
    u"putz! quem é que te deu o meu contato? tô fudido",
    u"fala{}".format(random.choice([
      u"",
      u", bagual",
      u", chê",
      u", tchê",
      u" duma vez",
      u" porra",
    ])),
    u"tu respira tu e aperta {}? tu é o bichão mesmo".format(
      message.get_command(),
    ),
    u"""viu, todo mundo tá de prova que quem veio puxar assunto foi tu. depois \
não vem de mimimi""",
  ])

## Pegadinha
async def pegadinha1(message):
  return await message.reply_photo(open('files/pegadinha1.jpg', 'rb'))
async def pegadinha2(message):
  return await message.reply_photo(open('files/pegadinha2.png', 'rb'))
async def pegadinha3(message):
  return await message.reply_animation(open('files/pegadinha3.mp4', 'rb'))
async def pegadinha(message):
  return await random.choice([
    pegadinha1,
    pegadinha2,
    pegadinha3,
  ])(message)

async def add_handlers(dispatcher):
  ## Bebida
  bebidas = [
    u"bebida",
    u"bira",
    u"cachaça",
    u"cerveja",
    u"ceva",
    u"trago",
    u"vinho",
  ]
  @dispatcher.message_handler(regexp=r'(?i)\b({})\b'.format('|'.join(bebidas)))
  async def bebida(message):
    resposta = random.choice([
      u"quem é que vai pagar?",
      u"tu que bota?",
      u"agora sim falou o que interessa",
      u"pudim de trago",
    ])
    await message.reply(resposta)
