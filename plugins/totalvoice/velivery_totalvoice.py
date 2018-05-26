# vim:fileencoding=utf-8

### Imports
import configparser
from totalvoice.cliente import Cliente

class velivery_totalvoice():
  def __init__(self):
    ### Variáveis
    self.tv_config_file = str("config/.matebot.cfg")
    self.tv_config = configparser.ConfigParser()
    try:
      self.tv_config.read(self.tv_config_file)
      self.tv_token = str(self.tv_config.get("totalvoice", "token"))
      self.tv_host = str(self.tv_config.get("totalvoice", "host"))
      self.fone_velivery = str(self.tv_config.get("agenda", "velivery"))
      self.fone_iuri = str(self.tv_config.get("agenda", "iuri"))
      self.fone_benhur = str(self.tv_config.get("agenda", "benhur"))
      self.fone_guilherme = str(self.tv_config.get("agenda", "guilherme"))
      self.cliente = Cliente(self.tv_token, self.tv_host)
      print(self.cliente)
      self.default_fone_restaurante = self.fone_iuri
      self.default_mensagem_pedido_atrasado = "Oi, aqui é a Shiva, tudo bem? Tem um pedido atrasado no aplicativo Velívery, aquele vegetariano! Obrigada!"
    except Exception as e:
      ## TODO tratar exceções
      if ( e == configparser.NoSectionError ):
        print(e)
      else:
        print(e)
    
  
  ##Cria SMS
  def sms_criar(self, numero_destino, mensagem):
    self.cliente.sms.enviar(numero_destino, mensagem)
  ##Cria TTS
  def tts_criar(self, numero_destino, mensagem):
    self.cliente.tts.enviar(numero_destino, mensagem)

### Chamadas

#Cria chamada
#numero_origem = fone_velivery
#numero_destino = fone_restaurante
#response = cliente.chamada.enviar(numero_origem, numero_destino)
#print(response)

#Get chamada
#id = "1958"
#response = cliente.chamada.get_by_id(id)
#print(response)

##Get URL da chamada
#id = "1958"
#response = cliente.chamada.get_gravacao_chamada(id) 
#print(response)

##Relatório de chamada
#data_inicio = "2016-03-30T17:15:59-03:00"
#data_fim = "2016-03-30T17:15:59-03:00"
#response = cliente.chamada.get_relatorio(data_inicio, data_fim)
#print(response)

##Escutar chamada (BETA)
#id_chamada = "1958"
#numero = "48999999999"
#modo = 1 #1=escuta, 2=sussurro, 3=conferência.
#response = cliente.chamada.escuta_chamada(id_chamada, numero, modo)
#print(response)

##Deletar
#id = "1958"
#response = cliente.chamada.deletar(id)
#print(response)

### SMS

#numero_destino = "48999999999"
#mensagem = "teste envio sms"
#response = cliente.sms.enviar(numero_destino, mensagem)
#print(response)

##Get sms
#id = "1958"
#response = cliente.sms.get_by_id(id)
#print(response)

##Relatório de sms
#data_inicio = "2016-03-30T17:15:59-03:00"
#data_fim = "2016-03-30T17:15:59-03:00"
#response = cliente.sms.get_relatorio(data_inicio, data_fim)
#print(response)


### Audio

##Cria audio
#numero = "48999999999"
#url_audio = "http://fooo.bar"
#response = cliente.audio.enviar(numero, url_audio)
#print(response)

##Get audio
#id = "1958"
#response = cliente.audio.get_by_id(id)
#print(response)

##Relatório de audio
#data_inicio = "2016-03-30T17:15:59-03:00"
#data_fim = "2016-03-30T17:15:59-03:00"
#response = cliente.audio.get_relatorio(data_inicio, data_fim)
#print(response)

### TTS

#numero_destino = fone_restaurante
#mensagem = mensagem_pedido_atrasado
#response = cliente.tts.enviar(numero_destino, mensagem)
#print(response)

##Get TTS
#id = "1958"
#response = cliente.tts.get_by_id(id)
#print(response)

##Relatório de TTS
#data_inicio = "2016-03-30T17:15:59-03:00"
#data_fim = "2016-03-30T17:15:59-03:00"
#response = cliente.tts.get_relatorio(data_inicio, data_fim)
#print(response)

### Conferência

##Cria conferência
#response = cliente.conferencia.cria_conferencia()
#print(response)

##Get conferência
#id = "1958"
#response = cliente.conferencia.get_by_id(id)
#print(response)

##Add número na conferência
#id_conferencia = "15"
#numero = "48999999999"
#response = cliente.conferencia.add_numero_conferencia(id_conferencia, numero)
#print(response)

### DID

##Lista todos os dids disponíveis em estoque
#response = cliente.did.get_estoque()
#print(response)

##Compra did do estoque
#did_id = "1958"
#response = cliente.did.compra_estoque(did_id)
#print(response)

##Lista todos os dids que a conta possuí
#response = cliente.did.get_my_dids()
#print(response)

##Edita os dados do seu DID, podendo alterar o ramal id e a ura id
#did_id = "1"
#ramal_id = None
#ura_id = "10"
#response = cliente.did.editar(did_id, ura_id, ramal_id)
#print(response)

##Remove o did da conta
#did_id = "1"
#response = cliente.did.deletar(did_id)
#print(response)

##Lista os dados de uma chamada recebida
#chamada_id = "5599"
#response = cliente.did.get_chamada_recebida(chamada_id)
#print(response)

