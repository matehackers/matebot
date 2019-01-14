# vim:fileencoding=utf-8
## Antes de sair debulhando, leia o manual
## Documentação de bots de telegram em https://core.telegram.org/bots
## Documentação do telepot em https://telepot.readthedocs.io/en/latest/
## Documentação do matehackers em https://matehackers.org/
## Documentação do Velivery em https://velivery.com.br/termos-de-uso-e-servicos.pdf

import os, json, curses, urllib3
from curses import wrapper

try:
  import configparser
except ImportError:
  import ConfigParser

from matebot import comandos,local
from plugins.log import log_str

try:
  import asyncio
  import telepot.aio
except ImportError:
  try:
    import telepot
  except ImportError as e:
    print(
      log_str.err(
        "\n".join([
          u"Este bot só funciona com telepot. Tente instalar telepot primeiro.",
          u"Para instalar telepot e todas as outras dependências deste bot: `pip3 install -r requirements.txt`.",
          u"Se isto não funcionar, tente `python3 -m pip install --user -r requirements`.",
          u"Caso isto não funcione também, então acesse https://pip.pypa.io/en/stable/installing/ para aprender a instalar pip.",
        ])
      )
    )
    exit()

class bot():

  def __init__(self, mode):
    self.config_file = str("config/.matebot.cfg")
    try:
      self.config = configparser.ConfigParser()
    except NameError:
      self.config = ConfigParser.ConfigParser()
    print(log_str.info(u"Tentando iniciar MateBot..."))
    try:
      self.config.read(self.config_file)
    except Exception as e:
      ## TODO acentuacao
      print(log_str.err(u"Problema com o arquivo de configuração.\nVossa excelência lerdes o manual antes de tentar usar este bot?\nCertificai-vos de que as instruções do arquivo README.md, seção 'Configurando' foram lidas e obedecidas.\nEncerrado abruptamente.\nMais informacoes: %s %s" % (type(e), e)))
      exit()

    ## TODO usar getattr
    if mode == "telepot":
      self.init_telepot()
    elif mode == "cli":
      self.init_cli()
    else:
      ## TODO acentuacao
      print(log_str.info(u"Nao sabe o que ta fazendo..."))
      exit()

  def init_telepot(self):
    print(log_str.info(u"O nosso token do @BotFather é '%s', os ids de usuária(o)s administradora(e)s são '%s' e os ids dos grupos administradores são '%s'. O nome de usuário da(o) administrador(a) é '%s'." % (self.config['botfather']['token'], json.loads(self.config.get('plugins_usuarios', 'admin')), json.loads(self.config.get('plugins_grupos', 'admin')), self.config['info']['telegram_admin'])))
    try:
      self.bot = telepot.Bot(self.config['botfather']['token'])
      ## TODO Reler o manual do telepot e fazer uma coisa mais inteligente
      self.bot.message_loop(self.rcv)
    except Exception as e:
      self.log(log_str.err(u'Erro do Telegram/Telepot: %s\nEncerrando abruptamente.' % (e)))
      exit()
    try:
      self.log(log_str.info(u'Iniciando %s...' % (self.bot.getMe()['first_name'])))
    except urllib3.exceptions.Exception as e:
      # TODO acentuacao
      print(log_str.err(u"Problema de conexao. Verifique se este computador esta conectado na rede.\n%s" % (e)))
      exit()

    self.matebot_local = local.local({'config':self.config,'bot':self.bot})
    while True:
      try:
        self.matebot_local.loop()
      except KeyboardInterrupt:
        self.log(log_str.info(u'Gentilmente encerrando %s...' % (self.bot.getMe()['first_name'])))
        return
      except Exception as e:
        self.log(log_str.err(u'%s morta(o) por exceção: %s' % (self.bot.getMe()['first_name'], e)))
        raise
        continue

  def cli_croak(self, stdscr):
    self.log_cli(stdscr, log_str.info(u"Gentilmente encerrando %s..." % (u"MateBot")))
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    print(log_str.info(u"Tchau!"))

  def init_cli(self):
    print(log_str.info(u"Iniciando em modo interativo..."))

    stdscr = curses.initscr()
    try:
      self.log_cli(stdscr, log_str.info(u'Iniciando %s...' % (u"MateBot")))
    except urllib3.exceptions.Exception as e:
      # TODO acentuacao
      print(log_str.err(u"Excecao: %s\n Encerrando abruptamente." % (e)))
      exit()

    self.matebot_local = local.local({'mode': "cli", 'config':self.config})

    while True:
      try:
        if self.matebot_local.loop_cli(stdscr) > 0:
          self.cli_croak(stdscr)
          return
      except KeyboardInterrupt:
        self.cli_croak(stdscr)
        return
      except Exception as e:
        self.log_cli(stdscr, log_str.err(u'%s morta(o) por exceção: %s' % (u"MateBot", e)))
        raise
        continue

  def enviarMensagem(self, ids_list, reply='Nada.', parse_mode=None):
    ## Log [SEND]
    self.log(log_str.send(ids_list[0], reply))
    ## Tenta enviar mensagem
    try:
      self.bot.sendMessage(ids_list[0], reply, parse_mode=str(parse_mode))
    except telepot.exception.TelegramError as e:
      self.log(log_str.err(u'Erro do Telegram tentando enviar mensagem para %s: %s' % (ids_list[0], e)))
      if e.error_code == 401:
        print(log_str.err(u'Não autorizado. Vossa excelência usou o token correto durante a configuração? Fale com o @BotFather no telegram e crie um bot antes de tentar novamente.'))
        exit()
      elif e.error_code == 400:
        if e.description == 'Bad Request: message must be non-empty':
          pass
        elif e.description == 'Forbidden: bot was blocked by the user':
          limit = 4000
          for chunk in [reply[i:i+limit] for i in range(0, len(reply), limit)]:
            self.bot.sendMessage(ids_list[0], chunk, parse_mode=str(parse_mode))
        else:
          self.bot.sendMessage(ids_list[1], u"Nao consegui enviar mensagem :(", parse_mode=str(parse_mode))
          self.log(log_str.debug(u'Não consegui enviar %s para %s. Avisei %s' % (reply, ids_list[0], ','.join(str(ids_list[1])))))
      elif e.error_code == 403:
        mensagem = u'Eu não consigo te mandar mensagem aqui. Clica em @%s para ativar as mensagens particulares e eu poder te responder!' % (self.bot.getMe()['username'])
        ## Log [SEND]
        try:
          self.log(log_str.send(ids_list[1], mensagem))
        except Exception as e:
          print(log_str.debug(u'Exceção tentando fazer log: %s' % (e)))
        ## Tenta enviar imagem para segunda opção
        try:
          self.bot.sendMessage(ids_list[1], mensagem, parse_mode=str(parse_mode))
        except telepot.exception.TelegramError as e1:
          self.log(log_str.err(u'Erro do Telegram tentando enviar mensagem para %s: %s' % (ids_list[1], e1)))
          if e.error_code == 400 and e.description == 'Forbidden: bot was blocked by the user':
            limit = 4000
            for chunk in [reply[i:i+limit] for i in range(0, len(reply), limit)]:
              self.bot.sendMessage(ids_list[1], chunk, parse_mode=str(parse_mode))
      else:
        self.log(log_str.debug(u'Não consegui enviar %s para %s. Não tentei enviar para %s' % (reply, ids_list[0], ','.join(str(ids_list[1:])))))

  def enviarImagem(self, ids_list, params, parse_mode):
    ## Log [SEND]
    if not ids_list[0] in json.loads(self.config.get('plugins_grupos', 'admin')):
      self.log(log_str.send(ids_list[0], str(params)))
    ## Tenta enviar mensagem
    try:
      if self.bot.sendPhoto(ids_list[0], photo=open(str(params['photo'][1]), 'rb'), caption=u''.join(params['text'])):
        os.remove(str(params['photo'][1]))
    except Exception as e:
      ## Log [SEND]
      self.log(log_str.err(u'Erro tentando enviar imagem para %s: %s' % (ids_list[0], e)))
      if int(e.args[2]['error_code']) == 403:
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
      if e.error_code == 401:
        print(log_str.err(u'Não autorizado. Vossa excelência usou o token correto durante a configuração? Fale com o @BotFather no telegram e crie um bot antes de tentar novamente.'))
        exit()
      if e.error_code == 400:
        # TODO acentuacao
        print(log_str.debug(u'Grupo de admin não existe ou nao fomos adicionados. Se a intenção era enviar mensagens de depuração e log para um grupo, então os dados no item "admin" da seção "plugins_grupos" do arquivo de configuração estão errados, incorretos, equivocados. Ou entao nos nunca fomos adicionados no grupo, ou ainda fomos expulsos.\nExceção ao tentar enviar erro ao grupo de admin: %s' % (e)))
      elif e.error_code == 403:
        print(log_str.debug(u'Fomos bloqueados pelo grupo de admin!\nExceção ao tentar enviar erro ao grupo de admin: %s' % (e)))
      else:
        print(log_str.debug(u'Erro do Telegram tentando enviar mensagem para o grupo de admin: %s' % (e)))
    except Exception as e:
      print(log_str.debug(u'Exceção excepcional que não conseguimos tratar tampouco prever: %s' % (e)))
      raise

  def log_cli(self, stdscr, reply):
    print(reply)
    try:
      for grupo_admin in json.loads(self.config.get('plugins_grupos', 'admin')):
        if str(grupo_admin) != str(-1):
          stdscr.addstr(': '.join([str(grupo_admin), reply]))
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
            'command_type': 'grupo',
          }
        )
        try:
          ## Log
          if str(response['type']) == 'erro':
            self.log(log_str.err(response['debug']))
          elif str(response['type']) == 'feedback':
            self.log('#feedback enviado de %s por %s:\n\n%s' % (chat_id, from_id, response['feedback']))
          else:
            self.log(log_str.info(response['debug']))
          ## Enviando resultado do comando
          ## TODO solução temporária, isto serve para controlar exibição em HTML ou Markdown.
          ## TODO https://core.telegram.org/bots/api#sendmessage
          if not 'parse_mode' in response:
            response.update(parse_mode = None)
            print(log_str.debug(u"parse_mode nao exisitia!"))
          if str(response['type']) == 'nada':
            pass
          elif str(response['type']) == 'feedback':
            self.enviarMensagem([from_id, chat_id], response['response'], response['parse_mode'])
          elif str(response['type']) == "image":
            self.enviarImagem((from_id, chat_id), response['response'], response['parse_mode'])
          elif str(response['type']) == 'mensagem':
            if response['multi']:
              for chunk in response['response'].split('$$$EOF$$$'):
                self.enviarMensagem([from_id, chat_id], chunk, response['parse_mode'])
            else:
                self.enviarMensagem([from_id, chat_id], response['response'], response['parse_mode'])
          elif str(response['type']) == 'grupo':
            if response['multi']:
              for chunk in response['response'].split('$$$EOF$$$'):
                self.enviarMensagem([chat_id, chat_id], chunk, response['parse_mode'])
            else:
              self.enviarMensagem([chat_id, chat_id], response['response'], response['parse_mode'])
          elif str(response['type']) == 'erro':
            self.enviarMensagem([from_id, chat_id], response['response'], response['parse_mode'])
          elif str(response['type']) == 'whisper':
            self.enviarMensagem([response['to_id'], from_id], response['response'], response['parse_mode'])
          elif str(response['type']) == 'comando':
            ## TODO não lembro qual era a relevância disto
#            mensagem = comandos.parse(chat_id, from_id, [''.join(['/', response['response'][0]]), response['response'][1:]])
            self.enviarMensagem([chat_id, from_id], mensagem['response'], response['parse_mode'])
          else:
            self.enviarMensagem([str(json.loads(self.config['plugins_usuarios']['admin'])[0]), str(json.loads(self.config['plugins_usuarios']['admin'])[0])], log_str.debug(response['debug']), response['parse_mode'])
        except Exception as e:
          raise
          self.log(log_str.debug(u'%s de %s para %s falhou.\nResponse: %s\nException: %s' % (command_list, from_id, chat_id, response, e)))

