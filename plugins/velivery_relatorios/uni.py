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
from plugins.velivery_pedidos import busca_pedidos,db_default_limit,db_timezone,db_datetime
from plugins.log import log_str
from plugins.hashes import inner_hash

def ltv(args):
  relatorio = inspect.currentframe().f_code.co_name
  ## Lifetime Value
  ## Tempo de relacionamento da(o) usuária(o): Do primeiro até o último pedido
  ## Dado 1: Quantidade de pedidos da(o) usuária(o) dentro do seu tempo de vida
  ## Dado 2: Soma do valor total de cada pedido excluindo a taxa de entrega de pedidos da(o) usuária(o) durante o seu tempo de vida
  ## Dado 3: Ticket médido da empresa
  ## Cálculo "ticket médio": Valor total de pedidos do período / Número de pedidos no período
  ## Cálculo "LTV (lifetime value)" de usuária(o): Ticket médio * Tempo de relacionamento
  try:
    args['bot'].sendMessage(args['chat_id'], u"Calculando %s..." % (relatorio))
  except Exception as e:
    print(log_str.debug(e))
  resultados = dict()
  try:
#    pedidos = dict()
#    pedidos['query'] = " ".join([
#      "SELECT", ",".join([
#        ".".join([busca_pedidos.db_tables()['pedidos'], 'reference_id']),
#        ".".join([busca_pedidos.db_tables()['pedidos'], 'order_user_id']),
#        ".".join([busca_pedidos.db_tables()['pedidos'], 'order_company_id']),
#        ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'city_id']),
#      ]),
#      "FROM", busca_pedidos.db_tables()['pedidos'],
#      "LEFT", "JOIN", busca_pedidos.db_tables()['estabelecimentos'],
#      "ON", "=".join([
#        ".".join([
#          busca_pedidos.db_tables()['pedidos'],
#          'order_company_id',
#        ]),
#        ".".join([
#          busca_pedidos.db_tables()['estabelecimentos'],
#          'reference_id'
#        ]),
#      ]),
#      "WHERE", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
#      "AND", ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'deleted_at']), "IS NULL",
#    ])
#    SELECT L.Nome_Livro AS Livro,
#A.Nome_autor AS Autor,
#E.Nome_Editora AS Editora,
#L.Preco_Livro AS 'Preço do Livro'
#FROM tbl_Livro AS L
#INNER JOIN tbl_autores AS A
#ON L.ID_autor = A.ID_autor
#INNER JOIN tbl_editoras AS E
#ON L.ID_editora = E.ID_editora
#WHERE E.Nome_Editora LIKE 'O%'
#ORDER BY L.Preco_Livro DESC;
    dados = dict()
    dados['query'] = " ".join([
      "SELECT", ",".join([
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'reference_id']),
          "AS", 'order_id',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'order_user_id']),
          "AS", 'user_id',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['usuarios'], 'name']),
          "AS", 'user_name',
        ]),
        ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'city_id']),
        " ".join([
          ".".join([busca_pedidos.db_tables()['cidades'], 'name']) ,
          "AS", 'city_name',
        ]),
      ]),
      "FROM", busca_pedidos.db_tables()['pedidos'],
      "INNER", "JOIN", busca_pedidos.db_tables()['usuarios'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_user_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['usuarios'],
          'id'
        ]),
      ]),
      "INNER", "JOIN", busca_pedidos.db_tables()['estabelecimentos'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_company_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['estabelecimentos'],
          'reference_id'
        ]),
      ]),
      "INNER", "JOIN", busca_pedidos.db_tables()['cidades'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['estabelecimentos'],
          'city_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['cidades'],
          'reference_id'
        ]),
      ]),
      "WHERE", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['cidades'], 'deleted_at']), "IS NULL",
    ])

    pracas = ['total', 'rs', 'ce', 'rj', 'sp']

    anos = ['2016', '2017', '2018']
    for ano in anos:
      print(log_str.debug(str(ano)))
#      pedidos[str(ano)] = dict()
#      usuarios[str(ano)] = dict()
      dados[str(ano)] = dict()
      resultados[str(ano)] = dict()
      meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
      for mes in meses:
        print(log_str.debug('-'.join([str(ano), str(mes)])))
        resultados[str(ano)][str(mes)] = dict()
        resultados[str(ano)][str(mes)]['total'] = dict()
        for praca in pracas:
          resultados[str(ano)][str(mes)][praca] = dict()

#        pedidos[str(ano)][str(mes)] = busca_pedidos.transaction_local(" ".join([
#          pedidos['query'],
#          "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
#          "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
#        ]))

#        usuarios[str(ano)][str(mes)] = busca_pedidos.transaction_local(" ".join([
#          usuarios['query'],
#          "AND", ">=".join([".".join([busca_pedidos.db_tables()['usuarios'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
#          "AND", "<=".join([".".join([busca_pedidos.db_tables()['usuarios'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
#        ]))

        dados[str(ano)][str(mes)] = busca_pedidos.transaction_local(" ".join([
          dados['query'],
          "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
          "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
        ]))

        ## Programação dos dados de pedidos
#        print(log_str.debug(pedidos[str(ano)][str(mes)]['status']))
#        if pedidos[str(ano)][str(mes)]['status']:
#          pass
#        else:
#          try:
#            args['bot'].sendMessage(args['chat_id'], u"Anota aí: Não consegui encontrar pedidos no mês %s do ano %s" % (str(mes), str(ano)))
#          except Exception as e:
#            print(log_str.debug(e))

        ## Programação dos dados de usuários
#        if usuarios[str(ano)][str(mes)]['status']:
#          resultados[str(ano)][str(mes)]['total']['usuarios'] = usuarios[str(ano)][str(mes)]['resultado']
#        else:
#          try:
#            args['bot'].sendMessage(args['chat_id'], u"Anota aí: Não consegui encontrar usuários no mês %s do ano %s" % (str(mes), str(ano)))
#          except Exception as e:
#            print(log_str.debug(e))

        ## Programação dos dados de usuários
        if dados[str(ano)][str(mes)]['status']:
#          resultados[str(ano)][str(mes)]['total']['dados']
          resultados[str(ano)][str(mes)]['total']['dados'] = dados[str(ano)][str(mes)]['resultado']
