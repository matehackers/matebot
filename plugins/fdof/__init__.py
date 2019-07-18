# vim:fileencoding=utf-8
#  Plugin fdof para matebot: Comandos Greatful para Fábrica do Futuro
#  Copyleft (C) 2019 Greatful

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Avisa que chegou por primeiro na Fábrica do Futuro
def cmd_cheguei(args):
  response = u"Chegou chegando, desnorteando a Fábrica toda!"
  return {
    'status': True,
    'type': args['command_type'],
    'response': response,
    'debug': 'cheguei',
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Avisa que foi embora da Fábrica do Futuro
def cmd_vazei(args):
  response = u"A Fábrica é boa, mas não dá pra morar aí!"
  return {
    'status': True,
    'type': args['command_type'],
    'response': response,
    'debug': 'vazei',
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Avisa que fez uma merda
def cmd_adubei(args):
  response = u"Adubando, dá. Dar abunda!"
  return {
    'status': True,
    'type': args['command_type'],
    'response': response,
    'debug': 'vazei',
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## TODO Usar SQL. Código extraído do Velivery Bike Entregas da Vegga
#def cmd_cheguei(args):
#  try:
#    quemchegou_db = dataset.connect('sqlite:///quemchegou.db')
#    try:
#      if args['command_list'][0].isdigit():
#        pedido_bike = int(args['command_list'][0])
#    except IndexError:
#      pass
#    if pedido_bike > 0:
#      pedidos_bike_db['pedidos'].insert(dict(reference_id=str(pedido_bike)))
#      return {
#        'status': True,
#        'type': args['command_type'],
#        'multi': False,
#        'destino': 'telegram',
#        'response': u"Pedido %s adicionado à lista de atendidos!" % (str(pedido_bike)),
#        'debug': u"Sucesso!",
#        'parse_mode': None,
#      }
#    else:
#      pedidos_lista = list()
#      for pedido in pedidos_bike_db['pedidos']:
#        pedidos_lista.append(pedido['reference_id'])
#      return {
#        'status': True,
#        'type': args['command_type'],
#        'multi': False,
#        'destino': 'telegram',
#        'response': u"Lista de pedidos atendidos:\n\n%s" % (str(sorted(set(pedidos_lista)))),
#        'debug': u"Sucesso!",
#        'parse_mode': None,
#      }
#  except sqlite3.ProgrammingError as e:
#    print(log_str.debug(e))
#  except Exception as e:
#    print(log_str.err(e))
#  return {
#    'status': False,
#    'type': 'ẽrro',
#    'multi': False,
#    'destino': 'telegram',
#    'response': u"O contrário de deu certo!",
#    'debug': u"O contrário do sucesso!",
#    'parse_mode': None,
#  }

