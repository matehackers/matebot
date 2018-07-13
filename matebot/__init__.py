# vim:fileencoding=utf-8
## Antes de sair debulhando, leia o manual
## Documentação de bots de telegram em https://core.telegram.org/bots
## Documentação do telepot em https://telepot.readthedocs.io/en/latest/
## Documentação do matehackers em https://matehackers.org/

import os, re, time, datetime, json

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
    print(log_str.err(u'Este bot só funciona com telepot. Tente instalar telepot primeiro.\nInstalar telepot e todas as outras dependências deste bot: `pip3 install -r requirements.txt`.\nSe isto não funcionar, tente `python3 -m pip install --user -r requirements`.\nCaso isto não funcione também, então acesse https://pip.pypa.io/en/stable/installing/ para aprender a instalar pip.'))
    exit()

class bot():

  def __init__(self):

    self.config_file = str("config/.matebot.cfg")
    try:
      self.config = configparser.ConfigParser()
    except NameError:
      self.config = ConfigParser.ConfigParser()

    try:
      self.config.read(self.config_file)
      print(log_str.info(u'Tentando iniciar MateBot...'))
      print(log_str.info(u"O nosso token do @BotFather é '%s', os ids de usuária(o)s administradora(e)s são '%s' e os ids dos grupos administradores são '%s'. O nome de usuário da(o) administrador(a) é '%s'." % (self.config['botfather']['token'], json.loads(self.config.get('plugins_usuarios', 'admin')), json.loads(self.config.get('plugins_grupos', 'admin')), self.config['info']['telegram_admin'])))
    except Exception as e:
      print(log_str.err(str(u'Problema com o arquivo de configuração. Vossa excelência lerdes o manual antes de tentar usar este bot?\nO problema aparentemente foi o seguinte:\n%s %s\n\nCertificai-vos de que as instruções do arquivo README.md, seção "Configurando" foram lidas e obedecidas.\nEncerrado abruptamente.\n\n' % (type(e), e))))
      return

    try:
      self.bot = telepot.Bot(self.config['botfather']['token'])
      ## TODO Reler o manual do telepot e fazer uma coisa mais inteligente
      self.bot.message_loop(self.rcv)
    except Exception as e:
      self.log(log_str.err(u'Erro do Telegram/Telepot: %s\nEncerrando abruptamente.' % (e)))
      return

    self.log(log_str.info(u'Iniciando %s...' % (self.bot.getMe()['first_name'])))

    while 1:
      try:
        time.sleep(datetime.timedelta(seconds=10).total_seconds())
        self.pedidos_pendentes()
      except KeyboardInterrupt:
        self.log(log_str.info(u'Gentilmente encerrando %s...' % (self.bot.getMe()['first_name'])))
        return
      except Exception as e:
        self.log(log_str.err(u'%s morta(o) por exceção: %s' % (self.bot.getMe()['first_name'], e)))
        raise
        continue

  def enviarMensagem(self, ids_list, reply='Nada.', parse_mode=None):
    ## Log [SEND]
    try:
      self.log(log_str.send(ids_list[0], reply))
    except Exception as e:
      print(log_str.debug(u'Exceção tentando fazer log: %s' % (e)))
      raise
    ## Tenta enviar mensagem
    try:
      self.bot.sendMessage(ids_list[0], reply, parse_mode=parse_mode)
    except telepot.exception.TelegramError as e:
      self.log(log_str.err(u'Erro do Telegram tentando enviar mensagem para %s: %s' % (ids_list[0], e)))
      if e.args[2]['error_code'] == 401:
        print(log_str.err(u'Não autorizado. Vossa excelência usou o token correto durante a configuração? Fale com o @BotFather no telegram e crie um bot antes de tentar novamente.'))
        exit()
      elif e.args[2]['error_code'] == 400:
        limit = 4000
        for chunk in [reply[i:i+limit] for i in range(0, len(reply), limit)]:
          self.bot.sendMessage(ids_list[0], chunk, parse_mode='Markdown')
      elif e.args[2]['error_code'] == 403:
        mensagem = u'Eu não consigo te mandar mensagem aqui. Clica em %s para ativar as mensagens particulares e eu poder te responder!' % (self.config['bot']['handle'])
        ## Log [SEND]
        try:
          self.log(log_str.send(ids_list[1], mensagem))
        except Exception as e:
          print(log_str.debug(u'Exceção tentando fazer log: %s' % (e)))
        ## Tenta enviar imagem para segunda opção
        try:
          self.bot.sendMessage(ids_list[1], mensagem, parse_mode='Markdown')
        except telepot.exception.TelegramError as e1:
          self.log(log_str.err(u'Erro do Telegram tentando enviar mensagem para %s: %s' % (ids_list[1], e1)))
          if e.args[2]['error_code'] == 400:
            limit = 4000
            for chunk in [reply[i:i+limit] for i in range(0, len(reply), limit)]:
              self.bot.sendMessage(ids_list[1], chunk, parse_mode='Markdown')
      else:
        self.log(log_str.debug(u'Não consegui enviar %s para %s. Não tentei enviar para %s' % (reply, ids_list[0], ','.join(str(ids_list[1:])))))

  def enviarImagem(self, ids_list, params):
    ## Log [SEND]
    if not ids_list[0] in json.loads(self.config.get('plugins_grupos', 'admin')):
      self.log(log_str.send(ids_list[0], str(params)))
    ## Tenta enviar mensagem
    try:
      if self.bot.sendPhoto(ids_list[0], photo=open(params['photo'][1], 'r'), caption=params['text']):
        os.remove(params['photo'][1])
    except Exception as e:
      ## Log [SEND]
      self.log(log_str.err(u'Erro tentando enviar imagem para %s: %s' % (ids_list[0], e)))
      if e.args[2]['error_code'] == 403:
        ## Tenta enviar imagem para segunda opção
        try:
          if self.bot.sendPhoto(ids_list[1], photo=open(params['photo'][1], 'r'), caption=params['text']):
            os.remove(params['photo'][1])
        except Exception as e1:
          self.log(log_str.err(u'Erro tentando enviar imagem para %s: %s' % (ids_list[1], e1)))

  def log(self, reply):
    print(reply)
    try:
      for grupo_admin in json.loads(self.config.get('plugins_grupos', 'admin')):
        if str(grupo_admin) != str(-1):
          self.bot.sendMessage(grupo_admin, reply)
    except telepot.exception.TelegramError as e:
      if e.args[2]['error_code'] == 401:
        print(log_str.err(u'Não autorizado. Vossa excelência usou o token correto durante a configuração? Fale com o @BotFather no telegram e crie um bot antes de tentar novamente.'))
        exit()
      if e.args[2]['error_code'] == 400:
          print(log_str.debug(u'Grupo de admin incorreto ou não existe. Se a intenção era enviar mensagens de depuração e log para um grupo, então os dados no item "admin" da seção "plugins_grupos" do arquivo de configuração estão errados, incorretos, equivocados.\nExceção ao tentar enviar erro ao grupo de admin: %s' % (e)))
      elif e.args[2]['error_code'] == 403:
        print(log_str.debug(u'Fomos bloqueados pelo grupo de admin!\nExceção ao tentar enviar erro ao grupo de admin: %s' % (e)))
      else:
        print(log_str.debug(u'Erro do Telegram tentando enviar mensagem para o grupo de admin: %s' % (e)))
      raise
    except Exception as e:
      print(log_str.debug(u'Exceção excepcional que não conseguimos tratar tampouco prever: %s' % (e)))
      raise

  def rcv(self, msg):
    self.log(log_str.rcv(str(msg['chat']['id']), str(msg)))
    glance = telepot.glance(msg)
    if glance[0] == 'text':
      chat_id = self.config['plugins_grupos']['admin']
      command_list = list()
      try:
        from_id = int(msg['from']['id'])
        chat_id = int(msg['chat']['id'])
        command_list = msg['text']
      except Exception as e:
        self.log(log_str.err(u'Erro do Telepot tentando receber mensagem: %s' % (e)))

      if command_list[0][0] == '/':
        self.log(log_str.cmd(command_list))
        response = comandos.parse(
          {
            'chat_id': chat_id,
            'from_id': from_id,
            'command_list': command_list,
            'bot': self.bot,
            'config': self.config,
          }
        )
        try:
          ## Log
          if response['type'] == 'erro':
            self.log(log_str.err(response['debug']))
          elif response['type'] == 'feedback':
            self.log('#feedback enviado de %s por %s:\n\n%s' % (chat_id, from_id, response['feedback']))
          else:
            self.log(log_str.info(response['debug']))
          ## Enviando resultado do comando
          ## TODO solução temporária, isto serve para controlar exibição em HTML ou Markdown.
          response.update(parse_mode = None)
          ## TODO https://core.telegram.org/bots/api#sendmessage
          if response['type'] == 'nada':
            pass
          elif response['type'] == 'feedback':
            self.enviarMensagem([from_id, chat_id], response['response'], response['parse_mode'])
          elif response['type'] == 'qrcode':
            self.enviarImagem((from_id, chat_id), response['response'])
          elif response['type'] == 'mensagem':
            if response['multi']:
              for chunk in response['response'].split('$$$EOF$$$'):
                self.enviarMensagem([from_id, chat_id], chunk, response['parse_mode'])
            else:
                self.enviarMensagem([from_id, chat_id], response['response'], response['parse_mode'])
          elif response['type'] == 'grupo':
            if response['multi']:
              for chunk in response['response'].split('$$$EOF$$$'):
                self.enviarMensagem([chat_id, chat_id], chunk, response['parse_mode'])
            else:
              self.enviarMensagem([chat_id, chat_id], response['response'], response['parse_mode'])
          elif response['type'] == 'erro':
            self.enviarMensagem([from_id, chat_id], response['response'], response['parse_mode'])
          elif response['type'] == 'whisper':
            self.enviarMensagem([response['to_id'], from_id], response['response'], response['parse_mode'])
          elif response['type'] == 'comando':
