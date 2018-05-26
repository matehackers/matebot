# vim:fileencoding=utf-8

## Telegram bots documentation at https://core.telegram.org/bots
## Telepot documentation at https://telepot.readthedocs.io/en/latest/

import os
import re
import time

try:
  import configparser
except ImportError:
  import ConfigParser

try:
  import asyncio
  import telepot.aio
except ImportError:
  try:
    import telepot
  except ImportError as e:
    print('You have to install telepot. Try again when you do.\nYou can do `pip install --user -r requirements.txt`.\nIf you are running python3, then try `python3 -m pip install --user -r requirements`.\nRemove --user option if running as root.')
    print(e)
    exit()

from matebot import comandos
from plugins.log import log_str

class bot():

  def __init__(self):
    self.log_str = log_str()

    self.config_file = str("config/.matebot.cfg")
    try:
      self.config = configparser.ConfigParser()
    except NameError:
      self.config = ConfigParser.ConfigParser()
    try:
      self.config.read(self.config_file)
      ## TODO: Esta exceção deveria ser tratada na primeira vez que a gente
      ## tentar acessar uma seção do arquivo
    except configparser.NoSectionError:
      print(self.log_str.info('Exiting %s' % (self.config['bot']['name'])))
      return

    print(self.log_str.info('Starting %s' % (self.config['bot']['name'])))
    print(self.log_str.info("Our telegram token is '%s', the admin id is '%s' and the admin group id is '%s'" % (self.config['botfather']['token'], self.config['admin']['id'], self.config['admin']['group'])))

#    self.command = command.command((self.config['admin']['id'], self.config['admin']['group']), (self.config['bot']['name'], self.config['bot']['handle']), dict(self.config.items('info')), dict(self.config.items('crypto_addresses')))

    try:
      self.bot = telepot.Bot(self.config['botfather']['token'])
      self.bot.message_loop(self.rcv)
    except Exception as e:
      self.log(self.log_str.err('DEBUG telegram error: %s' % (e)))
      pass
    self.log(self.log_str.info('Started %s' % (self.config['bot']['name'])))

    while 1:
      try:
        time.sleep(10)
      except KeyboardInterrupt:
        self.log(self.log_str.info('Exiting %s' % (self.config['bot']['name'])))
        time.sleep(1)
        return
      except Exception as e:
        self.log(self.log_str.err('DEBUG exception: %s' % (e)))
        continue

  def send(self, chatId_errorId, reply='Nevermind.'):
    try:
      if chatId_errorId[0] != self.config['admin']['group']:
        self.bot.sendMessage(self.config['admin']['group'], self.log_str.send(chatId_errorId[0], reply))
    except telepot.exception.TelegramError as e:
      self.bot.sendMessage(self.config['admin']['group'], self.log_str.err('DEBUG exception: %s' % (e)))
      print(self.log_str.err('DEBUG exception: %s' % (e)))
#      if e.args[2]['error_code'] == 429:
#        time.sleep(e[2]['parameters']['retry_after']+1)
#        self.bot.sendMessage(self.config['admin']['group'], self.log_str.send(chatId_errorId[0], reply))
    try:
      self.bot.sendMessage(chatId_errorId[0], reply)
    except telepot.exception.TelegramError as e:
      self.bot.sendMessage(self.config['admin']['group'], self.log_str.err('DEBUG telegram error: %s' % (e)))
      print(self.log_str.err('DEBUG telegram error: %s' % (e)))
      if e.args[2]['error_code'] == 403:
        self.bot.sendMessage(chatId_errorId[1], 'Eu não consigo te mandar mensagem aqui no grupo, clica em %s para me ativar e eu poder te responder!' % (self.config['bot']['handle']))
#      elif e.args[2]['error_code'] == 429:
#        time.sleep(e[2]['parameters']['retry_after']+1)
#        self.bot.sendMessage(chatId_errorId[0], reply)

  def sendPhotoActually(self, chat_id, params):
    try:
      if self.bot.sendPhoto(chat_id, photo=open(params['photo'][1], 'r'), caption=params['text']):
        os.remove(params['photo'][1])
        return True
    except Exception as e:
#      if e[1] == 429:
#        time.sleep(e[2]['parameters']['retry_after']+1)
#        if self.bot.sendPhoto(chat_id, photo=open(params['photo'][1], 'r'), caption=params['text']):
#          os.remove(params['photo'][1])
#          return True
#      else:
      raise

  def sendPhoto(self, chatId_errorId, params):
    try:
      self.sendPhotoActually(chatId_errorId[0], params)
    except telepot.exception.TelegramError as e:
      self.bot.sendMessage(self.config['admin']['group'], self.log_str.err('DEBUG telegram error: %s' % (e)))
      print(self.log_str.err('DEBUG telegram error: %s' % (e)))
#      if e.args[2]['error_code'] == 429:
#        time.sleep(e[2]['parameters']['retry_after']+1)
#        self.sendPhotoActually(chatId_errorId[0], params)
      if e.args[2]['error_code'] == 403:
        try:
          self.sendPhotoActually(chatId_errorId[1], params)
        except Exception as e:
#          if e[1] == 429:
#            time.sleep(e[2]['parameters']['retry_after']+1)
          self.sendPhotoActually(chatId_errorId[1], params)
          self.bot.sendMessage(self.config['admin']['group'], self.log_str.err('DEBUG telegram error: %s' % (e)))
          print(self.log_str.err('DEBUG telegram error: %s' % (e)))
#          self.bot.sendMessage(chatId_errorId[1], 'Eu não consigo te mandar mensagem aqui no grupo, clica em %s para me ativar e eu poder te responder!' % (self.config['bot']['handle']))

  def log(self, reply):
    print(reply)
    self.send((self.config['admin']['group'], self.config['admin']['id']), reply)

  def rcv(self, msg):
    self.log(self.log_str.rcv(str(msg['chat']['id']), '%s' % (msg)))
    glance = telepot.glance(msg)
    if glance[0] == 'text':
      chat_id = self.config['admin']['group']
      command_list = list()
      try:
        from_id = int(msg['from']['id'])
        chat_id = int(msg['chat']['id'])

        for subcommand in ' '.join(msg['text'].splitlines()).split(' '):
        ## TODO: Isto está impedindo de enviar links para o bot. Alguém tem uma ideia melhor pra eliminar caracteres indesejáveis das respostas? Eu não quero que as pessoas fiquem mandando código python pra rodar no servidor.
#          pattern = re.compile(u'(^[/]{1}|[@]{1}|[,.]|-?\d+|\n|\w+)', re.UNICODE)
#          item = ''.join(re.findall(pattern, subcommand))
#          if item != '':
#            command_list.append(item)
          command_list.append(subcommand)
      except Exception as e:
        self.log(self.log_str.err('DEBUG Telepot error: %s' % (e)))

      self.log(self.log_str.cmd(' '.join(command_list)))

      if command_list[0][0] == '/':
        response = comandos.parse(chat_id, from_id, command_list)
        try:
          ## Tell admin group what is running
          if response['type'] == 'erro':
            self.send((self.config['admin']['group'], self.config['admin']['id']), self.log_str.err(response['debug']))
          elif response['type'] == 'feedback':
            self.send((self.config['admin']['group'], self.config['admin']['id']), '#feedback enviado de %s por %s:\n\n%s' % (chat_id, from_id, response['feedback']))
          else:
            self.send((self.config['admin']['group'], self.config['admin']['id']), self.log_str.info(response['debug']))
          ## Send command result to command issuer
          if response['type'] == 'nada':
            pass
          elif response['type'] == 'feedback':
            self.send((from_id, chat_id), response['response'])
          elif response['type'] == 'qrcode':
            self.sendPhoto((from_id, chat_id), response['response'])
          elif response['type'] == 'mensagem':
            self.send((from_id, chat_id), response['response'])
          elif response['type'] == 'grupo':
            self.send((chat_id, chat_id), response['response'])
          elif response['type'] == 'erro':
            self.send((from_id, chat_id), response['response'])
          else:
            self.send((self.config['admin']['group'], self.config['admin']['id']), self.log_str.debug(response['debug']))
        except Exception as e:
          self.log(self.log_str.debug('%s from %s to %s failed.\nResponse: %s\nException: %s' % (command_list, from_id, chat_id, response, e)))

