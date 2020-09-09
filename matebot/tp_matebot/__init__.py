# vim:fileencoding=utf-8
## Antes de sair debulhando, leia o manual
## Documentação de bots de telegram em https://core.telegram.org/bots
## Documentação do python em https://docs.python.org
## Documentação do telepot em https://telepot.readthedocs.io/en/latest/
## Documentação do matehackers em https://matehackers.org
## Documentação do Velivery em https://velivery.com.br
## Documentação da Greatful em https://greatful.com.br
## Documentação da Fábrica do Futuro em https://fabricadofuturo.com

import os, json, urllib3
# ~ import curses
# ~ from curses import wrapper

try:
  import configparser
except ImportError:
  import ConfigParser

from matebot.tp_matebot import comandos,local
from matebot.plugins.log import log_str

try:
  import asyncio
  import telepot.aio
except ImportError:
  try:
    import telepot
  except ImportError as e:
    ## TODO e o pipenv? e o virtualenvwrapper?
    print(
      log_str.err(
        "\n".join([
          u"Este bot só funciona com telepot. Tente instalar telepot \
            primeiro.",
          u"Para instalar telepot e todas as outras dependências deste \
            bot: `pip3 install -r requirements.txt`.",
          u"Se isto não funcionar, tente `python3 -m pip install \
            --user -r requirements`.",
          u"Caso isto não funcione também, então acesse \
            https://pip.pypa.io/en/stable/installing/ para aprender a \
            instalar pip.",
          u"Ou então use o jeito mais fácil que é pipenv: \
            `pipenv install`e `pipenv run python start.py telepot \
            matebot`.",
          u"Caso tiver dúvidas, leia o arquivo README.md - caso ainda \
            tenha dúvidas, pergunte no grupo @matehackerspoa no \
            telegram: https://t.me/matehackerspoa"
        ])
      )
    )
    exit()

class bot():

  def __init__(self, mode, config_file):
    self.config_dir = 'instance'
    ## Compatiblidade com v0.0.13
    # ~ if not os.path.isdir(self.config_dir):
      # ~ print(log_str.warn(
# ~ u"""O diretório 'instance' não existe. O diretório 'config' não vai \
# ~ mais ser utilizado nas próximas versões. Leia o README.md e atualize o \
# ~ arquivo de configuração."""))
      # ~ self.config_dir = 'config'
    # ~ self.config_file = u"%s/.%s.cfg" % (self.config_dir, config_file)
    # ~ if not os.path.isfile(self.config_file):
      # ~ print(log_str.err(
# ~ u"""Problema com o arquivo de configuração.\nVossa excelência lerdes o \
# ~ manual antes de tentar usar este bot?\nCertificai-vos de que as \
# ~ instruções do arquivo README.md, seção 'Configurando' foram lidas e \
# ~ obedecidas.\nEncerrando abruptamente."""))
      # ~ exit()
    try:
      from instance.config import Config
      config = Config()
      self.config = config.bots[config_file]
    except Exception as e:
      print(log_str.debug(str(e)))
      self.config = None
    ## Compatibilidade com v0.0.14
    if self.config is None:
      try:
        self.config = configparser.ConfigParser()
      except NameError:
        self.config = ConfigParser.ConfigParser()
      print(log_str.info(u"Tentando iniciar MateBot..."))
      try:
        self.config.read(self.config_file)
      except Exception as e:
        try:
          self.config_file = u"config/.%s.cfg" % (config_file)
          self.config = configparser.ConfigParser()
          self.config.read(self.config_file)
        except Exception as e:
          print(log_str.err(
  u"""Problema com o arquivo de configuração.\nVossa excelência lerdes o \
  manual antes de tentar usar este bot?\nCertificai-vos de que as \
  instruções do arquivo README.md, seção 'Configurando' foram lidas e \
  obedecidas.\nEncerrando abruptamente.\nMais informações: %s %s"""
          % (type(e), str(e))))
          exit()

    self.interativo = 0

    ## TODO usar getattr
    if mode == "telepot":
      self.init_telepot()