#          str(len(set([pedido['order_id'] for pedido in dados[str(ano)][str(mes)]['resultado'] if pedido['user_id'] == dado['user_id']])))
#          str(len(set([pedido['order_id'] for pedido in dados[str(ano)][str(mes)]['resultado'] if pedido['user_id'] == dado['user_id']])))
#          print(set([dado for dado in dados[str(ano)][str(mes)]['resultado']]))
        else:
          try:
            args['bot'].sendMessage(args['chat_id'], u"Anota aí: Não consegui encontrar usuários no mês %s do ano %s" % (str(mes), str(ano)))
          except Exception as e:
            print(log_str.debug(e))

    ## Gerar arquivos CSV
    try:
      args['bot'].sendMessage(args['chat_id'], u"Mais um pouco...")
    except Exception as e:
      print(log_str.debug(e))
    ## Dados de usuária(o) por período
    try:
      for ano in sorted(resultados.items()):
        for mes in sorted(ano[1].items()):
          with open("/tmp/relatorio_%s-%s-%s.csv" % (relatorio, str(ano[0]), str(mes[0])), "w") as csvfile:
            fieldnames = [
              u"Período",
              u"Usuária(o)",
              u"Praça",
              u"Número de pedidos no período",
#              u"Soma do valor dos pedidos no período",
#              u"Ticket médio individual no período",
#              u"Lifetime value no período",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for dado in mes[1]['total']['dados']:
              print([pedido['order_id'] for pedido in mes[1]['total']['dados'] if pedido['user_id'] == dado['user_id']])
              print(set([pedido['order_id'] for pedido in mes[1]['total']['dados'] if pedido['user_id'] == dado['user_id']]))
              print(len(set([pedido['order_id'] for pedido in mes[1]['total']['dados'] if pedido['user_id'] == dado['user_id']])))
              writer.writerow({
                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
                'Usuária(o)': str(inner_hash('md5', "".join([str(dado['user_id']), str(dado['user_name'])]))),
#                'Usuária(o)': str(str(dado['user_name'])),
                'Praça': str(dado['city_name']),
                'Número de pedidos no período': str(len(set([pedido['order_id'] for pedido in mes[1]['total']['dados'] if pedido['user_id'] == dado['user_id']]))),
#                'Soma do valor dos pedidos no período': '',
#                'Ticket médio individual no período': '',
#                'Lifetime value no período': '',
              })
          with open("/tmp/relatorio_%s-%s-%s.csv" % (relatorio, str(ano[0]), str(mes[0])), "r") as csvfile:
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
    ## CSV Lifetime Value
#    try:
#      for ano in sorted(resultados.items()):
#        for mes in sorted(ano[1].items()):
#          with open("/tmp/relatorio_%s-%s-%s.csv" % (relatorio, str(ano[0]), str(mes[0])), "w") as csvfile:
#            fieldnames = [
#              u"Período",
#              u"Usuária(o)",
#              u"Praça",
#              u"Tempo de relacionamento",
#              u"Número de pedidos",
#              u"Soma do valor dos pedidos",
#              u"Ticket médio individual",
#              u"Lifetime value",
#            ]
#            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#            writer.writeheader()
#            for usuario in mes[1]['total']['usuarios']:
#              writer.writerow({
#                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
#                'Usuária(o)': usuario['id'],
#                'Praça': '',
#                'Tempo de relacionamento': '',
#                'Número de pedidos': '',
#                'Soma do valor dos pedidos': '',
#                'Ticket médio individual': '',
#                'Lifetime value': '',
#              })
#          with open("/tmp/relatorio_%s-%s-%s.csv" % (relatorio, str(ano[0]), str(mes[0])), "r") as csvfile:
#            args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
#    except Exception as e:
#      args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (e))
#      raise
#      return {
#        'status': False,
#        'type': 'erro',
#        'multi': False,
#        'destino': 'telegram',
#        'response': u"Erro catastrófico: %s" % (e),
#        'debug': log_str.debug(u"Exceção: %s" % (e)),
#        'parse_mode': None,
#      }

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

def recompra_2(args):
  relatorio = inspect.currentframe().f_code.co_name
  ## Taxa de recompra
  ## Data do primeiro pedido
  try:
    args['bot'].sendMessage(args['chat_id'], u"Calculando %s..." % (relatorio))
  except Exception as e:
    print(log_str.debug(e))
  resultados = dict()

  try:
    ## SQL query
    dados = dict()
    dados['query'] = " ".join([
      "SELECT", ",".join([
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'reference_id']),
          "AS", 'order_id',
        ]),
        ".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']),
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'order_user_id']),
          "AS", 'user_id',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['usuarios'], 'name']),
          "AS", 'user_name',
        ]),
        ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'city_id']),
        " ".join([
          ".".join([busca_pedidos.db_tables()['cidades'], 'name']) ,
          "AS", 'city_name',
        ]),
      ]),
      "FROM", busca_pedidos.db_tables()['pedidos'],
      "INNER", "JOIN", busca_pedidos.db_tables()['usuarios'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['usuarios'],
          'id'
        ]),
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_user_id',
        ]),
      ]),
      "INNER", "JOIN", busca_pedidos.db_tables()['estabelecimentos'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_company_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['estabelecimentos'],
          'reference_id'
        ]),
      ]),
      "INNER", "JOIN", busca_pedidos.db_tables()['cidades'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['estabelecimentos'],
          'city_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['cidades'],
          'reference_id'
        ]),
      ]),
      "WHERE", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['cidades'], 'deleted_at']), "IS NULL",
    ])

    ## Variáveis que permanecem com o mesmo valor durante todos loops
    pracas = ['total', 'rs', 'ce', 'rj', 'sp']
    anos = ['2015', '2016', '2017', '2018']
