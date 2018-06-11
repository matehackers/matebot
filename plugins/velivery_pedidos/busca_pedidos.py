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

### Imports
import configparser, datetime, json, pymysql, pymysql.cursors, pytz, time
from babel.dates import format_timedelta

def db_config():
  config_file = str("config/.matebot.cfg")
  config = configparser.ConfigParser()
  try:
      config.read(config_file)
      return {
        'status': True,
        'bot': config.items('bot'),
        'info': config.items('info'),
      }
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados\nExceçao ConfigParser: %s' % (e),
      'bot': dict(),
      'info': dict(),
    }

def db_tables():
  return {
    'pedidos': 'order_requests',
    'estabelecimentos': 'order_companies',
    'usuarios': 'app_users',
    'status': 'order_request_status',
    'metodos_pagamento': 'order_payment_methods',
    'enderecos': 'order_request_addresses',
  }

def db_rows():
  return {
    'pedidos': ['id', 'reference_id', 'updated_at', 'order_payment_method_id', 'order_request_address_id', 'order_company_id', 'payment_change', 'order_request_status_id', 'order_user_id', 'created_at', 'description', 'delivery_datetime', 'delivery_price', 'origin'],
    'estabelecimentos': ['short_name', 'phone_number', 'email', 'schedule_when_opened', 'schedule_when_closed'],
    'usuarios': ['name', 'email'],
    'status': ['short_name'],
    'metodos_pagamento': ['short_name'],
    'enderecos': ['street_code', 'street_name', 'street_number', 'street_complement', 'street_reference', 'district_name'],
  }

def db_default_limit():
  return 10

def db_timezone():
  return pytz.timezone('America/Sao_Paulo')

def db_datetime():
  return '%Y-%m-%d %H:%M:%S'

def transaction(db_query):
  try:
    db_config_file = str("config/.matebot.cfg")
    db_config = configparser.ConfigParser()
    try:
        db_config.read(db_config_file)
        db_host = str(db_config.get("database", "host"))
        db_user = str(db_config.get("database", "username"))
        db_password = str(db_config.get("database", "password"))
        db_database = str(db_config.get("database", "database"))
    except Exception as e:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
        'debug': u'Erro tentando contatar banco de dados\nExceçao ConfigParser: %s' % (e),
      }
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, cursorclass=pymysql.cursors.DictCursor)
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados\nExceção PyMysql: %s' % (e),
    }
  try:
    with connection.cursor() as cursor:
      cursor.execute(db_query)
    resultado = cursor.fetchall()
    return {
      'status': True,
      'resultado': resultado
    }
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados\nExceção PyMysql: %s' % (e),
    }
  connection.close()

