# vim:fileencoding=utf-8
#    Plugin velivery_bikeentregas para matebot: Gerencia entregas de Bike pelo
#    Velivery
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
import dataset, datetime, json, locale, requests, sqlite3
from babel.dates import format_timedelta
from plugins.velivery_pedidos import busca_pedidos,db_default_limit,db_timezone,db_datetime
from plugins.log import log_str
from plugins.velivery_bikeentregas import geocode

## Obtém coordenadas de GPS a partir de endereço
def husky_geo(args):
  args.update(geocode_address = ''.join(args['command_list']))
  request_geocode = geocode.address_latlng(args)
  if request_geocode['status']:
    return {
      'status': request_geocode['status'],
      'type': args['command_type'],
      'multi': False,
      'destino': 'telegram',
      'response': str(request_geocode['location']),
      'debug': u"Sucesso!",
      'parse_mode': None,
    }
  else:
    return {
      'status': request_geocode['status'],
      'type': 'erro',
      'multi': False,
      'destino': 'telegram',
      'response': u"Não conseguimos obter as coordenadas do endereço fornecido, ou não forneceram um endereço!",
      'debug': u"O contrário do sucesso!",
      'parse_mode': None,
    }

## Lista ou adiciona pedidos à lista de atendidos
def husky_atendidos(args):
  try:
    pedidos_bike_db = dataset.connect('sqlite:///pedidosbike.db')
    pedido_bike = 0
    try:
      if args['command_list'][0].isdigit():
        pedido_bike = int(args['command_list'][0])
    except IndexError:
      pass
    if pedido_bike > 0:
      pedidos_bike_db['pedidos'].insert(dict(reference_id=str(pedido_bike)))
      return {
        'status': True,
        'type': args['command_type'],
        'multi': False,
        'destino': 'telegram',
        'response': u"Pedido %s adicionado à lista de atendidos!" % (str(pedido_bike)),
        'debug': u"Sucesso!",
        'parse_mode': None,
      }
    else:
      pedidos_lista = list()
      for pedido in pedidos_bike_db['pedidos']:
        pedidos_lista.append(pedido['reference_id'])
      return {
        'status': True,
        'type': args['command_type'],
        'multi': False,
        'destino': 'telegram',
        'response': u"Lista de pedidos atendidos:\n\n%s" % (str(sorted(set(pedidos_lista)))),
        'debug': u"Sucesso!",
        'parse_mode': None,
      }
  except sqlite3.ProgrammingError as e:
    print(log_str.debug(e))
  except Exception as e:
    print(log_str.err(e))
  return {
    'status': False,
    'type': 'ẽrro',
    'multi': False,
    'destino': 'telegram',
    'response': u"O contrário de deu certo!",
    'debug': u"O contrário do sucesso!",
    'parse_mode': None,
  }

