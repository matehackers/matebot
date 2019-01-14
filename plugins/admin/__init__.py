# vim:fileencoding=utf-8
#    Plugin admin para matebot: Plugin para administração e testes

#    Copyleft (C) 2018-2019 Desobediente Civil, Matehackers, Velivery
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime,pytz
from plugins.velivery_pedidos import busca_pedidos,db_default_limit
from plugins.totalvoice import shiva_1, shiva_2, shiva_3, shiva_4
from plugins.log import log_str
from plugins.admin.velivery import *

def cmd_teste(args):
  return {
    'status': True,
    'type': 'mensagem',
    'response': str(args['command_list']),
    'debug': u'teste',
    'multi': False,
    'parse_mode': None,
  }

## TODO acentuacao
## Enviar mensagem para alguem
def cmd_enviar(args):
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
          'parse_mode': None,
        }
      else:
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