def formatar_telegram_antigo(pedido):
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['status']), "FROM", db_tables()['status'], "WHERE", '='.join(['reference_id', str(pedido['order_request_status_id'])])])
  time.sleep(0.001)
  status = transaction(db_query)
  if not status['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['status'], db_rows()['status'], db_query, status['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['metodos_pagamento']), "FROM", db_tables()['metodos_pagamento'], "WHERE", '='.join(['reference_id', str(pedido['order_payment_method_id'])]), "ORDER BY", 'updated_at', "DESC"])
  metodo_pagamento = transaction(db_query)
  if not metodo_pagamento['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['metodos_pagamento'], db_rows()['metodos_pagamento'], db_query, metodo_pagamento['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['usuarios']), "FROM", db_tables()['usuarios'], "WHERE", '='.join(['id', str(pedido['order_user_id'])]), "ORDER BY", 'updated_at', "DESC"])
  time.sleep(0.001)
  usuario = transaction(db_query)
  if not usuario['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['usuario'], db_rows()['usuario'], db_query, usuario['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['estabelecimentos']), "FROM", db_tables()['estabelecimentos'], "WHERE", '='.join(['reference_id', str(pedido['order_company_id'])]), "ORDER BY", 'updated_at', "DESC"])
  time.sleep(0.001)
  estabelecimento = transaction(db_query)
  if not estabelecimento['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['estabelecimento'], db_rows()['estabelecimento'], db_query, estabelecimento['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['enderecos']), "FROM", db_tables()['enderecos'], "WHERE", '='.join(['reference_id', str(pedido['order_request_address_id'])]), "ORDER BY", 'updated_at', "DESC"])
  time.sleep(0.001)
  endereco = transaction(db_query)
  if not endereco['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['endereco'], db_rows()['endereco'], db_query, endereco['resultado']),
    }
  
  retorno = list()
  retorno.append('\t'.join([u'Código:', str(pedido['reference_id'])]))
  retorno.append('\t'.join([u'Status:', str(status['resultado'][0]['short_name'])]))
  retorno.append('\t'.join([u'Criado em:', str(pedido['created_at'])]))
  if pedido['created_at'] == pedido['updated_at'] and pedido['order_request_status_id'] == 1:
      retorno.append('\t'.join([u'Tempo aguardando:', format_timedelta((datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()) - db_timezone().localize(pedido['created_at'])), locale='pt_BR')]))
  else:
    retorno.append('\t'.join([u'Atualizado em:', str(pedido['updated_at'])]))
  retorno.append('\t'.join([u'Descrição:', str(pedido['description'])]))
  retorno.append('\t'.join([u'Método de Pagamento:', str(metodo_pagamento['resultado'][0]['short_name'])]))
  if float(pedido['delivery_price']) > 0.00:
    retorno.append('\t'.join([u'Preço da entrega:', str(pedido['delivery_price'])]))
  if float(pedido['payment_change']) > 0.00:
    retorno.append('\t'.join([u'Troco:', str(pedido['payment_change'])]))
  retorno.append('\t'.join([u'Origem:', str(pedido['origin'])]))
  retorno.append('\t'.join([u'Usuária(o) Nome:', str(usuario['resultado'][0]['name'])]))
  retorno.append('\t'.join([u'Usuária(o) E-mail:', str(usuario['resultado'][0]['email'])]))
  retorno.append('\t'.join([u'Estabelecimento Nome:', str(estabelecimento['resultado'][0]['short_name'])]))
  retorno.append('\t'.join([u'Estabelecimento E-mail:', str(estabelecimento['resultado'][0]['email'])]))
  retorno.append('\t'.join([u'Estabelecimento Telefone:', str(estabelecimento['resultado'][0]['phone_number'])]))
  retorno.append('\t'.join([u'Endereço CEP:', str(endereco['resultado'][0]['street_code'])]))
  retorno.append('\t'.join([u'Endereço Nome:', str(endereco['resultado'][0]['street_name'])]))
  retorno.append('\t'.join([u'Endereço Número:', str(endereco['resultado'][0]['street_number'])]))
  retorno.append('\t'.join([u'Endereço Complemento:', str(endereco['resultado'][0]['street_complement'])]))
  retorno.append('\t'.join([u'Endereço Referência:', str(endereco['resultado'][0]['street_reference'])]))
  retorno.append('\t'.join([u'Endereço Distrito:', str(endereco['resultado'][0]['district_name'])]))
  if pedido['delivery_datetime'] != None:
    retorno.append('\t'.join([u'Agendado para:', str(pedido['delivery_datetime'])]))
  
  return {
    'status': True,
    'resultado': retorno,
  }

