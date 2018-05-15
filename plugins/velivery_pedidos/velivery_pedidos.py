# vim:fileencoding=utf-8

### Imports
import configparser
import pymysql
import pymysql.cursors
import datetime
import time
import json

class velivery_pedidos():
  def __init__(self):
    self.db_limit = str(5)

  def transaction(self, db_query):
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
          ## TODO tratar exceções
          if ( e == configparser.NoSectionError ):
              print(e)
          else:
              print(e)
      self.connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
      ## TODO tratar exceções
      print(e)
    try:
      with self.connection.cursor() as cursor:
        cursor.execute(db_query)
      result = cursor.fetchall()
      return result
    except Exception as e:
      print(e)
      return(1)
    connection.close()

  def formatar(self, pedido):
    time.sleep(1)
    retorno = list()
    status = self.transaction(' '.join(["SELECT", 'short_name', "FROM", 'order_request_status', "WHERE", '='.join(['reference_id', str(pedido['order_request_status_id'])])]))
    metodo_pagamento = self.transaction(' '.join(["SELECT", 'short_name', "FROM", 'order_payment_methods', "WHERE", '='.join(['reference_id', str(pedido['order_payment_method_id'])]), "ORDER BY", 'updated_at', "DESC"]))
    usuario = self.transaction(' '.join(["SELECT", 'name, email', "FROM", 'app_users', "WHERE", '='.join(['id', str(pedido['order_user_id'])]), "ORDER BY", 'updated_at', "DESC"]))
    estabelecimento = self.transaction(' '.join(["SELECT", 'short_name, phone_number, email, schedule_when_opened, schedule_when_closed', "FROM", 'order_companies', "WHERE", '='.join(['reference_id', str(pedido['order_company_id'])]), "ORDER BY", 'updated_at', "DESC"]))
    endereco = self.transaction(' '.join(["SELECT", 'street_code, street_name, street_number, street_complement, street_reference, district_name', "FROM", 'order_request_addresses', "WHERE", '='.join(['reference_id', str(pedido['order_request_address_id'])]), "ORDER BY", 'updated_at', "DESC"]))
    
    retorno.append('\t'.join([u'Código:', str(pedido['reference_id'])]))
    retorno.append('\t'.join([u'Hora:', str(pedido['created_at'])]))
    retorno.append('\t'.join([u'Status:', str(status[0]['short_name'])]))
    if pedido['order_request_status_id'] == 1 and pedido['created_at'] == pedido['updated_at']:
      retorno.append('\t'.join([u'Tempo aguardando:', str(datetime.datetime.now() - pedido['created_at'])]))
    elif pedido['deleted_at'] != None:
      retorno.append('\t'.join([u'Excluído:', str(pedido['deleted_at'])]))
    else:
      retorno.append('\t'.join([u'Atendido:', str(pedido['updated_at'])]))
    retorno.append('\t'.join([u'Descrição:', str(pedido['description'])]))
    retorno.append('\t'.join([u'Método de Pagamento:', str(metodo_pagamento[0]['short_name'])]))
    if float(pedido['delivery_price']) > 0.00:
      retorno.append('\t'.join([u'Preço da entrega:', str(pedido['delivery_price'])]))
    if float(pedido['payment_change']) > 0.00:
      retorno.append('\t'.join([u'Troco:', str(pedido['payment_change'])]))
    retorno.append('\t'.join([u'Origem:', str(pedido['origin'])]))
    retorno.append('\t'.join([u'Usuária(o) Nome:', str(usuario[0]['name'])]))
    retorno.append('\t'.join([u'Usuária(o) E-mail:', str(usuario[0]['email'])]))
    retorno.append('\t'.join([u'Estabelecimento Nome:', str(estabelecimento[0]['short_name'])]))
    retorno.append('\t'.join([u'Estabelecimento E-mail:', str(estabelecimento[0]['email'])]))
    retorno.append('\t'.join([u'Estabelecimento Telefone:', str(estabelecimento[0]['phone_number'])]))
    retorno.append('\t'.join([u'Endereço CEP:', str(endereco[0]['street_code'])]))
    retorno.append('\t'.join([u'Endereço Nome:', str(endereco[0]['street_name'])]))
    retorno.append('\t'.join([u'Endereço Número:', str(endereco[0]['street_number'])]))
    retorno.append('\t'.join([u'Endereço Complemento:', str(endereco[0]['street_complement'])]))
    retorno.append('\t'.join([u'Endereço Referência:', str(endereco[0]['street_reference'])]))
    retorno.append('\t'.join([u'Endereço Distrito:', str(endereco[0]['district_name'])]))
    if pedido['delivery_datetime'] != None:
      retorno.append('\t'.join([u'Agendado para:', str(pedido['delivery_datetime'])]))
    return retorno

  def todos_pedidos(self, limite):
    limite = self.db_limit
    retorno = list()
    resposta = dict()
#    try:
    pedidos = self.transaction(' '.join(["SELECT", 'reference_id, updated_at, order_payment_method_id, order_request_address_id, order_company_id, payment_change, order_request_status_id, order_user_id, created_at, description, delivery_datetime, delivery_price, origin, deleted_at', "FROM", 'order_requests', "WHERE 'company_hash' != ''", "ORDER BY", 'created_at', "DESC", "LIMIT", str(limite)]))
    retorno.append(u'Todos os pedidos (exibindo os últimos %s pedidos):\n' % (limite))
    for pedido in pedidos:
      retorno.append('\n'.join(self.formatar(pedido)))
      retorno.append('')
    return {
      'status': True,
      'type': 'mensagem',
      'response': str('\n'.join(retorno)),
      'debug': '[INFO] Sucesso: %s\nlimite: %s\nretorno: %s' % (self, limite, retorno),
    }