## Envia manualmente um pedido para a husky
def husky_pedido(args):
  locale.setlocale(locale.LC_ALL,'')
  try:
    limite = db_default_limit()
    limite = 1
    try:
      if args['command_list'][0].isdigit():
        pedido_id = str(args['command_list'][0])
    except Exception as e:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': u'Este comando só funciona se eu tiver o número do pedido!',
        'debug': u'O contrário do sucesso!',
        'parse_mode': None,
      }

    args['bot'].sendMessage(args['chat_id'], u'Enviando pedido %s para husky...' % (str(pedido_id)))

    pedidos_bike_db = dataset.connect('sqlite:///pedidosbike.db')
    pedidos_lista = list()
    for pedido in pedidos_bike_db['pedidos']:
      pedidos_lista.append(str(pedido['reference_id']))
    pedidos_atendidos = set(pedidos_lista)

    db_query = list()
    db_query.append(" = ".join(["reference_id",pedido_id]))
    db_query.append(" AND ")
    db_query.append(" >= ".join(["company_hash","0"]))

    args.update(db_query = ' '.join(db_query))
    args.update(db_limit = limite)
    args.update(modo = 'bike')
    args.update(cabecalho = u'Pedidos de bike (exibindo os últimos %s pedidos):\n' % (limite))
    args.update(pedidos_atendidos = pedidos_atendidos)
    primeiro_pedido = 43680
    args.update(primeiro_pedido = primeiro_pedido)

    pedidos = busca_pedidos.busca_bike(args)
    if pedidos['status']:
      for pedido in pedidos['response']:
        args.update(geocode_address = ', '.join([str(pedido['endereco']['street_name']).split('-')[0],str(pedido['endereco']['street_number'])]))
        requisicao_geocode = geocode.address_latlng(args)
        if str(requisicao_geocode['status']) == 'OK':
          criar_pedido = dict()
          criar_pedido['order_destiny'] = dict()
          criar_pedido['order_destiny'].update(lat = str(requisicao_geocode['location']['lat']))
          criar_pedido['order_destiny'].update(lng = str(requisicao_geocode['location']['lng']))
          criar_pedido['order_info'] = dict()
          criar_pedido['order_info'].update(client_id = str(args['config']['velivery_bikeentregas']['husky_client_id']))
          criar_pedido['order_info'].update(subclient_id = str(json.loads(args['config']['velivery_bikeentregas']['husky_subclient_ids'])[json.loads(args['config']['velivery_bikeentregas']['estabelecimentos_bike']).index(str(pedido['pedido']['order_company_id']))]))
          criar_pedido['order_info'].update(price = str(float(pedido['pedido']['delivery_price']) - 1.00))
          criar_pedido['order_destiny'].update(name = str(pedido['usuario']['name']))
          criar_pedido['order_destiny'].update(tel = str(pedido['endereco']['phone_number']))
          criar_pedido['order_destiny'].update(address = ', '.join([str(pedido['endereco']['street_name']).split('-')[0],str(pedido['endereco']['street_number'])]))
          criar_pedido['order_destiny'].update(comp = str(pedido['endereco']['street_complement']))
          criar_pedido['order_destiny'].update(hood = str(pedido['endereco']['district_name']))
          criar_pedido['order_destiny'].update(city = str(pedido['cidade']['name']))
          criar_pedido['order_destiny'].update(state = u"Rio Grande do Sul")
          criar_pedido['order_destiny'].update(country = u"Brasil")

          if float(pedido['pedido']['payment_change']) > 0.0:
            criar_pedido['order_destiny'].update(obs = ' '.join([
              u"Pagamento: ",
              str(locale.currency(float(pedido['valor_total']) + float(pedido['pedido']['delivery_price']))),
              u" com ",
              str(pedido['metodos_pagamento']['short_name']),
              u"; Troco: ",
              str(locale.currency(float(pedido['pedido']['payment_change']) - (float(pedido['valor_total']) + float(pedido['pedido']['delivery_price'])))),
              u" para ",
              str(locale.currency(float(pedido['pedido']['payment_change']))),
              u"; Obs:",
              str(pedido['pedido']['description']),
            ]))
          else:
            criar_pedido['order_destiny'].update(obs = ' '.join([
              u"Pagamento:",
              str(locale.currency(float(pedido['valor_total']) + float(pedido['pedido']['delivery_price']))),
              u" com ",
              str(pedido['metodos_pagamento']['short_name']),
              u"; Obs:",
              str(pedido['pedido']['description']),
            ]))

          requisicao_husky = dict()
          requisicao_husky['url'] = str(args['config']['velivery_bikeentregas']['husky_url'])
          requisicao_husky['headers'] = dict()
          requisicao_husky['headers'].update({"Content-Type" : "application/json"})
          requisicao_husky['headers'].update({"Cache-Control" : "no-cache"})
          requisicao_husky['params'] = dict()
          requisicao_husky['params'].update(token = str(args['config']['velivery_bikeentregas']['husky_token']))
          requisicao_husky['data'] = criar_pedido
          request_husky = requests.request("POST", requisicao_husky['url'], json = requisicao_husky['data'], params = requisicao_husky['params'], headers = requisicao_husky['headers'], verify=True)
          if int(request_husky.json()['success']) == 1:
            pedidos_bike_db['pedidos'].insert(dict(reference_id=str(pedido['pedido']['reference_id'])))
            return {
              'status': True,
              'type': args['command_type'],
              'multi': False,
              'destino': 'telegram',
              'response': str(request_husky.json()),
              'debug': u'Requisição husky: %s\nPedidos: %s' % (str(requisicao_husky), str(pedidos['response'])),
              'parse_mode': None,
            }
          else:
            return {
              'status': False,
              'type': 'erro',
              'multi': False,
              'destino': 'telegram',
              'response': str(request_husky.json()),
              'debug': u'Requisição husky: %s\nPedidos: %s' % (str(requisicao_husky), str(pedidos['response'])),
              'parse_mode': None,
            }
        else:
          return {
            'status': False,
            'type': 'erro',
            'multi': False,
            'destino': 'telegram',
            'response': u'Não conseguimos obter a latitude e a longitude com o geocode! Hora de entrar em pânico!',
            'debug': u'O contrário do sucesso!',
            'parse_mode': None,
          }
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': str(pedidos),
        'debug': u'O contrário do sucesso!',
        'parse_mode': None,
      }
  except sqlite3.ProgrammingError as e:
    print(log_str.debug(e))
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'destino': 'telegram',
      'response': u'Erro tentando enviar pedido para a husky, leia o console',
      'debug': u'Exceção tentando enviar pedido para a husky: %s' % (e),
      'parse_mode': None,
    }

