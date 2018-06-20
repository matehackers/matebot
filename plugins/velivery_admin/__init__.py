# vim:fileencoding=utf-8
#    Plugin velivery_admin para matebot: Tarefas reservadas pafunça do Velivery
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
from plugins.velivery_pedidos import busca_pedidos,db_default_limit

## Todos pedidos
def pedidos(args):
  limite = db_default_limit()
  try:
    if args['command_list'][0].isdigit():
      limite = str(args['command_list'][0])
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
    'type': args['command_type'],
  }
  return busca_pedidos.busca(requisicao)

## Exportar pedidos em CSV
## TODO obviamente trabalho em progresso
def exportar(args):
  return {
    'status': True,
    'type': args['command_type'],
    'multi': False,
    'destino': 'telegram',
    'response': u'Comando ainda não implementado :slightly_frowning_face:',
    'debug': u'Comando /exportar ainda não implementado',
  }
## Resolve #280 de project:velivery
def exportar_280(args):
  return busca_pedidos.busca_280(args)