#    except Exception as e:
#      return {
#        'status': False,
#        'type': 'erro',
#        'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
#        'debug': '[ERR] Exception em %s: %s' % (self, e),
#      }

  ## Pedidos pendentes das últimas 48 horas
  def pendentes(self, limite):
    limite = self.db_limit
    retorno = list()
    resposta = dict()
#    try:
    regra_tempo_2 = (datetime.datetime.now() - datetime.timedelta(days=2))
    pedidos = self.transaction(' '.join(["SELECT", 'reference_id, updated_at, order_payment_method_id, order_request_address_id, order_company_id, payment_change, order_request_status_id, order_user_id, created_at, description, delivery_datetime, delivery_price, origin, deleted_at', "FROM", 'order_requests', "WHERE", 'order_request_status_id=1', "AND", "company_hash != ''", "AND", 'created_at = updated_at', "AND", ''.join(['created_at >= ', "'", str(regra_tempo_2), "'"]), "ORDER BY", 'created_at', "DESC", "LIMIT", str(limite)]))
    pedidos_pendentes = (pedidos != ())
    if pedidos_pendentes:
      retorno.append(u'Temos %s pedidos pendentes (exibindo os últimos %s):\n' % (pedidos.length, limite))
      for pedido in pedidos:
        retorno.append('\n'.join(self.formatar(pedido)))
        retorno.append('')
      return {
        'status': True,
        'type': 'mensagem',
        'response': str('\n'.join(retorno)),
        'debug': '[INFO] Sucesso: %s\nlimite: %s\nretorno: %s' % (self, limite, retorno),
      }
    else:
      return {
        'status': False,
        'type': 'mensagem',
        'response': u'Nenhum pedido pendente. Bom trabalho, Velivery!',
        'debug': '[INFO] Sucesso: %s\nlimite: %s\npedidos: %s' % (self, limite, pedidos),
      }
#    except Exception as e:
#      return {
#        'status': False,
#        'type': 'erro',
#        'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
#        'debug': '[ERR] Exception em %s: %s' % (self, e),
#      }

  ## Pedidos atrasados
  def atrasados(self, limite):
    limite = self.db_limit
    retorno = list()
    resposta = dict()
#    try:
    regra_tempo_1 = (datetime.datetime.now() - datetime.timedelta(minutes=5))
    regra_tempo_2 = (datetime.datetime.now() - datetime.timedelta(days=2))
    pedidos = self.transaction(' '.join(["SELECT", 'reference_id, updated_at, order_payment_method_id, order_request_address_id, order_company_id, payment_change, order_request_status_id, order_user_id, created_at, description, delivery_datetime, delivery_price, origin, deleted_at', "FROM", 'order_requests', "WHERE", 'order_request_status_id = 1', "AND", "company_hash != ''", "AND", 'created_at = updated_at', "AND", ''.join(['created_at < ', "'", str(regra_tempo_1), "'"]), "AND", ''.join(['created_at >= ', "'", str(regra_tempo_2), "'"]), "AND", 'delivery_datetime', "IS", "NULL", "ORDER BY", 'created_at', "DESC", "LIMIT", str(limite)]))
    pedidos_pendentes = (pedidos != ())
    if pedidos_pendentes:
      retorno.append(u'Temos %s pedidos pendentes (exibindo os últimos %s):\n' % (pedidos.length, limite))
      for pedido in pedidos:
        retorno.append('\n'.join(self.formatar(pedido)))
        retorno.append('')
      return {
        'status': True,
        'type': 'mensagem',
        'response': str('\n'.join(retorno)),
        'debug': '[INFO] Sucesso: %s\nlimite: %s\nretorno: %s' % (self, limite, retorno),
      }
    else:
      return {
        'status': False,
        'type': 'mensagem',
        'response': u'Nenhum pedido atrasado. Bom trabalho, Velivery!',
        'debug': '[INFO] Sucesso: %s\nlimite: %s\npedidos: %s' % (self, limite, pedidos),
      }
#    except Exception as e:
#      return {
#        'status': False,
#        'type': 'erro',
#        'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
#        'debug': '[ERR] Exception em %s: %s' % (self, e),
#      }

  ## Pedidos El Pasito
  def pendentes_pasito(self):
    resultado = self.transaction(' '.join(["SELECT", '*', "FROM", 'order_requests', "WHERE", 'order_company_id=110', "ORDER BY", 'created_at', "DESC","LIMIT", self.db_limit]))
    print('resultado:', resultado)
    for row in resultado:
      print('row:', row)
    return [(resultado != ()), 'NENHUM']

## Todos pedidos
#for row in transaction(' '.join(["SELECT", '*', "FROM", 'order_requests', "ORDER BY", 'created_at', "DESC","LIMIT", db_limit])):
#    print(row)

## Todos pedidos pendentes
#for row in transaction(' '.join(["SELECT", '*', "FROM", 'order_requests', "WHERE", 'order_request_status_id=1', "AND", "company_hash != ''", "AND", 'created_at = updated_at', "AND", ''.join(['created_at < ', "'", str(regra_tempo_1), "'"]), "ORDER BY", 'created_at', "DESC", "LIMIT", str(10)])):
#    print(row)

## Achar El Pasito
#for row in transaction(' '.join(["SELECT", '*', "FROM", 'order_companies', "WHERE", "name='El Pasito'"])):
#    print(row)

## Pedido 37361
#for row in transaction(' '.join(["SELECT", '*', "FROM", 'order_requests', "WHERE", "reference_id=37361"])):
#    print(row)