## Verifica se há pedidos para enviar à husky
def husky_pendentes(args):
  locale.setlocale(locale.LC_ALL,'')
  try:
    primeiro_pedido = 43680

    pedidos_bike_db = dataset.connect('sqlite:///pedidosbike.db')
    pedidos_lista = list()
    for pedido in pedidos_bike_db['pedidos']:
      pedidos_lista.append(str(pedido['reference_id']))
    pedidos_atendidos = set(pedidos_lista)
    print(str(pedidos_atendidos))

    limite = db_default_limit()
    limite = 10
    try:
      if args['command_list'][0].isdigit():
        limite = str(args['command_list'][0])
    except IndexError:
      pass

    db_query_where = list()
    db_query_where.append("(")
    db_query_where.append(" = ".join(["order_request_status_id","3"]))
    db_query_where.append("AND")
    db_query_where.append(" > ".join(["reference_id", str(primeiro_pedido)]))
    db_query_where.append(")")
    db_query_where.append("AND")
    db_query_where.append("(")
    db_query_companies = list()
    for order_company_id in json.loads(args['config']['velivery_bikeentregas']['estabelecimentos_bike']):
      db_query_companies.append(" = ".join(["order_company_id",order_company_id]))
      db_query_companies.append(" OR ")
    db_query_companies.pop()
    db_query_where.append(''.join(db_query_companies))
    db_query_where.append(")")

    args.update(db_query = ' '.join(db_query_where))
    print(args['db_query'])
    args.update(db_limit = limite)
    args.update(modo = 'bike')
    args.update(cabecalho = u'Pedidos para Velivery BikeEntregas (exibindo os últimos %s pedidos):\n' % (limite))
    args.update(pedidos_atendidos = pedidos_atendidos)
    primeiro_pedido = 43680
    args.update(primeiro_pedido = primeiro_pedido)

    pedidos = busca_pedidos.busca_bike(args)
    if pedidos['status']:
      if (len(pedidos['response']) > 0):
        retorno = list()
        for pedido in pedidos['response']:
          if not str(pedido['pedido']['reference_id']) in pedidos_atendidos:
#            args.update(geocode_address = ', '.join([str(pedido['endereco']['street_name']).split('-')[0],str(pedido['endereco']['street_number'])]))
#            requisicao_geocode = geocode.address_latlng(args)
#            if requisicao_geocode['status']:
            resultado = list()
            criar_pedido = dict()
