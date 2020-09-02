# vim:fileencoding=utf-8
#  
#  Plugin PTB Flood Control para matebot: Trata limites de envio de
#    mensagens
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

from telegram.error import (
  TelegramError,
  Unauthorized,
  BadRequest,
  TimedOut,
  ChatMigrated,
  NetworkError,
)

def caps(update, context):
  ## Por que transformar uma lista de strings em uma string?
  text_caps = ' '.join(context.args).upper()
  context.bot.send_message(
    chat_id = update.effective_chat.id,
    text = text_caps,
  )
caps_handler = CommandHandler('caps', caps)
updaters[0].dispatcher.add_handler(caps_handler)


def send_message(args):
  try:
    args['bot'].sendMessage(args['send_message'])
  except TelegramError:
    pass
  except Unauthorized as e:
    text = list()
    text.append('#exception #unauthorized')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except telegram.error.BadRequest as e:
    # handle malformed requests - read more below!
    text = list()
    text.append('#exception #badrequest')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except telegram.error.TimedOut as e:
    # handle slow connection problems
    text = list()
    text.append('#exception #timedout')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except telegram.error.NetworkError as e:
    # handle other connection problems
    text = list()
    text.append('#exception #networkerror')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except telegram.error.ChatMigrated as e:
    # the chat_id of a group has changed, use e.new_chat_id instead
    text = list()
    text.append('#exception #chatmigrated')
    text.append(u"New chat: %s" % (str(e.new_chat_id)))
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except telegram.error.TelegramError as e:
    # handle all other telegram related errors
    text = list()
    text.append('#exception #telegramerror')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except Exception as e:
    text = list()
    text.append('#exception #notetelegram')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  finally:
    context.bot.send_message(
      text = u"Tive um problema mas já avisei o pessoal que cuida do desenvolvimento.",
      chat_id = update.effective_chat.id,
      reply_to_message_id = update.effective_message.message_id,
    )

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
## Enviar mensagem para alguem
def cmd_enviar(args):
  response = u"Enviar o que?"
  debug = u"Nada para enviar"
  try:
    if len(args['command_list']) > 1:
      if args['command_list'][0].isdigit():
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
    response = u"Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /enviar 1 mensagem\nOnde 1 é o número do telegram_id do alvo e `mensagem` é a mensagem."
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

