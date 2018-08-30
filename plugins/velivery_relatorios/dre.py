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

def dre_csv(args):
  ## 1 - Número de Pedidos (número de pedidos que foram feitos a cada mês no Velivery);
  ## 2 - Número de Novos cadastros (número de pessoas que se cadastraram a cada mês no velivery, seja pelo facebook ou por email);
  ## 3 - Número de Usuários Pagantes (número de clientes que fizeram pelo menos um pedido a cada mês no Velivery);
  ## 4 - Número de Novos Pagantes (número de clientes que fizeram um pedido pela primeira vez a cada mês no Velivery)
  args['bot'].sendMessage(args['chat_id'], u"Peraí...")
  resultados = dict()
  try:
    pedidos = dict()
    pedidos['query'] = " ".join([
      "SELECT", ",".join([
        'reference_id',
        'order_user_id',
      ]),
      "FROM", busca_pedidos.db_tables()['pedidos'],
      "WHERE", ".".join([busca_pedidos.db_tables()['pedidos'], 'deleted_at']), "IS NULL",
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
    for ano in ['2015', '2016', '2017', '2018']:
      pedidos[str(ano)] = dict()
      usuarios[str(ano)] = dict()
      resultados[str(ano)] = dict()
      for mes in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        resultados[str(ano)][str(mes)] = dict()

        pedidos[str(ano)][str(mes)] = busca_pedidos.transaction_local(" ".join([
          pedidos['query'],
          "AND", ">=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
          "AND", "<=".join([".".join([busca_pedidos.db_tables()['pedidos'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
        ]))
        if pedidos[str(ano)][str(mes)]['status']:
          usuarios_pagantes = set([pedido['order_user_id'] for pedido in pedidos[str(ano)][str(mes)]['resultado']])

          resultados[str(ano)][str(mes)]['numero_pedidos'] = len(pedidos[str(ano)][str(mes)]['resultado'])
          resultados[str(ano)][str(mes)]['usuarios_pagantes'] = len(usuarios_pagantes)
          novos_pagantes = list()
          for pedido in pedidos[str(ano)][str(mes)]['resultado']:
            if not pedido['order_user_id'] in usuarios_cumulativo:
              novos_pagantes.append(pedido['order_user_id'])
          resultados[str(ano)][str(mes)]['novos_pagantes'] = len(set(novos_pagantes))

          usuarios_cumulativo.update(usuarios_pagantes)
          usuarios_pagantes = set()
          novos_pagantes = set()
        else:
          args['bot'].sendMessage(args['chat_id'], u"Anota aí: Não consegui encontrar pedidos no mês %s do ano %s" % (str(mes), str(ano)))

        usuarios[str(ano)][str(mes)] = busca_pedidos.transaction_local(" ".join([
          usuarios['query'],
          "AND", ">=".join([".".join([busca_pedidos.db_tables()['usuarios'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
          "AND", "<=".join([".".join([busca_pedidos.db_tables()['usuarios'], 'created_at']), ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
        ]))
        if usuarios[str(ano)][str(mes)]['status']:
          resultados[str(ano)][str(mes)]['usuarios_novos'] = len(usuarios[str(ano)][str(mes)]['resultado'])
        else:
          args['bot'].sendMessage(args['chat_id'], u"Anota aí: Não consegui encontrar usuários no mês %s do ano %s" % (str(mes), str(ano)))

    args['bot'].sendMessage(args['chat_id'], u"Mais um pouco...")
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
          "Nº Pedidos/Restaurante Ativo",
          "Nº de Usuários (visitantes)",
          "* Nº de Novos Cadastros",
          "* Nº Usuários Pagantes",
          "* Nº de Novos Pagantes",
          "Taxa de Pedidos/Usuário",
          "CAC",
          "ROI",
          "Custo por Venda",
          "layout",
          "Faturamento mês",
          "Lucro líquido mês",
          "Taxa de Crescimento",
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
              'Nº Pedidos/Restaurante Ativo': '',
              'Nº de Usuários (visitantes)': '',
              '* Nº de Novos Cadastros': str(mes[1]['usuarios_novos']),
              '* Nº Usuários Pagantes': str(mes[1]['usuarios_pagantes']),
              '* Nº de Novos Pagantes': str(mes[1]['novos_pagantes']),
              'Taxa de Pedidos/Usuário': '',
              'CAC': '',
              'ROI': '',
              'Custo por Venda': '',
              'layout': '',
              'Faturamento mês': '',
              'Lucro líquido mês': '',
              'Taxa de Crescimento': '',
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