#            criar_pedido.update(lat = str(requisicao_geocode['location']['lat']))
#            criar_pedido.update(lng = str(requisicao_geocode['location']['lng']))
            criar_pedido.update(pedido_id = str(pedido['pedido']['reference_id']))
            criar_pedido.update(name = str(pedido['usuario']['name']))
            criar_pedido.update(tel = str(pedido['endereco']['phone_number']))
            criar_pedido.update(address = ', '.join([str(pedido['endereco']['street_name']).split('-')[0],str(pedido['endereco']['street_number'])]))
            criar_pedido.update(comp = str(pedido['endereco']['street_complement']))
            criar_pedido.update(hood = str(pedido['endereco']['district_name']))
            criar_pedido.update(city = str(pedido['cidade']['name']))
            criar_pedido.update(state = u"Rio Grande do Sul")
            criar_pedido.update(country = u"Brasil")

            if float(pedido['pedido']['payment_change']) > 0.0:
              criar_pedido.update(obs = ' '.join([
                u"Pagamento: ",
                str(locale.currency(float(pedido['valor_total']) + float(pedido['pedido']['delivery_price']))),
                u" com ",
                str(pedido['metodos_pagamento']['short_name']),
                u"; Troco: ",
                str(locale.currency(float(pedido['pedido']['payment_change']) - (float(pedido['valor_total']) + float(pedido['pedido']['delivery_price'])))),
                u" para ",
                str(locale.currency(float(pedido['pedido']['payment_change']))),
                u"; Obs:",
                str(pedido['pedido']['description']),
              ]))
            else:
              criar_pedido.update(obs = ' '.join([
                u"Pagamento:",
                str(locale.currency(float(pedido['valor_total']) + float(pedido['pedido']['delivery_price']))),
                u" com ",
                str(pedido['metodos_pagamento']['short_name']),
                u"; Obs:",
                str(pedido['pedido']['description']),
              ]))

            criar_pedido.update(atendido = "Não")
            if str(pedido['pedido']['reference_id']) in pedidos_atendidos:
              criar_pedido.update(atendido = "Sim")

            resultado.append('\t'.join([u'Código:', str(criar_pedido['pedido_id'])]))
            resultado.append(str(criar_pedido['obs']))
            resultado.append('\t'.join([u'Tempo aguardando:', format_timedelta((datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()) - db_timezone().localize(pedido['pedido']['created_at'])), locale='pt_BR')]))
            resultado.append('\t'.join([u'Usuária(o):', str(criar_pedido['name']), busca_pedidos.formatar_telefone(criar_pedido['tel'])]))
            resultado.append('\t'.join([u'Estabelecimento:', str(pedido['estabelecimento']['short_name']), busca_pedidos.formatar_telefone(pedido['estabelecimento']['phone_number'])]))
            resultado.append("\t".join([u"Endereço:", str(criar_pedido['address']), str(criar_pedido['comp']), str(criar_pedido['hood']), str(criar_pedido['city'])]))

            retorno.append("\n".join(resultado))

#            else:
#              return {
#                'status': False,
#                'type': 'erro',
#                'multi': False,
#                'destino': 'telegram',
#                'response': u'Não conseguimos obter a latitude e a longitude com o geocode! Hora de entrar em pânico!',
#                'debug': u'O contrário do sucesso!',
#                'parse_mode': None,
#              }

        retorno.insert(0, u'Temos %s pedidos Velivery Bike Entregas:\n' % (len(retorno)))
        retorno.append(u"Digite /husky_pedido <codigo> para enviar manualmente cada pedido para a fila da Husky!")
        return {
          'status': True,
          'type': args['command_type'],
          'multi': False,
          'destino': 'telegram',
          'response': "\n".join(retorno),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
      else:
        return {
          'status': False,
          'type': 'grupo',
          'multi': False,
          'destino': 'telegram',
          'response': u"Nenhum pedido de bike pendente. Bom trabalho, Velivery!",
          'debug': u'Nenhum pedido de bike pendente',
          'parse_mode': None,
        }
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'destino': 'telegram',
        'response': "Erro tentando ver se há pedidos de bike: %s" % (str(pedidos['response'])),
        'debug': u'O contrário do sucesso!',
        'parse_mode': None,
      }
  except sqlite3.ProgrammingError as e:
    print(log_str.debug(e))
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'destino': 'telegram',
      'response': u'Erro tentando enviar pedido para a husky, leia o console',
      'debug': u'Exceção tentando enviar pedido para a husky: %s' % (e),
      'parse_mode': None,
    }

