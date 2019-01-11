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

## TODO método não é mais utilizado, usar o lista_mailing_csv_2
def lista_mailing_csv_1(args):
#  relatorio = inspect.currentframe().f_code.co_name
  relatorio = args['relatorio']
  try:
    args['bot'].sendMessage(args['chat_id'], u"Calculando %s..." % (relatorio))
  except Exception as e:
    print(log_str.debug(e))
  resultados = dict()
  try:
    dados = dict()
    dados['query'] = " ".join([
      "SELECT", ",".join([
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'reference_id']),
          "AS", 'order_id',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']),
          "AS", 'order_date',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'order_user_id']),
          "AS", 'user_id',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['usuarios'], 'name']),
          "AS", 'user_name',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['usuarios'], 'email']),
          "AS", 'user_email',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'origin']),
          "AS", 'user_origin',
        ]),
        ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'city_id']),
        " ".join([
          ".".join([busca_pedidos.db_tables()['cidades'], 'name']) ,
          "AS", 'city_name',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['enderecos'], 'district_name']),
          "AS", 'district_name',
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
      "INNER", "JOIN", busca_pedidos.db_tables()['enderecos'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_request_address_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['enderecos'],
          'reference_id'
        ]),
      ]),
      "WHERE", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['cidades'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['enderecos'], 'deleted_at']), "IS NULL",
    ])

    pracas = ['total', 'rs', 'ce', 'rj', 'sp']

    for praca in pracas:
      resultados[praca] = dict()

    dados['total'] = busca_pedidos.transaction_local(" ".join([
      dados['query'],
    ]))

    ## Programação dos dados de usuários
    if dados['total']['status']:
      resultados['total']['dados'] = dados['total']['resultado']
    else:
      try:
        args['bot'].sendMessage(args['chat_id'], u"Anota aí: Não consegui encontrar usuários no período total")
      except Exception as e:
        print(log_str.debug(e))

    anos = ['2016', '2017', '2018']
    for ano in anos:
      print(log_str.debug(str(ano)))
      dados[str(ano)] = dict()
      resultados[str(ano)] = dict()
      meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
      for mes in meses:
        print(log_str.debug('-'.join([str(ano), str(mes)])))
        resultados[str(ano)][str(mes)] = dict()
        resultados[str(ano)][str(mes)]['total'] = dict()
        for praca in pracas:
          resultados[str(ano)][str(mes)][praca] = dict()

#        dados[str(ano)][str(mes)] = busca_pedidos.transaction_local(" ".join([
#          dados['query'],
#          "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
#          "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
#        ]))