#    elif mode == "cli":
#      self.init_cli()
    else:
      ## TODO mudar esta frase quando esta informação se tornar incorreta
      print(log_str.info(u"Por enquanto o único modo de operação é telepot"))
      exit()

  def init_telepot(self):
    print(log_str.info(
      u"O nosso token do @BotFather é '{}', \
      os ids de usuária(o)s administradora(e)s são '{}'. \
      O nome de usuário da(o) administrador(a) é '{}'.".format(
      self.config['token'],
      self.config['users']['alpha'],
      self.config['info']['admin'])
    ))
    try:
      self.bot = telepot.Bot(self.config['token'])
      ## TODO Reler o manual do telepot e fazer uma coisa mais inteligente
      self.bot.message_loop(self.rcv)
    except Exception as e:
      self.log(log_str.err(u"Erro do Telegram/Telepot: %s\nEncerrando abruptamente." % (e)))
      exit()
    try:
      print(log_str.info(u"Iniciando %s..." % (self.bot.getMe()['first_name'])))
      self.log(log_str.info(u"%s online!" % (self.bot.getMe()['first_name'])))
    except Exception as e:
      print(log_str.err(u"Problema de conexão. Verifique se este computador está conectado na rede.\nExceção: %s" % (e)))
      raise

    self.matebot_local = local.local({'config':self.config,'bot':self.bot})
    while True:
      try:
        self.matebot_local.loop()
      except KeyboardInterrupt:
        self.log(log_str.info(u"Gentilmente encerrando %s..." % (self.bot.getMe()['first_name'])))
        return
      except Exception as e:
        self.log(log_str.err(u"%s morta(o) por exceção: %s" % (self.bot.getMe()['first_name'], e)))
        raise
        continue

  # ~ def cli_croak(self, stdscr):
    # ~ self.log_cli(stdscr, log_str.info(u"Gentilmente encerrando %s..." % (u"MateBot")))
    # ~ curses.nocbreak()
    # ~ stdscr.keypad(False)
    # ~ curses.echo()
    # ~ curses.endwin()
    # ~ print(log_str.info(u"Tchau!"))

  # ~ def init_cli(self):
    # ~ print(log_str.info(u"Iniciando em modo interativo..."))
    # ~ try:
      # ~ stdscr = curses.initscr()
      # ~ self.log_cli(stdscr, log_str.info(u"Iniciando %s...\n" % (u"MateBot")))
      # ~ self.matebot_local = local.local({'mode': "cli", 'config':self.config})
    # ~ except Exception as e:
      # ~ print(log_str.debug(u"Excecao: %s\nEncerrando abruptamente." % (e)))
      # ~ exit()

    # ~ while True:
      # ~ try:
        # ~ if self.matebot_local.loop_cli(stdscr) > 0:
          # ~ self.cli_croak(stdscr)
          # ~ return
        # ~ else:
          # ~ stdscr.addstr(u"\n")
          # ~ stdscr.refresh()
      # ~ except KeyboardInterrupt:
        # ~ self.cli_croak(stdscr)
        # ~ return
      # ~ except Exception as e:
        # ~ self.cli_croak(stdscr)
        # ~ print(log_str.err(u"%s morta(o) por exceção: %s" % (u"MateBot", e)))
        # ~ raise
        # ~ continue

  ## TODO Eu não ia dizer, mas eu vou ter que dizer que esse wrapper aqui, tá uma
  def enviarMensagem(self, ids_list, reply='Nada.', parse_mode=None, reply_to_message_id = False):
    ## Log [SEND]
    try:
      self.log(log_str.send(ids_list[0], reply))
    except Exception as e:
      print(log_str.debug(u'Exceção tentando fazer log: %s' % (str(e))))
      raise
    ## Tenta enviar mensagem
    try:
      if reply_to_message_id:
        self.bot.sendMessage(ids_list[0], reply, parse_mode=parse_mode, reply_to_message_id = str(reply_to_message_id))
      else:
        self.bot.sendMessage(ids_list[0], reply, parse_mode=parse_mode)
    except telepot.exception.TelegramError as e:
      self.log(log_str.err(u'Erro do Telegram tentando enviar mensagem para %s: %s' % (ids_list[0], str(e))))
      if e.error_code == 401:
        print(log_str.err(u'Não autorizado. Vossa excelência usou o token correto durante a configuração? Fale com o @BotFather no telegram e crie um bot antes de tentar novamente.'))
        exit()
      elif e.error_code == 400:
        if e.description == 'Bad Request: message must be non-empty':
          self.bot.sendMessage(ids_list[1], u"Não consegui enviar mensagem :(\nErro: %s" % (str(e)), parse_mode=parse_mode, reply_to_message_id=reply_to_message_id)
        elif e.description == 'Forbidden: bot was blocked by the user':
          self.bot.sendMessage(ids_list[1], u"Não consegui enviar mensagem :(\nErro: %s" % (str(e)), parse_mode=parse_mode, reply_to_message_id=reply_to_message_id)
        else:
          ## FIXME isto não vai funcionar se o parse_mode não for None.
          ## O resultado vai ser um erro sem nenhum aviso.
          limit = 4000
          for chunk in [reply[i:i+limit] for i in range(0, len(reply), limit)]:
            self.bot.sendMessage(ids_list[0], chunk, parse_mode=parse_mode)
          self.log(log_str.debug(u'Não consegui enviar %s para %s. Avisei %s' % (reply, ids_list[0], ','.join(str(ids_list[1:])))))
      elif e.error_code == 403:
        mensagem = u"Eu não consigo te mandar mensagem aqui. Clica em @%s para ativar as mensagens particulares e eu poder te responder!" % (str(self.bot.getMe()['username']))
        ## Log [SEND]
        try:
          self.log(log_str.send(ids_list[1], mensagem))
        except Exception as e:
          print(log_str.debug(u"Exceção tentando fazer log: %s" % (str(e))))
        ## Tenta enviar imagem para segunda opção
        try:
          if reply_to_message_id:
            self.bot.sendMessage(ids_list[1], mensagem, parse_mode=parse_mode, reply_to_message_id=str(reply_to_message_id))
          else:
            self.bot.sendMessage(ids_list[1], mensagem)
        except telepot.exception.TelegramError as e1:
          self.log(log_str.err(u"Erro do Telegram tentando enviar mensagem para %s: %s" % (ids_list[1], str(e1))))
          if reply_to_message_id:
            self.bot.sendMessage(
              ids_list[1],
              u"Não consegui enviar mensagem :(\nErro: %s" % (str(e1)),
              reply_to_message_id=reply_to_message_id
            )
          else:
            self.bot.sendMessage(
              ids_list[1],
              u"Não consegui enviar mensagem :(\nErro: %s" % (str(e1)),
              parse_mode=parse_mode
            )
      else:
        self.log(log_str.debug(u"Não consegui enviar %s para %s. Não tentei enviar para %s" % (reply, ids_list[0], ','.join(ids_list))))

  def enviarImagem(self, ids_list, params, parse_mode, reply_to_message_id):
    ## Log [SEND]
    if not ids_list[0] in self.config['users']['alpha']:
      self.log(log_str.send(ids_list[0], str(params)))
    ## Tenta enviar mensagem
    try:
      if reply_to_message_id:
        if self.bot.sendPhoto(ids_list[0], photo=open(str(params['photo'][1]), 'rb'), caption=u''.join(params['text']), reply_to_message_id = str(reply_to_message_id)):
          os.remove(str(params['photo'][1]))
      else:
        if self.bot.sendPhoto(ids_list[0], photo=open(str(params['photo'][1]), 'rb'), caption=u''.join(params['text'])):
          os.remove(str(params['photo'][1]))
    except Exception as e:
      ## Log [SEND]
      self.log(log_str.err(u'Erro tentando enviar imagem para %s: %s' % (ids_list[0], e)))
      if e.error_code == 403:
        ## Tenta enviar imagem para segunda opção
        try:
          if self.bot.sendPhoto(ids_list[1], photo=open(params['photo'][1], 'r'), caption=params['text']):
            os.remove(params['photo'][1])
        except Exception as e1:
          self.log(log_str.err(u'Erro tentando enviar imagem para %s: %s' % (ids_list[1], e1)))

  def log(self, reply):
    print(reply)
    try:
      for grupo_admin in self.config['users']['alpha']:
        if str(grupo_admin) != str(-1):
          self.bot.sendMessage(grupo_admin, reply)
    except telepot.exception.TelegramError as e:
      if e.error_code == 401:
        print(log_str.err(u"Não autorizado. Vossa excelência usou o token correto durante a configuração? Fale com o @BotFather no telegram e crie um bot antes de tentar novamente."))
        exit()
      if e.error_code == 400:
        print(log_str.debug(u"Grupo de admin não existe ou não fomos adicionados. Se a intenção era enviar mensagens de depuração e log para um grupo, então os dados no item 'admin' da seção 'plugins_grupos' do arquivo de configuração estão errados, incorretos, equivocados. Ou então nós nunca fomos adicionados no grupo, ou ainda fomos expulsos.\nExceção ao tentar enviar erro ao grupo de admin: %s" % (e)))
      elif e.error_code == 403:
        print(log_str.debug(u"Fomos bloqueados pelo grupo de admin!\nExceção ao tentar enviar erro ao grupo de admin: %s" % (e)))
      else:
        print(log_str.debug(u"Erro do Telegram tentando enviar mensagem para o grupo de admin: %s" % (e)))
      raise
    except Exception as e:
      print(log_str.debug(u"Exceção excepcional que não conseguimos tratar tampouco prever: %s" % (e)))
      raise

  def log_cli(self, stdscr, reply):
    print(reply)
    try:
      for grupo_admin in self.config['users']['alpha']:
        if str(grupo_admin) != str(-1):
          stdscr.addstr(': '.join([str(grupo_admin), reply]))
    except Exception as e:
      print(log_str.debug(u'Exceção excepcional que não conseguimos tratar tampouco prever: %s' % (e)))
      raise

  def rcv(self, msg):
