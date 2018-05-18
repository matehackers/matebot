# vim:fileencoding=utf-8

from plugins.qrencode import qrencode
from plugins.hashes import hashes
from plugins.velivery_pedidos import velivery_pedidos
import configparser, json

class command():
  def __init__(self, adminId_groupId, botName_botHandle, botInfo, botCryptoAddresses):
    config_file = str("config/.matebot.cfg")
    self.grupo_velivery_pedidos = -1
    try:
      config = configparser.ConfigParser()
      config.read(config_file)
      self.grupo_velivery_pedidos = int(config.get("velivery", "grupo_pedidos"))
      self.ids_velivery_pedidos = json.loads(config.get("velivery", "ids_pedidos"))
      self.bot_admin = str(config.get("info", "telegram_admin"))
    except Exception as e:
      ## TODO tratar exceções
      if ( e == configparser.NoSectionError ):
        print('DEBUG configparser error: %s' % (e))
      else:
        print('DEBUG configparser error: %s' % (e))
    self.adminId = adminId_groupId[0]
    self.groupId = adminId_groupId[1]
    self.name = botName_botHandle[0]
    self.handle = botName_botHandle[1]
    self.qrencode = qrencode.qrencode()
    self.velivery_pedidos = velivery_pedidos.velivery_pedidos()
    self.hashes = hashes.hashes()
    self.info = dict(botInfo)
    self.crypto_addresses = dict(botCryptoAddresses)
    self.db_default_limit = 10

  def anyone(self, chat_id, from_id, command_list):
    if command_list[0] == '/start' or command_list[0] == ''.join(['/start', self.handle]):
      response = u'%s' % (str(self.info.get('website')))
      return {
        'status': True,
        'type': 'mensagem',
        'multi': False,
        'response': response,
        'debug': 'start',
      }
    elif command_list[0] == '/help' or command_list[0] == ''.join(['/help', self.handle]):
      response = u'%s' % (str(self.info.get('website')))
      return {
        'status': True,
        'type': 'mensagem',
        'multi': False,
        'response': response,
        'debug': 'help',
      }
    elif command_list[0] == '/doar' or command_list[0] == ''.join(['/doar', self.handle]):
      response = u'Página no site do Matehackers com todas as opções atualizadas para ajudar a manter o hackerspace: https://matehackers.org/renda\n\nLinks para doar em bitcoins (use o que funcionar no teu dispositivo):\nbitcoin:%s\nhttps://blockchain.info/payment_request?address=%s&message=https://matehackers.org/renda\nhttps://blockchainbdgpzk.onion/payment_request?address=%s&message=https://matehackers.org/renda\n\nOutros métodos de doação:\nhttps://apoia.se/matehackers\n' % (self.crypto_addresses['btc'], self.crypto_addresses['btc'], self.crypto_addresses['btc'])
      return {
        'status': True,
        'type': 'mensagem',
        'multi': False,
        'response': response,
        'debug': 'doar',
      }
    elif command_list[0] == '/qr' or command_list[0] == ''.join(['/qr', self.handle]):
      try:
        response = self.qrencode.svg(' '.join(command_list[1::1]))
        return {
          'status': True,
          'type': 'qrcode',
          'multi': False,
          'response': response,
          'debug': 'QR code sucess\nCommand: %s\nResponse: %s' % (self, command_list),
        }
      except Exception as e:
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
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
            'multi': False,
            'response': response,
            'feedback': ' '.join(command_list[1:]),
            'debug': 'Feedback success\n%s\nCommand: %s\nResponse: %s' % (self, command_list, response),
          }
        else:
          response = u'Erro tentando enviar feedback. Você deve seguir este modelo:\n\n/feedback Digite a mensagem aqui'
          return {
            'status': False,
            'type': 'erro',
            'multi': False,
            'response': response,
            'debug': 'Feedback failed\n%s\nCommand: %s\nResponse: %s' % (self, command_list, response),
          }
      except Exception as e:
          response = u'Erro tentando enviar feedback. Os desenvolvedores vão ser notificados de qualquer forma. Mas tente novamente, por favor.'
          return {
            'status': False,
            'type': 'erro',
            'multi': False,
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
            'multi': False,
            'response': response,
            'debug': 'hash success\nCommand: %s\nResponse: %s' % (command_list, response),
          }
        except Exception as e:
          response = u'Erro tentando calcular o hash %s de %s.\n\nOs desenvolvedores vão ser notificados de qualquer forma. Mas tente novamente, por favor.\n\nAlgoritmos suportados: %s' % (command_list[1], ' '.join(command_list[2:]), self.hashes.get_hashes())
          return {
            'status': False,
            'type': 'erro',
            'multi': False,
            'response': response,
            'debug': 'hash failed\n%s, Command: %s\nResponse: %s\nException: %s' % (self, command_list, response, e),
          }
      else:
        response = u'Vossa excelência está tentando usar o bot de uma maneira incorreta, errada, equivocada. Vamos tentar novamente?\n\nA sintaxe deve ser exatamente assim:\n\n/hash (algoritmo) (mensagem)\n\nExemplo: /hash md5 Agora sim eu aprendi a usar o comando\n\nOutro exemplo: /hash sha256 MinhaSenhaSecreta1234\n\nAlgoritmos disponíveis: %s' % (self.hashes.get_hashes())
        return {
          'status': False,
          'type': 'erro',
          'multi': False,
          'response': response,
          'debug': 'hash failed\nCommand: %s\nResponse: %s' % (command_list, response),
        }
    elif command_list[0] in ['/pedidos', ''.join(['/pedidos', self.handle]), '/pendentes', ''.join(['/pendentes', self.handle]), '/atrasados', ''.join(['/atrasados', self.handle])]:
      response = u'Vossa excelência não terdes autorização para realizar esta ação.'
      return {
        'status': False, 
        'type': 'grupo', 
        'multi': False,
        'response': response, 
        'debug': u'Não autorizado %s\nchat_id: %s\nfrom_id:%s\nCommand: %s\nResponse: %s' % (self, chat_id, from_id, command_list, response),
      }
    else:
      return {
        'status': True, 
        'type': 'grupo', 
        'multi': False,
        'response': u'Não entendi ou não estou programada para responder este comando. Te vira!', 
        'debug': 'Nothing happened\nCommand: %s\nResponse: %s' % (self, command_list),
      }

  def user_parse(self, chat_id, from_id, command_list):
    return self.anyone(chat_id, from_id, command_list)

  def group_parse(self, chat_id, from_id, command_list):
    return self.anyone(chat_id, from_id, command_list)

  def admin_user_parse(self, chat_id, from_id, command_list):
    if command_list[0] == '/pedidos' or command_list[0] == ''.join(['/pedidos', self.handle]):
      limite = self.db_default_limit
      try:
        if command_list[1].isdigit():
          limite = command_list[1]
      except IndexError:
        pass
      response = self.velivery_pedidos.todos(int(limite))
      return {
        'status': response['status'],
        'type': response['type'],
        'multi': response['multi'],
        'response': response['response'],
        'debug': response['debug'],
      }
    elif command_list[0] == '/pendentes' or command_list[0] == ''.join(['/pendentes', self.handle]):
      response = self.velivery_pedidos.pendentes(5)
      return {
        'status': response['status'],
        'type': 'mensagem',
        'multi': response['multi'],
        'response': response['response'],
        'debug': response['debug'],
      }
    elif command_list[0] == '/atrasados' or command_list[0] == ''.join(['/atrasados', self.handle]):
      response = self.velivery_pedidos.atrasados(5)
      return {
        'status': response['status'],
        'type': 'mensagem',
        'multi': response['multi'],
        'response': response['response'],
        'debug': response['debug'],
      }
    elif command_list[0] == '/pedido' or command_list[0] == ''.join(['/pedido', self.handle]):
      try:
        if command_list[1].isdigit():
          pedido = command_list[1]
          response = self.velivery_pedidos.pedido(pedido, self.db_default_limit)
          return {
            'status': response['status'],
            'type': response['type'],
            'multi': response['multi'],
            'response': response['response'],
            'debug': response['debug'],
          }
      except:
        pass
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /pedido 1\nOnde 1 é o código do pedido. Em caso de dúvida, pergunte pro %s' % (self.bot_admin),
        'debug': u'Erro tentando buscar %s\n:command_list: %s' % (command_list[0], command_list),
      }
    elif command_list[0] == '/teste' or command_list[0] == ''.join(['/teste', self.handle]):
      response = """
Teste
Mais um teste
$$$EOF$$$
Próxima mensagem
Afu
      """
      return {
        'status': True,
        'type': 'mensagem',
        'multi': True,
        'response': response,
        'debug': 'Nothing happened\nCommand: %s\nResponse: %s' % (self, command_list),
      }
    else:
      return self.user_parse(chat_id, from_id, command_list)

  def admin_group_parse(self, chat_id, from_id, command_list):
    return self.group_parse(chat_id, from_id, command_list)

  def group_velivery_pedidos_parse(self, chat_id, from_id, command_list):
    if command_list[0] == '/pendentes' or command_list[0] == ''.join(['/pendentes', self.handle]):
      response = self.velivery_pedidos.pendentes(5)
      return {
        'status': response['status'],
        'type': 'grupo',
        'multi': response['multi'],
        'response': response['response'],
        'debug': response['debug'],
      }
    elif command_list[0] == '/atrasados' or command_list[0] == ''.join(['/atrasados', self.handle]):
      response = self.velivery_pedidos.atrasados(5)
      return {
        'status': response['status'],
        'type': 'grupo',
        'multi': response['multi'],
        'response': response['response'],
        'debug': response['debug'],
      }
    elif command_list[0] == '/pedido' or command_list[0] == ''.join(['/pedido', self.handle]):
      try:
        if command_list[1].isdigit():
          pedido = command_list[1]
          response = self.velivery_pedidos.pedido(pedido, self.db_default_limit)
          return {
            'status': response['status'],
            'type': 'grupo',
            'multi': response['multi'],
            'response': response['response'],
            'debug': response['debug'],
          }
      except:
        pass
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /pedido 1\nOnde 1 é o código do pedido. Em caso de dúvida, pergunte pro %s' % (self.bot_admin),
        'debug': u'Erro tentando buscar %s\n:command_list: %s' % (command_list[0], command_list),
      }
    else:
      return self.group_parse(chat_id, from_id, command_list)

  def user_velivery_pedidos_parse(self, chat_id, from_id, command_list):
    if command_list[0] == '/pendentes' or command_list[0] == ''.join(['/pendentes', self.handle]):
      response = self.velivery_pedidos.pendentes(5)
      return {
        'status': response['status'],
        'type': 'mensagem',
        'multi': response['multi'],
        'response': response['response'],
        'debug': response['debug'],
      }
    elif command_list[0] == '/atrasados' or command_list[0] == ''.join(['/atrasados', self.handle]):
      response = self.velivery_pedidos.atrasados(5)
      return {
        'status': response['status'],
        'type': 'mensagem',
        'multi': response['multi'],
        'response': response['response'],
        'debug': response['debug'],
      }
    elif command_list[0] == '/pedido' or command_list[0] == ''.join(['/pedido', self.handle]):
      try:
        if command_list[1].isdigit():
          pedido = command_list[1]
          response = self.velivery_pedidos.pedido(pedido, self.db_default_limit)
          return {
            'status': response['status'],
            'type': 'mensagem',
            'multi': response['multi'],
            'response': response['response'],
            'debug': response['debug'],
          }
      except:
        pass
      return {
        'status': False,
        'type': 'erro',
        'multi': False,
        'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /pedido 1\nOnde 1 é o código do pedido. Em caso de dúvida, pergunte pro %s' % (self.bot_admin),
        'debug': u'Erro tentando buscar %s\n:command_list: %s' % (command_list[0], command_list),
      }
    else:
      return self.user_parse(chat_id, from_id, command_list)

  def parse(self, chat_id, from_id, command_list):
    ## If chat_id is negative, then we're talking with a group.
    if (chat_id < 0):
      ## Admin group
      if str(chat_id) == str(self.groupId):
        return self.admin_group_parse(chat_id, from_id, command_list)
      ## Velivery Pedidos
      elif str(chat_id) == str(self.grupo_velivery_pedidos):
        return self.group_velivery_pedidos_parse(chat_id, from_id, command_list)
      ## Regular group
      else:
        return self.group_parse(chat_id, from_id, command_list)
    ## Admin user
    elif str(chat_id) == str(self.adminId):
      return self.admin_user_parse(chat_id, from_id, command_list)
    ## Velivery Pedidos
    elif chat_id in self.ids_velivery_pedidos:
      return self.user_velivery_pedidos_parse(chat_id, from_id, command_list)
    ## Regular user
    else:
      return self.user_parse(chat_id, from_id, command_list)

