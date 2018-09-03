# vim:fileencoding=utf-8
#    Plugin velivery_relatorios para matebot: Faz relatórios, exibe informações e subsidia estatísticas com os dados do Velivery
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
import csv,datetime
#import itertools
from plugins.velivery_pedidos import busca_pedidos,db_default_limit,db_timezone,db_datetime
from plugins.log import log_str

def dre_csv(args):
  ## 1 - Número de Pedidos (número de pedidos que foram feitos a cada mês no Velivery);
  ## 2 - Número de Novos cadastros (número de pessoas que se cadastraram a cada mês no velivery, seja pelo facebook ou por email);
  ## 3 - Número de Usuários Pagantes (número de clientes que fizeram pelo menos um pedido a cada mês no Velivery);
  ## 4 - Número de Novos Pagantes (número de clientes que fizeram um pedido pela primeira vez a cada mês no Velivery)
  ## 5 - Número de Restaurantes Vendentes (restaurantes que atenderam pelo menos um pedido a cada mês no Velivery)
  ## Requisito novo: Todos dados discriminados por praça
  try:
    args['bot'].sendMessage(args['chat_id'], u"Peraí...")
  except Exception as e:
    print(log_str.debug(e))
  resultados = dict()
  try:
    pedidos = dict()
    pedidos['query'] = " ".join([
      "SELECT", ",".join([
        ".".join([busca_pedidos.db_tables()['pedidos'], 'reference_id']),
        ".".join([busca_pedidos.db_tables()['pedidos'], 'order_user_id']),
        ".".join([busca_pedidos.db_tables()['pedidos'], 'order_company_id']),
        ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'city_id']),
      ]),
      "FROM", busca_pedidos.db_tables()['pedidos'],
      "LEFT", "JOIN", busca_pedidos.db_tables()['estabelecimentos'],
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
      "WHERE", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
      "AND", ".".join([busca_pedidos.db_tables()['estabelecimentos'], 'deleted_at']), "IS NULL",
    ])
    usuarios = dict()
    usuarios['query'] = " ".join([
      "SELECT", ",".join([
        'id',
      ]),
      "FROM", busca_pedidos.db_tables()['usuarios'],
      "WHERE", ">".join([".".join([busca_pedidos.db_tables()['usuarios'], 'id']), "1"]),
    ])

    usuarios_cumulativo = set()
    usuarios_cumulativo_rs = set()
    usuarios_cumulativo_ce = set()
    usuarios_cumulativo_rj = set()
    usuarios_cumulativo_sp = set()
    for ano in ['2015', '2016', '2017', '2018']:
      print(log_str.debug(str(ano)))
      pedidos[str(ano)] = dict()
      usuarios[str(ano)] = dict()
      resultados[str(ano)] = dict()
      for mes in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        print(log_str.debug('-'.join([str(ano), str(mes)])))
        resultados[str(ano)][str(mes)] = dict()
        resultados[str(ano)][str(mes)]['rs'] = dict()
        resultados[str(ano)][str(mes)]['ce'] = dict()
        resultados[str(ano)][str(mes)]['rj'] = dict()
        resultados[str(ano)][str(mes)]['sp'] = dict()

        pedidos[str(ano)][str(mes)] = busca_pedidos.transaction_local(" ".join([
          pedidos['query'],
          "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
          "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
        ]))
        print(log_str.debug(pedidos[str(ano)][str(mes)]['status']))
        if pedidos[str(ano)][str(mes)]['status']:
          usuarios_pagantes = set([pedido['order_user_id'] for pedido in pedidos[str(ano)][str(mes)]['resultado']])
          usuarios_pagantes_rs = set([pedido['order_user_id'] for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 7994])
          usuarios_pagantes_ce = set([pedido['order_user_id'] for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 1347])
          usuarios_pagantes_rj = set([pedido['order_user_id'] for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 7043])
          usuarios_pagantes_sp = set([pedido['order_user_id'] for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 13649])
          resultados[str(ano)][str(mes)]['usuarios_pagantes'] = len(usuarios_pagantes)
          resultados[str(ano)][str(mes)]['rs']['usuarios_pagantes'] = len(usuarios_pagantes_rs)
          resultados[str(ano)][str(mes)]['ce']['usuarios_pagantes'] = len(usuarios_pagantes_ce)
          resultados[str(ano)][str(mes)]['rj']['usuarios_pagantes'] = len(usuarios_pagantes_rj)
          resultados[str(ano)][str(mes)]['sp']['usuarios_pagantes'] = len(usuarios_pagantes_sp)

          estabelecimentos_venderam = set([pedido['order_company_id'] for pedido in pedidos[str(ano)][str(mes)]['resultado']])
          estabelecimentos_venderam_rs = set([pedido['order_company_id'] for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 7994])
          estabelecimentos_venderam_ce = set([pedido['order_company_id'] for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 1347])
          estabelecimentos_venderam_rj = set([pedido['order_company_id'] for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 7043])
          estabelecimentos_venderam_sp = set([pedido['order_company_id'] for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 13649])
          resultados[str(ano)][str(mes)]['estabelecimentos_venderam'] = len(estabelecimentos_venderam)
          resultados[str(ano)][str(mes)]['rs']['estabelecimentos_venderam'] = len(estabelecimentos_venderam_rs)
          resultados[str(ano)][str(mes)]['ce']['estabelecimentos_venderam'] = len(estabelecimentos_venderam_ce)
          resultados[str(ano)][str(mes)]['rj']['estabelecimentos_venderam'] = len(estabelecimentos_venderam_rj)
          resultados[str(ano)][str(mes)]['sp']['estabelecimentos_venderam'] = len(estabelecimentos_venderam_sp)

          resultados[str(ano)][str(mes)]['numero_pedidos'] = len(pedidos[str(ano)][str(mes)]['resultado'])
          resultados[str(ano)][str(mes)]['rs']['numero_pedidos'] = len([pedido for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 7994])
          resultados[str(ano)][str(mes)]['ce']['numero_pedidos'] = len([pedido for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 1347])
          resultados[str(ano)][str(mes)]['rj']['numero_pedidos'] = len([pedido for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 7043])
          resultados[str(ano)][str(mes)]['sp']['numero_pedidos'] = len([pedido for pedido in pedidos[str(ano)][str(mes)]['resultado'] if pedido['city_id'] == 13649])

          novos_pagantes = list()
          novos_pagantes_rs = list()
          novos_pagantes_ce = list()
          novos_pagantes_rj = list()
          novos_pagantes_sp = list()
          for pedido in pedidos[str(ano)][str(mes)]['resultado']:
            print(log_str.debug(pedido['reference_id']))
            if not pedido['order_user_id'] in usuarios_cumulativo:
              novos_pagantes.append(pedido['order_user_id'])
            if pedido['city_id'] == 7994 and not pedido['order_user_id'] in usuarios_cumulativo_rs:
              novos_pagantes_rs.append(pedido['order_user_id'])
            if pedido['city_id'] == 1347 and not pedido['order_user_id'] in usuarios_cumulativo_ce:
              novos_pagantes_ce.append(pedido['order_user_id'])
            if pedido['city_id'] == 7043 and not pedido['order_user_id'] in usuarios_cumulativo_rj:
              novos_pagantes_rj.append(pedido['order_user_id'])
            if pedido['city_id'] == 13649 and not pedido['order_user_id'] in usuarios_cumulativo_sp:
              novos_pagantes_sp.append(pedido['order_user_id'])
          resultados[str(ano)][str(mes)]['novos_pagantes'] = len(set(novos_pagantes))
          resultados[str(ano)][str(mes)]['rs']['novos_pagantes'] = len(set(novos_pagantes_rs))
          resultados[str(ano)][str(mes)]['ce']['novos_pagantes'] = len(set(novos_pagantes_ce))
          resultados[str(ano)][str(mes)]['rj']['novos_pagantes'] = len(set(novos_pagantes_rj))
          resultados[str(ano)][str(mes)]['sp']['novos_pagantes'] = len(set(novos_pagantes_sp))

          usuarios_cumulativo.update(usuarios_pagantes)
          usuarios_cumulativo_rs.update(usuarios_pagantes_rs)
          usuarios_cumulativo_ce.update(usuarios_pagantes_ce)
          usuarios_cumulativo_rj.update(usuarios_pagantes_rj)
          usuarios_cumulativo_sp.update(usuarios_pagantes_sp)

          usuarios_pagantes = set()
          usuarios_pagantes_rs = set()
          usuarios_pagantes_ce = set()
          usuarios_pagantes_rj = set()
          usuarios_pagantes_sp = set()
          novos_pagantes = list()
          novos_pagantes_rs = list()
          novos_pagantes_ce = list()
          novos_pagantes_rj = list()
          novos_pagantes_sp = list()
        else:
          try:
            args['bot'].sendMessage(args['chat_id'], u"Anota aí: Não consegui encontrar pedidos no mês %s do ano %s" % (str(mes), str(ano)))
          except Exception as e:
            print(log_str.debug(e))

        usuarios[str(ano)][str(mes)] = busca_pedidos.transaction_local(" ".join([
          usuarios['query'],
          "AND", ">=".join([".".join([busca_pedidos.db_tables()['usuarios'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
          "AND", "<=".join([".".join([busca_pedidos.db_tables()['usuarios'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
        ]))
        if usuarios[str(ano)][str(mes)]['status']:
          resultados[str(ano)][str(mes)]['usuarios_novos'] = len(usuarios[str(ano)][str(mes)]['resultado'])
        else:
          try:
            args['bot'].sendMessage(args['chat_id'], u"Anota aí: Não consegui encontrar usuários no mês %s do ano %s" % (str(mes), str(ano)))
          except Exception as e:
            print(log_str.debug(e))

    try:
      args['bot'].sendMessage(args['chat_id'], u"Mais um pouco...")
    except Exception as e:
      print(log_str.debug(e))
    try:
      with open("/tmp/relatorio_dre_inverso.csv", "w") as csvfile:
        fieldnames = [
          "DRE",
          "Custo Fixo (aluguel, luz, internet)",
          "Custos Operacionais (contabilidade, impostos, empréstimo)",
          "Equipe",
          "Marketing",
          "Remarketing",
          "Aporte",
          "layout",
          "KPI",
          "Nº Restaurantes Ativos",
          "* Nº Pedidos",
          "* Nº Pedidos RS",
          "* Nº Pedidos CE",
          "* Nº Pedidos RJ",
          "* Nº Pedidos SP",
          "Nº Pedidos/Restaurante Ativo",
          "Nº de Usuários (visitantes)",
          "* Nº de Novos Cadastros",
          "* Nº Usuários Pagantes",
          "* Nº Usuários Pagantes RS",
          "* Nº Usuários Pagantes CE",
          "* Nº Usuários Pagantes RJ",
          "* Nº Usuários Pagantes SP",
          "* Nº de Novos Pagantes",
          "* Nº de Novos Pagantes RS",
          "* Nº de Novos Pagantes CE",
          "* Nº de Novos Pagantes RJ",
          "* Nº de Novos Pagantes SP",
          "Taxa de Pedidos/Usuário",
          "CAC",
          "ROI",
          "Custo por Venda",
          "layout",
          "Faturamento mês",
          "Lucro líquido mês",
          "Taxa de Crescimento",
          "* Nº de Restaurantes que venderam",
          "* Nº de Restaurantes que venderam RS",
          "* Nº de Restaurantes que venderam CE",
          "* Nº de Restaurantes que venderam RJ",
          "* Nº de Restaurantes que venderam SP",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ano in sorted(resultados.items()):
          for mes in sorted(ano[1].items()):
            writer.writerow({
              'DRE': u"%s/%s" % (str(mes[0]), str(ano[0])),
              'Custo Fixo (aluguel, luz, internet)': '',
              'Custos Operacionais (contabilidade, impostos, empréstimo)': '',
              'Equipe': '',
              'Marketing': '',
              'Remarketing': '',
              'Aporte': '',
              'layout': '',
              'KPI': '',
              'Nº Restaurantes Ativos': '',
              '* Nº Pedidos': str(mes[1]['numero_pedidos']),
              '* Nº Pedidos RS': str(mes[1]['rs']['numero_pedidos']),
              '* Nº Pedidos CE': str(mes[1]['ce']['numero_pedidos']),
              '* Nº Pedidos RJ': str(mes[1]['rj']['numero_pedidos']),
              '* Nº Pedidos SP': str(mes[1]['sp']['numero_pedidos']),
              'Nº Pedidos/Restaurante Ativo': '',
              'Nº de Usuários (visitantes)': '',
              '* Nº de Novos Cadastros': str(mes[1]['usuarios_novos']),
              '* Nº Usuários Pagantes': str(mes[1]['usuarios_pagantes']),
              '* Nº Usuários Pagantes RS': str(mes[1]['rs']['usuarios_pagantes']),
              '* Nº Usuários Pagantes CE': str(mes[1]['ce']['usuarios_pagantes']),
              '* Nº Usuários Pagantes RJ': str(mes[1]['rj']['usuarios_pagantes']),
              '* Nº Usuários Pagantes SP': str(mes[1]['sp']['usuarios_pagantes']),
              '* Nº de Novos Pagantes': str(mes[1]['novos_pagantes']),
              '* Nº de Novos Pagantes RS': str(mes[1]['rs']['novos_pagantes']),
              '* Nº de Novos Pagantes CE': str(mes[1]['ce']['novos_pagantes']),
              '* Nº de Novos Pagantes RJ': str(mes[1]['rj']['novos_pagantes']),
              '* Nº de Novos Pagantes SP': str(mes[1]['sp']['novos_pagantes']),
              'Taxa de Pedidos/Usuário': '',
              'CAC': '',
              'ROI': '',
              'Custo por Venda': '',
              'layout': '',
              'Faturamento mês': '',
              'Lucro líquido mês': '',
              'Taxa de Crescimento': '',
              '* Nº de Restaurantes que venderam': str(mes[1]['estabelecimentos_venderam']),
              '* Nº de Restaurantes que venderam RS': str(mes[1]['rs']['estabelecimentos_venderam']),
              '* Nº de Restaurantes que venderam CE': str(mes[1]['ce']['estabelecimentos_venderam']),
              '* Nº de Restaurantes que venderam RJ': str(mes[1]['rj']['estabelecimentos_venderam']),
              '* Nº de Restaurantes que venderam SP': str(mes[1]['sp']['estabelecimentos_venderam']),
            })

      args['bot'].sendMessage(args['chat_id'], u"Tentando enviar arquivo csv...")
      arquivo_inverso = open("/tmp/relatorio_dre_inverso.csv", "r")
      arquivo_zip = zip(*csv.reader(arquivo_inverso))
      csv.writer(open("/tmp/relatorio_dre.csv", "w")).writerows(arquivo_zip)
      arquivo_inverso.close()
      with open("/tmp/relatorio_dre.csv", "r") as csvfile:
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