def formatar_telegram(pedido):
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['status']), "FROM", db_tables()['status'], "WHERE", '='.join(['reference_id', str(pedido['order_request_status_id'])])])
  time.sleep(0.001)
  status = transaction(db_query)
  if not status['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['status'], db_rows()['status'], db_query, status['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['metodos_pagamento']), "FROM", db_tables()['metodos_pagamento'], "WHERE", '='.join(['reference_id', str(pedido['order_payment_method_id'])]), "ORDER BY", 'updated_at', "DESC"])
  metodo_pagamento = transaction(db_query)
  if not metodo_pagamento['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['metodos_pagamento'], db_rows()['metodos_pagamento'], db_query, metodo_pagamento['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['usuarios']), "FROM", db_tables()['usuarios'], "WHERE", '='.join(['id', str(pedido['order_user_id'])]), "ORDER BY", 'updated_at', "DESC"])
  time.sleep(0.001)
  usuario = transaction(db_query)
  if not usuario['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['usuario'], db_rows()['usuario'], db_query, usuario['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['estabelecimentos']), "FROM", db_tables()['estabelecimentos'], "WHERE", '='.join(['reference_id', str(pedido['order_company_id'])]), "ORDER BY", 'updated_at', "DESC"])
  time.sleep(0.001)
  estabelecimento = transaction(db_query)
  if not estabelecimento['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['estabelecimento'], db_rows()['estabelecimento'], db_query, estabelecimento['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['enderecos']), "FROM", db_tables()['enderecos'], "WHERE", '='.join(['reference_id', str(pedido['order_request_address_id'])]), "ORDER BY", 'updated_at', "DESC"])
  time.sleep(0.001)
  endereco = transaction(db_query)
  if not endereco['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['endereco'], db_rows()['endereco'], db_query, endereco['resultado']),
    }
  
  retorno = list()
#  bot_nome = db_config()['bot']['handle'].strip('@')
  bot_nome = 'velivery_dev_bot'
  retorno.append('\t'.join([u'Código:', ''.join(['[', str(pedido['reference_id']), ']', '(', 'https://t.me/%s?start=pedido_%s' % (bot_nome, str(pedido['reference_id'])), ')'])]))
  retorno.append('\t'.join([u'Status:', str(status['resultado'][0]['short_name'])]))
  retorno.append('\t'.join([u'Criado em:', str(pedido['created_at'])]))
  if pedido['created_at'] == pedido['updated_at'] and pedido['order_request_status_id'] == 1:
      retorno.append('\t'.join([u'Tempo aguardando:', format_timedelta((datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()) - db_timezone().localize(pedido['created_at'])), locale='pt_BR')]))
  else:
    retorno.append('\t'.join([u'Atualizado em:', str(pedido['updated_at'])]))
  if pedido['delivery_datetime'] != None:
    retorno.append('\t'.join([u'Agendado para:', str(pedido['delivery_datetime'])]))
  retorno.append('\t'.join([u'Usuária(o):', str(usuario['resultado'][0]['name'])]))
  retorno.append('\t'.join([u'Estabelecimento:', str(estabelecimento['resultado'][0]['short_name'])]))
  
  return {
    'status': True,
    'resultado': retorno,
  }

def formatar_sms(pedido):
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['status']), "FROM", db_tables()['status'], "WHERE", '='.join(['reference_id', str(pedido['order_request_status_id'])])])
  time.sleep(0.001)
  status = transaction(db_query)
  if not status['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['status'], db_rows()['status'], db_query, status['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['metodos_pagamento']), "FROM", db_tables()['metodos_pagamento'], "WHERE", '='.join(['reference_id', str(pedido['order_payment_method_id'])]), "ORDER BY", 'updated_at', "DESC"])
  metodo_pagamento = transaction(db_query)
  if not metodo_pagamento['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['metodos_pagamento'], db_rows()['metodos_pagamento'], db_query, metodo_pagamento['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['usuarios']), "FROM", db_tables()['usuarios'], "WHERE", '='.join(['id', str(pedido['order_user_id'])]), "ORDER BY", 'updated_at', "DESC"])
  time.sleep(0.001)
  usuario = transaction(db_query)
  if not usuario['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['usuario'], db_rows()['usuario'], db_query, usuario['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['estabelecimentos']), "FROM", db_tables()['estabelecimentos'], "WHERE", '='.join(['reference_id', str(pedido['order_company_id'])]), "ORDER BY", 'updated_at', "DESC"])
  time.sleep(0.001)
  estabelecimento = transaction(db_query)
  if not estabelecimento['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['estabelecimento'], db_rows()['estabelecimento'], db_query, estabelecimento['resultado']),
    }
  
  db_query = ' '.join(["SELECT", ", ".join(db_rows()['enderecos']), "FROM", db_tables()['enderecos'], "WHERE", '='.join(['reference_id', str(pedido['order_request_address_id'])]), "ORDER BY", 'updated_at', "DESC"])
  time.sleep(0.001)
  endereco = transaction(db_query)
  if not endereco['status']:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['endereco'], db_rows()['endereco'], db_query, endereco['resultado']),
    }
  
  retorno = list()
  retorno.append('\t'.join([u'Código:', str(pedido['reference_id'])]))
  retorno.append('\t'.join([u'Status:', str(status['resultado'][0]['short_name'])]))
  retorno.append('\t'.join([u'Criado em:', str(pedido['created_at'])]))
  if pedido['created_at'] == pedido['updated_at'] and pedido['order_request_status_id'] == 1:
      retorno.append('\t'.join([u'Tempo aguardando:', format_timedelta((datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()) - db_timezone().localize(pedido['created_at'])), locale='pt_BR')]))
  else:
    retorno.append('\t'.join([u'Atualizado em:', str(pedido['updated_at'])]))
  retorno.append('\t'.join([u'Usuária(o) Nome:', str(usuario['resultado'][0]['name'])]))
  retorno.append('\t'.join([u'Usuária(o) E-mail:', str(usuario['resultado'][0]['email'])]))
  retorno.append('\t'.join([u'Estabelecimento Nome:', str(estabelecimento['resultado'][0]['short_name'])]))
  retorno.append('\t'.join([u'Estabelecimento Telefone:', str(estabelecimento['resultado'][0]['phone_number'])]))
  
  return retorno

