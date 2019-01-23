# vim:fileencoding=utf-8
#    Plugin velivery_pedidos para matebot: Busca pedidos no banco de dados do velivery
#    Copyleft (C) 2018 Desobediente Civil, Velivery

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

### Imports
import datetime, pytz

from plugins.velivery_pedidos import busca_pedidos
from plugins.totalvoice import shiva_1, shiva_2, shiva_3, shiva_4
from plugins.log import log_str
from plugins.velivery_pedidos.atrasados import atrasados_v2,pendentes_v2

def db_default_limit():
  return 10

def db_timezone():
  return pytz.timezone('America/Sao_Paulo')

def db_datetime():
  return '%Y-%m-%d %H:%M:%S'

## Pedido por número
## TODO revisar
def cmd_pedido(args):
  limite = db_default_limit()
  try:
    if args['command_list'][0].isdigit():
      pedido = args['command_list'][0]
      requisicao = {
        'db_query': ' '.join([
          "AND", '='.join(['reference_id', str(pedido)]),
          "ORDER BY", 'id', "ASC",
          "LIMIT", str(limite)
        ]),
        'db_limit': limite,
        'modo': 'pedido',
        'cabecalho': u'Pedido %s:' % (str(pedido)),
        'nenhum': u'Pedido %s não encontrado!' % (str(pedido)),
        'multi': True,
        'destino': 'telegram',
        'type': args['command_type'],
      }
      return busca_pedidos.busca(requisicao)
  except IndexError:
    pass
  return {
    'status': False,
    'type': 'erro',
    'multi': False,
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /pedido 1\nOnde 1 é o código do pedido. Em caso de dúvida, pergunte pro %s' % (args['info_dict']['telegram_admin']),
    'debug': u'Erro tentando buscar pedido, command_list: %s' % (args['command_list']),
    'parse_mode': None,
  }

## Pedidos pendentes das últimas 48 horas
def pendentes_antigo(args):
  limite = db_default_limit()
  requisicao = {
    'db_query': ' '.join([
      "AND", '='.join(['order_request_status_id', '1']),
      "AND", '='.join(['created_at', 'updated_at']),
      "AND", '>='.join(['created_at', ''.join(["'", (datetime.datetime.now(db_timezone()) - datetime.timedelta(days=2)).strftime(db_datetime()), "'"])]),
      "ORDER BY", 'created_at', "DESC",
      "LIMIT", str(limite),
    ]),
    'db_limit': limite,
    'modo': 'pendentes',
    'cabecalho': str(),
    'nenhum': u'Nenhum pedido pendente. Bom trabalho, Velivery!',
    'multi': False,
    'destino': 'telegram',
    'type': args['command_type'],
  }
  return busca_pedidos.busca(requisicao)

## Pedidos atrasados
def atrasados_antigo(args):
  limite = db_default_limit()
  requisicao = {
    'db_query': ' '.join([
      "AND", '='.join(['order_request_status_id', '1']),
      "AND", '='.join(['created_at', 'updated_at']),
      "AND", '<'.join(['created_at',  ''.join(["'", (datetime.datetime.now(db_timezone()) - datetime.timedelta(minutes=5)).strftime(db_datetime()), "'"])]),
      "AND", '>='.join(['created_at', ''.join(["'", (datetime.datetime.now(db_timezone()) - datetime.timedelta(days=2)).strftime(db_datetime()), "'"])]),
      "AND", 'delivery_datetime', "IS", "NULL",
      "ORDER BY", 'created_at', "DESC",
      "LIMIT", str(limite),
    ]),
    'db_limit': limite,
    'modo': 'atrasados',
    'cabecalho': str(),
    'nenhum': u'Nenhum pedido atrasado. Bom trabalho, Velivery!',
    'multi': False,
    'destino': 'telegram',
    'type': args['command_type'],
  }
  return busca_pedidos.busca(requisicao)

## TODO revisar
def cmd_ligar_1(args):
  args.update(numero = ''.join(args['command_list']))
  args.update(telefones = [str(args['config']['agenda']['numero_2']), str(args['config']['agenda']['numero_3'])])
  try:
    return shiva_1(args)
  except Exception as e:
    print(log_str.debug(e))
  return {
    'status': False,
    'type': 'erro',
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /ligar 5199999999 \nOnde 5199999999 é o número de telefone do alvo.',
    'multi': False,
    'debug': u'Erro enviando mensagem.',
    'parse_mode': None,
  }

## TODO revisar
def cmd_ligar_2(args):
  args.update(numero = ''.join(args['command_list']))
  args.update(telefones = [str(args['config']['agenda']['numero_2']), str(args['config']['agenda']['numero_3'])])
  try:
    return shiva_2(args)
  except Exception as e:
    print(log_str.debug(e))
  return {
    'status': False,
    'type': 'erro',
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /ligar 5199999999 \nOnde 5199999999 é o número de telefone do alvo.',
    'multi': False,
    'debug': u'Erro enviando mensagem.',
    'parse_mode': None,
  }

## TODO revisar
def cmd_ligar_3(args):
  args.update(numero = ''.join(args['command_list']))
  args.update(telefones = [str(args['config']['agenda']['numero_2']), str(args['config']['agenda']['numero_3'])])
  try:
    return shiva_3(args)
  except Exception as e:
    print(log_str.debug(e))
  return {
    'status': False,
    'type': 'erro',
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /ligar 5199999999 \nOnde 5199999999 é o número de telefone do alvo.',
    'multi': False,
    'debug': u'Erro enviando mensagem.',
    'parse_mode': None,
  }

## TODO revisar
def cmd_ligar_4(args):
  args.update(numero = ''.join(args['command_list']))
  args.update(telefones = [str(args['config']['agenda']['numero_2']), str(args['config']['agenda']['numero_3'])])
  try:
    return shiva_4(args)
  except Exception as e:
    print(log_str.debug(e))
  return {
    'status': False,
    'type': 'erro',
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /ligar 5199999999 \nOnde 5199999999 é o número de telefone do alvo.',
    'multi': False,
    'debug': u'Erro enviando mensagem.',
    'parse_mode': None,
  }

## TODO revisar
def cmd_atrasados(args):
  return atrasados_v2(args)

## TODO revisar
def cmd_pendentes(args):
  return pendentes_v2(args)

