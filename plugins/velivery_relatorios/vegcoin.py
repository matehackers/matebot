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

import csv,datetime,inspect, locale
from plugins.velivery_pedidos import busca_pedidos,db_default_limit,db_timezone,db_datetime,queries
from plugins.log import log_str

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