def busca(requisicao):
  retorno = list()
  resposta = dict()
#    try:
  time.sleep(0.001)
  pedidos = transaction(' '.join(["SELECT", ", ".join(db_rows()['pedidos']), "FROM", db_tables()['pedidos'], "WHERE", 'deleted_at', "IS", "NULL", requisicao['db_query']]))
  if pedidos['status']:
    if (pedidos['resultado'] != ()):
      retorno.append(requisicao['cabecalho'])
      codigos = list()
      for pedido in pedidos['resultado']:
        if requisicao['modo'] == 'atrasados':
          codigos.append(str(pedido['reference_id']))
        elif requisicao['modo'] == 'pedido':
          retorno.append(''.join(['\n', '\t'.join([u'id:', str(pedido['id'])])]))
        if requisicao['destino'] == 'telegram':
          resultado = formatar_telegram(pedido)
          if not resultado['status']:
            return {
              'status': resultado['status'],
              'type': resultado['type'],
              'multi': resultado['multi'],
              'response': resultado['response'],
              'debug': resultado['debug'],
            }
          else:
            retorno.append('\n'.join(resultado['resultado']))
        elif requisicao['destino'] == 'sms':
          resultado = formatar_sms(pedido)
          if not resultado['status']:
            return {
              'status': resultado['status'],
              'type': resultado['type'],
              'multi': resultado['multi'],
              'response': resultado['response'],
              'debug': resultado['debug'],
            }
          else:
            retorno.append('\n'.join(resultado['resultado']))
        if requisicao['multi']:
          retorno.append('$$$EOF$$$')
        retorno.append(str())
      if requisicao['modo'] == 'atrasados':
        retorno.insert(0, u'%s pedidos atrasados (%s):\n' % (len(pedidos['resultado']), ', '.join(codigos)))
      elif requisicao['modo'] == 'pendentes':
        retorno.insert(0, u'Temos %s pedidos pendentes:\n' % (len(pedidos['resultado'])))
      return {
        'status': True,
        'type': requisicao['type'],
        'multi': requisicao['multi'],
        'destino': requisicao['destino'],
        'response': str('\n'.join(retorno)),
        'debug': u'Sucesso!\nRequisição: %s\nPedidos: %s' % (requisicao, pedidos),
      }
    else:
      return {
        'status': False,
        'type': requisicao['type'],
        'multi': False,
        'response': str(requisicao['nenhum']),
        'debug': u'Sucesso!\nRequisição: %s\nPedidos: %s' % (requisicao, pedidos),
      }
  else:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': pedidos['response'],
      'debug': pedidos['debug'],
    }
#    except Exception as e:
#      return {
#        'status': False,
#        'type': 'erro',
#        'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
#        'debug': '[ERR] Exception em %s: %s' % (e),
#      }

