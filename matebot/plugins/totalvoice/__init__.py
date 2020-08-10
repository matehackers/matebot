# vim:fileencoding=utf-8
#  Plugin totalvoice para matebot: Usa a API do totalvoice
#  Copyleft (C) 2018-2019 Desobediente Civil, 2018-2019 Matehackers,
#    2018-2019 Velivery, 2019 Greatful
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

### Imports
import json
from totalvoice.cliente import Cliente
from plugins.log import log_str

def cmd_sms(args):
  tv_config = args['config']
  try:
    tv_token = str(tv_config.get("totalvoice", "token"))
    tv_host = str(tv_config.get("totalvoice", "host"))
    cliente = Cliente(tv_token, tv_host)
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'response': u'Erro tentando enviar SMS. os desenvolvedores serão notificados de qualquer forma, mas tente novamente mais tarde.',
      'debug': u'Erro enviando SMS.\nExceção: %s' % (e),
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  try:
    if len(args['command_list']) > 1:
      if args['command_list'][0].isdigit():
        numero = args['command_list'][0]
        mensagem = str(args['command_list'][1::1])
        cliente.sms.enviar(numero, mensagem)
        return {
          'status': True,
          'reply_to_message_id': args['message_id'],
          'type': args['command_type'],
          'multi': False,
          'response': u'SMS enviado para %s' % (numero),
          'debug': u'Sucesso enviando SMS.\nNúmero: %s\nMensagem: %s' % (numero, mensagem),
          'parse_mode': None,
        }
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'response': u'Erro tentando enviar SMS. os desenvolvedores serão notificados de qualquer forma, mas tente novamente mais tarde.',
      'debug': u'Erro enviando SMS.\nExceção: %s' % (e),
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  return {
    'status': False,
    'type': 'erro',
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /sms 5199999999 mensagem\nOnde 5199999999 é o número de telefone com código de longa distância e `mensagem` é a mensagem. Em caso de dúvida, pergunte pro %s' % (args['info_dict']['telegram_admin']),
    'debug': u'Erro enviando SMS.\nNúmero: %s\nMensagem: %s' % (numero, mensagem),
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

def cmd_tts(args):
  tv_config = args['config']
  try:
    tv_token = str(tv_config.get("totalvoice", "token"))
    tv_host = str(tv_config.get("totalvoice", "host"))
    cliente = Cliente(tv_token, tv_host)
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'response': u'Erro tentando enviar SMS. os desenvolvedores serão notificados de qualquer forma, mas tente novamente mais tarde.',
      'debug': u'Erro enviando SMS.\nExceção: %s' % (e),
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  try:
    if len(args['command_list']) > 1:
      if args['command_list'][0].isdigit():
        numero = args['command_list'][0]
        mensagem = ' '.join(args['command_list'][1::1])
        cliente.tts.enviar(numero, mensagem)
        return {
          'status': True,
          'response': u'Mensagem de voz enviada para %s' % (args['command_list'][0]),
          'debug': u'Sucesso enviando TTS.\nNúmero: %s\nMensagem: %s' % (numero, mensagem),
          'multi': False,
          'parse_mode': None,
          'reply_to_message_id': args['message_id'],
          'type': args['command_type'],
        }
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'response': u'Erro tentando enviar TTS. os desenvolvedores serão notificados de qualquer forma, mas tente novamente mais tarde.',
      'debug': u'Erro enviando TTS.\nExceção: %s' % (e),
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  return {
    'status': False,
    'type': 'erro',
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /tts 5199999999 mensagem\nOnde 5199999999 é o número de telefone com código de longa distância e `mensagem` é a mensagem. Em caso de dúvida, pergunte pro %s' % (args['info_dict']['telegram_admin']),
    'debug': u'Erro enviando TTS.\nNúmero: %s\nMensagem: %s' % (numero, mensagem),
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## TODO ainda em fase experimental, favor manter as mensagens de depuração
def shiva(args):
  try:
    cliente = Cliente(str(args['config']['totalvoice']['token']), str(args['config']['totalvoice']['host']))
    numero = str(args['numero'])
    print(numero)
    url_audio = str(args['url_audio'])
    print(url_audio)
    response = cliente.audio.enviar(numero, url_audio)
    print(response)
#    print(mensagem)
#    print(type(mensagem))
#    print(mensagem.decode())
#    print(type(mensagem.decode()))
#    print(mensagem.decode("UTF-8"))
#    print(type(mensagem.decode("UTF-8")))
##    print(json.dumps(mensagem))
#    print(type(json.dumps(mensagem.decode())))
#    print(type(json.dumps(mensagem.decode("UTF-8"))))
##    print(json.loads(json.dumps(mensagem)))
#    print(type(json.loads(json.dumps(mensagem.decode()))))
#    print(type(json.loads(json.dumps(mensagem.decode("UTF-8")))))
##    print(type(dict(json.loads(json.dumps(mensagem.decode())))))
##    print(type(dict(json.loads(json.dumps(mensagem.decode("UTF-8"))))))
##    print(type(dict(json.dumps(mensagem.decode()))))
##    print(type(dict(json.dumps(mensagem.decode("UTF-8")))))
#    args['bot'].sendMessage(json.loads(args['config']['plugins_grupos']['velivery_admin'])[0], u'Eu enviaria áudio para o número %s, mas o %s disse que eu estou em estágio probatório por enquanto...' % (' '.join(args['telefones']), str(args['config']['info']['telegram_admin'])))
    args['bot'].sendMessage(json.loads(args['config']['plugins_grupos']['velivery_admin'])[0], u'Enviando áudio %s para o número %s...' % (url_audio, numero))
    return {
      'status': True,
      'type': 'grupo',
      'multi': False,
      'response': str(response.decode()),
      'debug': str(response.decode()),
      'parse_mode': None,
    }
  except Exception as e:
    raise
    print(log_str.debug(e))
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando enviar Audio. os desenvolvedores serão notificados de qualquer forma, mas tente novamente mais tarde.',
      'debug': u'Erro enviando Audio.\nExceção: %s' % (e),
      'parse_mode': None,
    }
  return {
    'status': False,
    'type': 'erro',
    'multi': False,
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /shiva 5199999999\nOnde 5199999999 é o número de telefone com código de longa distância. Em caso de dúvida, pergunte pro %s' % (str(args['config']['info']['telegram_admin'])),
    'debug': u'Erro enviando Audio.\nNúmero: %s\nMensagem: %s' % (str(args['numero'])),
    'parse_mode': None,
  }

def shiva_1(args):
  args.update(url_audio = str(args['config']['totalvoice']['url_1']))
  return shiva(args)

def shiva_2(args):
  args.update(url_audio = str(args['config']['totalvoice']['url_2']))
  return shiva(args)

def shiva_3(args):
  args.update(url_audio = str(args['config']['totalvoice']['url_3']))
  return shiva(args)

def shiva_4(args):
  args.update(url_audio = str(args['config']['totalvoice']['url_4']))
  return shiva(args)

### Chamadas

#Cria chamada
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

