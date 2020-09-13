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

### Personalidade metarec https://metareciclagem.github.io/

async def welcome(message):
  return u"""Bem vinde{members}!\n\nSe você quer ser desconstruíde e \
re-construíde, ter suas idéias modificadas, reificadas, pisoteadas e amadas, se\
 seu ego é grande o suficiente para ter amor ao que faz mas consegue reconhecer\
 o que os outros fazem sem inveja, se não está aqui buscando promoção social, m\
érito ou grana, e se, acima de tudo, acredita em fadas, duendes e um mundo perf\
eito, seja bem-vinde a {title}.\n\nUma rede onde maluques conversam, jogam bola\
, mandam emails, discutem e fazem as pazes, filosofam sobre vida e morte, colab\
oração, apropriação de tecnologia, como as coisas são por dentro, de onde viemo\
s e para onde vamos.\n\nAviso de utilidade pública: Não nos responsabilizamos p\
elas modificações causadas nos seus neurônios após o convívio (prolongado ou nã\
o) com esta comunidade. Use com moderação.\n\nSe apesar de todos esses avisos v\
ocê ainda está à procura de pessoas que fazem parte dessa rede, nós nos encontr\
amos aos sábados no Boteco Tropixel (use o comando /boteco pra pegar o link), e\
 fora do tempo no site/forum/rede Tropixel (use o comando /rede pra pegar o lin\
k).""".format(
    members = 's' if len(message.new_chat_members) > 1 else ' ' + 
      ', '.join([
        ' '.join([member['first_name'] or '', member['last_name'] or ''])
        for member in message.new_chat_members
      ]),
    title = message.chat.title,
  )

async def add_handlers(dispatcher):
  pass
