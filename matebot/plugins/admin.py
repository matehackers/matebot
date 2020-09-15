# vim:fileencoding=utf-8
#  Plugin admin para matebot: Plugin para administração e testes
#  Copyleft (C) 2018-2020 Iuri, 2018-2020 Matehackers,
#     2018-2019 Velivery, 2019 Greatful, 2019-2020 Fábrica do Futuro
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

### Telepot
import datetime, pytz
from matebot.plugins.log import log_str

def cmd_teste(args):
  return {
    'status': True,
    'type': 'mensagem',
    'response': str(args['command_list']),
    'debug': u'teste',
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## TODO acentuacao
## Enviar mensagem para alguém
def cmd_enviar(args):
  response = u"Enviar o que?"
  debug = u"Nada para enviar"
  try:
    if len(args['command_list']) > 1:
      if args['command_list'][0].lstrip('-').isdigit():
        telegram_id = args['command_list'][0]
        mensagem = ' '.join(args['command_list'][1::1])
        return {
          'status': True,
          'type': "whisper",
          'response': mensagem,
          'to_id': telegram_id,
          'debug': u"Sucesso enviando %s para %s" % (mensagem, telegram_id),
          'multi': False,
          'parse_mode': 'Markdown',
          'reply_to_message_id': args['message_id'],
        }
    response = u"Vossa Excelência está usando este comando de forma incorreta. \
    Este comando tem um jeito certo e tem que usar o comando do jeito certo. E \
    eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso \
    correto, certo do comando: /enviar 1 mensagem\nOnde 1 é o número do \
    telegram_id do alvo e `mensagem` é a mensagem."
    debug = u"Erro enviando mensagem."
  except Exception as e:
    response = u"Erro tentando enviar mensagem."
    debug = u"Erro enviando mensagem.\nExceção: %s" % (e)
  return {
    'status': False,
    'type': "erro",
    'response': response,
    'multi': False,
    'debug': debug,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Testar timezone do servidor
def cmd_tz(args):
  testetz_timezone = pytz.timezone('America/Sao_Paulo')
  testetz_format = '%Y-%m-%d %H:%M:%S'

  response = list()
  response.append(u'Timezone: %s, %s' % (str(testetz_timezone), testetz_timezone.zone))
  response.append(u'datetime.now(): %s' % (str(datetime.datetime.now())))
  response.append(u'datetime.now(testetz_timezone): %s' % (str(datetime.datetime.now(testetz_timezone))))
  response.append(u'(datetime.datetime.now(testetz_timezone()) - datetime.timedelta(days=2)).strftime(db_datetime()): %s' % ((datetime.datetime.now(testetz_timezone) - datetime.timedelta(days=2)).strftime(testetz_format)))
  response.append(u'(datetime.datetime.now(testetz_timezone()) - datetime.timedelta(minutes=5)).strftime(db_datetime()): %s' % ((datetime.datetime.now(testetz_timezone) - datetime.timedelta(minutes=5)).strftime(testetz_format)))
  response.append(u'(datetime.datetime.now(testetz_timezone()) - datetime.timedelta(days=2)).strftime(db_datetime()): %s' % ((datetime.datetime.now(testetz_timezone) - datetime.timedelta(days=2)).strftime(testetz_format)))
  return {
    'status': True,
    'type': args['command_type'],
    'response': '\n'.join(response),
    'debug': u'testetz: %s' % (response),
    'multi': False,
    'parse_mode': None,
  }

## Tentativa de uma forma mais simples pra criar comandos novos
def comando_um(argumentos):
  resposta = u"Olá %s, você me mandou a seguinte mensagem:\n\n%s\n\nMuito obrigado pela sua mensagem!" % (argumentos['pessoa'], argumentos['mensagem'])
  return resposta

def cmd_simples(args):
  argumentos = dict()
  argumentos['pessoa'] = args['from_id']
  argumentos['mensagem'] = ' '.join(args['command_list'])
  retorno = comando_um(argumentos)
  return {
    'status': True,
    'type': args['command_type'],
    'response': retorno,
    'debug': 'simples',
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Aiogram
async def add_handlers(dispatcher):
  from aiogram import (
    filters,
  )
  from matebot.aio_matebot.controllers.callbacks import (
    command_callback,
    message_callback,
  )

  ## Testar o bot. Ecoa o texto enviado ou produz um erro se não tiver nenhum \
  ##  argumento.
  @dispatcher.message_handler(
    filters.IDFilter(
      user_id = dispatcher.bot.users['alpha'] + dispatcher.bot.users['beta'],
      chat_id = dispatcher.bot.users['alpha'] + dispatcher.bot.users['beta'],
    ),
    commands = ['teste', 'test'],
  )
  async def test_callback(message):
    await message_callback(message, ['test', message.chat.type])
    command = await message.reply(message.get_args())
    await command_callback(command, ['test', message.chat.type])

  ## Enviar mensagem para alguém através do bot
  @dispatcher.message_handler(
    filters.IDFilter(
      user_id = dispatcher.bot.users['alpha'] + dispatcher.bot.users['beta'],
      chat_id = dispatcher.bot.users['alpha'] + dispatcher.bot.users['beta'],
    ),
    commands = ['enviar', 'send']
  )
  async def send_callback(message):
    await message_callback(message, ['send', message.chat.type])
    args = message.get_args().split(' ')
    command = await dispatcher.bot.send_message(
      chat_id = args[0],
      text = ' '.join(args[1::1]),
    )
    await command_callback(command, ['send', message.chat.type])

  ## Responder uma mensagem através do bot
  @dispatcher.message_handler(
    filters.IDFilter(
      user_id = dispatcher.bot.users['alpha'] + dispatcher.bot.users['beta'],
      chat_id = dispatcher.bot.users['alpha'] + dispatcher.bot.users['beta'],
    ),
    commands = ['responder', 'reply']
  )
  async def reply_callback(message):
    await message_callback(message, ['reply', message.chat.type])
    args = message.get_args().split(' ')
    command = await dispatcher.bot.send_message(
      chat_id = str(args[0]),
      text = ' '.join(args[2::1]),
      reply_to_message_id = int(args[1]),
    )
    await command_callback(command, ['reply', message.chat.type])

  ## Lista de comandos reservados para dev/admin
  @dispatcher.message_handler(
    filters.IDFilter(
      user_id = dispatcher.bot.users['alpha'] + dispatcher.bot.users['beta'],
      chat_id = dispatcher.bot.users['alpha'] + dispatcher.bot.users['beta'],
    ),
    commands = ['admin'],
  )
  async def admin_callback(message):
    await message_callback(message, ['admin', message.chat.type])
    lista = list()
    lista.append(u"""/enviar <chat_id> <texto>: Enviar "texto" para \
"chat_id".""")
    lista.append(u"""/responder <chat_id> <message_id> <texto>: Responder \
"message_id" em "chat_id" com "texto".""")
    lista.append(u"""/tz: Teste de timezone do servidor.""")
    command = await message.reply(
      u"Lista de comandos reservados para dev/admin:\n{lista}".format(
        lista = "\n".join(lista),
      )
    )
    await command_callback(command, ['admin', message.chat.type])

  ## Teste de timezone do servidor
  @dispatcher.message_handler(
    filters.IDFilter(
      user_id = dispatcher.bot.users['alpha'] + dispatcher.bot.users['beta'],
      chat_id = dispatcher.bot.users['alpha'] + dispatcher.bot.users['beta'],
    ),
    commands = ['tz', 'timezone'],
  )
  async def tz_callback(message):
    await message_callback(message, ['tz', message.chat.type])
    ## lol
    command = await message.reply(
      u"`{}`".format(cmd_tz({'command_type': None})['response']),
      parse_mode = "MarkdownV2",
    )
    await command_callback(command, ['tz', message.chat.type])
