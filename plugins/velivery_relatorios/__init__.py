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
import datetime, inspect
from plugins.velivery_pedidos import busca_pedidos, db_timezone, db_datetime
from plugins.velivery_relatorios.dre import dre_csv
from plugins.velivery_relatorios.vegcoin import pedidos_veganweek
from plugins.velivery_relatorios.uni import ltv,recompra_2, usuarios_unicos_1 as usuarios_unicos, vendas_soma, vendas_csv

def taxa_recompra(args):
  return busca_pedidos.busca_recompra(args)

def relatorio_recompra(args):
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
          return busca_pedidos.busca_recompra_10(args)
      except IndexError:
        pass
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
  except IndexError:
    args.update(periodo = "total")
    args.update(db_query = ' '.join([]))
    return busca_pedidos.busca_recompra_10(args)
  return {
    'status': False,
    'type': 'erro',
    'multi': False,
    'response': u"Vossa excelência estás a tirardes com a minha cara. Por favor, providencie um ano como argumento.",
    'debug': u"O contrário do sucesso!",
    'parse_mode': None,
  }
  return busca_pedidos.busca_recompra_10(args)

def relatorio_vendas(args):
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
          return busca_pedidos.busca_vendas_1(args)
      except IndexError:
        pass
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
  except IndexError:
    args.update(periodo = "total")
    args.update(db_query = ' '.join([]))
    return busca_pedidos.busca_vendas_1(args)
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

def relatorio_dre(args):
  return dre_csv(args)

def veganweek(args):
  try:
    return pedidos_veganweek(args)
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

def relatorio_ltv(args):
  return ltv(args)

def relatorio_recompra2(args):
  return recompra_2(args)

def relatorio_usuarios_unicos(args):
  return usuarios_unicos(args)

def resumo_vendas_2(args):
  args.update(relatorio = inspect.currentframe().f_code.co_name)
  return vendas_soma(args)

def relatorio_vendas_2(args):
  args.update(relatorio = inspect.currentframe().f_code.co_name)
  return vendas_csv(args)

