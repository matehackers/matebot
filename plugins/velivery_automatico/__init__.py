# vim:fileencoding=utf-8
#    Plugin velivery_automatico para matebot: Automatiza gerenciamento de pedidos
#    Copyleft (C) 2019 Desobediente Civil, Velivery

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
import telepot
from plugins.velivery_pedidos import busca_pedidos,db_default_limit
from plugins import velivery_relatorios

def semiauto(args):
  while args['comando'] != 'off':
    teste = args['bot'].getUpdates()
    print(teste)
  else:
    args['bot'].sendMessage(
      chat_id = args['chat_id'],
      text = u"Modo automatico *desligado*.",
      parse_mode = 'Markdown',
      reply_to_message_id = args['message_id'],
    )

#def rcv(msg):
#  print(log_str.rcv(str(msg['chat']['id']), str(msg)))
#  glance = telepot.glance(msg)
#  if glance[0] == 'text':
#    chat_id = args['config'].get("plugins_grupos", "admin")[0]
#    command_list = list()
#    try:
#      from_id = int(msg['from']['id'])
#      chat_id = int(msg['chat']['id'])
#      message_id = int(msg['message_id'])
#      command_list = msg['text']
#    except Exception as e:
#      print(log_str.err(u'Erro do Telepot tentando receber mensagem: %s' % (e)))
#    return command_list

def cmd_semiauto(args):
  try:
    args['bot'].sendMessage(
      chat_id = args['chat_id'],
      text = u"Modo semi automatico *ligado*. Todos demais comandos foram desativados. Para desabilitar o modo semi automatico envie a palavra 'off' (sem as aspas) - sem os parenteses - sem os hifens. sem ponto final",
      parse_mode = 'Markdown',
      reply_to_message_id = args['message_id'],
    )
    args.update(comando = 'on')
    semiauto(args)
  except Exception as e:
    return {
      'status': False,
      'type': "erro",
      'response': u"Modo semi automatico *desligado*.",
      'debug': u"[#semiauto]: [exception] %s" % (e),
      'multi': False,
      'parse_mode': 'Markdown',
    }

## Exportar pedidos em CSV
## TODO obviamente trabalho em progresso
#def exportar(args):
#  return {
#    'status': True,
#    'type': args['command_type'],
#    'multi': False,
#    'destino': 'telegram',
#    'response': u'Comando ainda não implementado :slightly_frowning_face:',
#    'debug': u'Comando /exportar ainda não implementado',
#  }

### Resolve #280 de project:velivery
#def exportar_280(args):
#  return busca_pedidos.busca_280(args)

### Resolve outro problema não especificado
#def relatorio_recompra(args):
#  return velivery_relatorios.taxa_recompra(args)

