# vim:fileencoding=utf-8
#    Plugin velivery_pedidos para matebot: Busca pedidos no banco de dados do velivery
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

import datetime, pytz
from babel.dates import format_timedelta
from plugins.velivery_pedidos import busca_pedidos, queries
from plugins.log import log_str

def atrasados_v2(args):
  try:
    pedidos_atrasados = busca_pedidos.transaction(queries.query_atrasados_1())
    if pedidos_atrasados['status']:
      if pedidos_atrasados['resultado'] != ():
        response = list()
        response.append(
          u"%s pedidos atrasados: (%s)" % (
            len(pedidos_atrasados['resultado']),
            ",".join([str(pedido['order_id']) for pedido in pedidos_atrasados['resultado']]),
          )
        )
        for pedido in pedidos_atrasados['resultado']:
          response.append("")
          response.append(
            u"Pedido %s - %s há %s" % (
              str(pedido['order_id']),
              str(pedido['status_name']),
              format_timedelta((datetime.datetime.now(datetime.timezone.utc).astimezone(queries.db_timezone()) - queries.db_timezone().localize(pedido['order_created_at'])), locale='pt_BR')
            )
          )
          response.append(
            u"Usuária(o): %s %s" % (
              str(pedido['user_name']),
              "".join([n.strip(" ").strip("-").strip("(").strip(")") for n in pedido['address_phone_number']]),
            )
          )
          response.append(
            u"Estabelecimento: %s %s" % (
              str(pedido['company_name']),
              "".join([n.strip(" ").strip("-").strip("(").strip(")") for n in pedido['company_phone_number']]),
            )
          )
          response.append(
            u"%s %s" % (
              str(pedido['company_id']),
              str(pedido['company_email']),
            )
          )
        return {
          'status': True,
          'type': 'grupo',
          'multi': False,
          'response': "\n".join(response),
          'debug': u"Pedidos atrasados",
          'parse_mode': None,
        }
      else:
        return {
          'status': False,
          'type': 'grupo',
          'multi': False,
          'response': u"Nenhum pedido atrasado. Bom trabalho, Velivery!",
          'debug': u"Nenhum pedido atrasado",
          'parse_mode': None,
        }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'grupo',
      'multi': False,
      'response': u"Tivemos um problema técnico e já avisamos os responsáveis!",
      'debug': u"Exceção: %s" % (str(e)),
      'parse_mode': None,
    }
  return {
    'status': False,
    'type': 'grupo',
    'multi': False,
    'response': u"O contrário de dar certo!",
    'debug': u"Isto nunca deveria acontecer",
    'parse_mode': None,
  }

def pendentes_v2(args):
  try:
    pedidos_atrasados = busca_pedidos.transaction(queries.query_pendentes())
    if pedidos_atrasados['status']:
      if pedidos_atrasados['resultado'] != ():
        response = list()
        response.append(
          u"%s pedidos pendentes: (%s)" % (
            len(pedidos_atrasados['resultado']),
            ",".join([str(pedido['order_id']) for pedido in pedidos_atrasados['resultado']]),
          )
        )
        for pedido in pedidos_atrasados['resultado']:
          response.append("")
          response.append(
            u"Pedido %s - %s há %s" % (
              str(pedido['order_id']),
              str(pedido['status_name']),
              format_timedelta((datetime.datetime.now(datetime.timezone.utc).astimezone(queries.db_timezone()) - queries.db_timezone().localize(pedido['order_created_at'])), locale='pt_BR')
            )
          )
          response.append(
            u"Usuária(o): %s %s" % (
              str(pedido['user_name']),
              "".join([n.strip(" ").strip("-").strip("(").strip(")") for n in pedido['address_phone_number']]),
            )
          )
          response.append(
            u"Estabelecimento: %s %s" % (
              str(pedido['company_name']),
              "".join([n.strip(" ").strip("-").strip("(").strip(")") for n in pedido['company_phone_number']]),
            )
          )
          response.append(
            u"%s %s" % (
              str(pedido['company_id']),
              str(pedido['company_email']),
            )
          )
        return {
          'status': True,
          'type': 'grupo',
          'multi': False,
          'response': "\n".join(response),
          'debug': u"Pedidos pendentes",
          'parse_mode': None,
        }
      else:
        return {
          'status': False,
          'type': 'grupo',
          'multi': False,
          'response': u"Nenhum pedido pendente. Bom trabalho, Velivery!",
          'debug': u"Nenhum pedido pendente",
          'parse_mode': None,
        }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'grupo',
      'multi': False,
      'response': u"Tivemos um problema técnico e já avisamos os responsáveis!",
      'debug': u"Exceção: %s" % (str(e)),
      'parse_mode': None,
    }
  return {
    'status': False,
    'type': 'grupo',
    'multi': False,
    'response': u"O contrário de dar certo!",
    'debug': u"Isto nunca deveria acontecer",
    'parse_mode': None,
  }