#    anos = ['2015', '2016']
    meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#    meses = ['01', '02', '03']
    todos_pedidos = dict()
    for praca in pracas:
      todos_pedidos[praca] = set()
    primeiros_pedidos = dict()
    for praca in pracas:
      primeiros_pedidos[praca] = set()
    segundos_pedidos = dict()
    for praca in pracas:
      segundos_pedidos[praca] = set()
    ultimos_pedidos = dict()
    for praca in pracas:
      ultimos_pedidos[praca] = set()
    dados['resultado'] = list()

    for ano in anos:
      print(log_str.debug(str(ano)))
      ## Variáveis que permanecem com o mesmo valor durante loop de meses
      dados[str(ano)] = dict()
      resultados[str(ano)] = dict()
      dados[str(ano)]['resultado'] = list()

      for mes in meses:
        print(log_str.debug('-'.join([str(ano), str(mes)])))
        ## Variáveis que mudam de valor todo mês
        resultados[str(ano)][str(mes)] = dict()
        for praca in pracas:
          resultados[str(ano)][str(mes)][praca] = dict()

        ## Busca no banco de dados por mês
        dados[str(ano)][str(mes)] = busca_pedidos.transaction_local(" ".join([
          dados['query'],
          "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
          "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
        ]))

        ## Programação dos dados de usuários
        if dados[str(ano)][str(mes)]['status'] and type(dados[str(ano)][str(mes)]['resultado']) == type(list()):
          resultados[str(ano)][str(mes)]['total']['dados'] = dados[str(ano)][str(mes)]['resultado']
          resultados[str(ano)][str(mes)]['total']['primeiro_pedido'] = set([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['resultado'] if pedido['user_id'] not in primeiros_pedidos['total']])
          primeiros_pedidos['total'].update(resultados[str(ano)][str(mes)]['total']['primeiro_pedido'])
          resultados[str(ano)][str(mes)]['total']['segundo_pedido'] = set([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['resultado'] if pedido['user_id'] in todos_pedidos['total'] and pedido['user_id'] in primeiros_pedidos['total'] and pedido['user_id'] not in segundos_pedidos['total']])
          segundos_pedidos['total'].update(resultados[str(ano)][str(mes)]['total']['segundo_pedido'])
          todos_pedidos['total'].update([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['resultado']])
        else:
          print(log_str.info(u"Anota aí: Não consegui encontrar usuários no mês %s do ano %s" % (str(mes), str(ano))))
          dados[str(ano)][str(mes)]['resultado'] = list()
          resultados[str(ano)][str(mes)]['total']['primeiro_pedido'] = set()
          resultados[str(ano)][str(mes)]['total']['segundo_pedido'] = set()
        dados[str(ano)]['resultado'] = dados[str(ano)]['resultado'] + dados[str(ano)][str(mes)]['resultado']
      dados['resultado'] = dados['resultado'] + dados[str(ano)]['resultado']

    ## Iterar ao contrário
    anos.reverse()
    meses.reverse()
    for ano in anos:
      print(log_str.debug(str(ano)))

      for mes in meses:
        print(log_str.debug('-'.join([str(ano), str(mes)])))

        ## Busca no banco de dados por mês
        dados[str(ano)][str(mes)]['inverso'] = busca_pedidos.transaction_local(" ".join([
          dados['query'],
          "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
          "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
        ]))

        ## Programação dos dados de usuários
        if dados[str(ano)][str(mes)]['inverso']['status']:
          resultados[str(ano)][str(mes)]['total']['ultimo_pedido'] = set([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['inverso']['resultado'] if pedido['user_id'] not in ultimos_pedidos['total']])
          ultimos_pedidos['total'].update(resultados[str(ano)][str(mes)]['total']['ultimo_pedido'])
        else:
          print(log_str.info(u"Anota aí: Não consegui encontrar usuários no mês %s do ano %s" % (str(mes), str(ano))))
          resultados[str(ano)][str(mes)]['total']['ultimo_pedido'] = set()
    anos.reverse()
    meses.reverse()

    try:
      usuarios = dict()
      usuarios['total'] = dict()
      for usuario in todos_pedidos['total']:
        usuarios['total'][str(usuario)] = dict()
        usuarios['total'][str(usuario)]['nome'] = [dado['user_name'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
        usuarios['total'][str(usuario)]['praca'] = [dado['city_name'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
        usuarios['total'][str(usuario)]['pedidos'] = len(set([dado['order_id'] for dado in dados['resultado'] if dado['user_id'] == usuario]))
        for ano in anos:
          for mes in meses:
            if usuario in resultados[str(ano)][str(mes)]['total']['primeiro_pedido']:
              usuarios['total'][str(usuario)]['primeiro_pedido'] = "/".join([str(mes),str(ano)])
            if usuario in resultados[str(ano)][str(mes)]['total']['segundo_pedido']:
              usuarios['total'][str(usuario)]['segundo_pedido'] = "/".join([str(mes),str(ano)])
            if usuario in resultados[str(ano)][str(mes)]['total']['ultimo_pedido']:
              usuarios['total'][str(usuario)]['ultimo_pedido'] = "/".join([str(mes),str(ano)])
        if 'segundo_pedido' not in usuarios['total'][str(usuario)]:
          usuarios['total'][str(usuario)]['segundo_pedido'] = usuarios['total'][str(usuario)]['ultimo_pedido']
    except Exception as e:
      args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (str(e)))
      raise
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Erro catastrófico: %s" % (str(e)),
        'debug': log_str.debug(u"Exceção: %s" % (str(e))),
        'parse_mode': None,
      }

    ## Gerar arquivos CSV
    try:
      args['bot'].sendMessage(args['chat_id'], u"Mais um pouco...")
    except Exception as e:
      print(log_str.debug(e))
    ## Dados de usuária(o) por período
    try:
#      ## Arquivo total (abrindo)
##      with open("/tmp/relatorio_%s.csv" % (relatorio), "w") as csvfile:
##        fieldnames = [
##          u"Período",
##          u"Usuária(o) (primeiro pedido)",
##        ]
##        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
##        writer.writeheader()
#      for ano in sorted(resultados.items()):
#        ## Arquivo anual (abrindo)
##        with open("/tmp/relatorio_%s-%s.csv" % (relatorio, str(ano[0])), "w") as csvfile:
##          fieldnames = [
##            u"Período",
##            u"Usuária(o) (primeiro pedido)",
##          ]
##          writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
##          writer.writeheader()
#        for mes in sorted(ano[1].items()):
#          ## Arquivo mensal
#          with open("/tmp/relatorio_%s-%s-%s.csv" % (relatorio, str(ano[0]), str(mes[0])), "w") as csvfile:
#            fieldnames = [
#              u"Período",
#              u"Primeiro pedido",
#              u"Segundo pedido",
#              u"Último pedido",
#            ]
#            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#            writer.writeheader()
#            for primeiro_pedido in mes[1]['total']['primeiro_pedido']:
#              writer.writerow({
#                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
#                'Primeiro pedido': str(primeiro_pedido),
#                'Segundo pedido': '',
#                'Último pedido': '',
#              })
#            for segundo_pedido in mes[1]['total']['segundo_pedido']:
#              writer.writerow({
#                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
#                'Primeiro pedido': '',
#                'Segundo pedido': str(segundo_pedido),
#                'Último pedido': '',
#              })
#            for ultimo_pedido in mes[1]['total']['ultimo_pedido']:
#              writer.writerow({
#                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
#                'Primeiro pedido': '',
#                'Segundo pedido': '',
#                'Último pedido': str(ultimo_pedido),
#              })
#          with open("/tmp/relatorio_%s-%s-%s.csv" % (relatorio, str(ano[0]), str(mes[0])), "r") as csvfile:
#            args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
#          ## Arquivo anual
##          with open("/tmp/relatorio_%s-%s.csv" % (relatorio, str(ano[0])), "a") as csvfile:
##            for primeiro_pedido in mes[1]['total']['primeiro_pedido']:
##              writer.writerow({
##                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
##                'Usuária(o) (primeiro pedido)': str(primeiro_pedido),
##              })
#          ## Arquivo total
##          with open("/tmp/relatorio_%s.csv" % (relatorio), "a") as csvfile:
##            for primeiro_pedido in mes[1]['total']['primeiro_pedido']:
##              writer.writerow({
##                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
##                'Usuária(o) (primeiro pedido)': str(primeiro_pedido),
##              })
#        ## Arquivo anual (fechando)
##        with open("/tmp/relatorio_%s-%s.csv" % (relatorio, str(ano[0])), "r") as csvfile:
##          args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
#      ## Arquivo total (fechando)
##      with open("/tmp/relatorio_%s.csv" % (relatorio, str(ano[0]), str(mes[0])), "r") as csvfile:
##        args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))

      with open("/tmp/relatorio_%s.csv" % (relatorio), "w") as csvfile:
        fieldnames = [
          u"Usuária(o)",
          u"Praça",
          u"Pedidos",
          u"Primeiro pedido",
          u"Segundo pedido",
          u"Último pedido",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for usuario in sorted(usuarios['total'].items()):
          writer.writerow({
            'Usuária(o)': usuario[1]['nome'],
            'Praça': usuario[1]['praca'],
            'Pedidos': usuario[1]['pedidos'],
            'Primeiro pedido': usuario[1]['primeiro_pedido'],
            'Segundo pedido': usuario[1]['segundo_pedido'],
            'Último pedido': usuario[1]['ultimo_pedido'],
          })
        with open("/tmp/relatorio_%s.csv" % (relatorio), "r") as csvfile:
          args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
    except Exception as e:
      args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (str(e)))
      raise
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Erro catastrófico: %s" % (str(e)),
        'debug': log_str.debug(u"Exceção: %s" % (str(e))),
        'parse_mode': None,
      }

  except Exception as e:
    args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (str(e)))
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u"Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.",
      'debug': log_str.debug(u"Exceção: %s" % (str(e))),
      'parse_mode': None,
    }

