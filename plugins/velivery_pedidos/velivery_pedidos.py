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
    self.db_tables = {
      'pedidos': 'order_requests',
      'estabelecimentos': 'order_companies',
      'usuarios': 'app_users',
      'status': 'order_request_status',
      'metodos_pagamento': 'order_payment_methods',
      'enderecos': 'order_request_addresses',
    }
    self.db_rows = {
      'pedidos': ['id', 'reference_id', 'updated_at', 'order_payment_method_id', 'order_request_address_id', 'order_company_id', 'payment_change', 'order_request_status_id', 'order_user_id', 'created_at', 'description', 'delivery_datetime', 'delivery_price', 'origin', 'deleted_at'],
      'estabelecimentos': ['short_name', 'phone_number', 'email', 'schedule_when_opened', 'schedule_when_closed'],
      'usuarios': ['name', 'email'],
      'status': ['short_name'],
      'metodos_pagamento': ['short_name'],
      'enderecos': ['street_code', 'street_name', 'street_number', 'street_complement', 'street_reference', 'district_name'],
    }
  
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
    db_query = ' '.join(["SELECT", ", ".join(self.db_rows['status']), "FROM", self.db_tables['status'], "WHERE", '='.join(['reference_id', str(pedido['order_request_status_id'])])])
    time.sleep(0.001)
    status = self.transaction(db_query)
    
    db_query = ' '.join(["SELECT", ", ".join(self.db_rows['metodos_pagamento']), "FROM", self.db_tables['metodos_pagamento'], "WHERE", '='.join(['reference_id', str(pedido['order_payment_method_id'])]), "ORDER BY", 'updated_at', "DESC"])
    metodo_pagamento = self.transaction(db_query)
    
    db_query = ' '.join(["SELECT", ", ".join(self.db_rows['usuarios']), "FROM", self.db_tables['usuarios'], "WHERE", '='.join(['id', str(pedido['order_user_id'])]), "ORDER BY", 'updated_at', "DESC"])
    time.sleep(0.001)
    usuario = self.transaction(db_query)
    
    db_query = ' '.join(["SELECT", ", ".join(self.db_rows['estabelecimentos']), "FROM", self.db_tables['estabelecimentos'], "WHERE", '='.join(['reference_id', str(pedido['order_company_id'])]), "ORDER BY", 'updated_at', "DESC"])
    time.sleep(0.001)
    estabelecimento = self.transaction(db_query)
    
    db_query = ' '.join(["SELECT", ", ".join(self.db_rows['enderecos']), "FROM", self.db_tables['enderecos'], "WHERE", '='.join(['reference_id', str(pedido['order_request_address_id'])]), "ORDER BY", 'updated_at', "DESC"])
    time.sleep(0.001)
    endereco = self.transaction(db_query)
    
    retorno = list()
    retorno.append('\t'.join([u'Código:', str(pedido['reference_id'])]))
    retorno.append('\t'.join([u'Status:', str(status[0]['short_name'])]))
    retorno.append('\t'.join([u'Criado em:', str(pedido['created_at'])]))
    if pedido['created_at'] == pedido['updated_at'] and pedido['order_request_status_id'] == 1:
        retorno.append('\t'.join([u'Tempo aguardando:', str(datetime.datetime.now() - pedido['created_at'])]))
    else:
      retorno.append('\t'.join([u'Atualizado em:', str(pedido['updated_at'])]))
    if pedido['deleted_at'] != None:
      retorno.append('\t'.join([u'Excluído em:', str(pedido['deleted_at'])]))
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
  
  def busca(self, requisicao):
    retorno = list()
    resposta = dict()
