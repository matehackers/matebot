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

def db_timezone():
  return pytz.timezone('America/Sao_Paulo')

def db_datetime():
  return '%Y-%m-%d %H:%M:%S'

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

def query_pedidos():
  return " ".join([
    "SELECT", ",".join([
      " ".join([
        ".".join([
          db_tables()['pedidos'],
          'reference_id',
        ]),
        "AS", 'order_id',
      ]),
      " ".join([
        ".".join([
          db_tables()['pedidos'],
          'created_at',
        ]),
        "AS", 'order_created_at',
      ]),
      " ".join([
        ".".join([
          db_tables()['pedidos'],
          'delivery_datetime',
        ]),
        "AS", 'order_delivery_datetime',
      ]),
      " ".join([
        ".".join([
          db_tables()['pedidos'],
          'origin',
        ]),
        "AS", 'order_origin',
      ]),
      " ".join([
        ".".join([
          db_tables()['pedidos'],
          'description',
        ]),
        "AS", 'order_description',
      ]),
      " ".join([
        ".".join([
          db_tables()['status'],
          'reference_id',
        ]),
        "AS", 'status_id',
      ]),
      " ".join([
        ".".join([
          db_tables()['status'],
          'name',
        ]),
        "AS", 'status_name',
      ]),
      " ".join([
        ".".join([
          db_tables()['metodos_pagamento'],
          'reference_id',
        ]),
        "AS", 'payment_id',
      ]),
      " ".join([
        ".".join([
          db_tables()['metodos_pagamento'],
          'name',
        ]),
        "AS", 'payment_name',
      ]),
      " ".join([
        ".".join([
          db_tables()['usuarios'],
          'id',
        ]),
        "AS", 'user_id',
      ]),
      " ".join([
        ".".join([
          db_tables()['usuarios'],
          'name',
        ]),
        "AS", 'user_name',
      ]),
      " ".join([
        ".".join([
          db_tables()['usuarios'],
          'email',
        ]),
        "AS", 'user_email',
      ]),
      " ".join([
        ".".join([
          db_tables()['estabelecimentos'],
          'reference_id',
        ]),
        "AS", 'company_id',
      ]),
      " ".join([
        ".".join([
          db_tables()['estabelecimentos'],
          'name',
        ]),
        "AS", 'company_name',
      ]),
      " ".join([
        ".".join([
          db_tables()['estabelecimentos'],
          'email',
        ]),
        "AS", 'company_email',
      ]),
      " ".join([
        ".".join([
          db_tables()['estabelecimentos'],
          'phone_number',
        ]),
        "AS", 'company_phone_number',
      ]),
      " ".join([
        ".".join([
          db_tables()['enderecos'],
          'reference_id',
        ]),
        "AS", 'address_id',
      ]),
      " ".join([
        ".".join([
          db_tables()['enderecos'],
          'street_code',
        ]),
        "AS", 'address_code',
      ]),
      " ".join([
        ".".join([
          db_tables()['enderecos'],
          'street_name',
        ]),
        "AS", 'address_name',
      ]),
      " ".join([
        ".".join([
          db_tables()['enderecos'],
          'street_number',
        ]),
        "AS", 'address_number',
      ]),
      " ".join([
        ".".join([
          db_tables()['enderecos'],
          'street_complement',
        ]),
        "AS", 'address_complement',
      ]),
      " ".join([
        ".".join([
          db_tables()['enderecos'],
          'street_reference',
        ]),
        "AS", 'address_reference',
      ]),
      " ".join([
        ".".join([
          db_tables()['enderecos'],
          'district_name',
        ]),
        "AS", 'address_district',
      ]),
      " ".join([
        ".".join([
          db_tables()['enderecos'],
          'phone_number',
        ]),
        "AS", 'address_phone_number',
      ]),
      " ".join([
        ".".join([
          db_tables()['cidades'],
          'reference_id',
        ]),
        "AS", 'city_id',
      ]),
      " ".join([
        ".".join([
          db_tables()['cidades'],
          'name',
        ]),
        "AS", 'city_name',
      ]),
    ]),
    "FROM", db_tables()['pedidos'],
    "INNER", "JOIN", db_tables()['estabelecimentos'],
    "ON", "=".join([
      ".".join([
        db_tables()['pedidos'],
        'order_company_id',
      ]),
      ".".join([
        db_tables()['estabelecimentos'],
        'reference_id',
      ]),
    ]),
    "INNER", "JOIN", db_tables()['usuarios'],
    "ON", "=".join([
      ".".join([
        db_tables()['pedidos'],
        'order_user_id',
      ]),
      ".".join([
        db_tables()['usuarios'],
        'id',
      ]),
    ]),
    "INNER", "JOIN", db_tables()['status'],
    "ON", "=".join([
      ".".join([
        db_tables()['pedidos'],
        'order_request_status_id',
      ]),
      ".".join([
        db_tables()['status'],
        'reference_id',
      ]),
    ]),
    "INNER", "JOIN", db_tables()['metodos_pagamento'],
    "ON", "=".join([
      ".".join([
        db_tables()['pedidos'],
        'order_payment_method_id',
      ]),
      ".".join([
        db_tables()['metodos_pagamento'],
        'reference_id',
      ]),
    ]),
    "INNER", "JOIN", db_tables()['enderecos'],
    "ON", "=".join([
      ".".join([
        db_tables()['pedidos'],
        'order_request_address_id',
      ]),
      ".".join([
        db_tables()['enderecos'],
        'reference_id',
      ]),
    ]),
    "INNER", "JOIN", db_tables()['cidades'],
    "ON", "=".join([
      ".".join([
        db_tables()['estabelecimentos'],
        'city_id',
      ]),
      ".".join([
        db_tables()['cidades'],
        'reference_id',
      ]),
    ]),
    "WHERE", ".".join([
      db_tables()['pedidos'],
      'deleted_at',
    ]), "IS NULL",
    "AND", ".".join([
      db_tables()['estabelecimentos'],
      'deleted_at',
    ]), "IS NULL",
    "AND", ".".join([
      db_tables()['status'],
      'deleted_at',
    ]), "IS NULL",
    "AND", ".".join([
      db_tables()['metodos_pagamento'],
      'deleted_at',
    ]), "IS NULL",
    "AND", ".".join([
      db_tables()['enderecos'],
      'deleted_at',
    ]), "IS NULL",
    "AND", ".".join([
      db_tables()['cidades'],
      'deleted_at',
    ]), "IS NULL",
  ])

