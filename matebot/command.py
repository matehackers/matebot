# vim:fileencoding=utf-8

from plugins.qrencode import qrencode
from plugins.hashes import hashes

class command():
  def __init__(self, adminId_groupId, botName_botHandle):
    self.adminId = adminId_groupId[0]
    self.groupId = adminId_groupId[1]
    self.name = botName_botHandle[0]
    self.handle = botName_botHandle[1]
    self.qrencode = qrencode.qrencode()
    self.hashes = hashes.hashes()

  def anyone(self, chat_id, from_id, command_list):
    if command_list[0] == '/start' or command_list[0] == ''.join(['/start', self.handle]):
      response = u'Este bot por enquanto só serve para criar qrcodes e calcular hashes. Use o comando /qr\nExemplo de comando para gerar um qr code para o site do Matehackers: /qr https://matehackers.org\n\nPara gerar um hash de qualquer texto, use o comando /hash\nExemplo: /hash md5 matehackers\n\nAlgortimos disponíveis: %s\n\nPara enviar sugestões, elogios ou vilipêndios, digite /feedback seguido do texto a ser enviado para nós.\n\nO código fonte está no github em https://github.com/matehackers/tg-matebot' % (self.hashes.get_hashes())
      return {
        'status': True,
        'type': 'mensagem',
        'response': response,
        'debug': 'start',
      }
    elif command_list[0] == '/help' or command_list[0] == ''.join(['/help', self.handle]):
      response = u'Este bot por enquanto só serve para criar qrcodes e calcular hashes. Use o comando /qr\nExemplo de comando para gerar um qr code para o site do Matehackers: /qr https://matehackers.org\n\nPara gerar um hash de qualquer texto, use o comando /hash\nExemplo: /hash md5 matehackers\n\nAlgortimos disponíveis: %s\n\nPara enviar sugestões, elogios ou vilipêndios, digite /feedback seguido do texto a ser enviado para nós.\n\nO código fonte está no github em https://github.com/matehackers/tg-matebot' % (self.hashes.get_hashes())
      return {
        'status': True,
        'type': 'mensagem',
        'response': response,
        'debug': 'help',
      }
    elif command_list[0] == '/qr' or command_list[0] == ''.join(['/qr', self.handle]):
      try:
        response = self.qrencode.svg(' '.join(command_list[1::1]))
        return {
          'status': True,
          'type': 'qrcode',
          'response': response,
          'debug': 'QR code sucess\nCommand: %s\nResponse: %s' % (self, command_list),
        }
      except Exception as e:
        return {
          'status': False,
          'type': 'erro',
          'response':  u'Não consegui gerar um qr code com %s\nOs desenvolvedores devem ter sido avisados já, eu acho.' % (' '.join(command_list[1::1])),
          'debug': 'QR code error\nCommand: %s\nResponse: %s\nException: %s' % (self, command_list[1::1], e),
        }
    elif command_list[0] == '/feedback' or command_list[0] == ''.join(['/feedback', self.handle]):
      try:
        if len(command_list) > 1:
          response = u'Obrigado pelo feedback! Alguém em algum momento vai ler, eu acho.'
          return {
            'status': True,
            'type': 'feedback',
            'response': response,
            'feedback': ' '.join(command_list[1:]),
            'debug': 'Feedback success\n%s\nCommand: %s\nResponse: %s' % (self, command_list, response),
          }
        else:
          response = u'Erro tentando enviar feedback. Você deve seguir este modelo:\n\n/feedback Digite a mensagem aqui'
          return {
            'status': False,
            'type': 'erro',
            'response': response,
            'debug': 'Feedback failed\n%s\nCommand: %s\nResponse: %s' % (self, command_list, response),
          }
      except Exception as e:
          response = u'Erro tentando enviar feedback. Os desenvolvedores vão ser notificados de qualquer forma. Mas tente novamente, por favor.'
          return {
            'status': False,
            'type': 'erro',
            'response': response,
            'debug': 'Feedback failed\n%s\nCommand: %s\nResponse: %s\nException: %s' % (self, command_list, response, e),
          }
    elif command_list[0] == '/hash' or command_list[0] == ''.join(['/hash', self.handle]):
      if len(command_list) > 2:
        try:
          response = self.hashes.return_hash(command_list[1], ' '.join(command_list[2:]))
          return {
            'status': True,
            'type': 'grupo',
            'response': response,
            'debug': 'hash success\nCommand: %s\nResponse: %s' % (command_list, response),
          }
        except Exception as e:
          response = u'Erro tentando calcular o hash %s de %s.\n\nOs desenvolvedores vão ser notificados de qualquer forma. Mas tente novamente, por favor.\n\nAlgoritmos suportados: %s' % (command_list[1], ' '.join(command_list[2:]), self.hashes.get_hashes())
          return {
            'status': False,
            'type': 'erro',
            'response': response,
            'debug': 'hash failed\n%s, Command: %s\nResponse: %s\nException: %s' % (self, command_list, response, e),
          }
      else:
        response = u'Vossa excelência está tentando usar o bot de uma maneira incorreta, errada, equivocada. Vamos tentar novamente?\n\nA sintaxe deve ser exatamente assim:\n\n/hash (algoritmo) (mensagem)\n\nExemplo: /hash md5 Agora sim eu aprendi a usar o comando\n\nOutro exemplo: /hash sha256 MinhaSenhaSecreta1234\n\nAlgoritmos disponíveis: %s' % (self.hashes.get_hashes())
        return {
          'status': False,
          'type': 'erro',
          'response': response,
          'debug': 'hash failed\nCommand: %s\nResponse: %s' % (command_list, response),
        }
    else:
      return {
        'status': True, 
        'type': 'nada', 
        'response': u'Reservado para implementação futura', 
        'debug': 'Nothing happened\nCommand: %s\nResponse: %s' % (self, command_list),
      }

  def user_parse(self, chat_id, from_id, command_list):
    return self.anyone(chat_id, from_id, command_list)

  def group_parse(self, chat_id, from_id, command_list):
    return self.anyone(chat_id, from_id, command_list)

  def admin_user_parse(self, chat_id, from_id, command_list):
    return self.anyone(chat_id, from_id, command_list)

  def admin_group_parse(self, chat_id, from_id, command_list):
    return self.anyone(chat_id, from_id, command_list)

  def parse(self, chat_id, from_id, command_list):
    ## If chat_id is negative, then we're talking with a group.
    if chat_id < 0:
      ## Admin group
      if chat_id == self.groupId:
        return self.admin_group_parse(chat_id, from_id, command_list)
      ## Regular group
      else:
        return self.group_parse(chat_id, from_id, command_list)
    ## Admin user
    elif chat_id == self.adminId:
      return self.admin_user_parse(chat_id, from_id, command_list)
    ## Regular user
    else:
      return self.user_parse(chat_id, from_id, command_list)

