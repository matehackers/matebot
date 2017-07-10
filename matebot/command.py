# vim:fileencoding=utf-8

from plugins.qrencode import qrencode

class command():
  def __init__(self, (admin_id, group_id), (bot_name, bot_handle)):
    self.admin_id = admin_id
    self.group_id = group_id
    self.name = bot_name
    self.handle = bot_handle
    self.qrencode = qrencode.qrencode()

  def anyone(self, chat_id, from_id, command_list):
    if command_list[0] == '/start' or command_list[0] == ''.join(['/start', self.handle]) or command_list[0] == '/help' or command_list[0] == ''.join(['/help', self.handle]):
      response = u'Este bot por enquanto só serve para criar qrcodes. Use o comando /qr\n\nExemplo de comando para gerar um qr code para o site do Matehackers: /qr https://matehackers.org\n\nPara enviar sugestões, elogios ou vilipêndios, digite /feedback seguido do texto a ser enviado para nós.\n\nO código fonte está no github em https://github.com/matehackers/tg-matebot'
      return {
        'status': True,
        'type': 'mensagem',
        'response': response,
        'debug': 'start',
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
          return {
            'status': True,
            'type': 'feedback',
            'response':  u'Obrigado pelo feedback! Alguém em algum momento vai ler, eu acho.',
            'debug': 'Feedback sucess\nCommand: %s\nResponse: %s' % (self, command_list),
          }
        else:
          return {
            'status': False,
            'type': 'erro',
            'response': u'Erro tentando enviar feedback. Você deve seguir este modelo:\n\n/feedback Digite a mensagem aqui',
            'debug': 'Feedback failed\nCommand: %s\nResponse: %s' % (self, command_list),
          }
      except Exception as e:
          return {
            'status': False,
            'type': 'erro',
            'response': u'Erro tentando enviar feedback. Os desenvolvedores vão ser notificados de qualquer forma. Mas tente novamente, por favor.',
            'debug': 'Feedback failed\nCommand: %s\nResponse: %s\nException: %s' % (self, command_list, e),
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
      if chat_id == self.group_id:
        return self.admin_group_parse(chat_id, from_id, command_list)
      ## Regular group
      else:
        return self.group_parse(chat_id, from_id, command_list)
    ## Admin user
    elif chat_id == self.admin_id:
      return self.admin_user_parse(chat_id, from_id, command_list)
    ## Regular user
    else:
      return self.user_parse(chat_id, from_id, command_list)

