# vim:fileencoding=utf-8
## Antes de sair debulhando, leia o manual
## Documentação de bots de telegram em https://core.telegram.org/bots
## Documentação do telepot em https://telepot.readthedocs.io/en/latest/
## Documentação do matehackers em https://matehackers.org/

import os, re, time

try:
  import configparser
except ImportError:
  import ConfigParser

from matebot import comandos
from plugins.log import log_str

try:
  import asyncio
  import telepot.aio
except ImportError:
  try:
    import telepot
  except ImportError as e:
    print(log_str.err(u'Este bot só funciona com telepot. Tente instalar telepot primeiro.\nInstalar telepot e todas as outras dependências deste bot: `pip install --user -r requirements.txt`.\nSe isto não funcionar, tente `python3 -m pip install --user -r requirements`.\nCaso isto não funcione também, então acesse https://pip.pypa.io/en/stable/installing/ para aprender a instalar pip.'))
    exit()

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
    except configparser.Exception as e:
      print(self.log_str.err(u'Problema com o arquivo de configuração. Vossa excelência lerdes o manual antes de tentar usar este bot?\n%s' % (e)))
      return

    print(self.log_str.info(u'Tentando iniciar %s' % (self.config['bot']['name'])))
    print(self.log_str.info(u"O nosso token do @BotFather é '%s', o id de usuário administrador é '%s' e o id do grupo administrador é '%s'. O nome de usuário do administrador é '%s' e o nosso é '%s'." % (self.config['botfather']['token'], self.config['admin']['id'], self.config['admin']['group'], self.config['info']['telegram_admin'], self.config['bot']['handle'])))

    try:
      self.bot = telepot.Bot(self.config['botfather']['token'])
      self.bot.message_loop(self.rcv)
    except Exception as e:
      self.log(self.log_str.err(u'Erro do Telegram/Telepot: %s' % (e)))

    self.log(self.log_str.info(u'Iniciando %s' % (self.config['bot']['name'])))

    while 1:
      try:
        time.sleep(1)
      except KeyboardInterrupt:
        self.log(self.log_str.info(u'Gentilmente encerrando %s...' % (self.config['bot']['name'])))
        return
      except Exception as e:
        self.log(self.log_str.err(u'%s processo morto por exceção: %s' % (self.config['bot']['name'], e)))
        continue

  def enviarMensagem(self, ids_list, reply='Nevermind.'):
    try:
      if ids_list[0] != self.config['admin']['group']:
        self.bot.sendMessage(self.config['admin']['group'], self.log_str.send(ids_list[0], reply))
    except telepot.exception.TelegramError as e:
      erro = self.log_str.err(u'Erro do Telegram tentando enviar mensagem para %s: %s' % (self.config['admin']['group'], e))
      print(erro)
      self.bot.sendMessage(self.config['admin']['group'], erro)
    try:
      self.bot.sendMessage(ids_list[0], reply)
    except telepot.exception.TelegramError as e:
      erro = self.log_str.err(u'Erro do Telegram tentando enviar mensagem para %s: %s' % (ids_list[0], e))
      print(erro)
      self.bot.sendMessage(self.config['admin']['group'], erro)
      if e.args[2]['error_code'] == 403:
        mensagem = u'Eu não consigo te mandar mensagem aqui no grupo, clica em %s para me ativar e eu poder te responder!' % (self.config['bot']['handle'])
        try:
          self.bot.sendMessage(self.config['admin']['group'], self.log_str.send(ids_list[1], mensagem))
        except telepot.exception.TelegramError as e:
          erro = self.log_str.err(u'Erro do Telegram tentando enviar mensagem para %s: %s' % (self.config['admin']['group'], e))
          print(erro)
          self.bot.sendMessage(self.config['admin']['group'], erro)
        self.bot.sendMessage(ids_list[1], mensagem)
      else:
        mensagem = u'Não consegui enviar %s para %s. Não tentei enviar para %s' % (reply, ids_list[0], ','.join(ids_list[1:]))
        try:
          self.bot.sendMessage(self.config['admin']['group'], self.log_str.err(mensagem))
        except telepot.exception.TelegramError as e:
          erro = self.log_str.err(u'Erro do Telegram tentando enviar mensagem para %s: %s' % (self.config['admin']['group'], e))
          print(erro)
          self.bot.sendMessage(self.config['admin']['group'], erro)

  def enviarImagem(self, ids_list, params):
    try:
      if ids_list[0] != self.config['admin']['group']:
        self.bot.sendMessage(self.config['admin']['group'], self.log_str.send(ids_list[0], str(params)))
    except telepot.exception.TelegramError as e:
      erro = self.log_str.err(u'Erro do Telegram tentando enviar imagem para %s: %s' % (self.config['admin']['group'], e))
      print(erro)
      self.bot.sendMessage(self.config['admin']['group'], erro)
    try:
      if self.bot.sendPhoto(ids_list[0], photo=open(params['photo'][1], 'r'), caption=params['text']):
        os.remove(params['photo'][1])
    except Exception as e:
      erro = self.log_str.err(u'Erro tentando enviar imagem para %s: %s' % (ids_list[0], e))
      print(erro)
      self.bot.sendMessage(self.config['admin']['group'], erro)
      if e.args[2]['error_code'] == 403:
        try:
          if self.bot.sendPhoto(ids_list[1], photo=open(params['photo'][1], 'r'), caption=params['text']):
            os.remove(params['photo'][1])
        except Exception as e:
          erro = self.log_str.err(u'Erro tentando enviar imagem para %s: %s' % (ids_list[1], e))
          print(erro)
          self.bot.sendMessage(self.config['admin']['group'], erro)

  def log(self, reply):
    print(reply)
    self.enviarMensagem([self.config['admin']['group'], self.config['admin']['id']], reply)

  def rcv(self, msg):
    self.log(self.log_str.rcv(str(msg['chat']['id']), str(msg)))
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
        self.log(self.log_str.err(u'Erro do Telepot tentando receber mensagem: %s' % (e)))


      if command_list[0][0] == '/':
        self.log(self.log_str.cmd(' '.join(command_list)))
        response = comandos.parse(chat_id, from_id, command_list)
        try:
          ## Log
          if response['type'] == 'erro':
            self.enviarMensagem([self.config['admin']['group'], self.config['admin']['id']], self.log_str.err(response['debug']))
          elif response['type'] == 'feedback':
            self.enviarMensagem([self.config['admin']['group'], self.config['admin']['id']], '#feedback enviado de %s por %s:\n\n%s' % (chat_id, from_id, response['feedback']))
          else:
            self.enviarMensagem([self.config['admin']['group'], self.config['admin']['id']], self.log_str.info(response['debug']))
          ## Enviando resultado do comando
          if response['type'] == 'nada':
            pass
          elif response['type'] == 'feedback':
            self.enviarMensagem([from_id, chat_id], response['response'])
          elif response['type'] == 'qrcode':
            self.enviarImagem((from_id, chat_id), response['response'])
          elif response['type'] == 'mensagem':
            self.enviarMensagem([from_id, chat_id], response['response'])
          elif response['type'] == 'grupo':
            self.enviarMensagem([chat_id, chat_id], response['response'])
          elif response['type'] == 'erro':
            self.enviarMensagem([from_id, chat_id], response['response'])
          else:
            self.enviarMensagem([self.config['admin']['group'], self.config['admin']['id']], self.log_str.debug(response['debug']))
        except Exception as e:
          self.log(self.log_str.debug(u'%s de %s para %s falhou.\nResponse: %s\nException: %s' % (command_list, from_id, chat_id, response, e)))