def query_pendentes():
  return " ".join([
    query_pedidos(),
    "AND", "=".join([
      ".".join([
        db_tables()['pedidos'],
        'order_request_status_id',
      ]),
      '1',
    ]),
    "AND", ">=".join([
      ".".join([
        db_tables()['pedidos'],
        'created_at',
      ]),
      "".join([
        "'",
        (datetime.datetime.now(db_timezone()) - datetime.timedelta(days=2)).strftime(db_datetime()),
        "'",
      ]),
    ]),
  ])

def query_atrasados():
  return " ".join([
    query_pendentes(),
    "AND", " ".join([
      ".".join([
        db_tables()['pedidos'],
        'delivery_datetime',
      ]),
      "IS", "NULL",
    ]),
  ])

def query_atrasados_1():
  return " ".join([
    query_atrasados(),
    "AND", "<".join([
      ".".join([
        db_tables()['pedidos'],
        'created_at',
      ]),
      "".join([
        "'",
        (datetime.datetime.now(db_timezone()) - datetime.timedelta(minutes=7)).strftime(db_datetime()),
        "'",
      ]),
    ]),
  ])

def query_atrasados_2():
  return " ".join([
    query_atrasados(),
    "AND", "<".join([
      ".".join([
        db_tables()['pedidos'],
        'created_at',
      ]),
      "".join([
        "'",
        (datetime.datetime.now(db_timezone()) - datetime.timedelta(minutes=14)).strftime(db_datetime()),
        "'",
      ]),
    ]),
  ])

def query_atrasados_3():
  return " ".join([
    query_atrasados(),
    "AND", "<".join([
      ".".join([
        db_tables()['pedidos'],
        'created_at',
      ]),
      "".join([
        "'",
        (datetime.datetime.now(db_timezone()) - datetime.timedelta(minutes=21)).strftime(db_datetime()),
        "'",
      ]),
    ]),
  ])

def query_atrasados_teste():
  return " ".join([
    query_pedidos(),
    "AND", "=".join([
      ".".join([
        db_tables()['pedidos'],
        'order_request_status_id',
      ]),
      '4',
    ]),
    "AND", ">=".join([
      ".".join([
        db_tables()['pedidos'],
        'created_at',
      ]),
      "".join([
        "'",
        (datetime.datetime.now(db_timezone()) - datetime.timedelta(days=10)).strftime(db_datetime()),
        "'",
      ]),
    ]),
  ])
