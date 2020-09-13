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

async def start(message):
  return u"""Oi oi oi {first_name} {last_name}, me use, me use. O teu id no te\
legram é {telegram_id}""".format(
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
    members = 's' if len(message.new_chat_members) > 1 else '' + 
      ', '.join([
        ' '.join([member['first_name'] or '', member['last_name'] or ''])
        for member in message.new_chat_members
      ]),
    title = message.chat.title,
  )

async def add_handlers(dispatcher):
  pass
