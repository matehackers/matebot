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
import datetime
from plugins.velivery_pedidos import busca_pedidos, db_timezone, db_datetime

def taxa_recompra(args):
  return busca_pedidos.busca_recompra(args)

def relatorio_recompra_total(args):
  args.update(db_query = ' '.join([
      # Pendentes
#      "AND", '='.join(['order_request_status_id', '1']),
      # Gambiarra
#      "AND", '='.join(['created_at', 'updated_at']),
      # Criados há 5 minutos
#      "AND", '<'.join(['created_at',  ''.join(["'", (datetime.datetime.now(db_timezone()) - datetime.timedelta(minutes=5)).strftime(db_datetime()), "'"])]),
      # Criados há 30 dias
#      "AND", '>='.join(['created_at', ''.join(["'", (datetime.datetime.now(db_timezone()) - datetime.timedelta(days=30)).strftime(db_datetime()), "'"])]),
#      "AND", 'delivery_datetime', "IS", "NULL",
    ]))
  args.update(periodo = "total")
  return busca_pedidos.busca_recompra_10(args)

def relatorio_recompra_ano(args):
  try:
    if args['command_list'][0].isdigit():
      ano = str(args['command_list'][0])
      if str(ano) in ['2015', '2016', '2017', '2018']:
        args.update(db_query = ' '.join([
          "AND", '>='.join(['created_at', ''.join(["'", str(ano), "-01-01 00:00:00", "'"])]),
          "AND", '<='.join(['created_at', ''.join(["'", str(ano), "-12-31 23:59:59", "'"])]),
        ]))
        args.update(periodo = str(ano))
        return busca_pedidos.busca_recompra_10(args)
      else:
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
          'response': u"Vossa excelência estás a tirardes com a minha cara. Por acaso '%s' é um ano?" % (str(ano)),
          'debug': u"O contrário do sucesso!",
          'parse_mode': None,
        }
  except KeyError:
    pass
  return {
    'status': False,
    'type': 'erro',
    'multi': False,
    'response': u"Vossa excelência estás a tirardes com a minha cara. Por favor, providencie um ano como argumento.",
    'debug': u"O contrário do sucesso!",
    'parse_mode': None,
  }

def relatorio_vendas_total(args):
  args.update(db_query = ' '.join([
      # Pendentes
#      "AND", '='.join(['order_request_status_id', '1']),
      # Gambiarra
#      "AND", '='.join(['created_at', 'updated_at']),
      # Criados há 5 minutos
#      "AND", '<'.join(['created_at',  ''.join(["'", (datetime.datetime.now(db_timezone()) - datetime.timedelta(minutes=5)).strftime(db_datetime()), "'"])]),
      # Criados há 30 dias
#      "AND", '>='.join(['created_at', ''.join(["'", (datetime.datetime.now(db_timezone()) - datetime.timedelta(days=30)).strftime(db_datetime()), "'"])]),
#      "AND", 'delivery_datetime', "IS", "NULL",
    ]))
  args.update(periodo = "total")
  return busca_pedidos.busca_vendas_1(args)

def relatorio_vendas_ano(args):
  try:
    if args['command_list'][0].isdigit():
      ano = str(args['command_list'][0])
      if str(ano) in ['2015', '2016', '2017', '2018']:
        args.update(db_query = ' '.join([
          "AND", '>='.join(['created_at', ''.join(["'", str(ano), "-01-01 00:00:00", "'"])]),
          "AND", '<='.join(['created_at', ''.join(["'", str(ano), "-12-31 23:59:59", "'"])]),
        ]))
        args.update(periodo = str(ano))
        return busca_pedidos.busca_vendas_1(args)
      else:
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
          'response': u"Vossa excelência estás a tirardes com a minha cara. Por acaso '%s' é um ano?" % (str(ano)),
          'debug': u"O contrário do sucesso!",
          'parse_mode': None,
        }
  except KeyError:
    pass
  return {
    'status': False,
    'type': 'erro',
    'multi': False,
    'response': u"Vossa excelência estás a tirardes com a minha cara. Por favor, providencie um ano como argumento.",
    'debug': u"O contrário do sucesso!",
    'parse_mode': None,
  }

