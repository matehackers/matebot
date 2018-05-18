# vim:fileencoding=utf-8

### Imports
import configparser
from totalvoice.cliente import Cliente

### Variáveis
tv_config_file = str(".matebot.cfg")
tv_config = configparser.ConfigParser()

try:
    tv_config.read(tv_config_file)
    tv_token = str(tv_config.get("totalvoice", "token"))
    tv_host = str(tv_config.get("totalvoice", "host"))
    fone_velivery = str(tv_config.get("agenda", "velivery"))
    fone_iuri = str(tv_config.get("agenda", "iuri"))
    fone_benhur = str(tv_config.get("agenda", "benhur"))
    fone_guilherme = str(tv_config.get("agenda", "guilherme"))
except Exception as e:
    ## TODO tratar exceções
    if ( e == configparser.NoSectionError ):
        print(e)
    else:
        print(e)

fone_restaurante = fone_iuri
cliente = Cliente(tv_token, tv_host)

mensagem_pedido_atrasado = "Oi, aqui é a Shiva, tudo bem? Tem um pedido atrasado no aplicativo Velívery, aquele vegetariano! Obrigada!"
#fone_restaurante = fone_benhur

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

##Cria TTS
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

