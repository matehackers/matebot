# vim:fileencoding=utf-8
#    Plugin admin para matebot: Plugin para administração e testes

#    Copyleft (C) 2018-2019 Desobediente Civil, Matehackers, Velivey
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

def croak(response, debug):
  return {
    'status': False,
    'type': "erro",
    'response': response,
    'multi': False,
    'debug': debug,
    'parse_mode': None,
  }

## Testar valor total do pedido
def cmd_valor(args):
#	$totalItems = 0;
#	$totalSubItems = 0;
  limite = 3
  try:
    pedido = 43982
    requisicao = {
      'db_query': ' '.join([
        "AND", '='.join(['reference_id', str(pedido)]),
        "ORDER BY", 'id', "ASC",
        "LIMIT", str(limite)
      ]),
      'db_limit': limite,
      'modo': "pedido",
      'cabecalho': u"Pedido %s:" % (str(pedido)),
      'nenhum': u"Pedido %s não encontrado!" % (str(pedido)),
      'multi': False,
      'destino': "telegram",
      'type': args['command_type'],
    }
    return busca_pedidos.busca(requisicao)
  except IndexError:
    pass
  return croak(u"Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /pedido 1\nOnde 1 é o código do pedido. Em caso de dúvida, pergunte pro %s" % (args['info_dict']['telegram_admin']), u"Erro tentando buscar pedido, command_list: %s" % (args['command_list']))

def cmd_url(args):
  response = u"Teste de URL: [pedidos](https://t.me/%s?%s=%s) [atrasados](https://t.me/%s?%s)" % ('velivery_dev_bot', 'start', 'pedidos_42', 'velivery_dev_bot', 'atrasados')
  return {
    'status': True,
    'type': args['command_type'],
    'response': response,
    'debug': u"teste_url",
    'multi': False,
    'parse_mode': "Markdown",
  }

## Testes Totalvoice
mensagem_erro_ligacao = u"Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /ligar 5199999999 \nOnde 5199999999 é o número de telefone do alvo."

def ligar(args):
  debug = u"Erro rodando %s." % (__name__)
  try:
    args.update(telefones = [str(args['config']['agenda']['numero_2']), str(args['config']['agenda']['numero_3'])])
    return shiva_1(args)
  except Exception as e:
    print(log_str.debug(e))
    debug = u"Erro tentando ligar para %s." % (args['numero'])
  return croak(mensagem_erro_ligacao, debug)

def cmd_ligar_p0(args):
  args.update(numero = ''.join(args['command_list']))
  return ligar(args)

def cmd_ligar_p1(args):
  args.update(numero = str(args['config']['agenda']['numero_1']))
  return ligar(args)

def cmd_ligar_p2(args):
  args.update(numero = str(args['config']['agenda']['numero_2']))
  return ligar(args)

def cmd_ligar_p3(args):
  args.update(numero = str(args['config']['agenda']['numero_3']))
  return ligar(args)

def cmd_ligar_p4(args):
  args.update(numero = str(args['config']['agenda']['numero_4']))
  return ligar(args)

