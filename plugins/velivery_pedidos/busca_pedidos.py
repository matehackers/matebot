# vim:fileencoding=utf-8
#    Plugin velivery_pedidos para matebot: Busca pedidos no banco de dados do velivery
#    Copyleft (C) 2018-2019 Desobediente Civil, Velivery

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

## DISCLAIMER
## Este arquivo se encontra de uma forma que ninguém teria coragem de fazer commit e enviar para o repositório público.
## Embora a minha coragem de publicar isto deveria ser levada em consideração, a minha justificativa pra esse horror abaixo é que tudo foi escrito no calor da batalha.
## Praticamente todas as funções deste bot serão transferidas para uma plataforma usando Flask e boas práticas de programação.
## Isto já começou a ser feito, verifique os repositórios git para ver o status da migração.
## Em 2432 linhas de código contando com comentários, este foi o maior espaguete que eu já fiz em Python.

## TODO
## Fazer um módulo novo, por exemplo 'velivery_db' que funcione como uma DAL.
## Pra quem não sabe o que é DAL ou não curte essas siglas feias que nem eu,
## pesquise na wikipedia: Database Abstraction Layer.

## TODO
## Remover todas referencias para config/.matebot.cfg:wq

### Imports
import csv, configparser, copy, datetime, locale, json, pymysql, pymysql.cursors, pytz, re, time
from plugins.log import log_str
from babel.dates import format_timedelta
from collections import Counter

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
    'cidades': 'address_cities',
    'usuario_telefone': 'order_request_addresses',
    'produtos_pedido': 'order_request_products',
    'produtos': 'order_products',
    'produto_adicionais_pedido': 'order_request_product_additionals',
    'produto_adicionais': 'order_product_additionals',
    'produto_itens_pedido': 'order_request_product_items',
    'produto_itens': 'order_product_items',
    'produto_opcionais_pedido': 'order_request_product_options',
    'produto_opcionais': 'order_product_options',
  }

def db_rows():
  return {
    'pedidos': ['id', 'reference_id', 'updated_at', 'order_payment_method_id', 'order_request_address_id', 'order_company_id', 'payment_change', 'order_request_status_id', 'order_user_id', 'created_at', 'description', 'delivery_datetime', 'delivery_price', 'origin'],
    'estabelecimentos': ['id', 'reference_id', 'name', 'short_name', 'phone_number', 'email', 'schedule_when_opened', 'schedule_when_closed', 'city_id'],
    'usuarios': ['id', 'name', 'email', 'user_group_id', 'system_id', 'type_id'],
    'status': ['id', 'short_name'],
    'metodos_pagamento': ['id', 'reference_id', 'name', 'short_name'],
    'enderecos': ['reference_id', 'street_code', 'street_name', 'street_number', 'street_complement', 'street_reference', 'district_name', 'user_id', 'phone_number'],
    'cidades': ['reference_id', 'name'],
    'usuario_telefone': ['reference_id', 'user_id', 'phone_number'],
    'produtos_pedido': ['reference_id', 'order_request_id', 'order_product_id', 'price', 'observation'],
    'produtos': ['reference_id', 'name', 'short_name', 'description', 'price', 'company_id', 'product_category_id', 'user_id'],
    'produto_adicionais_pedido': ['reference_id', 'order_request_product_id', 'order_product_additional_id', 'price', 'user_id'],
    'produto_adicionais': ['reference_id', 'name', 'short_name', 'price', 'active', 'product_id', 'user_id'],
    'produto_itens_pedido': ['reference_id', 'order_request_product_id', 'order_product_item_id', 'user_id'],
    'produto_itens': ['reference_id', 'name', 'short_name', 'active', 'product_id', 'user_id', 'optional'],
    'produto_opcionais_pedido': ['reference_id', 'order_request_product_id', 'product_option_id', 'price', 'user_id'],
    'produto_opcionais': ['reference_id', 'name', 'short_name', 'optional', 'price', 'active', 'product_option_category_id', 'product_id', 'user_id', 'description', 'product_option_subcategory_id'],
  }

def db_default_limit():
  return 10

def db_timezone():
  return pytz.timezone('America/Sao_Paulo')

def db_datetime():
  return '%Y-%m-%d %H:%M:%S'

def transaction_local(db_query):
  try:
    db_config_file = str("config/.matebot.cfg")
    db_config = configparser.ConfigParser()
    try:
        db_config.read(db_config_file)
        db_host = str(db_config.get("velivery_database", "local_host"))
        db_user = str(db_config.get("velivery_database", "local_username"))
        db_password = str(db_config.get("velivery_database", "local_password"))
        db_database = str(db_config.get("velivery_database", "local_database"))
        db_port = str(db_config.get("velivery_database", "local_port"))
    except Exception as e:
      connection.close()
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
        'debug': u'Erro tentando contatar banco de dados\nExceçao ConfigParser: %s' % (e),
        'parse_mode': None,
      }
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, cursorclass=pymysql.cursors.DictCursor)
  except Exception as e:
    connection.close()
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados\nExceção PyMysql: %s' % (e),
      'parse_mode': None,
    }
  try:
    with connection.cursor() as cursor:
      cursor.execute(db_query)
    resultado = cursor.fetchall()
    return {
      'status': True,
      'type': 'local_db',
      'multi': False,
      'response': resultado,
      'debug': u"Sucesso!",
      'parse_mode': None,
      'resultado': resultado,
    }
  except Exception as e:
    connection.close()
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados\nExceção PyMysql: %s' % (e),
      'parse_mode': None,
    }
  connection.close()

def transaction(db_query):
  time.sleep(0.001)
  try:
    db_config_file = str("config/.matebot.cfg")
    db_config = configparser.ConfigParser()
    try:
        db_config.read(db_config_file)
        db_host = str(db_config.get("velivery_database", "host"))
        db_user = str(db_config.get("velivery_database", "username"))
        db_password = str(db_config.get("velivery_database", "password"))
        db_database = str(db_config.get("velivery_database", "database"))
        db_port = str(db_config.get("velivery_database", "port"))
    except Exception as e:
      raise
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
        'debug': u'Erro tentando contatar banco de dados\nExceçao ConfigParser: %s' % (e),
        'parse_mode': None,
      }
    try:
      connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, cursorclass=pymysql.cursors.DictCursor)
    except pymysql.err.OperationalError as e:
      raise
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
        'debug': u'Erro tentando contatar banco de dados\nExceção PyMysql: %s' % (e),
        'parse_mode': None,
      }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados\nExceção PyMysql: %s' % (e),
      'parse_mode': None,
    }
  try:
    with connection.cursor() as cursor:
      cursor.execute(db_query)
    resultado = cursor.fetchall()
    return {
      'status': True,
      'type': 'db',
      'multi': False,
      'response': resultado,
      'debug': u"Sucesso!",
      'parse_mode': None,
      'resultado': resultado,
    }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(db_config.get("info", "telegram_admin"))),
      'debug': u'Erro tentando contatar banco de dados\nExceção PyMysql: %s' % (e),
      'parse_mode': None,
    }
  connection.close()

#(datetime.datetime.now(db_timezone()) - datetime.timedelta(minutes=5)).strftime(db_datetime())

