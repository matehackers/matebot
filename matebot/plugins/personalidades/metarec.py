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

from matebot.plugins.personalidades.default import info

### Personalidade metarec https://metareciclagem.github.io/

async def welcome(message):
  return u"""Bem vinde{members}!\n\nSe você quer ser desconstruíde e re-constru\
íde, ter suas idéias modificadas, reificadas, pisoteadas e amadas, se seu ego é\
 grande o suficiente para ter amor ao que faz mas consegue reconhecer o que os \
outros fazem sem inveja, se não está aqui buscando promoção social, mérito ou g\
rana, e se, acima de tudo, acredita em fadas, duendes e um mundo perfeito, seja\
 bem-vinde a {title}.\n\nUma rede onde maluques conversam, jogam bola, mandam e\
mails, discutem e fazem as pazes, filosofam sobre vida e morte, colaboração, ap\
ropriação de tecnologia, como as coisas são por dentro, de onde viemos e para o\
nde vamos.\n\nAviso de utilidade pública: Não nos responsabilizamos pelas modif\
icações causadas nos seus neurônios após o convívio (prolongado ou não) com est\
a comunidade. Use com moderação.\n\nSe apesar de todos esses avisos você ainda \
está à procura de pessoas que fazem parte dessa rede, nós nos encontramos aos s\
ábados no Boteco Tropixel (use o comando /boteco pra pegar o link), e fora do t\
empo no site/forum/rede Tropixel (use o comando /rede pra pegar o link).\
""".format(
    members = 's' if len(message.new_chat_members) > 1 else ' ' + 
      ', '.join([
        ' '.join([member['first_name'] or '', member['last_name'] or ''])
        for member in message.new_chat_members
      ]),
    title = message.chat.title,
  )

async def add_handlers(dispatcher):
  ## Comando /info herdado da personalidade padrão
  @dispatcher.message_handler(
    commands = ['info'],
  )
  async def info_callback(message):
    await message_callback(message, ['info', message.chat.type])
    command = await message.reply(info(message, dispatcher.bot.info))
    await command_callback(command, ['info', message.chat.type])