## TODO arrumar a função pra todo e qualquer caso e renomear pra usuarios_unicos
def usuarios_unicos_1(args):
  ano_inicial = "2015"
  ano_final = "2018"
  mes_inicial = "12"
  mes_final = "08"
  try:
    if args['command_list'][0].isdigit() and args['command_list'][1].isdigit() and args['command_list'][2].isdigit() and args['command_list'][3].isdigit():
      mes_inicial = str(args['command_list'][0])
      ano_inicial = str(args['command_list'][1])
      mes_final = str(args['command_list'][2])
      ano_final = str(args['command_list'][3])
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u"Formato correto do comando:\n/relatorio_usuarios_unicos 12 2015 08 2018\n\nonde '12' é o mês inicial;\n'2015' é o ano inicial;\n'08' é o mês final;'2018' é o ano final.\n\nNeste exemplo, o período fornecido é de dezembro de 2015 a agosto de 2018.",
        'debug': log_str.debug(u"Exceção: %s" % (str(e))),
        'parse_mode': None,
      }
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u"Formato correto do comando:\n/relatorio_usuarios_unicos 12 2015 08 2018\n\nonde '12' é o mês inicial;\n'2015' é o ano inicial;\n'08' é o mês final;'2018' é o ano final.\n\nNeste exemplo, o período fornecido é de dezembro de 2015 a agosto de 2018.",
      'debug': log_str.debug(u"Exceção: %s" % (str(e))),
      'parse_mode': None,
    }

  relatorio = inspect.currentframe().f_code.co_name
  ## Usuária(o)s única(o)s por período
  try:
    args['bot'].sendMessage(args['chat_id'], u"Calculando %s..." % (relatorio))
  except Exception as e:
    print(log_str.debug(e))
  resultados = dict()

  try:
    ## SQL query
    dados = dict()
    dados['query'] = " ".join([
      "SELECT", ",".join([
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'reference_id']),
          "AS", 'order_id',
        ]),
        ".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']),
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'order_user_id']),
          "AS", 'user_id',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['usuarios'], 'name']),
          "AS", 'user_name',
        ]),
        ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'city_id']),
        " ".join([
          ".".join([busca_pedidos.db_tables()['cidades'], 'name']) ,
          "AS", 'city_name',
        ]),
      ]),
      "FROM", busca_pedidos.db_tables()['pedidos'],
      "INNER", "JOIN", busca_pedidos.db_tables()['usuarios'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['usuarios'],
          'id'
        ]),
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_user_id',
        ]),
      ]),
      "INNER", "JOIN", busca_pedidos.db_tables()['estabelecimentos'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_company_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['estabelecimentos'],
          'reference_id'
        ]),
      ]),
      "INNER", "JOIN", busca_pedidos.db_tables()['cidades'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['estabelecimentos'],
          'city_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['cidades'],
          'reference_id'
        ]),
      ]),
      "WHERE", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['cidades'], 'deleted_at']), "IS NULL",
    ])

    ## Busca no banco de dados por período
    dados = busca_pedidos.transaction_local(" ".join([
      dados['query'],
      "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano_inicial), "-", str(mes_inicial), "-01 00:00:00", "'"])]),
      "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano_final), "-", str(mes_final), "-31 23:59:59", "'"])]),
    ]))

    ## Programação dos dados
    if dados['status']:
      todos_pedidos = set([pedido['order_id'] for pedido in dados['resultado']])
      usuarios_unicos = set([usuario['user_id'] for usuario in dados['resultado']])

      response = list()
      response.append(u"Período: de %s de %s a %s de %s" % (str(mes_inicial), str(ano_inicial), str(mes_final), str(ano_final)))
      response.append(u"")
      response.append(u"Total de pedidos no período: %s" % (str(len(todos_pedidos))))
      response.append(u"Usuária(o)s única(o)s no período: %s" % (str(len(usuarios_unicos))))
      response.append(u"")
      response.append(u"Ou seja, neste período, a média é de %s pedidos por usuária(o)." % ("{:2.2f}".format(float(len(todos_pedidos)/len(usuarios_unicos)))))

      return {
        'status': True,
        'type': 'grupo',
        'multi': False,
        'destino': 'telegram',
        'response': "\n".join(response),
        'debug': u"Deu certo!",
        'parse_mode': None,
      }

  except Exception as e:
    args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (str(e)))
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u"Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.",
      'debug': log_str.debug(u"Exceção: %s" % (str(e))),
      'parse_mode': None,
    }

