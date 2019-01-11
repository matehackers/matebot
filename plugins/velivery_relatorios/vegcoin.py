# vim:fileencoding=utf-8
#    Plugin velivery_relatorios para matebot: Faz relatórios, exibe informações
#      e subsidia estatísticas com os dados do Velivery
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

import csv, datetime, inspect, locale, operator
from plugins.velivery_pedidos import busca_pedidos, db_default_limit, db_timezone, db_datetime, queries
from plugins.log import log_str

## TODO Nao usamos pra nada
def pedidos_veganweek(args):
  relatorio = inspect.currentframe().f_code.co_name
  try:
    args['bot'].sendMessage(args['chat_id'], u"Calculando %s..." % (relatorio))
  except Exception as e:
    print(log_str.debug(e))
  resultado = list()
  try:
    dados = dict()
    dados['query'] = queries.query_veganweek()
    dados = busca_pedidos.transaction(dados['query'])

    if dados['status']:
      resultado = dados['resultado']
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Não deu certo!",
        'debug': log_str.debug(u"O contrário do sucesso!"),
        'parse_mode': None,
      }

    ## Gerar arquivos CSV
    try:
      args['bot'].sendMessage(args['chat_id'], u"Mais um pouco...")
    except Exception as e:
      print(log_str.debug(e))
    ## Dados de usuária(o) por período
    try:
      with open("/tmp/relatorio_%s.csv" % (relatorio), "w") as csvfile:
        fieldnames = [
          u"Nome",
          u"E-mail",
          u"Número de pedidos no período",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dado in resultado:
          writer.writerow({
            'Nome': str(dado['user_name']),
            'E-mail': str(dado['user_email']),
            'Número de pedidos no período': str(len(set([pedido['order_id'] for pedido in resultado if pedido['user_id'] == dado['user_id']]))),
          })
      with open("/tmp/relatorio_%s.csv" % (relatorio), "r") as csvfile:
        args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
    except Exception as e:
      args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (e))
      raise
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Erro catastrófico: %s" % (e),
        'debug': log_str.debug(u"Exceção: %s" % (e)),
        'parse_mode': None,
      }
  except Exception as e:
    args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (e))
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u"Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.",
      'debug': log_str.debug(u"Exceção: %s" % (e)),
      'parse_mode': None,
    }

## Gera CSV com pedidos feitos de 19 de novembro a 25 de novembro de 2018
def pedidos_veganweek_csv(args):
  relatorio = inspect.currentframe().f_code.co_name
  try:
    args['bot'].sendMessage(args['chat_id'], u"Calculando %s..." % (relatorio))
  except Exception as e:
    print(log_str.debug(e))
  resultado = list()
  try:
    dados = dict()
    dados['query'] = queries.query_veganweek()
    dados = busca_pedidos.transaction(dados['query'])

    if dados['status']:
      resultado = dados['resultado']
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Não deu certo!",
        'debug': log_str.debug(u"O contrário do sucesso!"),
        'parse_mode': None,
      }

    ## Gerar arquivos CSV
    try:
      args['bot'].sendMessage(args['chat_id'], u"Mais um pouco...")
    except Exception as e:
      print(log_str.debug(e))
    ## Dados de usuária(o) por período
    try:
      with open("/tmp/relatorio_%s.csv" % (relatorio), "w") as csvfile:
        fieldnames = [
          u"Nome",
          u"E-mail",
          u"Número de pedidos no período",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dado in resultado:
          writer.writerow({
            'Nome': str(dado['user_name']),
            'E-mail': str(dado['user_email']),
            'Número de pedidos no período': str(len(set([pedido['order_id'] for pedido in resultado if pedido['user_id'] == dado['user_id']]))),
          })
      with open("/tmp/relatorio_%s.csv" % (relatorio), "r") as csvfile:
        args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
    except Exception as e:
      args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (e))
      raise
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Erro catastrófico: %s" % (e),
        'debug': log_str.debug(u"Exceção: %s" % (e)),
        'parse_mode': None,
      }
  except Exception as e:
    args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (e))
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u"Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.",
      'debug': log_str.debug(u"Exceção: %s" % (e)),
      'parse_mode': None,
    }

