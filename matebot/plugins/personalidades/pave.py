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