def vendas_soma(args):
  locale.setlocale(locale.LC_ALL,'')
  ano_inicial = "2015"
  ano_final = "2018"
  mes_inicial = "12"
  mes_final = "08"
  try:
    if args['command_list'][0].isdigit() and args['command_list'][1].isdigit() and args['command_list'][2].isdigit() and args['command_list'][3].isdigit():
      mes_inicial = str(args['command_list'][0])
      ano_inicial = str(args['command_list'][1])
      mes_final = str(args['command_list'][2])
      ano_final = str(args['command_list'][3])
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u"Formato correto do comando:\n/%s 12 2015 08 2018\n\nonde '12' é o mês inicial;\n'2015' é o ano inicial;\n'08' é o mês final;'2018' é o ano final.\n\nNeste exemplo, o período fornecido é de dezembro de 2015 a agosto de 2018." % (str(args['relatorio'])),
        'debug': log_str.debug(u"Exceção: %s" % (str(e))),
        'parse_mode': None,
      }
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u"Formato correto do comando:\n/%s 12 2015 08 2018\n\nonde '12' é o mês inicial;\n'2015' é o ano inicial;\n'08' é o mês final;'2018' é o ano final.\n\nNeste exemplo, o período fornecido é de dezembro de 2015 a agosto de 2018." % (str(args['relatorio'])),
      'debug': log_str.debug(u"Exceção: %s" % (str(e))),
      'parse_mode': None,
    }

  try:
    args['bot'].sendMessage(args['chat_id'], u"Calculando %s..." % (str(args['relatorio'])))
  except Exception as e:
    print(log_str.debug(e))
  resultados = dict()

  try:
    ## SQL query
    dados = dict()
    dados['query'] = " ".join([
      "SELECT", ",".join([
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'reference_id']),
          "AS", 'order_id',
        ]),
        ".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']),
        ".".join([busca_pedidos.db_tables()['pedidos'], 'delivery_price']),
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'order_user_id']),
          "AS", 'user_id',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['usuarios'], 'name']),
          "AS", 'user_name',
        ]),
        ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'city_id']),
        " ".join([
          ".".join([busca_pedidos.db_tables()['cidades'], 'name']) ,
          "AS", 'city_name',
        ]),
      ]),
      "FROM", busca_pedidos.db_tables()['pedidos'],
      "INNER", "JOIN", busca_pedidos.db_tables()['usuarios'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['usuarios'],
          'id'
        ]),
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_user_id',
        ]),
      ]),
      "INNER", "JOIN", busca_pedidos.db_tables()['estabelecimentos'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_company_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['estabelecimentos'],
          'reference_id'
        ]),
      ]),
      "INNER", "JOIN", busca_pedidos.db_tables()['cidades'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['estabelecimentos'],
          'city_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['cidades'],
          'reference_id'
        ]),
      ]),
      "WHERE", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['cidades'], 'deleted_at']), "IS NULL",
    ])

    ## Busca no banco de dados por período
    dados = busca_pedidos.transaction_local(" ".join([
      dados['query'],
      "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano_inicial), "-", str(mes_inicial), "-01 00:00:00", "'"])]),
      "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano_final), "-", str(mes_final), "-31 23:59:59", "'"])]),
    ]))

    ## Programação dos dados
    if dados['status']:
      todos_pedidos = dict()
      todos_pedidos['total'] = set([pedido['order_id'] for pedido in dados['resultado']])
      todos_pedidos['rs'] = set([pedido['order_id'] for pedido in dados['resultado'] if str(pedido['city_id']) == str(7994)])
      todos_pedidos['ce'] = set([pedido['order_id'] for pedido in dados['resultado'] if str(pedido['city_id']) == str(1347)])
      todos_pedidos['rj'] = set([pedido['order_id'] for pedido in dados['resultado'] if str(pedido['city_id']) == str(7043)])
      todos_pedidos['sp'] = set([pedido['order_id'] for pedido in dados['resultado'] if str(pedido['city_id']) == str(13649)])
      usuarios_unicos = dict()
      usuarios_unicos['total'] = set([usuario['user_id'] for usuario in dados['resultado']])
      usuarios_unicos['rs'] = set([usuario['user_id'] for usuario in dados['resultado'] if str(usuario['city_id']) == str(7994)])
      usuarios_unicos['ce'] = set([usuario['user_id'] for usuario in dados['resultado'] if str(usuario['city_id']) == str(1347)])
      usuarios_unicos['rj'] = set([usuario['user_id'] for usuario in dados['resultado'] if str(usuario['city_id']) == str(7043)])
      usuarios_unicos['sp'] = set([usuario['user_id'] for usuario in dados['resultado'] if str(usuario['city_id']) == str(13649)])

      valores_totais = dict()
      valores_totais['total'] = list()
      valores_totais['rs'] = list()
      valores_totais['ce'] = list()
      valores_totais['rj'] = list()
      valores_totais['sp'] = list()
      teleentrega_totais = dict()
      teleentrega_totais['total'] = list()
      teleentrega_totais['rs'] = list()
      teleentrega_totais['ce'] = list()
      teleentrega_totais['rj'] = list()
      teleentrega_totais['sp'] = list()
      for pedido in dados['resultado']:
        ## Busca dados de preço do produto, seus adicionais e opcionais (items não têm preço)
        ## É utilizado o preço do produto do pedido, que é imutável, e não o preço atual do produto. O mesmo pode ser afirmado acerca dos adicionais e opcionais.
        pedido['query'] = " ".join([
          "SELECT", ",".join([
            " ".join([
              ".".join([busca_pedidos.db_tables()['produtos_pedido'], 'price']),
              "AS", 'product_price',
            ]),
            " ".join([
              ".".join([busca_pedidos.db_tables()['produto_opcionais_pedido'], 'price']),
              "AS", 'option_price',
            ]),
            " ".join([
              ".".join([busca_pedidos.db_tables()['produto_adicionais_pedido'], 'price']),
              "AS", 'additional_price',
            ]),
          ]),
          "FROM", busca_pedidos.db_tables()['produtos_pedido'],
          "LEFT", "JOIN", busca_pedidos.db_tables()['produto_opcionais_pedido'],
          "ON", "=".join([
            ".".join([
              busca_pedidos.db_tables()['produto_opcionais_pedido'],
              'order_request_product_id',
            ]),
            ".".join([
              busca_pedidos.db_tables()['produtos_pedido'],
              'reference_id'
            ]),
          ]),
          "LEFT", "JOIN", busca_pedidos.db_tables()['produto_adicionais_pedido'],
          "ON", "=".join([
            ".".join([
              busca_pedidos.db_tables()['produto_adicionais_pedido'],
              'order_request_product_id',
            ]),
            ".".join([
              busca_pedidos.db_tables()['produtos_pedido'],
              'reference_id'
            ]),
          ]),
          "WHERE", "=".join([
            ".".join([
              busca_pedidos.db_tables()['produtos_pedido'],
              'order_request_id',
            ]),
            str(pedido['order_id']),
          ]),
          "AND", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
          "AND", ".".join([busca_pedidos.db_tables()['produtos_pedido'], 'deleted_at']), "IS NULL",
          "AND", ".".join([busca_pedidos.db_tables()['produto_adicionais_pedido'], 'deleted_at']), "IS NULL",
          "AND", ".".join([busca_pedidos.db_tables()['produto_opcionais_pedido'], 'deleted_at']), "IS NULL",
        ])

        produtos_pedido = busca_pedidos.transaction_local(" ".join([
          pedido['query'],
        ]))

        ## Calcula dados de preços caso a requisição seja sucedida
        if len(produtos_pedido['response']) > 0:
          teleentrega_totais['total'].append(float(pedido['delivery_price']))
          valor_total = float()
          for produto_pedido in produtos_pedido['response']:
            valor_total = valor_total + float(produto_pedido['product_price'] or 0.0)
            valor_total = valor_total + float(produto_pedido['additional_price'] or 0.0)
            valor_total = valor_total + float(produto_pedido['option_price'] or 0.0)
          valores_totais['total'].append(valor_total)
          ## Acrescenta aos totais de tele entrega
          if str(pedido['city_id']) == str(7994):
            teleentrega_totais['rs'].append(float(pedido['delivery_price']))
            valores_totais['rs'].append(valor_total)
          elif str(pedido['city_id']) == str(1347):
            teleentrega_totais['ce'].append(float(pedido['delivery_price']))
            valores_totais['ce'].append(valor_total)
          elif str(pedido['city_id']) == str(7043):
            teleentrega_totais['rj'].append(float(pedido['delivery_price']))
            valores_totais['rj'].append(valor_total)
          elif str(pedido['city_id']) == str(13649):
            teleentrega_totais['sp'].append(float(pedido['delivery_price']))
            valores_totais['sp'].append(valor_total)
        else:
          print(log_str.err(u"Não consegui pesquisar dados do pedido número %s" % (str(pedido['order_id']))))

      print(log_str.info(u"Todos pedidos processados! Somando tudo..."))
      valor_todos_pedidos = dict()
      valor_todos_pedidos['total'] = float()
      valor_todos_pedidos['rs'] = float()
      valor_todos_pedidos['ce'] = float()
      valor_todos_pedidos['rj'] = float()
      valor_todos_pedidos['sp'] = float()
      for valores_total in valores_totais['total']:
        valor_todos_pedidos['total'] = valor_todos_pedidos['total'] + float(valores_total)
      for valores_total in valores_totais['rs']:
        valor_todos_pedidos['rs'] = valor_todos_pedidos['rs'] + float(valores_total)
      for valores_total in valores_totais['ce']:
        valor_todos_pedidos['ce'] = valor_todos_pedidos['ce'] + float(valores_total)
      for valores_total in valores_totais['rj']:
        valor_todos_pedidos['rj'] = valor_todos_pedidos['rj'] + float(valores_total)
      for valores_total in valores_totais['sp']:
        valor_todos_pedidos['sp'] = valor_todos_pedidos['sp'] + float(valores_total)
      teleentrega_todos_pedidos = dict()
      teleentrega_todos_pedidos['total'] = float()
      teleentrega_todos_pedidos['rs'] = float()
      teleentrega_todos_pedidos['ce'] = float()
      teleentrega_todos_pedidos['rj'] = float()
      teleentrega_todos_pedidos['sp'] = float()
      for teleentrega_total in teleentrega_totais['total']:
        teleentrega_todos_pedidos['total'] = teleentrega_todos_pedidos['total'] + float(teleentrega_total)
      for teleentrega_total in teleentrega_totais['rs']:
        teleentrega_todos_pedidos['rs'] = teleentrega_todos_pedidos['rs'] + float(teleentrega_total)
      for teleentrega_total in teleentrega_totais['ce']:
        teleentrega_todos_pedidos['ce'] = teleentrega_todos_pedidos['ce'] + float(teleentrega_total)
      for teleentrega_total in teleentrega_totais['rj']:
        teleentrega_todos_pedidos['rj'] = teleentrega_todos_pedidos['rj'] + float(teleentrega_total)
      for teleentrega_total in teleentrega_totais['sp']:
        teleentrega_todos_pedidos['sp'] = teleentrega_todos_pedidos['sp'] + float(teleentrega_total)

      response = list()
      response.append(u"Período: de %s de %s a %s de %s" % (str(mes_inicial), str(ano_inicial), str(mes_final), str(ano_final)))
      response.append(u"")
      response.append(u"Total de pedidos no período: %s" % (str(len(todos_pedidos['total']))))
      response.append(u"Usuária(o)s única(o)s no período: %s" % (str(len(usuarios_unicos['total']))))
      response.append(u"")
      response.append(u"Ou seja, neste período, a média é de %s pedidos por usuária(o)." % ("{:2.2f}".format(float(len(todos_pedidos['total'])/len(usuarios_unicos['total'])))))
      response.append(u"")
      response.append(u"A soma em reais brasileiros de todos os pedidos feitos no Velivery que não foram excluídos durante o período é de: %s" % (str(locale.currency(valor_todos_pedidos['total']))))
      response.append("")
      response.append(u"O total de dinheiro para tele entregas para os pedidos do periodo é de %s. Ou seja, a soma de todos pedidos mais tele entrega é de %s." % (str(locale.currency(teleentrega_todos_pedidos['total'])), str(locale.currency(valor_todos_pedidos['total'] + teleentrega_todos_pedidos['total']))))
      response.append("")
      response.append(u"Ticket médio do período: %s, com a taxa de tele entrega: %s" % (str(locale.currency(float(valor_todos_pedidos['total']/len(todos_pedidos['total'])))), str(locale.currency(float((valor_todos_pedidos['total'] + teleentrega_todos_pedidos['total'])/len(todos_pedidos['total']))))))
      response.append("")
      response.append(u"Total de pedidos que entraram neste cálculo: %s" % (str(len(dados['resultado']))))

      response.append('$$$EOF$$$')
      response.append(u"Praça: Porto Alegre")
      response.append(u"")
      response.append(u"Total de pedidos na praça no período: %s (%s%%)" % (str(len(todos_pedidos['rs'])), "{:2.2f}".format(float((100.0*len(todos_pedidos['rs']))/len(todos_pedidos['total'])))))
      response.append(u"Usuária(o)s única(o)s na praça no período: %s (%s%%)" % (str(len(usuarios_unicos['rs'])), "{:2.2f}".format(float((100.0*len(usuarios_unicos['rs']))/len(usuarios_unicos['total'])))))
      response.append(u"")
      response.append(u"Ou seja, neste período e praça, a média é de %s pedidos por usuária(o)." % ("{:2.2f}".format(float(len(todos_pedidos['rs'])/len(usuarios_unicos['rs'])))))
      response.append(u"")
      response.append(u"A soma em reais brasileiros de todos os pedidos feitos no Velivery nesta praça que não foram excluídos durante o período é de: %s (%s%%)" % (str(locale.currency(valor_todos_pedidos['rs'])), "{:2.2f}".format(float((100.0*valor_todos_pedidos['rs'])/valor_todos_pedidos['total']))))
      response.append("")
      response.append(u"O total de dinheiro para tele entregas para os pedidos neste período e praça é de %s. Ou seja, a soma de todos pedidos mais tele entrega é de %s." % (str(locale.currency(teleentrega_todos_pedidos['rs'])), str(locale.currency(valor_todos_pedidos['rs'] + teleentrega_todos_pedidos['rs']))))
      response.append("")
      response.append(u"Ticket médio na praça no período: %s, com a taxa de tele entrega: %s" % (str(locale.currency(float(valor_todos_pedidos['rs']/len(todos_pedidos['rs'])))), str(locale.currency(float((valor_todos_pedidos['rs'] + teleentrega_todos_pedidos['rs'])/len(todos_pedidos['rs']))))))

      response.append('$$$EOF$$$')
      response.append(u"Praça: Fortaleza")
      response.append(u"")
      response.append(u"Total de pedidos na praça no período: %s (%s%%)" % (str(len(todos_pedidos['ce'])), "{:2.2f}".format(float((100.0*len(todos_pedidos['ce']))/len(todos_pedidos['total'])))))
      response.append(u"Usuária(o)s única(o)s na praça no período: %s (%s%%)" % (str(len(usuarios_unicos['ce'])), "{:2.2f}".format(float((100.0*len(usuarios_unicos['ce']))/len(usuarios_unicos['total'])))))
      response.append(u"")
      response.append(u"Ou seja, neste período e praça, a média é de %s pedidos por usuária(o)." % ("{:2.2f}".format(float(len(todos_pedidos['ce'])/len(usuarios_unicos['ce'])))))
      response.append(u"")
      response.append(u"A soma em reais brasileiros de todos os pedidos feitos no Velivery nesta praça que não foram excluídos durante o período é de: %s (%s%%)" % (str(locale.currency(valor_todos_pedidos['ce'])), "{:2.2f}".format(float((100.0*valor_todos_pedidos['ce'])/valor_todos_pedidos['total']))))
      response.append("")
      response.append(u"O total de dinheiro para tele entregas para os pedidos neste período e praça é de %s. Ou seja, a soma de todos pedidos mais tele entrega é de %s." % (str(locale.currency(teleentrega_todos_pedidos['ce'])), str(locale.currency(valor_todos_pedidos['ce'] + teleentrega_todos_pedidos['ce']))))
      response.append("")
      response.append(u"Ticket médio na praça no período: %s, com a taxa de tele entrega: %s" % (str(locale.currency(float(valor_todos_pedidos['ce']/len(todos_pedidos['ce'])))), str(locale.currency(float((valor_todos_pedidos['ce'] + teleentrega_todos_pedidos['ce'])/len(todos_pedidos['ce']))))))

      response.append('$$$EOF$$$')
      response.append(u"Praça: Rio de Janeiro")
      response.append(u"")
      response.append(u"Total de pedidos na praça no período: %s (%s%%)" % (str(len(todos_pedidos['rj'])), "{:2.2f}".format(float((100.0*len(todos_pedidos['rj']))/len(todos_pedidos['total'])))))
      response.append(u"Usuária(o)s única(o)s na praça no período: %s (%s%%)" % (str(len(usuarios_unicos['rj'])), "{:2.2f}".format(float((100.0*len(usuarios_unicos['rj']))/len(usuarios_unicos['total'])))))
      response.append(u"")
      response.append(u"Ou seja, neste período e praça, a média é de %s pedidos por usuária(o)." % ("{:2.2f}".format(float(len(todos_pedidos['rj'])/len(usuarios_unicos['rj'])))))
      response.append(u"")
      response.append(u"A soma em reais brasileiros de todos os pedidos feitos no Velivery nesta praça que não foram excluídos durante o período é de: %s (%s%%)" % (str(locale.currency(valor_todos_pedidos['rj'])), "{:2.2f}".format(float((100.0*valor_todos_pedidos['rj'])/valor_todos_pedidos['total']))))
      response.append("")
      response.append(u"O total de dinheiro para tele entregas para os pedidos neste período e praça é de %s. Ou seja, a soma de todos pedidos mais tele entrega é de %s." % (str(locale.currency(teleentrega_todos_pedidos['rj'])), str(locale.currency(valor_todos_pedidos['rj'] + teleentrega_todos_pedidos['rj']))))
      response.append("")
      response.append(u"Ticket médio na praça no período: %s, com a taxa de tele entrega: %s" % (str(locale.currency(float(valor_todos_pedidos['rj']/len(todos_pedidos['rj'])))), str(locale.currency(float((valor_todos_pedidos['rj'] + teleentrega_todos_pedidos['rj'])/len(todos_pedidos['rj']))))))

      response.append('$$$EOF$$$')
      response.append(u"Praça: São Paulo")
      response.append(u"")
      response.append(u"Total de pedidos na praça no período: %s (%s%%)" % (str(len(todos_pedidos['sp'])), "{:2.2f}".format(float((100.0*len(todos_pedidos['sp']))/len(todos_pedidos['total'])))))
      response.append(u"Usuária(o)s única(o)s na praça no período: %s (%s%%)" % (str(len(usuarios_unicos['sp'])), "{:2.2f}".format(float((100.0*len(usuarios_unicos['sp']))/len(usuarios_unicos['total'])))))
      response.append(u"")
      response.append(u"Ou seja, neste período e praça, a média é de %s pedidos por usuária(o)." % ("{:2.2f}".format(float(len(todos_pedidos['sp'])/len(usuarios_unicos['sp'])))))
      response.append(u"")
      response.append(u"A soma em reais brasileiros de todos os pedidos feitos no Velivery nesta praça que não foram excluídos durante o período é de: %s (%s%%)" % (str(locale.currency(valor_todos_pedidos['sp'])), "{:2.2f}".format(float((100.0*valor_todos_pedidos['sp'])/valor_todos_pedidos['total']))))
      response.append("")
      response.append(u"O total de dinheiro para tele entregas para os pedidos neste período e praça é de %s. Ou seja, a soma de todos pedidos mais tele entrega é de %s." % (str(locale.currency(teleentrega_todos_pedidos['sp'])), str(locale.currency(valor_todos_pedidos['sp'] + teleentrega_todos_pedidos['sp']))))
      response.append("")
      response.append(u"Ticket médio na praça no período: %s, com a taxa de tele entrega: %s" % (str(locale.currency(float(valor_todos_pedidos['sp']/len(todos_pedidos['sp'])))), str(locale.currency(float((valor_todos_pedidos['sp'] + teleentrega_todos_pedidos['sp'])/len(todos_pedidos['sp']))))))

      return {
        'status': True,
        'type': 'grupo',
        'multi': True,
        'destino': 'telegram',
        'response': "\n".join(response),
        'debug': u"Deu certo!",
        'parse_mode': None,
      }

  except Exception as e:
    args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (str(e)))
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u"Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.",
      'debug': log_str.debug(u"Exceção: %s" % (str(e))),
      'parse_mode': None,
    }

