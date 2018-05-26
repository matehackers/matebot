# vim:fileencoding=utf-8

from plugins import qrencode, hashes

def start(info_dict, bot_dict, addr_dict, command_list):
  response = u'Este bot por enquanto só serve para criar qrcodes e calcular hashes. Use o comando /qr\nExemplo de comando para gerar um qr code para o site do Matehackers: /qr %s\n\nPara gerar um hash de qualquer texto, use o comando /hash\nExemplo: /hash md5 matehackers\n\nAlgoritmos disponíveis: %s\n\nPara enviar sugestões, elogios ou vilipêndios, digite /feedback seguido do texto a ser enviado para nós.\n\nPara ajudar o hackerspace a se manter, use o comando /doar\n\nO código fonte deste bot está em %s\n\nMatehackers no telegram: %s' % (info_dict['website'], hashes.get_hashes(), info_dict['code_repository'], info_dict['telegram_group'])
  return {
    'status': True,
    'type': 'mensagem',
    'response': response,
    'debug': 'start',
  }

def help(info_dict, bot_dict, addr_dict, command_list):
  response = u'Este bot por enquanto só serve para criar qrcodes e calcular hashes. Use o comando /qr\nExemplo de comando para gerar um qr code para o site do Matehackers: /qr %s\n\nPara gerar um hash de qualquer texto, use o comando /hash\nExemplo: /hash md5 matehackers\n\nAlgoritmos disponíveis: %s\n\nPara enviar sugestões, elogios ou vilipêndios, digite /feedback seguido do texto a ser enviado para nós.\n\nPara ajudar o hackerspace a se manter, use o comando /doar\n\nO código fonte deste bot está em %s\n\nMatehackers no telegram: %s' % (info_dict['website'], hashes.get_hashes(), info_dict['code_repository'], info_dict['telegram_group'])
  return {
    'status': True,
    'type': 'mensagem',
    'response': response,
    'debug': 'help',
  }

def doar(info_dict, bot_dict, addr_dict, command_list):
  response = u'Página no site do Matehackers com todas as opções atualizadas para ajudar a manter o hackerspace: https://matehackers.org/renda\n\nLinks para doar em bitcoins (use o que funcionar no teu dispositivo):\nbitcoin:%s\nhttps://blockchain.info/payment_request?address=%s&message=https://matehackers.org/renda\nhttps://blockchainbdgpzk.onion/payment_request?address=%s&message=https://matehackers.org/renda\n\nOutros métodos de doação:\nhttps://apoia.se/matehackers\n' % (addr_dict['btc'], addr_dict['btc'], addr_dict['btc'])
  return {
    'status': True,
    'type': 'mensagem',
    'response': response,
    'debug': 'doar',
  }

def qr(info_dict, bot_dict, addr_dict, command_list):
  try:
    response = qrencode.svg(' '.join(command_list))
    return {
      'status': True,
      'type': 'qrcode',
      'response': response,
      'debug': 'QR code sucess\nResponse: %s' % (command_list),
    }
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'response':  u'Não consegui gerar um qr code com %s\nOs desenvolvedores devem ter sido avisados já, eu acho.' % (' '.join(command_list)),
      'debug': 'QR code error\nResponse: %s\nException: %s' % (command_list, e),
    }

def feedback(info_dict, bot_dict, addr_dict, command_list):
  try:
    if len(command_list) > 0:
      response = u'Obrigado pelo feedback! Alguém em algum momento vai ler, eu acho.'
      return {
        'status': True,
        'type': 'feedback',
        'response': response,
        'feedback': ' '.join(command_list),
        'debug': 'Feedback success\n%s\nResponse: %s' % (command_list, response),
      }
    else:
      response = u'Erro tentando enviar feedback. Você deve seguir este modelo:\n\n/feedback Digite a mensagem aqui'
      return {
        'status': False,
        'type': 'erro',
        'response': response,
        'debug': 'Feedback failed\n%s\nResponse: %s' % (command_list, response),
      }
  except Exception as e:
      response = u'Erro tentando enviar feedback. Os desenvolvedores vão ser notificados de qualquer forma. Mas tente novamente, por favor.'
      return {
        'status': False,
        'type': 'erro',
        'response': response,
        'debug': 'Feedback failed\n%s\nResponse: %s\nException: %s' % (command_list, response, e),
      }

def hash(info_dict, bot_dict, addr_dict, command_list):
  if len(command_list) > 1:
    try:
      response = hashes.return_hash(command_list[0], ' '.join(command_list[1:]))
      return {
        'status': True,
        'type': 'grupo',
        'response': response,
        'debug': 'hash success\nCommand: %s\nResponse: %s' % (command_list, response),
      }
    except Exception as e:
      response = u'Erro tentando calcular o hash %s de %s.\n\nOs desenvolvedores vão ser notificados de qualquer forma. Mas tente novamente, por favor.\n\nAlgoritmos suportados: %s' % (command_list[1], ' '.join(command_list[1:]), hashes.get_hashes())
      return {
        'status': False,
        'type': 'erro',
        'response': response,
        'debug': 'hash failed\n%s, Response: %s\nException: %s' % (command_list, response, e),
      }
  else:
    response = u'Vossa excelência está tentando usar o bot de uma maneira incorreta, errada, equivocada. Vamos tentar novamente?\n\nA sintaxe deve ser exatamente assim:\n\n/hash (algoritmo) (mensagem)\n\nExemplo: /hash md5 Agora sim eu aprendi a usar o comando\n\nOutro exemplo: /hash sha256 MinhaSenhaSecreta1234\n\nAlgoritmos disponíveis: %s' % (hashes.get_hashes())
    return {
      'status': False,
      'type': 'erro',
      'response': response,
      'debug': 'hash failed\nCommand: %s\nResponse: %s' % (command_list, response),
    }

