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
    if command_list[0] == '/start' or command_list[0] == ''.join(['/start', self.handle]):
      return (True, 'mensagem', u'Este bot por enquanto só serve para criar qrcodes. Use o comando /qr\n\nExemplo de comando para gerar um qr code para o site do Matehackers: /qr https://matehackers.org\n\nPara enviar sugestões, elogios ou vilipêndios, digite /feedback seguido do texto a ser enviado para nós.\n\nO código fonte está no github em https://github.com/matehackers/tg-matebot', 'start')
    elif command_list[0] == '/qr' or command_list[0] == ''.join(['/qr', self.handle]):
      try:
        return (True, 'qrcode', self.qrencode.svg(' '.join(command_list[1::1])), ' '.join(command_list[1::1]))
      except Exception as e:
        return (False, 'erro', u'Não consegui gerar um qr code com %s' % (' '.join(command_list[1::1])), 'QR ERROR: %s' % (e))
    elif command_list[0] == '/feedback' or command_list[0] == ''.join(['/feedback', self.handle]):
      try:
        if len(command_list) > 1:
          return (True, 'feedback', u'Obrigado pelo feedback! Alguém em algum momento vai ler, eu acho.', ' '.join(command_list[1::1]))
        else:
          return (False, 'erro', 'Errrooou!', 'erro')
      except Exception as e:
        return (False, 'debug', 'DEBUG %s%sexception: %s' % (self, '\n', e), 'DEBUG')
    else:
      return (True, 'nada', 'Nada de interessante!', 'NADA')

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