#    self.log(log_str.rcv(str(msg['chat']['id']), str(msg)))
    self.log(log_str.rcv(str(msg['chat']['id']), json.dumps(msg, sort_keys=True, indent=2)))
    glance = telepot.glance(msg)
    if glance[0] == 'text':
      chat_id = self.config['users']['alpha'][0]
      command_list = list()
      try:
        from_id = int(msg['from']['id'])
        chat_id = int(msg['chat']['id'])
        message_id = int(msg['message_id'])
        command_list = msg['text']
      except Exception as e:
        self.log(log_str.err(u'Erro do Telepot tentando receber mensagem: %s' % (e)))

      if self.interativo > 0:
        args.update
        automatico(args)
      elif command_list[0][0] == '/':
        self.log(log_str.cmd(command_list))
        response = comandos.parse(
          {
            'chat_id': chat_id,
            'from_id': from_id,
            'message_id': message_id,
            'command_list': command_list,
            'bot': self.bot,
            'config': self.config,
            'command_type': 'grupo',
          }
        )
        try:
          ## Log
          if str(response['type']) == 'erro':
            self.log(log_str.err(response['debug']))
          elif str(response['type']) == 'feedback':
            self.log('#feedback enviado de %s por %s:\n\n%s' % (chat_id, from_id, response['feedback']))
          elif str(response['type']) == "whisper":
            self.log('#whisper enviado de %s por %s para %s:\n\n%s' % (chat_id, from_id, response['to_id'], response['response']))
          else:
            self.log(log_str.info(response['debug']))
          ## Enviando resultado do comando
          ## TODO solução temporária, isto serve para controlar exibição em HTML ou Markdown.
          ## TODO https://core.telegram.org/bots/api#sendmessage
          if not 'parse_mode' in response:
            response.update(parse_mode = None)
            print(log_str.debug(u"parse_mode nao exisitia!"))
          ## TODO mais solução temporária
          if not 'reply_to_message_id' in response:
            response.update(reply_to_message_id = False)
            print(log_str.debug(u"reply_to_message_id nao exisitia!"))
          if str(response['type']) == 'nada':
            self.log(u"#nada\n\nresponse:\n%s\n\ndebug:\n%s" % (response['response'], response['debug']))
            pass
          elif str(response['type']) == 'feedback':
            self.enviarMensagem([chat_id, chat_id], response['response'], response['parse_mode'], response['reply_to_message_id'])
          elif str(response['type']) == "image":
            self.enviarImagem((chat_id, chat_id), response['response'], response['parse_mode'], response['reply_to_message_id'])
          elif str(response['type']) == 'qrcode':
            self.enviarImagem((chat_id, chat_id), response['response'], response['parse_mode'], response['reply_to_message_id'])
          elif str(response['type']) == 'video':
            self.log(log_str.info(response['debug']))
          elif str(response['type']) == 'mensagem':
            if response['multi']:
              for chunk in response['response'].split('$$$EOF$$$'):
                self.enviarMensagem([chat_id, chat_id], chunk, response['parse_mode'], response['reply_to_message_id'])
            else:
              self.enviarMensagem([from_id, chat_id], response['response'], response['parse_mode'], response['reply_to_message_id'])
          elif str(response['type']) == 'grupo':
            if response['multi']:
              for chunk in response['response'].split('$$$EOF$$$'):
                self.enviarMensagem([chat_id, chat_id], chunk, response['parse_mode'], response['reply_to_message_id'])
            else:
              self.enviarMensagem([chat_id, chat_id], response['response'], response['parse_mode'], response['reply_to_message_id'])
          elif str(response['type']) == 'erro':
            self.enviarMensagem([chat_id, chat_id], response['response'], response['parse_mode'], response['reply_to_message_id'])
          elif str(response['type']) == 'whisper':
            self.enviarMensagem([response['to_id'], chat_id], response['response'], response['parse_mode'], False)
          elif str(response['type']) == 'comando':
            ## TODO não lembro qual era a relevância disto
#            mensagem = comandos.parse(chat_id, from_id, [''.join(['/', response['response'][0]]), response['response'][1:]])
            self.enviarMensagem([chat_id, from_id], mensagem['response'], response['parse_mode'], response['reply_to_message_id'])
          else:
            self.enviarMensagem([str(self.config['users']['alpha'][0]), str(self.config['users']['alpha'][0])], log_str.debug(response['debug']), response['parse_mode'], response['reply_to_message_id'])
        except Exception as e:
          raise
          self.log(log_str.debug(u'%s de %s para %s falhou.\nResponse: %s\nException: %s' % (command_list, from_id, chat_id, response, e)))