def relatorio_vendas_mes(args):
  try:
    if args['command_list'][0] in ['2015', '2016', '2017', '2018']:
      ano = str(args['command_list'][0])
      args.update(db_query = ' '.join([
        "AND", '>='.join(['created_at', ''.join(["'", str(ano), "-01-01 00:00:00", "'"])]),
        "AND", '<='.join(['created_at', ''.join(["'", str(ano), "-12-31 23:59:59", "'"])]),
      ]))
      if str(args['command_list'][1]) in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        mes = str(args['command_list'][1])
        args.update(db_query = ' '.join([
          "AND", '>='.join(['created_at', ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
          "AND", '<='.join(['created_at', ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
        ]))
        args.update(periodo = ' '.join([str(mes), " de ", str(ano)]))
        return busca_pedidos.busca_vendas_1(args)
      else:
        args.update(periodo = str(ano))
        return busca_pedidos.busca_vendas_1(args)
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u"Vossa excelência estás a tirardes com a minha cara. Por acaso '%s' é um ano?" % (str(ano)),
        'debug': u"O contrário do sucesso!",
        'parse_mode': None,
      }
  except KeyError:
    pass
  return {
    'status': False,
    'type': 'erro',
    'multi': False,
    'response': u"Vossa excelência estás a tirardes com a minha cara. Por favor, providencie um ano como argumento.",
    'debug': u"O contrário do sucesso!",
    'parse_mode': None,
  }

def relatorio_usuarios(args):
  try:
    if args['command_list'][0] in ['2015', '2016', '2017', '2018']:
      ano = str(args['command_list'][0])
      args.update(db_query = ' '.join([
        "AND", '>='.join(['created_at', ''.join(["'", str(ano), "-01-01 00:00:00", "'"])]),
        "AND", '<='.join(['created_at', ''.join(["'", str(ano), "-12-31 23:59:59", "'"])]),
      ]))
      if str(args['command_list'][1]) in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        mes = str(args['command_list'][1])
        args.update(db_query = ' '.join([
          "AND", '>='.join(['created_at', ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
          "AND", '<='.join(['created_at', ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
        ]))
        args.update(periodo = ' '.join([str(mes), " de ", str(ano)]))
        return busca_pedidos.busca_usuarios(args)
      else:
        args.update(periodo = str(ano))
        return busca_pedidos.busca_usuarios(args)
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u"Vossa excelência estás a tirardes com a minha cara. Por acaso '%s' é um ano?" % (str(ano)),
        'debug': u"O contrário do sucesso!",
        'parse_mode': None,
      }
  except IndexError:
    args.update(periodo = "total")
    args.update(db_query = ' '.join([]))
    return busca_pedidos.busca_usuarios(args)
  return {
    'status': False,
    'type': 'erro',
    'multi': False,
    'response': u"Vossa excelência estás a tirardes com a minha cara. Por favor, providencie um ano como argumento.",
    'debug': u"O contrário do sucesso!",
    'parse_mode': None,
  }

def dados_estabelecimentos(args):
  args.update(db_query = ' '.join([]))
  return busca_pedidos.busca_dados_estabelecimentos(args)

def relatorio_uf(args):
  args.update(periodo = "total")
  args.update(db_query = ' '.join([]))
  try:
    if args['command_list'][0] in ['2015', '2016', '2017', '2018']:
      ano = str(args['command_list'][0])
      args.update(db_query = ' '.join([
        "AND", '>='.join(['created_at', ''.join(["'", str(ano), "-01-01 00:00:00", "'"])]),
        "AND", '<='.join(['created_at', ''.join(["'", str(ano), "-12-31 23:59:59", "'"])]),
      ]))
      try:
        if str(args['command_list'][1]) in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
          mes = str(args['command_list'][1])
          args.update(db_query = ' '.join([
            "AND", '>='.join(['created_at', ''.join(["'", str(ano), "-", str(mes), "-01 00:00:00", "'"])]),
            "AND", '<='.join(['created_at', ''.join(["'", str(ano), "-", str(mes), "-31 23:59:59", "'"])]),
          ]))
          args.update(periodo = ' '.join([str(mes), " de ", str(ano)]))
          return busca_pedidos.busca_uf(args)
      except IndexError:
        pass
      args.update(periodo = str(ano))
      return busca_pedidos.busca_uf(args)
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u"Vossa excelência estás a tirardes com a minha cara. Por acaso '%s' é um ano?" % (str(ano)),
        'debug': u"O contrário do sucesso!",
        'parse_mode': None,
      }
  except IndexError:
    args.update(periodo = "total")
    args.update(db_query = ' '.join([]))
    return busca_pedidos.busca_uf(args)
  return {
    'status': False,
    'type': 'erro',
    'multi': False,
    'response': u"Vossa excelência estás a tirardes com a minha cara. Por favor, providencie um ano como argumento.",
    'debug': u"O contrário do sucesso!",
    'parse_mode': None,
  }