## Gera CSV com usuários que nunca fizeram um pedido
def usuarios_inativos_csv(args):
  relatorio = inspect.currentframe().f_code.co_name
  try:
    args['bot'].sendMessage(args['chat_id'], u"Calculando %s..." % (relatorio))
  except Exception as e:
    print(log_str.debug(e))
  resultado = list()
  try:
    dados = dict()
    dados['pedidos'] = busca_pedidos.transaction(queries.query_pedidos())
    dados['usuarios'] = busca_pedidos.transaction(queries.query_usuarios())

    if dados['pedidos']['status'] and dados['usuarios']['status']:
      ## Encontrar usuários sem pedido
      pedidos = [pedido['user_id'] for pedido in dados['pedidos']['resultado']]
      usuarios_inativos = [{'user_name': usuario['user_name'], 'user_email': usuario['user_email']} for usuario in dados['usuarios']['resultado'] if usuario['user_id'] not in pedidos]
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Não deu certo!",
        'debug': log_str.debug(u"O contrário do sucesso!"),
        'parse_mode': None,
      }

    ## Gerar arquivos CSV
    try:
      args['bot'].sendMessage(args['chat_id'], u"Mais um pouco...")
    except Exception as e:
      print(log_str.debug(e))
    ## Dados de usuária(o) por período
    try:
      with open("/tmp/relatorio_%s.csv" % (relatorio), "w") as csvfile:
        fieldnames = [
          u"Nome",
          u"E-mail",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dado in usuarios_inativos:
          writer.writerow({
            'Nome': str(dado['user_name']),
            'E-mail': str(dado['user_email']),
          })
      with open("/tmp/relatorio_%s.csv" % (relatorio), "r") as csvfile:
        args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
    except Exception as e:
      args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (e))
      raise
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Erro catastrófico: %s" % (e),
        'debug': log_str.debug(u"Exceção: %s" % (e)),
        'parse_mode': None,
      }
  except Exception as e:
    args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (e))
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u"Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.",
      'debug': log_str.debug(u"Exceção: %s" % (e)),
      'parse_mode': None,
    }

## Gera CSV com pedidos feitos de 19 de novembro a 25 de novembro de 2018
## Cálculo do CAC - considera somente o primeiro pedido do usuário
def usuarios_vegcoinweek_cac_csv(args):
  relatorio = inspect.currentframe().f_code.co_name
  try:
    args['bot'].sendMessage(args['chat_id'], u"Calculando %s..." % (relatorio))
  except Exception as e:
    print(log_str.debug(e))
  resultado = list()
  try:
    dados = dict()
    ## TODO olha a cagada
    dados['pedidos_todos'] = busca_pedidos.transaction(queries.query_pedidos_vegcoinweek_inverso())
    dados['pedidos_vegcoinweek'] = busca_pedidos.transaction(queries.query_pedidos_vegcoinweek())
    dados['usuarios'] = busca_pedidos.transaction(queries.query_usuarios())

    if dados['pedidos_todos']['status'] and dados['pedidos_vegcoinweek']['status'] and dados['usuarios']['status']:
      ## Encontrar primeiro pedido do usuário
      primeiros_pedidos = {pedido['user_id'] for pedido in sorted(dados['pedidos_todos']['resultado'], key=lambda k: k['order_inner_id'])}
      primeiros_pedidos_vegcoinweek = {pedido['user_id'] for pedido in sorted(dados['pedidos_vegcoinweek']['resultado'], key=lambda k: k['order_inner_id']) if pedido['user_id'] not in primeiros_pedidos}
      usuarios_vegcoinweek = [{'user_name': usuario['user_name'], 'user_email': usuario['user_email'], 'user_created_at': usuario['user_created_at']} for usuario in dados['usuarios']['resultado'] if usuario['user_id'] in primeiros_pedidos_vegcoinweek]
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Não deu certo!",
        'debug': log_str.debug(u"O contrário do sucesso!"),
        'parse_mode': None,
      }

    ## Gerar arquivos CSV
    try:
      args['bot'].sendMessage(args['chat_id'], u"Mais um pouco...")
    except Exception as e:
      print(log_str.debug(e))
    ## Dados de usuária(o) por período
    try:
      with open("/tmp/relatorio_%s.csv" % (relatorio), "w") as csvfile:
        fieldnames = [
          u"Nome",
          u"E-mail",
          u"Adesão",
          u"Primeiro pedido",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dado in usuarios_vegcoinweek:
          writer.writerow({
            'Nome': str(dado['user_name']),
            'E-mail': str(dado['user_email']),
            'Adesão': str(dado['user_created_at']),
            'Primeiro pedido': str(u"Eu sei que foi nessa semana."),
          })
      with open("/tmp/relatorio_%s.csv" % (relatorio), "r") as csvfile:
        args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
    except Exception as e:
      args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (e))
      raise
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Erro catastrófico: %s" % (e),
        'debug': log_str.debug(u"Exceção: %s" % (e)),
        'parse_mode': None,
      }
  except Exception as e:
    args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (e))
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u"Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.",
      'debug': log_str.debug(u"Exceção: %s" % (e)),
      'parse_mode': None,
    }

