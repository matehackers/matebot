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
import datetime

from plugins.velivery_pedidos import busca_pedidos

def db_default_limit():
  return 10

## Todos pedidos
def pedidos(info_dict, bot_dict, addr_dict, command_list):
  limite = db_default_limit()
  try:
    if command_list[0].isdigit():
      limite = str(command_list[0])
  except IndexError:
    pass
  requisicao = {
    'db_query': ' '.join([
      "ORDER BY", 'created_at', "DESC",
      "LIMIT", str(limite)
    ]),
    'db_limit': limite,
    'modo': 'todos',
    'cabecalho': u'Todos os pedidos (exibindo os últimos %s pedidos):\n' % (limite),
    'multi': True,
    'destino': 'telegram',
  }
  return busca_pedidos.busca(requisicao)

## Pedido por número
def pedido(info_dict, bot_dict, addr_dict, command_list):
  limite = db_default_limit()
  try:
    if command_list[0].isdigit():
      pedido = command_list[0]
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
        'multi': False,
        'destino': 'telegram',
      }
      return busca_pedidos.busca(requisicao)
  except IndexError:
    pass
  return {
    'status': False,
    'type': 'erro',
    'multi': False,
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /pedido 1\nOnde 1 é o código do pedido. Em caso de dúvida, pergunte pro %s' % (bot_admin),
    'debug': u'Erro tentando buscar pedido, command_list: %s' % (command_list),
  }

## Pedidos pendentes das últimas 48 horas
def pendentes(info_dict, bot_dict, addr_dict, command_list):
  limite = db_default_limit()
  requisicao = {
    'db_query': ' '.join([
      "AND", '='.join(['order_request_status_id', '1']),
      "AND", '='.join(['created_at', 'updated_at']),
      "AND", '>='.join(['created_at', ''.join(["'", str(datetime.datetime.now() - datetime.timedelta(days=2)), "'"])]),
      "ORDER BY", 'created_at', "DESC",
      "LIMIT", str(limite),
    ]),
    'db_limit': limite,
    'modo': 'pendentes',
    'cabecalho': str(),
    'nenhum': u'Nenhum pedido pendente. Bom trabalho, Velivery!',
    'multi': False,
    'destino': 'telegram',
  }
  return busca_pedidos.busca(requisicao)

## Pedidos atrasados
def atrasados(info_dict, bot_dict, addr_dict, command_list):
  limite = db_default_limit()
  requisicao = {
    'db_query': ' '.join([
      "AND", '='.join(['order_request_status_id', '1']),
      "AND", '='.join(['created_at', 'updated_at']),
      "AND", '<'.join(['created_at',  ''.join(["'", str(datetime.datetime.now() - datetime.timedelta(minutes=5)), "'"])]),
      "AND", '>='.join(['created_at', ''.join(["'", str(datetime.datetime.now() - datetime.timedelta(days=2)), "'"])]),
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
  }
  return busca_pedidos.busca(requisicao)