#        ## Programação dos dados de usuários
#        if dados[str(ano)][str(mes)]['status']:
#          resultados[str(ano)][str(mes)]['total']['dados'] = dados[str(ano)][str(mes)]['resultado']
#        else:
#          try:
#            args['bot'].sendMessage(args['chat_id'], u"Anota aí: Não consegui encontrar usuários no mês %s do ano %s" % (str(mes), str(ano)))
#          except Exception as e:
#            print(log_str.debug(e))

    ## Gerar arquivos CSV
    try:
      args['bot'].sendMessage(args['chat_id'], u"Mais um pouco...")
    except Exception as e:
      print(log_str.debug(e))
    ## Dados de usuária(o) por período
    try:
      with open("/tmp/relatorio_%s-%s.csv" % (relatorio, str(u"total")), "w") as csvfile:
        fieldnames = [
          u"Nome",
          u"E-mail",
          u"Cidade",
          u"Bairro",
          u"Origem",
          u"Pedidos",
          u"Último pedido",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dado in resultados['total']['dados']:
          writer.writerow({
            'Nome': str(dado['user_name']),
            'E-mail': str(dado['user_email']),
            'Cidade': str(dado['city_name']),
            'Bairro': str(dado['district_name']),
            'Origem': str(dado['user_origin']),
            'Pedidos': str(len(set([pedido['order_id'] for pedido in resultados['total']['dados'] if pedido['user_id'] == dado['user_id']]))),
            'Último pedido': str(sorted([pedido['order_date'] for pedido in resultados['total']['dados'] if pedido['user_id'] == dado['user_id']])[-1]),
          })
      with open("/tmp/relatorio_%s-%s.csv" % (relatorio, str(u"total")), "r") as csvfile:
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

def lista_mailing_csv_2(args):
  relatorio = args['relatorio']
  ## Lista de mailing
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
        " ".join([
          ".".join([busca_pedidos.db_tables()['pedidos'], 'origin']),
          "AS", 'user_origin',
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
        " ".join([
          ".".join([busca_pedidos.db_tables()['usuarios'], 'email']),
          "AS", 'user_email',
        ]),
        ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'city_id']),
        " ".join([
          ".".join([busca_pedidos.db_tables()['cidades'], 'name']) ,
          "AS", 'city_name',
        ]),
        " ".join([
          ".".join([busca_pedidos.db_tables()['enderecos'], 'district_name']) ,
          "AS", 'district_name',
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
      "INNER", "JOIN", busca_pedidos.db_tables()['enderecos'],
      "ON", "=".join([
        ".".join([
          busca_pedidos.db_tables()['pedidos'],
          'order_request_address_id',
        ]),
        ".".join([
          busca_pedidos.db_tables()['enderecos'],
          'reference_id'
        ]),
      ]),
      "WHERE", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['cidades'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['enderecos'], 'deleted_at']), "IS NULL",
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
        usuarios['total'][str(usuario)]['email'] = [dado['user_email'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
        usuarios['total'][str(usuario)]['origem'] = [dado['user_origin'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
        usuarios['total'][str(usuario)]['praca'] = [dado['city_name'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
        usuarios['total'][str(usuario)]['bairro'] = [dado['district_name'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
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
      args['bot'].sendMessage(args['chat_id'], u"Mais um pouco, processando %s linhas..." % (str(len(usuarios['total']))))
    except Exception as e:
      print(log_str.debug(e))
    ## Dados de usuária(o) por período
    try:
      with open("/tmp/relatorio_%s.csv" % (relatorio), "w") as csvfile:
        fieldnames = [
          u"Nome",
          u"E-mail",
          u"Origem",
          u"Cidade",
          u"Bairro",
          u"Pedidos",
          u"Primeiro pedido",
          u"Segundo pedido",
          u"Último pedido",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for usuario in sorted(usuarios['total'].items()):
          writer.writerow({
            'Nome': unicode(usuario[1]['nome']),
            'E-mail': unicode(usuario[1]['email']),
            'Origem': unicode(usuario[1]['origem']),
            'Cidade': unicode(usuario[1]['praca']),
            'Bairro': unicode(usuario[1]['bairro']),
            'Pedidos': unicode(usuario[1]['pedidos']),
            'Primeiro pedido': unicode(usuario[1]['primeiro_pedido']),
            'Segundo pedido': unicode(usuario[1]['segundo_pedido']),
            'Último pedido': unicode(usuario[1]['ultimo_pedido']),
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

## TODO código pela metade, copiado e colado do método acima
def usuarios_por_pedidos(args):
  pass
#  relatorio = args['relatorio']
#  ## Lista a quantidade de pedidos de cada usuário
#  try:
#    args['bot'].sendMessage(args['chat_id'], u"Calculando %s..." % (relatorio))
#  except Exception as e:
#    print(log_str.debug(e))
#  resultados = dict()

#  try:
#    ## SQL query
#    usuarios = dict()
#    pedidos = dict()
#    usuarios['query'] = " ".join([
#      "SELECT", ",".join([
#        " ".join([
#          ".".join([busca_pedidos.db_tables()['usuarios'], 'id']),
#          "AS", 'user_id',
#        ]),
#        " ".join([
#          ".".join([busca_pedidos.db_tables()['usuarios'], 'name']),
#          "AS", 'user_name',
#        ]),
#        " ".join([
#          ".".join([busca_pedidos.db_tables()['usuarios'], 'email']),
#          "AS", 'user_email',
#        ]),
#      ]),
#      "FROM", busca_pedidos.db_tables()['usuarios'],
#      ]),
#      "WHERE", ".".join([busca_pedidos.db_tables()['usuarios'], 'id']), "IS NOT NULL",
#    ])
#    pedidos['query'] = " ".join([
#      "SELECT", ",".join([
#        " ".join([
#          ".".join([busca_pedidos.db_tables()['pedidos'], 'reference_id']),
#          "AS", 'order_id',
#        ]),
#        " ".join([
#          ".".join([busca_pedidos.db_tables()['pedidos'], 'origin']),
#          "AS", 'user_origin',
#        ]),
#        ".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']),
#        " ".join([
#          ".".join([busca_pedidos.db_tables()['pedidos'], 'order_user_id']),
#          "AS", 'user_id',
#        ]),
#        ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'city_id']),
#        " ".join([
#          ".".join([busca_pedidos.db_tables()['cidades'], 'name']) ,
#          "AS", 'city_name',
#        ]),
#        " ".join([
#          ".".join([busca_pedidos.db_tables()['enderecos'], 'district_name']) ,
#          "AS", 'district_name',
#        ]),
#      ]),
#      "FROM", busca_pedidos.db_tables()['pedidos'],
#      "INNER", "JOIN", busca_pedidos.db_tables()['usuarios'],
#      "ON", "=".join([
#        ".".join([
#          busca_pedidos.db_tables()['usuarios'],
#          'id'
#        ]),
#        ".".join([
#          busca_pedidos.db_tables()['pedidos'],
#          'order_user_id',
#        ]),
#      ]),
#      "INNER", "JOIN", busca_pedidos.db_tables()['estabelecimentos'],
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
#      "INNER", "JOIN", busca_pedidos.db_tables()['cidades'],
#      "ON", "=".join([
#        ".".join([
#          busca_pedidos.db_tables()['estabelecimentos'],
#          'city_id',
#        ]),
#        ".".join([
#          busca_pedidos.db_tables()['cidades'],
#          'reference_id'
#        ]),
#      ]),
#      "INNER", "JOIN", busca_pedidos.db_tables()['enderecos'],
#      "ON", "=".join([
#        ".".join([
#          busca_pedidos.db_tables()['pedidos'],
#          'order_request_address_id',
#        ]),
#        ".".join([
#          busca_pedidos.db_tables()['enderecos'],
#          'reference_id'
#        ]),
#      ]),
#      "WHERE", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
#      "AND", ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'deleted_at']), "IS NULL",
#      "AND", ".".join([busca_pedidos.db_tables()['cidades'], 'deleted_at']), "IS NULL",
#      "AND", ".".join([busca_pedidos.db_tables()['enderecos'], 'deleted_at']), "IS NULL",
#    ])

#    ## Variáveis que permanecem com o mesmo valor durante todos loops
#    pracas = ['total', 'rs', 'ce', 'rj', 'sp']
#    anos = ['2015', '2016', '2017', '2018']
##    anos = ['2015', '2016']
#    meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
##    meses = ['01', '02', '03']
#    todos_pedidos = dict()
#    for praca in pracas:
#      todos_pedidos[praca] = set()
#    primeiros_pedidos = dict()
#    for praca in pracas:
#      primeiros_pedidos[praca] = set()
#    segundos_pedidos = dict()
#    for praca in pracas:
#      segundos_pedidos[praca] = set()
#    ultimos_pedidos = dict()
#    for praca in pracas:
#      ultimos_pedidos[praca] = set()
#    dados['resultado'] = list()

#    for ano in anos:
#      print(log_str.debug(str(ano)))
#      ## Variáveis que permanecem com o mesmo valor durante loop de meses
#      dados[str(ano)] = dict()
#      resultados[str(ano)] = dict()
#      dados[str(ano)]['resultado'] = list()

#      for mes in meses:
#        print(log_str.debug('-'.join([str(ano), str(mes)])))
#        ## Variáveis que mudam de valor todo mês
#        resultados[str(ano)][str(mes)] = dict()
#        for praca in pracas:
#          resultados[str(ano)][str(mes)][praca] = dict()

#        ## Busca no banco de dados por mês
#        dados[str(ano)][str(mes)] = busca_pedidos.transaction_local(" ".join([
#          dados['query'],
#          "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
#          "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
#        ]))

#        ## Programação dos dados de usuários
#        if dados[str(ano)][str(mes)]['status'] and type(dados[str(ano)][str(mes)]['resultado']) == type(list()):
#          resultados[str(ano)][str(mes)]['total']['dados'] = dados[str(ano)][str(mes)]['resultado']
#          resultados[str(ano)][str(mes)]['total']['primeiro_pedido'] = set([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['resultado'] if pedido['user_id'] not in primeiros_pedidos['total']])
#          primeiros_pedidos['total'].update(resultados[str(ano)][str(mes)]['total']['primeiro_pedido'])
#          resultados[str(ano)][str(mes)]['total']['segundo_pedido'] = set([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['resultado'] if pedido['user_id'] in todos_pedidos['total'] and pedido['user_id'] in primeiros_pedidos['total'] and pedido['user_id'] not in segundos_pedidos['total']])
#          segundos_pedidos['total'].update(resultados[str(ano)][str(mes)]['total']['segundo_pedido'])
#          todos_pedidos['total'].update([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['resultado']])
#        else:
#          print(log_str.info(u"Anota aí: Não consegui encontrar usuários no mês %s do ano %s" % (str(mes), str(ano))))
#          dados[str(ano)][str(mes)]['resultado'] = list()
#          resultados[str(ano)][str(mes)]['total']['primeiro_pedido'] = set()
#          resultados[str(ano)][str(mes)]['total']['segundo_pedido'] = set()
#        dados[str(ano)]['resultado'] = dados[str(ano)]['resultado'] + dados[str(ano)][str(mes)]['resultado']
#      dados['resultado'] = dados['resultado'] + dados[str(ano)]['resultado']

#    ## Iterar ao contrário
#    anos.reverse()
#    meses.reverse()
#    for ano in anos:
#      print(log_str.debug(str(ano)))

#      for mes in meses:
#        print(log_str.debug('-'.join([str(ano), str(mes)])))

#        ## Busca no banco de dados por mês
#        dados[str(ano)][str(mes)]['inverso'] = busca_pedidos.transaction_local(" ".join([
#          dados['query'],
#          "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
#          "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
#        ]))

#        ## Programação dos dados de usuários
#        if dados[str(ano)][str(mes)]['inverso']['status']:
#          resultados[str(ano)][str(mes)]['total']['ultimo_pedido'] = set([pedido['user_id'] for pedido in dados[str(ano)][str(mes)]['inverso']['resultado'] if pedido['user_id'] not in ultimos_pedidos['total']])
#          ultimos_pedidos['total'].update(resultados[str(ano)][str(mes)]['total']['ultimo_pedido'])
#        else:
#          print(log_str.info(u"Anota aí: Não consegui encontrar usuários no mês %s do ano %s" % (str(mes), str(ano))))
#          resultados[str(ano)][str(mes)]['total']['ultimo_pedido'] = set()
#    anos.reverse()
#    meses.reverse()

#    try:
#      usuarios = dict()
#      usuarios['total'] = dict()
#      for usuario in todos_pedidos['total']:
#        usuarios['total'][str(usuario)] = dict()
#        usuarios['total'][str(usuario)]['nome'] = [dado['user_name'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
#        usuarios['total'][str(usuario)]['email'] = [dado['user_email'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
#        usuarios['total'][str(usuario)]['origem'] = [dado['user_origin'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
#        usuarios['total'][str(usuario)]['praca'] = [dado['city_name'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
#        usuarios['total'][str(usuario)]['bairro'] = [dado['district_name'] for dado in dados['resultado'] if dado['user_id'] == usuario][0]
#        usuarios['total'][str(usuario)]['pedidos'] = len(set([dado['order_id'] for dado in dados['resultado'] if dado['user_id'] == usuario]))
#        for ano in anos:
#          for mes in meses:
#            if usuario in resultados[str(ano)][str(mes)]['total']['primeiro_pedido']:
#              usuarios['total'][str(usuario)]['primeiro_pedido'] = "/".join([str(mes),str(ano)])
#            if usuario in resultados[str(ano)][str(mes)]['total']['segundo_pedido']:
#              usuarios['total'][str(usuario)]['segundo_pedido'] = "/".join([str(mes),str(ano)])
#            if usuario in resultados[str(ano)][str(mes)]['total']['ultimo_pedido']:
#              usuarios['total'][str(usuario)]['ultimo_pedido'] = "/".join([str(mes),str(ano)])
#        if 'segundo_pedido' not in usuarios['total'][str(usuario)]:
#          usuarios['total'][str(usuario)]['segundo_pedido'] = usuarios['total'][str(usuario)]['ultimo_pedido']
#    except Exception as e:
#      args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (str(e)))
#      raise
#      return {
#        'status': False,
#        'type': 'erro',
#        'multi': False,
#        'destino': 'telegram',
#        'response': u"Erro catastrófico: %s" % (str(e)),
#        'debug': log_str.debug(u"Exceção: %s" % (str(e))),
#        'parse_mode': None,
#      }

#    ## Gerar arquivos CSV
#    try:
#      args['bot'].sendMessage(args['chat_id'], u"Mais um pouco, processando %s linhas..." % (str(len(usuarios['total']))))
#    except Exception as e:
#      print(log_str.debug(e))
#    ## Dados de usuária(o) por período
#    try:
#      with open("/tmp/relatorio_%s.csv" % (relatorio), "w") as csvfile:
#        fieldnames = [
#          u"Nome",
#          u"E-mail",
#          u"Origem",
#          u"Cidade",
#          u"Bairro",
#          u"Pedidos",
#          u"Primeiro pedido",
#          u"Segundo pedido",
#          u"Último pedido",
#        ]
#        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#        writer.writeheader()
#        for usuario in sorted(usuarios['total'].items()):
#          writer.writerow({
#            'Nome': unicode(usuario[1]['nome']),
#            'E-mail': unicode(usuario[1]['email']),
#            'Origem': unicode(usuario[1]['origem']),
#            'Cidade': unicode(usuario[1]['praca']),
#            'Bairro': unicode(usuario[1]['bairro']),
#            'Pedidos': unicode(usuario[1]['pedidos']),
#            'Primeiro pedido': unicode(usuario[1]['primeiro_pedido']),
#            'Segundo pedido': unicode(usuario[1]['segundo_pedido']),
#            'Último pedido': unicode(usuario[1]['ultimo_pedido']),
#          })
#        with open("/tmp/relatorio_%s.csv" % (relatorio), "r") as csvfile:
#          args['bot'].sendDocument(args['chat_id'], csvfile, caption=u"Arquivo exportado por Vegga em %s" % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))
#    except Exception as e:
#      args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (str(e)))
#      raise
#      return {
#        'status': False,
#        'type': 'erro',
#        'multi': False,
#        'destino': 'telegram',
#        'response': u"Erro catastrófico: %s" % (str(e)),
#        'debug': log_str.debug(u"Exceção: %s" % (str(e))),
#        'parse_mode': None,
#      }

#  except Exception as e:
#    args['bot'].sendMessage(args['chat_id'], u"Erro catastrófico: %s" % (str(e)))
#    raise
#    return {
#      'status': False,
#      'type': 'erro',
#      'multi': False,
#      'response': u"Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.",
#      'debug': log_str.debug(u"Exceção: %s" % (str(e))),
#      'parse_mode': None,
#    }