#            mensagem = comandos.parse(chat_id, from_id, [''.join(['/', response['response'][0]]), response['response'][1:]])
            self.enviarMensagem([chat_id, from_id], mensagem['response'], response['parse_mode'])
          else:
            self.enviarMensagem(self.config['plugins_grupos']['admin'] + self.config['plugins_usuarios']['admin'], log_str.debug(response['debug']), response['parse_mode'])
        except Exception as e:
          self.log(log_str.debug(u'%s de %s para %s falhou.\nResponse: %s\nException: %s' % (command_list, from_id, chat_id, response, e)))

  def pedidos_pendentes(self):
    velivery_pedidos_grupos = json.loads(self.config.get("plugins_grupos", "velivery_pedidos"))
    velivery_pedidos_usuarios = json.loads(self.config.get("plugins_grupos", "velivery_pedidos"))
    grupos_debug = json.loads(self.config['plugins_grupos']['admin'])
    usuarios_debug = json.loads(self.config['plugins_usuarios']['admin'])
    mensagem = comandos.parse(
      {
        'chat_id': int(str(velivery_pedidos_usuarios[0])),
        'from_id': int(str(velivery_pedidos_grupos[0])),
        'command_list': "/atrasados",
        'bot': self.bot,
        'config': self.config,
      }
    )
    if mensagem['status']:
      self.log(log_str.cmd(mensagem['debug']))
      for velivery_pedidos_grupo in velivery_pedidos_grupos:
        self.enviarMensagem([velivery_pedidos_grupo, grupos_debug[0]], mensagem['response'], response['parse_mode'])
      for velivery_pedidos_usuario in velivery_pedidos_usuarios:
        self.enviarMensagem([velivery_pedidos_usuario, grupos_debug[0]], mensagem['response'], response['parse_mode'])

