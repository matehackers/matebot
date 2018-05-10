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
    self.db_limit = str(30)

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
      self.connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database)
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

  ## Pedidos pendentes das últimas 48 horas
  def pendentes_u48h(self):
    retorno = list()
    resposta = dict()
    regra_tempo_1 = (datetime.datetime.now() - datetime.timedelta(minutes=5))
    regra_tempo_2 = (datetime.datetime.now() - datetime.timedelta(days=2))
    pedidos = self.transaction(' '.join(["SELECT", 'reference_id', "FROM", 'order_requests', "WHERE", 'order_request_status_id=1', "AND", "company_hash != ''", "AND", 'created_at = updated_at', "AND", ''.join(['created_at < ', "'", str(regra_tempo_1), "'"]), "AND", ''.join(['created_at >= ', "'", str(regra_tempo_2), "'"]), "ORDER BY", 'created_at', "DESC", "LIMIT", str(10)]))
    for pedido in pedidos:
      resposta['pedido_codigo'] = str(pedido[0])
      time.sleep(1)
      data_criacao = self.transaction(' '.join(["SELECT", 'created_at', "FROM", 'order_requests', "WHERE", '='.join(['reference_id', str(pedido[0])])]))
      resposta['pedido_data_criacao'] = data_criacao[0][0]
      time.sleep(1)
      estabelecimento_id = self.transaction(' '.join(["SELECT", 'order_company_id', "FROM", 'order_requests', "WHERE", '='.join(['id', str(pedido[0])])]))
      time.sleep(1)
      estabelecimento_dados = self.transaction(' '.join(["SELECT", 'short_name, default_opening_time, default_closing_time, phone_number, email, default_opening_time_2, default_closing_time_2, schedule_when_opened, schedule_when_closed', "FROM", 'order_companies', "WHERE", '='.join(['id', str(estabelecimento_id[0][0])]), "ORDER BY", 'updated_at', "DESC"]))
      
      ## TODO identificando problema com nomes alterados recentemente
      print(estabelecimento_dados)
      print(estabelecimento_dados[0])
      
      resposta['pedido_estabelecimento'] = dict()
      resposta['pedido_estabelecimento']['nome'] = estabelecimento_dados[0][0]
      resposta['pedido_estabelecimento']['horario_abertura'] = estabelecimento_dados[0][1]
      resposta['pedido_estabelecimento']['horario_fechamento'] = estabelecimento_dados[0][2]
      resposta['pedido_estabelecimento']['telefone'] = estabelecimento_dados[0][3]
      resposta['pedido_estabelecimento']['email'] = estabelecimento_dados[0][4]
      resposta['pedido_estabelecimento']['horario_abertura_2'] = estabelecimento_dados[0][5]
      resposta['pedido_estabelecimento']['horario_fechamento_2'] = estabelecimento_dados[0][6]
      resposta['pedido_estabelecimento']['agenda_abertura'] = bool(estabelecimento_dados[0][7])
      resposta['pedido_estabelecimento']['agenda_fechamento'] = bool(estabelecimento_dados[0][8])
      retorno.append('\n'.join([
        '\t'.join([u'Código:', str(resposta['pedido_codigo'])]),
        '\t'.join([u'Hora:', str(resposta['pedido_data_criacao'])]),
        '\t'.join([u'Tempo aguardando:', str(datetime.datetime.now() - resposta['pedido_data_criacao'])]),
        '\t'.join([u'Estabelecimento:', str(resposta['pedido_estabelecimento']['nome'])]),
        '\t'.join([u'Telefone:', str(resposta['pedido_estabelecimento']['telefone'])]),
        '\t'.join([u'E-mail:', str(resposta['pedido_estabelecimento']['email'])]),
        '\t'.join([u'Horário de abertura:', str(resposta['pedido_estabelecimento']['horario_abertura'])]),
        '\t'.join([u'Horário de encerramento:', str(resposta['pedido_estabelecimento']['horario_fechamento'])]),
        '\t'.join([u'Horário de abertura 2:', str(resposta['pedido_estabelecimento']['horario_abertura_2'])]),
        '\t'.join([u'Horário de encerramento 2:', str(resposta['pedido_estabelecimento']['horario_fechamento_2'])]),
        '\t'.join([u'Agenda abertura:', str(resposta['pedido_estabelecimento']['agenda_abertura'])]),
        '\t'.join([u'Agenda encerramento:', str(resposta['pedido_estabelecimento']['agenda_fechamento'])]),
        ''
        ]))
    pedidos_pendentes = (pedidos != ())
    if pedidos_pendentes:
      return [pedidos_pendentes, '\n'.join(retorno)]
    else:
      return [pedidos_pendentes, u'Nenhum pedido pendente. Bom trabalho, Velivery!']

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