def vendas_csv(args):
  relatorio = inspect.currentframe().f_code.co_name
  ## Taxa de recompra
  ## Data do primeiro pedido
  try:
    args['bot'].sendMessage(args['chat_id'], u"Calculando %s..." % (relatorio))
  except Exception as e:
    print(log_str.debug(e))
  resultados = dict()

  try:
    ## SQL query
    dados = dict()
    dados['query'] = " ".join([
      "SELECT", ",".join([
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'reference_id']),
          "AS", 'order_id',
        ]),
        ".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']),
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'order_user_id']),
          "AS", 'user_id',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['usuarios'], 'name']),
          "AS", 'user_name',
        ]),
        ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'city_id']),
        " ".join([
          ".".join([busca_pedidos.db_tables()['cidades'], 'name']) ,
          "AS", 'city_name',
        ]),
      ]),
      "FROM", busca_pedidos.db_tables()['pedidos'],
      "INNER", "JOIN", busca_pedidos.db_tables()['usuarios'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['usuarios'],
          'id'
        ]),
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_user_id',
        ]),
      ]),
      "INNER", "JOIN", busca_pedidos.db_tables()['estabelecimentos'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_company_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['estabelecimentos'],
          'reference_id'
        ]),
      ]),
      "INNER", "JOIN", busca_pedidos.db_tables()['cidades'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['estabelecimentos'],
          'city_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['cidades'],
          'reference_id'
        ]),
      ]),
      "WHERE", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['cidades'], 'deleted_at']), "IS NULL",
    ])

    ## Variáveis que permanecem com o mesmo valor durante todos loops
    pracas = ['total', 'rs', 'ce', 'rj', 'sp']
    anos = ['2015', '2016', '2017', '2018']