def obter_telefone(company_id):
  print(log_str.info(u'Procurando telefone...'))
  db_query = ' '.join([
    "SELECT", "phone_number",
    "FROM", db_tables()['estabelecimentos'],
    "WHERE", '='.join([
      'reference_id',
      str(company_id),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER", "BY", 'updated_at', "DESC",
  ])
  numeros = transaction(db_query)
  if numeros['status']:
    numero = numeros['response'][0]['phone_number']
    numero_formatado = ''.join([n.strip(' ').strip('-').strip('(').strip(')') for n in numero])
    return numero_formatado[:10]
  else:
    return '51993570973'

def busca_status(pedido):
  print(log_str.info(u'Processando dados de status do pedido...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['status']),
    "FROM", db_tables()['status'],
    "WHERE", '='.join([
      'reference_id',
      str(pedido['order_request_status_id']),
    ]),
  ])
  return transaction(db_query)

def busca_metodo_pagamento(pedido):
  print(log_str.info(u'Processando dados de métodos de pagamento...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['metodos_pagamento']),
    "FROM", db_tables()['metodos_pagamento'],
    "WHERE", '='.join([
      'reference_id',
      str(pedido['order_payment_method_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_usuario(pedido):
  print(log_str.info(u'Processando dados de usuário...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['usuarios']),
    "FROM", db_tables()['usuarios'],
    "WHERE", '='.join([
      'id',
      str(pedido['order_user_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_estabelecimento(pedido):
  print(log_str.info(u'Processando dados de estabelecimento...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['estabelecimentos']),
    "FROM", db_tables()['estabelecimentos'],
    "WHERE", '='.join([
      'reference_id',
      str(pedido['order_company_id'],
    )]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_endereco(pedido):
  print(log_str.info(u'Processando dados de endereço...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['enderecos']),
    "FROM", db_tables()['enderecos'],
    "WHERE", '='.join([
      'reference_id',
      str(pedido['order_request_address_id']),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_cidade(estabelecimento):
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['cidades']),
    "FROM", db_tables()['cidades'],
    "WHERE", '='.join([
      'reference_id',
      str(estabelecimento['city_id'])
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_produto(produto_id):
  print(log_str.info(u'Processando dados de produto...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produtos']),
    "FROM", db_tables()['produtos'],
    "WHERE", '='.join([
      'reference_id',
      str(produto_id),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_produtos_pedido(pedido):
  print(log_str.info(u'Processando dados de produtos do pedido...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produtos_pedido']),
    "FROM", db_tables()['produtos_pedido'],
    "WHERE", '='.join([
      'order_request_id',
      str(pedido['reference_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_adicional(adicional_id):
  print(log_str.info(u'Processando dados de adicional...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_adicionais']),
    "FROM", db_tables()['produto_adicionais'],
    "WHERE", '='.join([
      'reference_id',
      str(adicional_id),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_adicionais_produto(produto):
  print(log_str.info(u'Processando dados de adicionais de produto...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_adicionais_pedido']),
    "FROM", db_tables()['produto_adicionais_pedido'],
    "WHERE", '='.join([
      'product_id',
      str(produto['reference_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_adicionais_produto_pedido(produto_pedido):
  print(log_str.info(u'Processando dados de adicionais de produtos do pedido...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_adicionais_pedido']),
    "FROM", db_tables()['produto_adicionais_pedido'],
    "WHERE", '='.join([
      'order_request_product_id',
      str(produto_pedido['reference_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_item(item_id):
  print(log_str.info(u'Processando dados de item %s...' % (item_id)))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_itens']),
    "FROM", db_tables()['produto_itens'],
    "WHERE", '='.join([
      'reference_id',
      str(item_id),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_itens_produto(produto):
  print(log_str.info(u'Processando dados de itens de produto...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_itens']),
    "FROM", db_tables()['produto_itens'],
    "WHERE", '='.join([
      'product_id',
      str(produto['reference_id']),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_itens_produto_pedido(produto_pedido):
  print(log_str.info(u'Processando dados de itens de produtos do pedido...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_itens_pedido']),
    "FROM", db_tables()['produto_itens_pedido'],
    "WHERE", '='.join([
      'order_request_product_id',
      str(produto_pedido['reference_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_opcional(opcional_id):
  print(log_str.info(u'Processando dados de opcional %s...' % (opcional_id)))
  db_query = ' '.join([
    "SELECT", ",".join(db_rows()['produto_opcionais']),
    "FROM", db_tables()['produto_opcionais'],
    "WHERE", '='.join([
      'reference_id',
      str(opcional_id),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_opcionais_produto(produto):
  print(log_str.info(u'Processando dados de opcionais de produto...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_opcionais']),
    "FROM", db_tables()['produto_opcionais'],
    "WHERE", '='.join([
      'product_id',
      str(produto['reference_id']),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_opcionais_produto_pedido(produto_pedido):
  print(log_str.info(u'Processando dados de opcionais de produtos do pedido...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_opcionais_pedido']),
    "FROM", db_tables()['produto_opcionais_pedido'],
    "WHERE", '='.join([
      'order_request_product_id',
      str(produto_pedido['reference_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction(db_query)

def busca_status_local(pedido):
  print(log_str.info(u'Processando dados de status do pedido...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['status']),
    "FROM", db_tables()['status'],
    "WHERE", '='.join([
      'reference_id',
      str(pedido['order_request_status_id']),
    ]),
  ])
  return transaction_local(db_query)

def busca_metodo_pagamento_local(pedido):
  print(log_str.info(u'Processando dados de métodos de pagamento...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['metodos_pagamento']),
    "FROM", db_tables()['metodos_pagamento'],
    "WHERE", '='.join([
      'reference_id',
      str(pedido['order_payment_method_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_usuario_local(pedido):
  print(log_str.info(u'Processando dados de usuário...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['usuarios']),
    "FROM", db_tables()['usuarios'],
    "WHERE", '='.join([
      'id',
      str(pedido['order_user_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_estabelecimento_local(pedido):
  print(log_str.info(u'Processando dados de estabelecimento...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['estabelecimentos']),
    "FROM", db_tables()['estabelecimentos'],
    "WHERE", '='.join([
      'reference_id',
      str(pedido['order_company_id'],
    )]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_endereco_local(pedido):
  print(log_str.info(u'Processando dados de endereço...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['enderecos']),
    "FROM", db_tables()['enderecos'],
    "WHERE", '='.join([
      'reference_id',
      str(pedido['order_request_address_id']),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_cidade_local(estabelecimento):
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['cidades']),
    "FROM", db_tables()['cidades'],
    "WHERE", '='.join([
      'reference_id',
      str(estabelecimento['city_id'])
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_produto_local(produto_id):
  print(log_str.info(u'Processando dados de produto...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produtos']),
    "FROM", db_tables()['produtos'],
    "WHERE", '='.join([
      'reference_id',
      str(produto_id),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_produtos_pedido_local(pedido):
  print(log_str.info(u'Processando dados de produtos do pedido...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produtos_pedido']),
    "FROM", db_tables()['produtos_pedido'],
    "WHERE", '='.join([
      'order_request_id',
      str(pedido['reference_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_adicional_local(adicional_id):
  print(log_str.info(u'Processando dados de adicional...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_adicionais']),
    "FROM", db_tables()['produto_adicionais'],
    "WHERE", '='.join([
      'reference_id',
      str(adicional_id),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_adicionais_produto_local(produto):
  print(log_str.info(u'Processando dados de adicionais de produto...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_adicionais_pedido']),
    "FROM", db_tables()['produto_adicionais_pedido'],
    "WHERE", '='.join([
      'product_id',
      str(produto['reference_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_adicionais_produto_pedido_local(produto_pedido):
  print(log_str.info(u'Processando dados de adicionais de produtos do pedido...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_adicionais_pedido']),
    "FROM", db_tables()['produto_adicionais_pedido'],
    "WHERE", '='.join([
      'order_request_product_id',
      str(produto_pedido['reference_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_item_local(item_id):
  print(log_str.info(u'Processando dados de item %s...' % (item_id)))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_itens']),
    "FROM", db_tables()['produto_itens'],
    "WHERE", '='.join([
      'reference_id',
      str(item_id),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_itens_produto_local(produto):
  print(log_str.info(u'Processando dados de itens de produto...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_itens']),
    "FROM", db_tables()['produto_itens'],
    "WHERE", '='.join([
      'product_id',
      str(produto['reference_id']),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_itens_produto_pedido_local(produto_pedido):
  print(log_str.info(u'Processando dados de itens de produtos do pedido...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_itens_pedido']),
    "FROM", db_tables()['produto_itens_pedido'],
    "WHERE", '='.join([
      'order_request_product_id',
      str(produto_pedido['reference_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_opcional_local(opcional_id):
  print(log_str.info(u'Processando dados de opcional %s...' % (opcional_id)))
  db_query = ' '.join([
    "SELECT", ",".join(db_rows()['produto_opcionais']),
    "FROM", db_tables()['produto_opcionais'],
    "WHERE", '='.join([
      'reference_id',
      str(opcional_id),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_opcionais_produto_local(produto):
  print(log_str.info(u'Processando dados de opcionais de produto...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_opcionais']),
    "FROM", db_tables()['produto_opcionais'],
    "WHERE", '='.join([
      'product_id',
      str(produto['reference_id']),
    ]),
    "AND", 'deleted_at', "IS", "NULL",
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)

def busca_opcionais_produto_pedido_local(produto_pedido):
  print(log_str.info(u'Processando dados de opcionais de produtos do pedido...'))
  db_query = ' '.join([
    "SELECT", ", ".join(db_rows()['produto_opcionais_pedido']),
    "FROM", db_tables()['produto_opcionais_pedido'],
    "WHERE", '='.join([
      'order_request_product_id',
      str(produto_pedido['reference_id']),
    ]),
    "ORDER BY", 'updated_at', "DESC",
  ])
  return transaction_local(db_query)


## TODO ta dando problema
#def formatar_telefone(numero):
#  try:
#    numero_lista = re.sub('[()/-]', '', numero).split(' ')
#    numeros = list()
#    if len(numero_lista) > 1:
#      numeros.append(''.join(['+55', numero_lista[0], numero_lista[1]]))
#      if len(numero_lista) > 2:
#        numeros.append(''.join(['+55', numero_lista[3], numero_lista[4]]))
#        if len(numero_lista) > 5:
#          numeros.append(''.join(['+55', numero_lista[6], numero_lista[7]]))
#    else:
#      numeros.append(''.join(['+55', numero_lista[0]]))
#    return ' '.join(numeros)
#  except Exception as e:
#    raise
#    print(log_str.debug(e))
def formatar_telefone(numero):
  numero_formatado = ''.join(['+55', ''.join([n.strip(' ').strip('-') for n in numero])])
  return numero_formatado

def formatar_telegram_antigo(pedido):
  locale.setlocale(locale.LC_ALL,'')
  status = busca_status(pedido)
  metodos_pagamento = busca_metodo_pagamento(pedido)
  usuario = busca_usuario(pedido)
  estabelecimento = busca_estabelecimento(pedido)
  endereco = busca_endereco(pedido)
  produtos_pedido = busca_produtos_pedido(pedido)

  ## Opções, itens e adicionais de produtos do pedido
  print(log_str.info(u'Processando dados de opções, itens e adicionais de produtos do pedido...'))
  lista_produtos_pedido = list()
  if len(produtos_pedido['response']) > 0:
    for produto_pedido in produtos_pedido['response']:
      print(log_str.info(u'Processando produto %s do  pedido %s...' % (str(produto_pedido['reference_id']), str(pedido['reference_id']))))
      produto_pedido.update(dados = busca_produto(produto_pedido['order_product_id'])['response'][0])
      produto_pedido.update(adicionais = list())
      produto_pedido.update(opcionais = list())
      produto_pedido.update(itens = list())
      print(log_str.info(u'Processando adicionais do produto %s do pedido %s...' % (str(produto_pedido['reference_id']), str(pedido['reference_id']))))
      adicionais_produto_pedido = busca_adicionais_produto_pedido(produto_pedido)
      if len(adicionais_produto_pedido['response']) > 0:
        for adicional_produto_pedido in adicionais_produto_pedido['response']:
          print(log_str.info(u'Processando adicional de produto %s do produto %s do pedido %s...' % (str(adicional_produto_pedido['reference_id']), str(produto_pedido['reference_id']), str(pedido['reference_id']))))
          adicional_produto_pedido.update(dados = busca_adicional(adicional_produto_pedido['order_product_additional_id'])['response'][0])
          produto_pedido['adicionais'].append(adicional_produto_pedido)
      print(log_str.info(u'Processando opcionais do produto %s do pedido %s...' % (str(produto_pedido['reference_id']), str(pedido['reference_id']))))
      opcionais_produto_pedido = busca_opcionais_produto_pedido(produto_pedido)
      if len(opcionais_produto_pedido['response']) > 0:
        for opcional_produto_pedido in opcionais_produto_pedido['response']:
          print(log_str.info(u'Processando opcional de produto %s do produto %s do pedido %s...' % (str(opcional_produto_pedido['reference_id']), str(produto_pedido['reference_id']), str(pedido['reference_id']))))
          opcional_produto_pedido.update(dados = busca_opcional(opcional_produto_pedido['product_option_id'])['response'][0])
          produto_pedido['opcionais'].append(opcional_produto_pedido)
      print(log_str.info(u'Processando itens do produto %s do pedido %s...' % (str(produto_pedido['reference_id']), str(pedido['reference_id']))))
      itens_produto_pedido = busca_itens_produto_pedido(produto_pedido)
      if len(itens_produto_pedido['response']) > 0:
        for item_produto_pedido in itens_produto_pedido['response']:
          print(log_str.info(u'Processando item de produto %s do produto %s do pedido %s...' % (str(item_produto_pedido['reference_id']), str(produto_pedido['reference_id']), str(pedido['reference_id']))))
          item_produto_pedido.update(dados = busca_item(item_produto_pedido['order_product_item_id'])['response'][0])
          produto_pedido['itens'].append(item_produto_pedido)
      lista_produtos_pedido.append(produto_pedido)

  print(log_str.info(u'Calculando valor total do pedido...'))
  valor_total = float()
  if len(lista_produtos_pedido) > 0:
    for produto_pedido in lista_produtos_pedido:
      valor_total = valor_total + float(produto_pedido['price'])
      if len(produto_pedido['adicionais']) > 0:
        for adicional_produto_pedido in produto_pedido['adicionais']:
          valor_total = valor_total + float(adicional_produto_pedido['price'])
      if len(produto_pedido['opcionais']) > 0:
        for opcional_produto_pedido in produto_pedido['opcionais']:
          valor_total = valor_total + float(opcional_produto_pedido['price'])
  print(log_str.info(u"Valor total calculado: %s" % (str(valor_total))))

  try:
    retorno = list()
    retorno.append('\t'.join([u'Código:', str(pedido['reference_id'])]))
    retorno.append('\t'.join([u'Status:', str(status['resultado'][0]['short_name'])]))
    retorno.append('\t'.join([u'Criado em:', str(pedido['created_at'])]))
    if pedido['created_at'] == pedido['updated_at'] and pedido['order_request_status_id'] == 1:
      retorno.append('\t'.join([u'Tempo aguardando:', format_timedelta((datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()) - db_timezone().localize(pedido['created_at'])), locale='pt_BR')]))
    else:
      retorno.append('\t'.join([u'Atualizado em:', str(pedido['updated_at'])]))
    if pedido['delivery_datetime'] != None:
      retorno.append('\t'.join([u'Agendado para:', str(pedido['delivery_datetime'])]))
    retorno.append('\t'.join([u'Origem:', str(pedido['origin'])]))
    retorno.append('\t'.join([u'Descrição:', str(pedido['description'])]))

    retorno.append('$$$EOF$$$')
    retorno.append('\t'.join([u'Usuária(o) Nome:', str(usuario['resultado'][0]['name'])]))
    retorno.append('\t'.join([u'Usuária(o) E-mail:', str(usuario['resultado'][0]['email'])]))
    retorno.append('\t'.join([u"Usuária(o) Telefone:", str(formatar_telefone(endereco['resultado'][0]['phone_number']))]))

    retorno.append('$$$EOF$$$')
    retorno.append('\t'.join([u'Estabelecimento Nome:', str(estabelecimento['resultado'][0]['short_name'])]))
    retorno.append('\t'.join([u'Estabelecimento E-mail:', str(estabelecimento['resultado'][0]['email'])]))
    retorno.append('\t'.join([u'Estabelecimento ID:', str(estabelecimento['resultado'][0]['reference_id'])]))
    retorno.append('\t'.join([u'Estabelecimento Telefone:', str(formatar_telefone(estabelecimento['resultado'][0]['phone_number']))]))

    retorno.append('$$$EOF$$$')
    retorno.append('\t'.join([u'Endereço CEP:', str(endereco['resultado'][0]['street_code'])]))
    retorno.append('\t'.join([u'Endereço Nome:', str(endereco['resultado'][0]['street_name'])]))
    retorno.append('\t'.join([u'Endereço Número:', str(endereco['resultado'][0]['street_number'])]))
    retorno.append('\t'.join([u'Endereço Complemento:', str(endereco['resultado'][0]['street_complement'])]))
    retorno.append('\t'.join([u'Endereço Referência:', str(endereco['resultado'][0]['street_reference'])]))
    retorno.append('\t'.join([u'Endereço Distrito:', str(endereco['resultado'][0]['district_name'])]))

    retorno.append('$$$EOF$$$')
    retorno.append(u"Produtos:")
    for produto_pedido in lista_produtos_pedido:
      retorno.append('\t'.join([str(produto_pedido['dados']['name']), str(locale.currency(float(produto_pedido['dados']['price'])))]))
      if len(produto_pedido['adicionais']) > 0:
        retorno.append(u"\tAdicionais:")
        for adicional_produto_pedido in produto_pedido['adicionais']:
          retorno.append('\t'.join(["\t\t", str(adicional_produto_pedido['dados']['name']), str(locale.currency(float(adicional_produto_pedido['dados']['price'])))]))
      if len(produto_pedido['opcionais']) > 0:
        retorno.append(u"\tOpcionais:")
        for opcional_produto_pedido in produto_pedido['opcionais']:
          retorno.append('\t'.join(["\t\t", str(opcional_produto_pedido['dados']['name']), str(locale.currency(float(opcional_produto_pedido['dados']['price'])))]))
      if len(produto_pedido['itens']) > 0:
        lista_itens = list()
        for item_produto_pedido in produto_pedido['itens']:
          lista_itens.append(str(item_produto_pedido['name']))
        retorno.append("\t".join(["Itens:", ','.join(lista_itens)]))

    retorno.append('$$$EOF$$$')
    retorno.append('\t'.join([u'Método de Pagamento:', str(metodos_pagamento['resultado'][0]['short_name'])]))
    retorno.append('\t'.join([u'Valor Total (sem entrega):', str(locale.currency(valor_total))]))
    retorno.append('\t'.join([u'Valor Total (com entrega):', str(locale.currency(valor_total + float(pedido['delivery_price'])))]))
    retorno.append('\t'.join([u'Preço da entrega (para o cliente):', str(locale.currency(float(pedido['delivery_price'])))]))
    retorno.append('\t'.join([u'Preço da entrega (para a(o) entregador(a)):', str(locale.currency(float(pedido['delivery_price']) - 1.00))]))
    if float(pedido['payment_change']) > 0.00:
      retorno.append('\t'.join([u'Troco:', str(locale.currency(float(pedido['payment_change']) - (valor_total + float(pedido['delivery_price'])))), " para ", str(locale.currency(float(pedido['payment_change'])))]))
  except Exception as e:
    raise
    print(log_str.debug(e))

  return {
    'status': True,
    'resultado': retorno,
  }

def formatar_telegram(pedido):
  locale.setlocale(locale.LC_ALL,'')
  status = busca_status(pedido)
  metodos_pagamento = busca_metodo_pagamento(pedido)
  usuario = busca_usuario(pedido)
  estabelecimento = busca_estabelecimento(pedido)
  endereco = busca_endereco(pedido)

  retorno = list()
#  bot_nome = db_config()['bot']['handle'].strip('@')
#  bot_nome = 'velivery_dev_bot'
#  retorno.append('\t'.join([u'Código:', ''.join(['[', str(pedido['reference_id']), ']', '(', 'https://t.me/%s?start=pedido_%s' % (bot_nome, str(pedido['reference_id'])), ')'])]))
  retorno.append('\t'.join([u'Código:', str(pedido['reference_id'])]))
  retorno.append('\t'.join([u'Status:', str(status['resultado'][0]['short_name'])]))
  if pedido['created_at'] == pedido['updated_at'] and pedido['order_request_status_id'] == 1:
      retorno.append('\t'.join([u'Tempo aguardando:', format_timedelta((datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()) - db_timezone().localize(pedido['created_at'])), locale='pt_BR')]))
  if pedido['delivery_datetime'] != None:
    retorno.append('\t'.join([u'Agendado para:', str(pedido['delivery_datetime'])]))
  retorno.append('\t'.join([u'Usuária(o):', str(usuario['resultado'][0]['name']), str(formatar_telefone(endereco['resultado'][0]['phone_number']))]))
  retorno.append('\t'.join([u'Estabelecimento:', str(estabelecimento['resultado'][0]['short_name']), str(estabelecimento['resultado'][0]['reference_id']), str(estabelecimento['resultado'][0]['email']), str(formatar_telefone(estabelecimento['resultado'][0]['phone_number']))]))
  
  return {
    'status': True,
    'resultado': retorno,
  }

def formatar_sms(pedido):
  status = busca_status(pedido)
  metodos_pagamento = busca_metodo_pagamento(pedido)
  usuario = busca_usuario(pedido)
  estabelecimento = busca_estabelecimento(pedido)
  endereco = busca_endereco(pedido)
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
  telefones = list()
  retorno = list()
  resposta = dict()
  try:
    pedidos = transaction(' '.join(["SELECT", ", ".join(db_rows()['pedidos']), "FROM", db_tables()['pedidos'], "WHERE", 'deleted_at', "IS", "NULL", requisicao['db_query']]))
    if pedidos['status']:
      if (pedidos['resultado'] != ()):
        retorno.append(requisicao['cabecalho'])
        codigos = list()
        for pedido in pedidos['resultado']:
          if requisicao['modo'] == 'atrasados':
            codigos.append(str(pedido['reference_id']))
            telefones.append(obter_telefone(str(pedido['order_company_id'])))
          elif requisicao['modo'] == 'pedido':
            retorno.append(''.join(['\n', '\t'.join([u'id:', str(pedido['id'])])]))
          if requisicao['destino'] == 'telegram':
            if requisicao['modo'] == 'pedido':
              resultado = formatar_telegram_antigo(pedido)
            else:
              resultado = formatar_telegram(pedido)
            if not resultado['status']:
              return {
                'status': resultado['status'],
                'type': resultado['type'],
                'multi': resultado['multi'],
                'response': resultado['response'],
                'debug': resultado['debug'],
                'parse_mode': None,
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
                'parse_mode': None,
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
          'debug': u'Sucesso!',
          'parse_mode': None,
          'telefones': telefones,
        }
      else:
        return {
          'status': False,
          'type': requisicao['type'],
          'multi': False,
          'response': str(requisicao['nenhum']),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
    else:
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': pedidos['response'],
        'debug': pedidos['debug'],
        'parse_mode': None,
      }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
      'debug': '[ERR] Exception em %s: %s' % (e),
      'parse_mode': None,
      }

## TODO não dar commit nessa merda, em fase de produção
## TODO só pra registrar que eu dei commit nessa merda
def busca_280(args):
  offset = 0
  limite = 10000
  try:
    if args['command_list'][0].isdigit():
      offset = str(args['command_list'][0])
  except IndexError:
    pass
  requisicao = {
    'db_query': ' '.join([
      "ORDER BY", 'created_at', "DESC",
      "LIMIT", str(limite),
      "OFFSET", str(offset),
    ]),
    'db_limit': limite,
    'modo': 'todos',
    'cabecalho': u'Comando recebido, aguarde...',
    'multi': False,
    'destino': 'telegram',
    'type': args['command_type'],
  }
  args['bot'].sendMessage(args['chat_id'], requisicao['cabecalho'])
  
  retornos = list()
  try:
    pedidos = transaction_local(' '.join([
      "SELECT", ", ".join(db_rows()['pedidos']),
      "FROM", db_tables()['pedidos'],
      "WHERE", 'deleted_at', "IS", "NULL",
      requisicao['db_query'],
    ]))
    if pedidos['status']:
      args['bot'].sendMessage(args['chat_id'], u'Acho que a requisição para o banco de dados deu certo, só mais um pouco...')
      
      if (pedidos['resultado'] != ()):
        args['bot'].sendMessage(args['chat_id'], u'Pedidos recebidos. Processando pedidos...')
        for pedido in pedidos['resultado']:
          
          ## Usuário
          db_query = ' '.join([
            "SELECT", ", ".join(db_rows()['usuarios']),
            "FROM", db_tables()['usuarios'],
            "WHERE", '='.join(['id', str(pedido['order_user_id'])]),
            "ORDER BY", 'updated_at', "DESC",
          ])
          usuario = transaction_local(db_query)
          if not usuario['status']:
            return {
              'status': False,
              'type': 'erro',
              'multi': False,
              'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(args['config'].get("info", "telegram_admin"))),
              'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['usuario'], db_rows()['usuario'], db_query, usuario['resultado']),
              'parse_mode': None,
            }
          
          ## Estabelecimento
          db_query = ' '.join([
            "SELECT", ", ".join(db_rows()['estabelecimentos']),
            "FROM", db_tables()['estabelecimentos'],
            "WHERE", '='.join(['reference_id', str(pedido['order_company_id'])]),
            "ORDER BY", 'updated_at', "DESC",
          ])
          estabelecimento = transaction_local(db_query)
          if not estabelecimento['status']:
            return {
              'status': False,
              'type': 'erro',
              'multi': False,
              'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(args['config'].get("info", "telegram_admin"))),
              'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['estabelecimento'], db_rows()['estabelecimento'], db_query, estabelecimento['resultado']),
              'parse_mode': None,
            }
          
          ## Endereços
          db_query = ' '.join([
            "SELECT", ", ".join(db_rows()['enderecos']),
            "FROM", db_tables()['enderecos'],
            "WHERE", '='.join(['reference_id', str(pedido['order_request_address_id'])]),
            "ORDER BY", 'updated_at', "DESC",
          ])
          endereco = transaction_local(db_query)
          if not endereco['status']:
            return {
              'status': False,
              'type': 'erro',
              'multi': False,
              'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(args['config'].get("info", "telegram_admin"))),
              'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['endereco'], db_rows()['endereco'], db_query, endereco['resultado']),
              'parse_mode': None,
            }
          
          ## Cidade
          db_query = ' '.join([
            "SELECT", ", ".join(db_rows()['cidades']),
            "FROM", db_tables()['cidades'],
            "WHERE", '='.join(['reference_id', str(estabelecimento['resultado'][0]['city_id'])]),
            "ORDER BY", 'updated_at', "DESC",
          ])
          cidade = transaction_local(db_query)
          if not cidade['status']:
            return {
              'status': False,
              'type': 'erro',
              'multi': False,
              'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(args['config'].get("info", "telegram_admin"))),
              'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['cidades'], db_rows()['cidades'], db_query, cidade['resultado']),
              'parse_mode': None,
            }
            
          #codigo: SELECT reference_id FROM order_requests;
          #estabelecimento: SELECT short_name FROM order_companies WHERE order_companies.reference_id IS order_requests.order_company_id;
          #cliente: SELECT name FROM order_users WHERE order_users.id IS order_requests.order_user_id;
          #email: SELECT email FROM order_users WHERE order_users.id IS order_requests.order_user_id;
          #cidade: SELECT name FROM address_cities WHERE address_cities.reference_id IS order_companies.city_id AND order_companies.reference_id IS order_requests.order_company_id;
          #bairro: SELECT district_name FROM order_request_addresses WHERE order_request_addresses.reference_id IS order_requests.order_request_address_id;
          #origin: SELECT origin FROM order_requests;
          
          resultado = dict()
          resultado.update(codigo = str(pedido['reference_id']))
          resultado.update(origem = str(pedido['origin']))
          resultado.update(cliente = str(usuario['resultado'][0]['name']))
          resultado.update(email = str(usuario['resultado'][0]['email']))
          resultado.update(estabelecimento = str(estabelecimento['resultado'][0]['short_name']))
          resultado.update(bairro = str(endereco['resultado'][0]['district_name']))
          resultado.update(cidade = str(cidade['resultado'][0]['name']))
          retornos.append(resultado)
          
        args['bot'].sendMessage(args['chat_id'], u'Pedidos processados. Tentando gerar arquivo csv...')
        try:
          with open('/tmp/exportar_280.csv', 'w', newline='') as csvfile:
            fieldnames = ['codigo', 'estabelecimento', 'cliente', 'email', 'cidade', 'bairro', 'origem']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for retorno in retornos:
              writer.writerow(
                {
                  'codigo': retorno['codigo'],
                  'estabelecimento': retorno['estabelecimento'],
                  'cliente': retorno['cliente'],
                  'email': retorno['email'],
                  'cidade': retorno['cidade'],
                  'bairro': retorno['bairro'],
                  'origem': retorno['origem'],
                }
              )
          
          sucesso = False
          with open('/tmp/exportar_280.csv', 'r', newline='') as csvfile:
            args['bot'].sendMessage(args['chat_id'], u'Tentando enviar arquivo csv...')
            if (args['bot'].sendDocument(args['chat_id'], csvfile, caption=u'Arquivo exportado por Vegga em %s' % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))):
              sucesso = True
            else:
              args['bot'].sendMessage(args['chat_id'], u'Não consegui enviar o arquivo csv. Só esperando o @desobedientecivil agora :(')
          
          return {
            'status': sucesso,
            'type': requisicao['type'],
            'multi': False,
            'destino': requisicao['destino'],
            'response': u'Acho que eu enviei o arquivo. Caso contrário, não sei o que aconteceu.',
            'debug': u'Sucesso!',
            'parse_mode': None,
          }
        except Exception as e:
          raise
          return {
            'status': False,
            'type': 'erro',
            'multi': False,
            'destino': requisicao['destino'],
            'response': u'Erro catastrófico: %s' % (e),
            'debug': u'Exceção: %s' % (e),
            'parse_mode': None,
          }
      else:
        args['bot'].sendMessage(args['chat_id'], u'Nenhum pedido foi encontrado. Só esperando o @desobedientecivil agora :(')
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
          'response': str(requisicao['nenhum']),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
    else:
      args['bot'].sendMessage(args['chat_id'], u'Erro tentando requisitar o banco de dados. Só esperando o @desobedientecivil agora :(')
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': pedidos['response'],
        'debug': pedidos['debug'],
        'parse_mode': None,
      }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
      'debug': u'Exceção: %s' % (e),
      'parse_mode': None,
    }

## TODO não dar commit nessa merda, em fase de produção
## TODO só pra registrar que eu dei commit nessa merda
## TODO só pra registrar que eu copiei e colei o adubo supracitado
## TODO testar e tratar exceções
def busca_recompra(args):
  offset = 0
  limite = 0
  try:
    if args['command_list'][0].isdigit():
      offset = str(args['command_list'][0])
  except IndexError:
    pass
  requisicao = {
    'db_query': ' '.join([
      "ORDER BY", 'created_at', "DESC",
#      "LIMIT", str(limite),
#      "OFFSET", str(offset),
    ]),
    'db_limit': limite,
    'modo': 'todos',
    'cabecalho': u'Comando recebido, aguarde...',
    'multi': False,
    'destino': 'telegram',
    'type': args['command_type'],
  }
  args['bot'].sendMessage(args['chat_id'], requisicao['cabecalho'])
  
  retornos = list()
  try:
    pedidos = transaction_local(' '.join([
      "SELECT", ", ".join(db_rows()['pedidos']),
      "FROM", db_tables()['pedidos'],
      "WHERE", 'deleted_at', "IS", "NULL",
      requisicao['db_query'],
    ]))
    if pedidos['status']:
      args['bot'].sendMessage(args['chat_id'], u'Acho que a requisição para o banco de dados deu certo, só mais um pouco...')
      
      if (pedidos['resultado'] != ()):
        args['bot'].sendMessage(args['chat_id'], u'Pedidos recebidos. Processando pedidos...')
        for pedido in pedidos['resultado']:
          ## Usuário
          db_query = ' '.join([
            "SELECT", ", ".join(db_rows()['usuarios']),
            "FROM", db_tables()['usuarios'],
            "WHERE", '='.join(['id', str(pedido['order_user_id'])]),
            "ORDER BY", 'updated_at', "DESC",
          ])
          usuario = transaction_local(db_query)
          if not usuario['status']:
            return {
              'status': False,
              'type': 'erro',
              'multi': False,
              'response': u'Erro tentando contatar banco de dados. Avise o %s' % (str(args['config'].get("info", "telegram_admin"))),
              'debug': u'Erro tentando contatar banco de dados, tabela %s, colunas %s.\nQuery: %s\nResultado: %s' % (db_tables()['usuario'], db_rows()['usuario'], db_query, usuario['resultado']),
              'parse_mode': None,
            }
            
          recompra = False
          resultado = dict()
          resultado.update(cliente = str(usuario['resultado'][0]['name']))
          for retorno in retornos:
            if retorno['cliente'] == str(usuario['resultado'][0]['name']):
              recompra = True
              retorno['recompra'] = recompra
          resultado.update(recompra = recompra)
          if (not recompra):
            retornos.append(resultado)
          
        args['bot'].sendMessage(args['chat_id'], u'Pedidos processados. Calculando taxa de recompra...')
        
        recompra_contador = Counter(uma_compra=0, mais_de_uma_compra=0)
        for retorno in retornos:
          if retorno['recompra']:
            recompra_contador.update(mais_de_uma_compra = 1)
          else:
            recompra_contador.update(uma_compra = 1)
        # Cálculo da taxa de recompra de acordo com "A Internet"
        taxa_recompra = (100*recompra_contador['mais_de_uma_compra'])/(recompra_contador['uma_compra']+recompra_contador['mais_de_uma_compra'])
        response = list()
        response.append("Taxa de recompra no Velivery:")
        response.append("")
        response.append("Pessoas que só pediram uma vez: %s" % (recompra_contador['uma_compra']))
        response.append("Pessoas que pediram mais de uma vez: %s" % (recompra_contador['mais_de_uma_compra']))
        response.append("Ou seja, a taxa de recompra é de %s%%." % (taxa_recompra))
        if (taxa_recompra > 50 ):
          response.append("")
          response.append("Concluímos então que o Velivery está fazendo um ótimo trabalho, pois a taxa de recompra é superior a 2 para 1. Go Veg!")
        else:
          response.append("")
          response.append("E por consequência disto, concluímos que é necessário investir o vosso tempo em vender, para aumentar a taxa de recompra. Bora trabalhar? Mas primeiro, um café a 70°C do Alimentarte!")
        return {
          'status': True,
          'type': requisicao['type'],
          'multi': False,
          'destino': requisicao['destino'],
          'response': '\n'.join(response),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
      else:
        args['bot'].sendMessage(args['chat_id'], u'Nenhum pedido foi encontrado. Só esperando o @desobedientecivil agora :(')
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
          'response': str(requisicao['nenhum']),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
    else:
      args['bot'].sendMessage(args['chat_id'], u'Erro tentando requisitar o banco de dados. Só esperando o @desobedientecivil agora :(')
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': pedidos['response'],
        'debug': pedidos['debug'],
        'parse_mode': None,
      }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
      'debug': u'Exceção: %s' % (e),
      'parse_mode': None,
    }

## TODO não dar commit nessa merda, em fase de produção
## TODO só pra registrar que eu dei commit nessa merda
## TODO só pra registrar que eu copiei e colei o adubo supracitado
## TODO a gambiarra ressucita outra vez
def busca_bike(args):
  locale.setlocale(locale.LC_ALL,'')
  offset = 0
  limite = 100
  try:
    if args['command_list'][0].isdigit():
      offset = str(args['command_list'][0])
  except IndexError:
    pass
  requisicao = {
    'db_query': args['db_query'],
    'db_limit': limite,
    'modo': 'bike',
    'cabecalho': u'Comando recebido, aguarde...',
    'multi': False,
    'destino': 'telegram',
    'type': args['command_type'],
  }
  print(log_str.info(requisicao['cabecalho']))
  
  retornos = list()
  try:
    pedidos = transaction(' '.join([
      "SELECT", ", ".join(db_rows()['pedidos']),
      "FROM", db_tables()['pedidos'],
      "WHERE", requisicao['db_query'],
      "AND", 'deleted_at', "IS", "NULL",
      "ORDER", "BY", 'reference_id', "DESC",
    ]))
    if pedidos['status']:
      print(log_str.info(u'Acho que a requisição para o banco de dados deu certo, só mais um pouco...'))
      if (pedidos['resultado'] != ()):
        print(log_str.info(u'Pedidos recebidos. Processando pedidos...'))
        for pedido in pedidos['resultado']:
          if str(pedido['reference_id']) not in args['pedidos_atendidos'] and int(pedido['reference_id']) > int(args['primeiro_pedido']):
            print(log_str.info(u"Processando pedido %s..." % (pedido['reference_id'])))
            status = busca_status(pedido)
            metodos_pagamento = busca_metodo_pagamento(pedido)
            usuario = busca_usuario(pedido)
            estabelecimento = busca_estabelecimento(pedido)
            endereco = busca_endereco(pedido)
            cidade = busca_cidade(estabelecimento['response'][0])
            produtos_pedido = busca_produtos_pedido(pedido)

            ## Opções, itens e adicionais de produtos do pedido
            print(log_str.info(u'Processando dados de opções, itens e adicionais de produtos do pedido...'))
            lista_produtos_pedido = list()
            if len(produtos_pedido['response']) > 0:
              for produto_pedido in produtos_pedido['response']:
                print(log_str.info(u'Processando produto %s do  pedido %s...' % (str(produto_pedido['reference_id']), str(pedido['reference_id']))))
                produto_pedido.update(dados = busca_produto(produto_pedido['order_product_id'])['response'][0])
                produto_pedido.update(adicionais = list())
                produto_pedido.update(opcionais = list())
                produto_pedido.update(itens = list())
                print(log_str.info(u'Processando adicionais do produto %s do pedido %s...' % (str(produto_pedido['reference_id']), str(pedido['reference_id']))))
                adicionais_produto_pedido = busca_adicionais_produto_pedido(produto_pedido)
                if len(adicionais_produto_pedido['response']) > 0:
                  for adicional_produto_pedido in adicionais_produto_pedido['response']:
                    print(log_str.info(u'Processando adicional de produto %s do produto %s do pedido %s...' % (str(adicional_produto_pedido['reference_id']), str(produto_pedido['reference_id']), str(pedido['reference_id']))))
                    adicional_produto_pedido.update(dados = busca_adicional(adicional_produto_pedido['order_product_additional_id'])['response'][0])
                    produto_pedido['adicionais'].append(adicional_produto_pedido)
                print(log_str.info(u'Processando opcionais do produto %s do pedido %s...' % (str(produto_pedido['reference_id']), str(pedido['reference_id']))))
                opcionais_produto_pedido = busca_opcionais_produto_pedido(produto_pedido)
                if len(opcionais_produto_pedido['response']) > 0:
                  for opcional_produto_pedido in opcionais_produto_pedido['response']:
                    print(log_str.info(u'Processando opcional de produto %s do produto %s do pedido %s...' % (str(opcional_produto_pedido['reference_id']), str(produto_pedido['reference_id']), str(pedido['reference_id']))))
                    opcional_produto_pedido.update(dados = busca_opcional(opcional_produto_pedido['product_option_id'])['response'][0])
                    produto_pedido['opcionais'].append(opcional_produto_pedido)
                print(log_str.info(u'Processando itens do produto %s do pedido %s...' % (str(produto_pedido['reference_id']), str(pedido['reference_id']))))
                itens_produto_pedido = busca_itens_produto_pedido(produto_pedido)
                if len(itens_produto_pedido['response']) > 0:
                  for item_produto_pedido in itens_produto_pedido['response']:
                    print(log_str.info(u'Processando item de produto %s do produto %s do pedido %s...' % (str(item_produto_pedido['reference_id']), str(produto_pedido['reference_id']), str(pedido['reference_id']))))
                    item_produto_pedido.update(dados = busca_item(item_produto_pedido['order_product_item_id'])['response'][0])
                    produto_pedido['itens'].append(item_produto_pedido)
                lista_produtos_pedido.append(produto_pedido)

            print(log_str.info(u'Banco de dados processado. Organizando dados...'))
            resultado = dict()
            resultado.update(pedido = pedido)
            resultado.update(usuario = usuario['response'][0])
            resultado.update(estabelecimento = estabelecimento['response'][0])
            resultado.update(endereco = endereco['response'][0])
            resultado.update(cidade = cidade['response'][0])
            resultado.update(metodos_pagamento = metodos_pagamento['resultado'][0])
            resultado.update(endereco_estabelecimento = {"address":"Rua José do Patrocínio, 824","longitude":"-51.2211564","latitude":"-30.0417169"})

            print(log_str.info(u'Calculando valor total do pedido...'))
            valor_total = float()
            if len(lista_produtos_pedido) > 0:
              for produto_pedido in lista_produtos_pedido:
                valor_total = valor_total + float(produto_pedido['price'])
                if len(produto_pedido['adicionais']) > 0:
                  for adicional_produto_pedido in produto_pedido['adicionais']:
                    valor_total = valor_total + float(adicional_produto_pedido['price'])
                if len(produto_pedido['opcionais']) > 0:
                  for opcional_produto_pedido in produto_pedido['opcionais']:
                    valor_total = valor_total + float(opcional_produto_pedido['price'])
            print(log_str.info(u"Valor total calculado: %s" % (str(valor_total))))
            resultado['valor_total'] = valor_total
            retornos.append(resultado)
            print(log_str.info(u"Pedido %s processado com sucesso!" % (pedido['reference_id'])))
          else:
            print(log_str.info(u"Pedido %s já foi atendido." % (pedido['reference_id'])))
        print(log_str.info(u"Todos pedidos processados! Alguma coisa deveria acontecer agora!"))
        return {
          'status': True,
          'type': 'husky',
          'multi': False,
          'destino': 'telegram',
          'response': retornos,
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
      else:
        print(log_str.info(u'Nenhum pedido foi encontrado. Só esperando o @desobedientecivil agora :('))
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
          'response': u"Nenhum pedido encontrado",
          'debug': u'Nenhum pedido encontrado',
          'parse_mode': None,
        }
    else:
      print(log_str.info(u'Erro tentando requisitar o banco de dados. Só esperando o @desobedientecivil agora :('))
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': pedidos['response'],
        'debug': pedidos['debug'],
        'parse_mode': None,
      }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
      'debug': u'Exceção: %s' % (e),
      'parse_mode': None,
    }

## TODO não dar commit nessa merda, em fase de produção
## TODO só pra registrar que eu dei commit nessa merda
## TODO só pra registrar que eu copiei e colei o adubo supracitado
## TODO três vezes!
## TODO testar e tratar exceções
def busca_recompra_10(args):
  offset = 0
  limite = 0
  try:
    if args['command_list'][0].isdigit():
      offset = str(args['command_list'][0])
  except IndexError:
    pass
  requisicao = {
    'db_query': ' '.join([
      "SELECT", "order_user_id",
      "FROM", db_tables()['pedidos'],
      "WHERE", 'deleted_at', "IS", "NULL",
      args['db_query'],
      "ORDER BY", 'reference_id', "DESC",
    ]),
    'db_limit': limite,
    'modo': 'todos',
    'cabecalho': u'Comando recebido, aguarde...',
    'multi': False,
    'destino': 'telegram',
    'type': 'grupo',
    'parse_mode': None,
  }
  args['bot'].sendMessage(args['chat_id'], requisicao['cabecalho'])
  
  retornos = list()
  try:
    pedidos = transaction_local(requisicao['db_query'])
    if pedidos['status']:
      args['bot'].sendMessage(args['chat_id'], u'Acho que a requisição para o banco de dados deu certo, só mais um pouco...')
      if (pedidos['resultado'] != ()):
        args['bot'].sendMessage(args['chat_id'], u'Pedidos recebidos. Contando pedidos por usuário...')
        usuarios = list()
        for pedido in pedidos['response']:
          usuarios.append(pedido['order_user_id'])
        universo = dict(Counter(Counter(usuarios).values()))
        recompras = copy.deepcopy(universo)
        recompras.pop(1)
        recompra_total = 0
        for recompra in recompras.values():
          recompra_total += recompra
        umavez = {1: copy.deepcopy(universo)[1]}
        args['bot'].sendMessage(args['chat_id'], u'Pedidos processados. Calculando taxa de recompra...')

        # Cálculo da taxa de recompra de acordo com "A Internet"
        taxa_recompra = (100*recompra_total)/(umavez[1]+recompra_total)
        response = list()
        response.append(u"Taxa de recompra no Velivery (período = %s):" % (str(args['periodo'])))
        response.append("")
        response.append(u"Pessoas que só pediram uma vez: %s" % (str(umavez[1])))
        response.append(u"Pessoas que pediram mais de uma vez: %s" % (recompra_total))
        response.append(u"Ou seja, a taxa de recompra é de %s%%." % (taxa_recompra))
        if (taxa_recompra > 50 ):
          response.append("")
          response.append(u"Concluímos então que o Velivery está fazendo um ótimo trabalho, pois a taxa de recompra é superior a 2 para 1. Go Veg!")
        else:
          response.append("")
          response.append(u"E por consequência disto, concluímos que é necessário investir o vosso tempo em vender, para aumentar a taxa de recompra. Bora trabalhar? Mas primeiro, um café a 70°C do Alimentarte!")
        response.append("")
        response.append(u"Estou enviando um arquivo CSV com os dados do período solicitado.")
        try:
          with open(''.join(["/tmp/relatorio_recompra_", str(args['periodo']), ".csv"]), 'w', newline='') as csvfile:
            fieldnames = ['numero de compras', 'quantidade de usuarios']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in universo.keys():
              writer.writerow(
                {
                  'numero de compras': item,
                  'quantidade de usuarios': universo[item],
                }
              )
          with open(''.join(["/tmp/relatorio_recompra_", str(args['periodo']), ".csv"]), 'r', newline='') as csvfile:
            args['bot'].sendMessage(args['chat_id'], u'Tentando enviar arquivo csv...')
            if (args['bot'].sendDocument(args['chat_id'], csvfile, caption=u'Arquivo exportado por Vegga em %s' % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))):
              args['bot'].sendMessage(args['chat_id'], u"Acho que eu enviei o arquivo. Caso contrário, não sei o que aconteceu.")
            else:
              args['bot'].sendMessage(args['chat_id'], u'Não consegui enviar o arquivo csv. Só esperando o @desobedientecivil agora :(')
        except Exception as e:
          raise
          return {
            'status': False,
            'type': 'erro',
            'multi': False,
            'destino': 'telegram',
            'response': u'Erro catastrófico: %s' % (e),
            'debug': u'Exceção: %s' % (e),
            'parse_mode': None,
          }
        return {
          'status': True,
          'type': requisicao['type'],
          'multi': False,
          'destino': 'telegram',
          'response': '\n'.join(response),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
      else:
        args['bot'].sendMessage(args['chat_id'], u'Nenhum pedido foi encontrado. Só esperando o @desobedientecivil agora :(')
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
          'response': str(requisicao['nenhum']),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
    else:
      args['bot'].sendMessage(args['chat_id'], u'Erro tentando requisitar o banco de dados. Só esperando o @desobedientecivil agora :(')
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': pedidos['response'],
        'debug': pedidos['debug'],
        'parse_mode': None,
      }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
      'debug': u'Exceção: %s' % (e),
      'parse_mode': None,
    }

## TODO não dar commit nessa merda, em fase de produção
## TODO só pra registrar que eu dei commit nessa merda
## TODO só pra registrar que eu copiei e colei o adubo supracitado
## TODO a gambiarra ressucita outra vez
## TODO quatro vezes!
def busca_vendas_1(args):
  locale.setlocale(locale.LC_ALL,'')
  offset = 0
  limite = 0
  try:
    if args['command_list'][0].isdigit():
      offset = str(args['command_list'][0])
  except IndexError:
    pass
  requisicao = {
    'db_query': ' '.join([
      "SELECT", ",".join(db_rows()['pedidos']),
      "FROM", db_tables()['pedidos'],
      "WHERE", 'deleted_at', "IS", "NULL",
      args['db_query'],
      "ORDER", "BY", 'reference_id', "DESC",
    ]),
    'db_limit': limite,
    'modo': 'relatorio',
    'cabecalho': u'Comando recebido, aguarde...',
    'multi': False,
    'destino': 'telegram',
    'type': args['command_type'],
  }
  
  valores_totais = list()
  teleentrega_totais = list()
  try:
#    pedidos = transaction_local(requisicao['db_query'])
    pedidos = transaction(requisicao['db_query'])
    if pedidos['status']:
      print(log_str.info(u'Acho que a requisição para o banco de dados deu certo, só mais um pouco...'))
      if (pedidos['resultado'] != ()):
        print(log_str.info(u'Pedidos recebidos. Processando pedidos...'))
        for pedido in pedidos['resultado']:
          teleentrega_totais.append(float(pedido['delivery_price']))
          produtos_pedido = busca_produtos_pedido_local(pedido)
          lista_produtos_pedido = list()
          if produtos_pedido['status'] and len(produtos_pedido['response']) > 0:
            for produto_pedido in produtos_pedido['response']:
              produto = busca_produto_local(produto_pedido['order_product_id'])
              if produto['status'] and len(produto['response']) > 0:
                produto_pedido.update(dados = produto['response'][0])
              else:
                produto_pedido.update(dados = {'price': 0.0})
              produto_pedido.update(adicionais = list())
              produto_pedido.update(opcionais = list())
              produto_pedido.update(itens = list())
              adicionais_produto_pedido = busca_adicionais_produto_pedido_local(produto_pedido)
              if len(adicionais_produto_pedido['response']) > 0:
                for adicional_produto_pedido in adicionais_produto_pedido['response']:
                  adicional = busca_adicional_local(adicional_produto_pedido['order_product_additional_id'])
                  if adicional['status'] and len(adicional['response']) > 0:
                    adicional_produto_pedido.update(dados = adicional['response'][0])
                  else:
                    adicional_produto_pedido.update(dados = {'price': 0.0})
                  produto_pedido['adicionais'].append(adicional_produto_pedido)
              opcionais_produto_pedido = busca_opcionais_produto_pedido_local(produto_pedido)
              if len(opcionais_produto_pedido['response']) > 0:
                for opcional_produto_pedido in opcionais_produto_pedido['response']:
                  opcional = busca_opcional_local(opcional_produto_pedido['product_option_id'])
                  if opcional['status'] and len(opcional['response']) > 0:
                    opcional_produto_pedido.update(dados = opcional['response'][0])
                  else:
                    opcional_produto_pedido.update(dados = {'price': 0.0})
                  produto_pedido['opcionais'].append(opcional_produto_pedido)
              itens_produto_pedido = busca_itens_produto_pedido_local(produto_pedido)
              if len(itens_produto_pedido['response']) > 0:
                for item_produto_pedido in itens_produto_pedido['response']:
                  item = busca_item_local(item_produto_pedido['order_product_item_id'])
                  if item['status'] and len(item['response']) > 0:
                    item_produto_pedido.update(dados = item['response'][0])
                  else:
                    item_produto_pedido.update(dados = {'price': 0.0})
                  produto_pedido['itens'].append(item_produto_pedido)
              lista_produtos_pedido.append(produto_pedido)
          else:
            return produtos_pedido
          valor_total = float()
          if len(lista_produtos_pedido) > 0:
            for produto_pedido in lista_produtos_pedido:
              valor_total = valor_total + float(produto_pedido['price'])
              if len(produto_pedido['adicionais']) > 0:
                for adicional_produto_pedido in produto_pedido['adicionais']:
                  valor_total = valor_total + float(adicional_produto_pedido['price'])
              if len(produto_pedido['opcionais']) > 0:
                for opcional_produto_pedido in produto_pedido['opcionais']:
                  valor_total = valor_total + float(opcional_produto_pedido['price'])
          valores_totais.append(valor_total)
        print(log_str.info(u"Todos pedidos processados! Somando tudo..."))
        valor_todos_pedidos = float()
        for valores_total in valores_totais:
          valor_todos_pedidos = valor_todos_pedidos + float(valores_total)
        teleentrega_todos_pedidos = float()
        for teleentrega_total in teleentrega_totais:
          teleentrega_todos_pedidos = teleentrega_todos_pedidos + teleentrega_total
        response = list()
        response.append(u"Total de todos os pedidos no Velivery (período = %s):" % (str(args['periodo'])))
        response.append("")
        response.append(u"A soma em reais brasileiros de todos os pedidos feitos no Velivery que não foram excluídos durante o período é de: %s" % (str(locale.currency(valor_todos_pedidos))))
        response.append("")
        response.append(u"O total de dinheiro para tele entregas para os pedidos do periodo é de %s, e a soma anterior mais o total de tele entregas é de %s" % (str(locale.currency(teleentrega_todos_pedidos)), str(locale.currency(valor_todos_pedidos + teleentrega_todos_pedidos))))
        response.append("")
        response.append(u"Total de pedidos que entraram neste cálculo: %s" % (str(len(pedidos['resultado']))))
        response.append("")
        return {
          'status': True,
          'type': 'grupo',
          'multi': False,
          'destino': 'telegram',
          'response': "\n".join(response),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
      else:
        print(log_str.info(u'Nenhum pedido foi encontrado. Só esperando o @desobedientecivil agora :('))
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
          'response': u"Nenhum pedido encontrado",
          'debug': u'Nenhum pedido encontrado',
          'parse_mode': None,
        }
    else:
      print(log_str.info(u'Erro tentando requisitar o banco de dados. Só esperando o @desobedientecivil agora :('))
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': pedidos['response'],
        'debug': pedidos['debug'],
        'parse_mode': None,
      }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
      'debug': u'Exceção: %s' % (e),
      'parse_mode': None,
    }

## TODO não dar commit nessa merda, em fase de produção
## TODO só pra registrar que eu dei commit nessa merda
## TODO só pra registrar que eu copiei e colei o adubo supracitado
## TODO a gambiarra ressucita outra vez
## TODO cinco vezes!
def busca_usuarios(args):
  locale.setlocale(locale.LC_ALL,'')
  offset = 0
  limite = 10
#  try:
#    if args['command_list'][0].isdigit():
#      offset = str(args['command_list'][0])
#  except IndexError:
#    pass
  requisicao_pedidos = {
    'db_query': ' '.join([
      "SELECT", 'order_user_id',
      "FROM", db_tables()['pedidos'],
      "WHERE", 'deleted_at', "IS", "NULL",
      args['db_query'],
      "ORDER", "BY", 'reference_id', "DESC",
#      "LIMIT", str(limite),
    ]),
    'db_limit': limite,
    'modo': 'relatorio',
    'cabecalho': u'Comando recebido, aguarde...',
    'multi': False,
    'destino': 'telegram',
    'type': args['command_type'],
  }
  requisicao_usuarios = {
    'db_query': ' '.join([
      "SELECT", 'id, type_id',
      "FROM", db_tables()['usuarios'],
      "WHERE", 'type_id', 'IS', 'NOT', 'NULL',
      "ORDER", "BY", 'id', "DESC",
#      "LIMIT", str(limite),
    ]),
    'db_limit': limite,
    'modo': 'relatorio',
    'cabecalho': u'Comando recebido, aguarde...',
    'multi': False,
    'destino': 'telegram',
    'type': args['command_type'],
  }

#        recompra_contador = Counter(uma_compra=0, mais_de_uma_compra=0)
#        for retorno in retornos:
#          if retorno['recompra']:
#            recompra_contador.update(mais_de_uma_compra = 1)
#          else:
#            recompra_contador.update(uma_compra = 1)

#        usuarios = list()
#        for pedido in pedidos['response']:
#          usuarios.append(pedido['order_user_id'])
#        universo = dict(Counter(Counter(usuarios).values()))
#        recompras = copy.deepcopy(universo)
#        recompras.pop(1)
#        recompra_total = 0
#        for recompra in recompras.values():
#          recompra_total += recompra
#        umavez = {1: copy.deepcopy(universo)[1]}

  try:
#    pedidos = transaction_local(requisicao_pedidos['db_query'])
#    usuarios = transaction_local(requisicao_usuarios['db_query'])
    pedidos = transaction(requisicao_pedidos['db_query'])
    usuarios = transaction(requisicao_usuarios['db_query'])
    if pedidos['status'] and usuarios['status']:
      print(log_str.info(u'Acho que a requisição para o banco de dados deu certo, só mais um pouco...'))
      if (usuarios['resultado'] != ()) and (pedidos['resultado'] != ()):
        print(log_str.info(u'Dados de usuários e pedidos recebidos. Processando dados...'))
        universo_usuarios = len(usuarios['response'])
        opcao_usuarios = Counter(vegano=0, vegetariano=0, simpatizante=0)
        for usuario in usuarios['response']:
          if int(usuario['type_id']) == 1:
            opcao_usuarios.update(vegano = 1)
          elif int(usuario['type_id']) == 2:
            opcao_usuarios.update(vegetariano = 1)
          elif int(usuario['type_id']) == 3:
            opcao_usuarios.update(simpatizante = 1)
        usuarios_pediram = list()
        opcao_usuarios_pedido = Counter(vegano=0, vegetariano=0, simpatizante=0)
        for pedido in pedidos['response']:
          usuarios_pediram.append(pedido['order_user_id'])
        todos_usuarios_pediram = len(set(usuarios_pediram))
        for usuario_pediu in set(usuarios_pediram):
          usuario_pedido = next((usuario for usuario in usuarios['response'] if usuario['id'] == usuario_pediu), False)
          if usuario_pedido:
            if int(usuario_pedido['type_id']) == 1:
              opcao_usuarios_pedido.update(vegano = 1)
            elif int(usuario_pedido['type_id']) == 2:
              opcao_usuarios_pedido.update(vegetariano = 1)
            elif int(usuario_pedido['type_id']) == 3:
              opcao_usuarios_pedido.update(simpatizante = 1)

        print(log_str.info(u"Todos dados processados! Formatando..."))
        response = list()
        response.append(u"Relatório de usuária(o)s do Velivery:")
        response.append("")
        response.append(u"Total de usuária(o)s: %s, que já fizeram pelo menos um pedido: %s\t\t- %s%%" % (str(universo_usuarios), str(todos_usuarios_pediram), str((100*float(todos_usuarios_pediram))/float(universo_usuarios))))
        response.append(u"Vegana(o)s: %s\t\t- %s%%, que já pediram: %s\t\t - %s%%" % (str(opcao_usuarios['vegano']), str((100.0*float(opcao_usuarios['vegano']))/float(universo_usuarios)), str(opcao_usuarios_pedido['vegano']), str((100.0*float(opcao_usuarios_pedido['vegano']))/float(todos_usuarios_pediram))))
        response.append(u"Vegetariana(o)s: %s\t\t- %s%%, que já pediram: %s\t\t - %s%%" % (str(opcao_usuarios['vegetariano']), str((100.0*float(opcao_usuarios['vegetariano']))/float(universo_usuarios)), str(opcao_usuarios_pedido['vegetariano']), str((100.0*float(opcao_usuarios_pedido['vegetariano']))/float(todos_usuarios_pediram))))
        response.append(u"Simpatizantes: %s\t\t- %s%%, que já pediram: %s\t\t - %s%%" % (str(opcao_usuarios['simpatizante']), str((100.0*float(opcao_usuarios['simpatizante']))/float(universo_usuarios)), str(opcao_usuarios_pedido['simpatizante']), str((100.0*float(opcao_usuarios_pedido['simpatizante']))/float(todos_usuarios_pediram))))
#        response.append("")
#        response.append(u"Total de pedidos que entraram neste cálculo: %s" % (str(len(pedidos['resultado']))))
#        response.append("")

#  requisicao = {
#    'db_query': ' '.join([
#      "SELECT", "order_user_id",
#      "FROM", db_tables()['pedidos'],
#      "WHERE", 'deleted_at', "IS", "NULL",
#      args['db_query'],
#      "ORDER BY", 'reference_id', "DESC",
#    ]),
#    'db_limit': limite,
#    'modo': 'todos',
#    'cabecalho': u'Comando recebido, aguarde...',
#    'multi': False,
#    'destino': 'telegram',
#    'type': 'grupo',
#    'parse_mode': None,
#  }
#  args['bot'].sendMessage(args['chat_id'], requisicao['cabecalho'])
#  
#  retornos = list()
#  try:
#    pedidos = transaction_local(requisicao['db_query'])
#    if pedidos['status']:
#      args['bot'].sendMessage(args['chat_id'], u'Acho que a requisição para o banco de dados deu certo, só mais um pouco...')
#      if (pedidos['resultado'] != ()):
#        args['bot'].sendMessage(args['chat_id'], u'Pedidos recebidos. Contando pedidos por usuário...')
#        usuarios = list()
#        for pedido in pedidos['response']:
#          usuarios.append(pedido['order_user_id'])
#        universo = dict(Counter(Counter(usuarios).values()))
#        recompras = copy.deepcopy(universo)
#        recompras.pop(1)
#        recompra_total = 0
#        for recompra in recompras.values():
#          recompra_total += recompra
#        umavez = {1: copy.deepcopy(universo)[1]}


        return {
          'status': True,
          'type': 'grupo',
          'multi': False,
          'destino': 'telegram',
          'response': "\n".join(response),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
      else:
        print(log_str.info(u'Nenhum usuário ou pedido foi encontrado. Só esperando o @desobedientecivil agora :('))
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
          'response': u"Nenhum usuário ou pedido encontrado",
          'debug': u'Nenhum usuário ou pedido encontrado',
          'parse_mode': None,
        }
    else:
      print(log_str.info(u'Erro tentando requisitar o banco de dados. Só esperando o @desobedientecivil agora :('))
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': usuarios['response'],
        'debug': usuarios['debug'],
        'parse_mode': None,
      }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
      'debug': u'Exceção: %s' % (e),
      'parse_mode': None,
    }

## TODO não dar commit nessa merda, em fase de produção
## TODO só pra registrar que eu dei commit nessa merda
## TODO só pra registrar que eu copiei e colei o adubo supracitado
## TODO testar e tratar exceções
## TODO se algum dia isto for commitado, pode me chamar de o pior desenvolvedor da história do velivery. mais de 2 mil linhas de código pra uma coisa que da pra fazer em 50 é o cúmulo da preguiça.
def busca_dados_estabelecimentos(args):
  offset = 0
  limite = 0
  requisicao = {
    'db_query': ' '.join([
      "SELECT", "id, reference_id, name, email, phone_number",
      "FROM", db_tables()['estabelecimentos'],
      "WHERE", 'deleted_at', "IS", "NULL",
#      args['db_query'],
      "ORDER BY", 'reference_id', "DESC",
    ]),
    'db_limit': limite,
    'modo': 'todos',
    'cabecalho': u'Comando recebido, aguarde...',
    'multi': False,
    'destino': 'telegram',
    'type': 'grupo',
    'parse_mode': None,
  }
  args['bot'].sendMessage(args['chat_id'], requisicao['cabecalho'])
  
  retornos = list()
  try:
    estabelecimentos = transaction(requisicao['db_query'])
    if estabelecimentos['status']:
      args['bot'].sendMessage(args['chat_id'], u'Acho que a requisição para o banco de dados deu certo, só mais um pouco...')
      if (estabelecimentos['response'] != ()):
        args['bot'].sendMessage(args['chat_id'], u'Dados de estabelecimentos recebidos. Organizando dados...')
        try:
          with open("/tmp/dados_estabelecimentos.csv", 'w', newline='') as csvfile:
            fieldnames = ['id site', 'nome', 'telefone', 'email', 'id db']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for estabelecimento in estabelecimentos['response']:
              writer.writerow(
                {
                  'id site': estabelecimento['reference_id'],
                  'nome': estabelecimento['name'],
                  'telefone': estabelecimento['phone_number'],
                  'email': estabelecimento['email'],
                  'id db': estabelecimento['id'],
                }
              )
          with open("/tmp/dados_estabelecimentos.csv", 'r', newline='') as csvfile:
            args['bot'].sendMessage(args['chat_id'], u'Tentando enviar arquivo csv...')
            if (args['bot'].sendDocument(args['chat_id'], csvfile, caption=u'Arquivo exportado por Vegga em %s' % (str(datetime.datetime.now(datetime.timezone.utc).astimezone(db_timezone()))))):
              args['bot'].sendMessage(args['chat_id'], u"Acho que eu enviei o arquivo. Caso contrário, não sei o que aconteceu.")
            else:
              args['bot'].sendMessage(args['chat_id'], u'Não consegui enviar o arquivo csv. Só esperando o @desobedientecivil agora :(')
        except Exception as e:
          raise
          return {
            'status': False,
            'type': 'erro',
            'multi': False,
            'destino': 'telegram',
            'response': u'Erro catastrófico: %s' % (e),
            'debug': u'Exceção: %s' % (e),
            'parse_mode': None,
          }
        response = ['Dados de estabelecimento enviados em formato csv']
        return {
          'status': True,
          'type': requisicao['type'],
          'multi': False,
          'destino': 'telegram',
          'response': '\n'.join(response),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
      else:
        args['bot'].sendMessage(args['chat_id'], u'Nenhum pedido foi encontrado. Só esperando o @desobedientecivil agora :(')
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
          'response': str(requisicao['nenhum']),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
    else:
      args['bot'].sendMessage(args['chat_id'], u'Erro tentando requisitar o banco de dados. Só esperando o @desobedientecivil agora :(')
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': estabelecimentos['response'],
        'debug': estabelecimentos['debug'],
        'parse_mode': None,
      }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
      'debug': u'Exceção: %s' % (e),
      'parse_mode': None,
    }

## TODO não dar commit nessa merda, em fase de produção
## TODO só pra registrar que eu dei commit nessa merda
## TODO só pra registrar que eu copiei e colei o adubo supracitado
## TODO a gambiarra ressucita outra vez
## TODO sete vezes!
def busca_uf(args):
  locale.setlocale(locale.LC_ALL,'')
  offset = 0
  limite = 100
#  try:
#    if args['command_list'][0].isdigit():
#      offset = str(args['command_list'][0])
#  except IndexError:
#    pass
  requisicao_pedidos = {
    'db_query': ' '.join([
      "SELECT", ','.join(db_rows()['pedidos']),
      "FROM", db_tables()['pedidos'],
      "WHERE", 'deleted_at', "IS", "NULL",
      args['db_query'],
      "ORDER", "BY", 'reference_id', "DESC",
#      "LIMIT", str(limite),
    ]),
    'db_limit': limite,
    'modo': 'relatorio',
    'cabecalho': u'Comando recebido, aguarde...',
    'multi': False,
    'destino': 'telegram',
    'type': args['command_type'],
  }
  requisicao_usuarios = {
    'db_query': ' '.join([
      "SELECT", ','.join(db_rows()['usuarios']),
      "FROM", db_tables()['usuarios'],
#      "WHERE", 'type_id', 'IS', 'NOT', 'NULL',
      "ORDER", "BY", 'id', "DESC",
#      "LIMIT", str(limite),
    ]),
    'db_limit': limite,
    'modo': 'relatorio',
    'cabecalho': u'Comando recebido, aguarde...',
    'multi': False,
    'destino': 'telegram',
    'type': args['command_type'],
  }
  requisicao_estabelecimentos = {
    'db_query': ' '.join([
      "SELECT", ','.join(db_rows()['estabelecimentos']),
      "FROM", db_tables()['estabelecimentos'],
      "WHERE", 'deleted_at', "IS", "NULL",
      "ORDER", "BY", 'reference_id', "DESC",
#      "LIMIT", str(limite),
    ]),
    'db_limit': limite,
    'modo': 'relatorio',
    'cabecalho': u'Comando recebido, aguarde...',
    'multi': False,
    'destino': 'telegram',
    'type': args['command_type'],
  }

  try:
    pedidos = transaction_local(requisicao_pedidos['db_query'])
    usuarios = transaction_local(requisicao_usuarios['db_query'])
    estabelecimentos = transaction_local(requisicao_estabelecimentos['db_query'])
    if pedidos['status'] and usuarios['status'] and estabelecimentos['status']:
      print(log_str.info(u'Acho que a requisição para o banco de dados deu certo, só mais um pouco...'))
      if (usuarios['response'] != ()) and (pedidos['response'] != ()) and (estabelecimentos['response'] != ()):
        print(log_str.info(u'Dados de usuários e pedidos recebidos. Processando dados...'))

        universo_pedidos = len(pedidos['response'])
        universo_usuarios = len(usuarios['response'])
        pedidos_praca = Counter(rs=0, ce=0, rj=0, sp=0)
        usuarios_pediram = list()
        usuarios_pediram_praca_rs = list()
        usuarios_pediram_praca_ce = list()
        usuarios_pediram_praca_rj = list()
        usuarios_pediram_praca_sp = list()
        opcao_usuarios = Counter(vegano=0, vegetariano=0, simpatizante=0)
        opcao_usuarios_pediram = Counter(vegano=0, vegetariano=0, simpatizante=0)
        opcao_usuarios_pediram_rs = Counter(vegano=0, vegetariano=0, simpatizante=0)
        opcao_usuarios_pediram_ce = Counter(vegano=0, vegetariano=0, simpatizante=0)
        opcao_usuarios_pediram_rj = Counter(vegano=0, vegetariano=0, simpatizante=0)
        opcao_usuarios_pediram_sp = Counter(vegano=0, vegetariano=0, simpatizante=0)
        usuarios_unicos_praca = Counter(rs=0, ce=0, rj=0, sp=0)

        for usuario in usuarios['response']:
          if usuario['type_id'] != None:
            if int(usuario['type_id']) == 1:
              opcao_usuarios.update(vegano = 1)
            elif int(usuario['type_id']) == 2:
              opcao_usuarios.update(vegetariano = 1)
            elif int(usuario['type_id']) == 3:
              opcao_usuarios.update(simpatizante = 1)

        for pedido in pedidos['response']:
          usuario_pedido = next((usuario for usuario in usuarios['response'] if usuario['id'] == pedido['order_user_id']), False)
          estabelecimento_pedido = next((estabelecimento for estabelecimento in estabelecimentos['response'] if estabelecimento['reference_id'] == pedido['order_company_id']), False)
          cidade_pedido = int(estabelecimento_pedido['city_id'])
          usuarios_pediram.append(pedido['order_user_id'])
          if cidade_pedido == 7994:
            pedidos_praca.update(rs=1)
            usuarios_pediram_praca_rs.append(pedido['order_user_id'])
            if usuario_pedido['type_id'] != None:
              if int(usuario_pedido['type_id']) == 1:
                opcao_usuarios_pediram_rs.update(vegano = 1)
              elif int(usuario_pedido['type_id']) == 2:
                opcao_usuarios_pediram_rs.update(vegetariano = 1)
              elif int(usuario_pedido['type_id']) == 3:
                opcao_usuarios_pediram_rs.update(simpatizante = 1)
          elif cidade_pedido == 1347:
            pedidos_praca.update(ce=1)
            usuarios_pediram_praca_ce.append(pedido['order_user_id'])
            if usuario_pedido['type_id'] != None:
              if int(usuario_pedido['type_id']) == 1:
                opcao_usuarios_pediram_ce.update(vegano = 1)
              elif int(usuario_pedido['type_id']) == 2:
                opcao_usuarios_pediram_ce.update(vegetariano = 1)
              elif int(usuario_pedido['type_id']) == 3:
                opcao_usuarios_pediram_ce.update(simpatizante = 1)
          elif cidade_pedido == 7043:
            pedidos_praca.update(rj=1)
            usuarios_pediram_praca_rj.append(pedido['order_user_id'])
            if usuario_pedido['type_id'] != None:
              if int(usuario_pedido['type_id']) == 1:
                opcao_usuarios_pediram_rj.update(vegano = 1)
              elif int(usuario_pedido['type_id']) == 2:
                opcao_usuarios_pediram_rj.update(vegetariano = 1)
              elif int(usuario_pedido['type_id']) == 3:
                opcao_usuarios_pediram_rj.update(simpatizante = 1)
          elif cidade_pedido == 13649:
            pedidos_praca.update(sp=1)
            usuarios_pediram_praca_sp.append(pedido['order_user_id'])
            if usuario_pedido['type_id'] != None:
              if int(usuario_pedido['type_id']) == 1:
                opcao_usuarios_pediram_sp.update(vegano = 1)
              elif int(usuario_pedido['type_id']) == 2:
                opcao_usuarios_pediram_sp.update(vegetariano = 1)
              elif int(usuario_pedido['type_id']) == 3:
                opcao_usuarios_pediram_sp.update(simpatizante = 1)

        universo_usuarios_pediram = len(usuarios_pediram)
        unicos_usuarios = len(set(usuarios_pediram))
        universo_usuarios_pediram_praca_rs = len(usuarios_pediram_praca_rs)
        unicos_usuarios_praca_rs = len(set(usuarios_pediram_praca_rs))
        universo_usuarios_pediram_praca_ce = len(usuarios_pediram_praca_ce)
        unicos_usuarios_praca_ce = len(set(usuarios_pediram_praca_ce))
        universo_usuarios_pediram_praca_rj = len(usuarios_pediram_praca_rj)
        unicos_usuarios_praca_rj = len(set(usuarios_pediram_praca_rj))
        universo_usuarios_pediram_praca_sp = len(usuarios_pediram_praca_sp)
        unicos_usuarios_praca_sp = len(set(usuarios_pediram_praca_sp))

        for usuario_pediu in set(usuarios_pediram):
          usuario_pedido = next((usuario for usuario in usuarios['response'] if usuario['id'] == usuario_pediu), False)
          if usuario_pedido:
            if usuario_pedido['type_id'] != None:
              if int(usuario_pedido['type_id']) == 1:
                opcao_usuarios_pediram.update(vegano = 1)
              elif int(usuario_pedido['type_id']) == 2:
                opcao_usuarios_pediram.update(vegetariano = 1)
              elif int(usuario_pedido['type_id']) == 3:
                opcao_usuarios_pediram.update(simpatizante = 1)

        print(log_str.info(u"Todos dados processados! Formatando..."))
        if universo_usuarios == 0:
          universo_usuarios = -1
        if universo_usuarios_pediram == 0:
          universo_usuarios_pediram = -1
        if universo_usuarios_pediram_praca_rs == 0:
          universo_usuarios_pediram_praca_rs = -1
        if universo_usuarios_pediram_praca_ce == 0:
          universo_usuarios_pediram_praca_ce = -1
        if universo_usuarios_pediram_praca_rj == 0:
          universo_usuarios_pediram_praca_rj = -1
        if universo_usuarios_pediram_praca_sp == 0:
          universo_usuarios_pediram_praca_sp = -1
        if pedidos_praca['rs'] == 0:
          pedidos_praca.subtract(rs = 1)
        if pedidos_praca['ce'] == 0:
          pedidos_praca.subtract(ce = 1)
        if pedidos_praca['rj'] == 0:
          pedidos_praca.subtract(rj = 1)
        if pedidos_praca['sp'] == 0:
          pedidos_praca.subtract(sp = 1)
        response = list()
        response.append(u"Relatório de pedidos e usuária(o)s do Velivery para o período %s:" % (str(args['periodo'])))
        response.append("")
        response.append(
          u"Total de usuária(o)s: %s, que já fizeram pelo menos um pedido: %s (%s%%), únicos: %s (%s%%)" % (
            str(universo_usuarios),
            str(universo_usuarios_pediram),
            str((100*float(universo_usuarios_pediram))/float(universo_usuarios)),
            str(unicos_usuarios),
            str((100*float(unicos_usuarios))/float(universo_pedidos)),
          )
        )
        response.append(
          u"\tVegana(o)s: %s (%s%%), que já pediram: %s (%s%%)" % (
            str(opcao_usuarios['vegano']),
            str((100.0*float(opcao_usuarios['vegano']))/float(universo_usuarios)),
            str(opcao_usuarios_pediram['vegano']),
            str((100.0*float(opcao_usuarios_pediram['vegano']))/float(universo_usuarios_pediram)),
          )
        )
        response.append(
          u"\tVegetariana(o)s: %s (%s%%), que já pediram: %s (%s%%)" % (
            str(opcao_usuarios['vegetariano']),
            str((100.0*float(opcao_usuarios['vegetariano']))/float(universo_usuarios)),
            str(opcao_usuarios_pediram['vegetariano']),
            str((100.0*float(opcao_usuarios_pediram['vegetariano']))/float(universo_usuarios_pediram)),
          )
        )
        response.append(
          u"\tSimpatizantes: %s (%s%%), que já pediram: %s (%s%%)" % (
            str(opcao_usuarios['simpatizante']),
            str((100.0*float(opcao_usuarios['simpatizante']))/float(universo_usuarios)),
            str(opcao_usuarios_pediram['simpatizante']),
            str((100.0*float(opcao_usuarios_pediram['simpatizante']))/float(universo_usuarios_pediram)),
          )
        )
        response.append('$$$EOF$$$')

        response.append(u"Total de pedidos e usuária(o)s por praça:")
        response.append(
          u"\tPorto Alegre: %s pedidos (%s%%), %s usuária(o)s que pediram (%s%%), únicos: %s (%s%%)" % (
            str(pedidos_praca['rs']),
            str((100.00*float(pedidos_praca['rs']))/float(universo_pedidos)),
            str(universo_usuarios_pediram_praca_rs),
            str((100.00*float(universo_usuarios_pediram_praca_rs))/float(universo_usuarios_pediram)),
            str(unicos_usuarios_praca_rs),
            str((100.00*float(unicos_usuarios_praca_rs))/float(pedidos_praca['rs'])),
          )
        )
        response.append(
          u"\t\tVegana(o)s: %s (%s%%)" % (
            str(opcao_usuarios_pediram_rs['vegano']),
            str((100.0*float(opcao_usuarios_pediram_rs['vegano']))/float(universo_usuarios_pediram_praca_rs)),
          )
        )
        response.append(
          u"\t\tVegetarian(o)s: %s (%s%%)" % (
            str(opcao_usuarios_pediram_rs['vegetariano']),
            str((100.0*float(opcao_usuarios_pediram_rs['vegetariano']))/float(universo_usuarios_pediram_praca_rs)),
          )
        )
        response.append(
          u"\t\tSimpatizantes: %s (%s%%)" % (
            str(opcao_usuarios_pediram_rs['simpatizante']),
            str((100.0*float(opcao_usuarios_pediram_rs['simpatizante']))/float(universo_usuarios_pediram_praca_rs)),
          )
        )
        response.append('$$$EOF$$$')
        response.append(
          u"\tFortaleza: %s pedidos (%s%%), %s usuária(o)s que pediram (%s%%), únicos: %s (%s%%)" % (
            str(pedidos_praca['ce']),
            str((100.00*float(pedidos_praca['ce']))/float(universo_pedidos)),
            str(universo_usuarios_pediram_praca_ce),
            str((100.00*float(universo_usuarios_pediram_praca_ce))/float(universo_usuarios_pediram)),
            str(unicos_usuarios_praca_ce),
            str((100.00*float(unicos_usuarios_praca_ce))/float(pedidos_praca['ce'])),
          )
        )
        response.append(
          u"\t\tVegana(o)s: %s (%s%%)" % (
            str(opcao_usuarios_pediram_ce['vegano']),
            str((100.0*float(opcao_usuarios_pediram_ce['vegano']))/float(universo_usuarios_pediram_praca_ce)),
          )
        )
        response.append(
          u"\t\tVegetarian(o)s: %s (%s%%)" % (
            str(opcao_usuarios_pediram_ce['vegetariano']),
            str((100.0*float(opcao_usuarios_pediram_ce['vegetariano']))/float(universo_usuarios_pediram_praca_ce)),
          )
        )
        response.append(
          u"\t\tSimpatizantes: %s (%s%%)" % (
            str(opcao_usuarios_pediram_ce['simpatizante']),
            str((100.0*float(opcao_usuarios_pediram_ce['simpatizante']))/float(universo_usuarios_pediram_praca_ce)),
          )
        )
        response.append('$$$EOF$$$')
        response.append(
          u"\tRio de Janeiro: %s pedidos (%s%%), %s usuária(o)s que pediram (%s%%), únicos: %s (%s%%)" % (
            str(pedidos_praca['rj']),
            str((100.00*float(pedidos_praca['rj']))/float(universo_pedidos)),
            str(universo_usuarios_pediram_praca_rj),
            str((100.00*float(universo_usuarios_pediram_praca_rj))/float(universo_usuarios_pediram)),
            str(unicos_usuarios_praca_rj),
            str((100.00*float(unicos_usuarios_praca_rj))/float(pedidos_praca['rj'])),
          )
        )
        response.append(
          u"\t\tVegana(o)s: %s (%s%%)" % (
            str(opcao_usuarios_pediram_rs['vegano']),
            str((100.0*float(opcao_usuarios_pediram_rj['vegano']))/float(universo_usuarios_pediram_praca_rj)),
          )
        )
        response.append(
          u"\t\tVegetarian(o)s: %s (%s%%)" % (
            str(opcao_usuarios_pediram_rj['vegetariano']),
            str((100.0*float(opcao_usuarios_pediram_rj['vegetariano']))/float(universo_usuarios_pediram_praca_rj)),
          )
        )
        response.append(
          u"\t\tSimpatizantes: %s (%s%%)" % (
            str(opcao_usuarios_pediram_rj['simpatizante']),
            str((100.0*float(opcao_usuarios_pediram_rj['simpatizante']))/float(universo_usuarios_pediram_praca_rj)),
          )
        )
        response.append('$$$EOF$$$')
        response.append(
          u"\tSão Paulo: %s pedidos (%s%%), %s usuária(o)s que pediram (%s%%), únicos: %s (%s%%)" % (
            str(pedidos_praca['sp']),
            str((100.00*float(pedidos_praca['sp']))/float(universo_pedidos)),
            str(universo_usuarios_pediram_praca_sp),
            str((100.00*float(universo_usuarios_pediram_praca_sp))/float(universo_usuarios_pediram)),
            str(unicos_usuarios_praca_sp),
            str((100.00*float(unicos_usuarios_praca_sp))/float(pedidos_praca['sp'])),
          )
        )
        response.append(
          u"\t\tVegana(o)s: %s (%s%%)" % (
            str(opcao_usuarios_pediram_sp['vegano']),
            str((100.0*float(opcao_usuarios_pediram_sp['vegano']))/float(universo_usuarios_pediram_praca_sp)),
          )
        )
        response.append(
          u"\t\tVegetarian(o)s: %s (%s%%)" % (
            str(opcao_usuarios_pediram_sp['vegetariano']),
            str((100.0*float(opcao_usuarios_pediram_sp['vegetariano']))/float(universo_usuarios_pediram_praca_sp)),
          )
        )
        response.append(
          u"\t\tSimpatizantes: %s (%s%%)" % (
            str(opcao_usuarios_pediram_sp['simpatizante']),
            str((100.0*float(opcao_usuarios_pediram_sp['simpatizante']))/float(universo_usuarios_pediram_praca_sp)),
          )
        )
        response.append('$$$EOF$$$')

        response.append("<insira piada sem graça do dia aqui>")

        return {
          'status': True,
          'type': 'grupo',
          'multi': True,
          'destino': 'telegram',
          'response': "\n".join(response),
          'debug': u'Sucesso!',
          'parse_mode': None,
        }
      else:
        print(log_str.info(u'Nenhum usuário ou pedido foi encontrado. Só esperando o @desobedientecivil agora :('))
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
          'response': u"Nenhum usuário ou pedido encontrado",
          'debug': u'Nenhum usuário ou pedido encontrado',
          'parse_mode': None,
        }
    else:
      print(log_str.info(u'Erro tentando requisitar o banco de dados. Só esperando o @desobedientecivil agora :('))
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': usuarios['response'],
        'debug': usuarios['debug'],
        'parse_mode': None,
      }
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
      'debug': u'Exceção: %s' % (e),
      'parse_mode': None,
    }

