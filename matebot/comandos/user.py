# vim:fileencoding=utf-8

from plugins import totalvoice

def default(info_dict, bot_dict, addr_dict, command_list):
  raise AttributeError

def sms(info_dict, bot_dict, addr_dict, command_list):
  try:
    if len(command_list) > 1:
      if command_list[0].isdigit():
        numero = command_list[0]
        mensagem = ' '.join(command_list[1::1])
        totalvoice.sms_criar(numero, mensagem)
        return {
          'status': True,
          'type': 'mensagem',
          'multi': False,
          'response': u'SMS enviado para %s' % (command_list[0]),
          'debug': u'Sucesso enviando SMS.\nNúmero: %s\nMensagem: %s' % (command_list[0], ' '.join(command_list[1::1])),
        }
  except:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando enviar SMS. os desenvolvedores serão notificados de qualquer forma, mas tente novamente mais tarde.' % (info_dict['telegram_admin']),
      'debug': u'Erro enviando SMS.\nNúmero: %s\nMensagem: %s' % (command_list[0], ' '.join(command_list[1::1])),
    }
  return {
    'status': False,
    'type': 'erro',
    'multi': False,
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /sms 5199999999 mensagem\nOnde 5199999999 é o número de telefone e `mensagem` é a mensagem. Em caso de dúvida, pergunte pro %s' % (info_dict['telegram_admin']),
    'debug': u'Erro enviando SMS.\nNúmero: %s\nMensagem: %s' % (command_list[0], ' '.join(command_list[1::1])),
  }

def tts(info_dict, bot_dict, addr_dict, command_list):
  try:
    if len(command_list) > 1:
      if command_list[0].isdigit():
        numero = command_list[0]
        mensagem = ' '.join(command_list[1::1])
        totalvoice.tts_criar(numero, mensagem)
        return {
          'status': True,
          'type': 'mensagem',
          'multi': False,
          'response': u'Mensagem de voz enviada para %s' % (command_list[0]),
          'debug': u'Sucesso enviando TTS.\nNúmero: %s\nMensagem: %s' % (command_list[0], ' '.join(command_list[1::1])),
        }
  except:
    return {
      'status': False,
      'type': 'erro',
      'multi': False,
      'response': u'Erro tentando enviar TTS. os desenvolvedores serão notificados de qualquer forma, mas tente novamente mais tarde.' % (info_dict['telegram_admin']),
      'debug': u'Erro enviando TTS.\nNúmero: %s\nMensagem: %s' % (command_list[0], ' '.join(command_list[1::1])),
    }
  return {
    'status': False,
    'type': 'erro',
    'multi': False,
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /tts 5199999999 mensagem\nOnde 5199999999 é o número de telefone e `mensagem` é a mensagem. Em caso de dúvida, pergunte pro %s' % (info_dict['telegram_admin']),
    'debug': u'Erro enviando TTS.\nNúmero: %s\nMensagem: %s' % (command_list[0], ' '.join(command_list[1::1])),
  }