#    anos = ['2015', '2016']
    meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#    meses = ['01', '02', '03']
    todos_pedidos = dict()
    for praca in pracas:
      todos_pedidos[praca] = set()
    primeiros_pedidos = dict()
    for praca in pracas:
      primeiros_pedidos[praca] = set()
    segundos_pedidos = dict()
    for praca in pracas:
      segundos_pedidos[praca] = set()
    ultimos_pedidos = dict()
    for praca in pracas:
      ultimos_pedidos[praca] = set()
    dados['resultado'] = list()

    for ano in anos:
      print(log_str.debug(str(ano)))
      ## Variáveis que permanecem com o mesmo valor durante loop de meses
      dados[str(ano)] = dict()
      resultados[str(ano)] = dict()
      dados[str(ano)]['resultado'] = list()

      for mes in meses:
        print(log_str.debug('-'.join([str(ano), str(mes)])))
        ## Variáveis que mudam de valor todo mês
        resultados[str(ano)][str(mes)] = dict()
        for praca in pracas:
          resultados[str(ano)][str(mes)][praca] = dict()

        ## Busca no banco de dados por mês
        dados[str(ano)][str(mes)] = busca_pedidos.transaction_local(" ".join([
          dados['query'],
          "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
          "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
        ]))

        ## Programação dos dados de usuários
        if dados[str(ano)][str(mes)]['status'] and type(dados[str(ano)][str(mes)]['resultado']) == type(list()):
          resultados[str(ano)][str(mes)]['total']['dados'] = dados[str(ano)][str(mes)]['resultado']
          resultados[str(ano)][str(mes)]['total']['primeiro_pedido'] = set([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['resultado'] if pedido['user_id'] not in primeiros_pedidos['total']])
          primeiros_pedidos['total'].update(resultados[str(ano)][str(mes)]['total']['primeiro_pedido'])
          resultados[str(ano)][str(mes)]['total']['segundo_pedido'] = set([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['resultado'] if pedido['user_id'] in todos_pedidos['total'] and pedido['user_id'] in primeiros_pedidos['total'] and pedido['user_id'] not in segundos_pedidos['total']])
          segundos_pedidos['total'].update(resultados[str(ano)][str(mes)]['total']['segundo_pedido'])
          todos_pedidos['total'].update([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['resultado']])
        else:
          print(log_str.info(u"Anota aí: Não consegui encontrar usuários no mês %s do ano %s" % (str(mes), str(ano))))
          dados[str(ano)][str(mes)]['resultado'] = list()
          resultados[str(ano)][str(mes)]['total']['primeiro_pedido'] = set()
          resultados[str(ano)][str(mes)]['total']['segundo_pedido'] = set()
        dados[str(ano)]['resultado'] = dados[str(ano)]['resultado'] + dados[str(ano)][str(mes)]['resultado']
      dados['resultado'] = dados['resultado'] + dados[str(ano)]['resultado']

    ## Iterar ao contrário
    anos.reverse()
    meses.reverse()
    for ano in anos:
      print(log_str.debug(str(ano)))

      for mes in meses:
        print(log_str.debug('-'.join([str(ano), str(mes)])))

        ## Busca no banco de dados por mês
        dados[str(ano)][str(mes)]['inverso'] = busca_pedidos.transaction_local(" ".join([
          dados['query'],
          "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
          "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
        ]))

        ## Programação dos dados de usuários
        if dados[str(ano)][str(mes)]['inverso']['status']:
          resultados[str(ano)][str(mes)]['total']['ultimo_pedido'] = set([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['inverso']['resultado'] if pedido['user_id'] not in ultimos_pedidos['total']])
          ultimos_pedidos['total'].update(resultados[str(ano)][str(mes)]['total']['ultimo_pedido'])
        else:
          print(log_str.info(u"Anota aí: Não consegui encontrar usuários no mês %s do ano %s" % (str(mes), str(ano))))
          resultados[str(ano)][str(mes)]['total']['ultimo_pedido'] = set()
    anos.reverse()
    meses.reverse()

    try:
      usuarios = dict()
      usuarios['total'] = dict()
      for usuario in todos_pedidos['total']:
        usuarios['total'][str(usuario)] = dict()
        usuarios['total'][str(usuario)]['nome'] = [dado['user_name'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
        usuarios['total'][str(usuario)]['praca'] = [dado['city_name'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
        usuarios['total'][str(usuario)]['pedidos'] = len(set([dado['order_id'] for dado in dados['resultado'] if dado['user_id'] == usuario]))
        for ano in anos:
          for mes in meses:
            if usuario in resultados[str(ano)][str(mes)]['total']['primeiro_pedido']:
              usuarios['total'][str(usuario)]['primeiro_pedido'] = "/".join([str(mes),str(ano)])
            if usuario in resultados[str(ano)][str(mes)]['total']['segundo_pedido']:
              usuarios['total'][str(usuario)]['segundo_pedido'] = "/".join([str(mes),str(ano)])
            if usuario in resultados[str(ano)][str(mes)]['total']['ultimo_pedido']:
              usuarios['total'][str(usuario)]['ultimo_pedido'] = "/".join([str(mes),str(ano)])
        if 'segundo_pedido' not in usuarios['total'][str(usuario)]:
          usuarios['total'][str(usuario)]['segundo_pedido'] = usuarios['total'][str(usuario)]['ultimo_pedido']
    except Exception as e:
      args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (str(e)))
      raise
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Erro catastrófico: %s" % (str(e)),
        'debug': log_str.debug(u"Exceção: %s" % (str(e))),
        'parse_mode': None,
      }

    ## Gerar arquivos CSV
    try:
      args['bot'].sendMessage(args['chat_id'], u"Mais um pouco...")
    except Exception as e:
      print(log_str.debug(e))
    ## Dados de usuária(o) por período
    try:
#      ## Arquivo total (abrindo)
##      with open("/tmp/relatorio_%s.csv" % (relatorio), "w") as csvfile:
##        fieldnames = [
##          u"Período",
##          u"Usuária(o) (primeiro pedido)",
##        ]
##        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
##        writer.writeheader()
#      for ano in sorted(resultados.items()):
#        ## Arquivo anual (abrindo)
##        with open("/tmp/relatorio_%s-%s.csv" % (relatorio, str(ano[0])), "w") as csvfile:
##          fieldnames = [
##            u"Período",
##            u"Usuária(o) (primeiro pedido)",
##          ]
##          writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
##          writer.writeheader()
#        for mes in sorted(ano[1].items()):
#          ## Arquivo mensal
#          with open("/tmp/relatorio_%s-%s-%s.csv" % (relatorio, str(ano[0]), str(mes[0])), "w") as csvfile:
#            fieldnames = [
#              u"Período",
#              u"Primeiro pedido",
#              u"Segundo pedido",
#              u"Último pedido",
#            ]
#            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#            writer.writeheader()
#            for primeiro_pedido in mes[1]['total']['primeiro_pedido']:
#              writer.writerow({
#                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
#                'Primeiro pedido': str(primeiro_pedido),
#                'Segundo pedido': '',
#                'Último pedido': '',
#              })
#            for segundo_pedido in mes[1]['total']['segundo_pedido']:
#              writer.writerow({
#                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
#                'Primeiro pedido': '',
#                'Segundo pedido': str(segundo_pedido),
#                'Último pedido': '',
#              })
#            for ultimo_pedido in mes[1]['total']['ultimo_pedido']:
#              writer.writerow({
#                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
#                'Primeiro pedido': '',
#                'Segundo pedido': '',
#                'Último pedido': str(ultimo_pedido),
#              })
#          with open("/tmp/relatorio_%s-%s-%s.csv" % (relatorio, str(ano[0]), str(mes[0])), "r") as csvfile:
#            args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
#          ## Arquivo anual
##          with open("/tmp/relatorio_%s-%s.csv" % (relatorio, str(ano[0])), "a") as csvfile:
##            for primeiro_pedido in mes[1]['total']['primeiro_pedido']:
##              writer.writerow({
##                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
##                'Usuária(o) (primeiro pedido)': str(primeiro_pedido),
##              })
#          ## Arquivo total
##          with open("/tmp/relatorio_%s.csv" % (relatorio), "a") as csvfile:
##            for primeiro_pedido in mes[1]['total']['primeiro_pedido']:
##              writer.writerow({
##                'Período': u"%s/%s" % (str(mes[0]), str(ano[0])),
##                'Usuária(o) (primeiro pedido)': str(primeiro_pedido),
##              })
#        ## Arquivo anual (fechando)
##        with open("/tmp/relatorio_%s-%s.csv" % (relatorio, str(ano[0])), "r") as csvfile:
##          args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
#      ## Arquivo total (fechando)
##      with open("/tmp/relatorio_%s.csv" % (relatorio, str(ano[0]), str(mes[0])), "r") as csvfile:
##        args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))

      with open("/tmp/relatorio_%s.csv" % (relatorio), "w") as csvfile:
        fieldnames = [
          u"Usuária(o)",
          u"Praça",
          u"Pedidos",
          u"Primeiro pedido",
          u"Segundo pedido",
          u"Último pedido",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for usuario in sorted(usuarios['total'].items()):
          writer.writerow({
            'Usuária(o)': usuario[1]['nome'],
            'Praça': usuario[1]['praca'],
            'Pedidos': usuario[1]['pedidos'],
            'Primeiro pedido': usuario[1]['primeiro_pedido'],
            'Segundo pedido': usuario[1]['segundo_pedido'],
            'Último pedido': usuario[1]['ultimo_pedido'],
          })
        with open("/tmp/relatorio_%s.csv" % (relatorio), "r") as csvfile:
          args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
    except Exception as e:
      args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (str(e)))
      raise
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u"Erro catastrófico: %s" % (str(e)),
        'debug': log_str.debug(u"Exceção: %s" % (str(e))),
        'parse_mode': None,
      }

  except Exception as e:
    args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (str(e)))
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u"Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.",
      'debug': log_str.debug(u"Exceção: %s" % (str(e))),
      'parse_mode': None,
    }