#    try:
    time.sleep(0.001)
    pedidos = self.transaction(' '.join(["SELECT", ", ".join(self.db_rows['pedidos']), "FROM", self.db_tables['pedidos'], requisicao['db_query']]))
    if (pedidos != ()):
      retorno.append(requisicao['cabecalho'])
      codigos = list()
      for pedido in pedidos:
        if requisicao['modo'] == 'atrasados':
          codigos.append(str(pedido['reference_id']))
        elif requisicao['modo'] == 'pedido':
          retorno.append(''.join(['\n', '\t'.join([u'id:', str(pedido['id'])])]))
        retorno.append('\n'.join(self.formatar(pedido)))
        if requisicao['multi']:
          retorno.append('$$$EOF$$$')
        retorno.append(str())
      if requisicao['modo'] == 'atrasados':
        retorno.insert(0, u'%s pedidos atrasados (%s):\n' % (len(pedidos), ', '.join(codigos)))
      elif requisicao['modo'] == 'pendentes':
        retorno.insert(0, u'Temos %s pedidos pendentes:\n' % (len(pedidos)))
      return {
        'status': True,
        'type': 'mensagem',
        'multi': requisicao['multi'],
        'response': str('\n'.join(retorno)),
        'debug': '[INFO] Sucesso: %s\nrequisicao: %s\npedidos: %s' % (self, requisicao, pedidos),
      }
    else:
      return {
        'status': False,
        'type': 'mensagem',
        'multi': False,
        'response': str(requisicao['nenhum']),
        'debug': '[INFO] Sucesso: %s\nrequisicao: %s\npedidos: %s' % (self, requisicao, pedidos),
      }
#    except Exception as e:
#      return {
#        'status': False,
#        'type': 'erro',
#        'response': u'Tivemos um problema técnico e não conseguimos encontrar o que pedirdes.',
#        'debug': '[ERR] Exception em %s: %s' % (self, e),
#      }
  
  ## Todos pedidos
  def todos(self, limite):
    requisicao = {
      'db_query': ' '.join(["WHERE 'company_hash' != ''", "ORDER BY", 'created_at', "DESC", "LIMIT", str(limite)]),
      'db_limit': limite,
      'modo': 'todos',
      'cabecalho': u'Todos os pedidos (exibindo os últimos %s pedidos):\n' % (limite),
      'multi': True,
    }
    return self.busca(requisicao)
  
  ## Pedido por número
  def pedido(self, pedido, limite):
    requisicao = {
      'db_query': ' '.join(["WHERE", '='.join(['reference_id', str(pedido)]), "ORDER BY", 'id', "ASC", "LIMIT", str(limite)]),
      'db_limit': limite,
      'modo': 'pedido',
      'cabecalho': u'Pedido %s:' % (str(pedido)),
      'nenhum': u'Pedido %s não encontrado!' % (str(pedido)),
      'multi': False,
    }
    return self.busca(requisicao)

  ## Pedidos pendentes das últimas 48 horas
  def pendentes(self, limite):
    requisicao = {
      'db_query': ' '.join(["WHERE", 'order_request_status_id = 1', "AND", "company_hash != ''", "AND", 'created_at = updated_at', "AND", ''.join(['created_at >= ', "'", str(datetime.datetime.now() - datetime.timedelta(days=2)), "'"]), "ORDER BY", 'created_at', "DESC", "LIMIT", str(limite)]),
      'db_limit': limite,
      'modo': 'pendentes',
      'cabecalho': str(),
      'nenhum': u'Nenhum pedido pendente. Bom trabalho, Velivery!',
      'multi': False,
    }
    return self.busca(requisicao)
  
  ## Pedidos atrasados
  def atrasados(self, limite):
    requisicao = {
      'db_query': ' '.join(["WHERE", 'order_request_status_id = 1', "AND", "company_hash != ''", "AND", 'created_at = updated_at', "AND", ''.join(['created_at < ', "'", str(datetime.datetime.now() - datetime.timedelta(minutes=5)), "'"]), "AND", ''.join(['created_at >= ', "'", str(datetime.datetime.now() - datetime.timedelta(days=2)), "'"]), "AND", 'delivery_datetime', "IS", "NULL", "ORDER BY", 'created_at', "DESC", "LIMIT", str(limite)]),
      'db_limit': limite,
      'modo': 'atrasados',
      'cabecalho': str(),
      'nenhum': u'Nenhum pedido atrasado. Bom trabalho, Velivery!',
      'multi': False,
    }
    return self.busca(requisicao)

