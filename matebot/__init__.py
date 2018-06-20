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
    print(log_str.err(u'Este bot só funciona com telepot. Tente instalar telepot primeiro.\nInstalar telepot e todas as outras dependências deste bot: `pip install --user -r requirements.txt`.\nSe isto não funcionar, tente `python3 -m pip install --user -r requirements`.\nCaso isto não funcione também, então acesse https://pip.pypa.io/en/stable/installing/ para aprender a instalar pip.'))
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
      print(log_str.info(u'Tentando iniciar %s' % (self.config['bot']['name'])))
      print(log_str.info(u"O nosso token do @BotFather é '%s', o id de usuário administrador é '%s' e o id do grupo administrador é '%s'. O nome de usuário do administrador é '%s' e o nosso é '%s'." % (self.config['botfather']['token'], self.config['admin']['id'], self.config['admin']['group'], self.config['info']['telegram_admin'], self.config['bot']['handle'])))
    except Exception as e:
      print(log_str.err(str(u'Problema com o arquivo de configuração. Vossa excelência lerdes o manual antes de tentar usar este bot?\nO problema aparentemente foi o seguinte: %s %s\nCertificai-vos de que as instruções do arquivo README.md, seção "Configurando" foram lidas e obedecidas.\nEncerrado abruptamente.\n\n' % (type(e), e))))
      return

    try:
      self.bot = telepot.Bot(self.config['botfather']['token'])
      self.bot.message_loop(self.rcv)
    except Exception as e:
      self.log(log_str.err(u'Erro do Telegram/Telepot: %s\nEncerrando abruptamente.' % (e)))
      return

    self.log(log_str.info(u'Iniciando %s...' % (self.config['bot']['name'])))

    while 1:
      try:
        time.sleep(datetime.timedelta(minutes=4).total_seconds())
        self.pedidos_pendentes()
      except KeyboardInterrupt:
        self.log(log_str.info(u'Gentilmente encerrando %s...' % (self.config['bot']['name'])))
        return
      except Exception as e:
        self.log(log_str.err(u'%s processo morto por exceção: %s' % (self.config['bot']['name'], e)))
        continue

  def enviarMensagem(self, ids_list, reply='Nevermind.'):
    ## Log [SEND]
    try:
      self.log(log_str.send(ids_list[0], reply))
    except Exception as e:
      print(log_str.debug(u'Exceção tentando fazer log: %s' % (e)))
    ## Tenta enviar mensagem
    try:
      self.bot.sendMessage(ids_list[0], reply, parse_mode='Markdown')
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
    if ids_list[0] != self.config['admin']['group']:
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
      self.bot.sendMessage(self.config['admin']['group'], reply)
    except telepot.exception.TelegramError as e:
      if e.args[2]['error_code'] == 401:
        print(log_str.err(u'Não autorizado. Vossa excelência usou o token correto durante a configuração? Fale com o @BotFather no telegram e crie um bot antes de tentar novamente.'))
        exit()
      if str(self.config['admin']['group']) != str(-1):
        if e.args[2]['error_code'] == 400:
            print(log_str.debug(u'Grupo de admin incorreto ou não existe. Se a intenção era enviar mensagens de depuração e log para um grupo, então os dados na seção [admin] do arquivo de configuração estão errados, incorretos, equivocados.\nExceção ao tentar enviar erro ao grupo de admin: %s' % (e)))
        elif e.args[2]['error_code'] == 403:
          print(log_str.debug(u'Fomos bloqueados pelo grupo de admin!\nExceção ao tentar enviar erro ao grupo de admin: %s' % (e)))
        else:
          print(log_str.debug(u'Erro do Telegram tentando enviar mensagem para %s: %s' % (self.config['admin']['group'], e)))
    except Exception as e:
      print(log_str.debug(u'Merdão: %s' % (e)))

  def rcv(self, msg):
    self.log(log_str.rcv(str(msg['chat']['id']), str(msg)))
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
        self.log(log_str.err(u'Erro do Telepot tentando receber mensagem: %s' % (e)))


      if command_list[0][0] == '/':
        self.log(log_str.cmd(' '.join(command_list)))
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
          if response['type'] == 'nada':
            pass
          elif response['type'] == 'feedback':
            self.enviarMensagem([from_id, chat_id], response['response'])
          elif response['type'] == 'qrcode':
            self.enviarImagem((from_id, chat_id), response['response'])
          elif response['type'] == 'mensagem':
            if response['multi']:
              for chunk in response['response'].split('$$$EOF$$$'):
                self.enviarMensagem([from_id, chat_id], chunk)
            else:
                self.enviarMensagem([from_id, chat_id], response['response'])
          elif response['type'] == 'grupo':
            if response['multi']:
              for chunk in response['response'].split('$$$EOF$$$'):
                self.enviarMensagem([chat_id, chat_id], chunk)
            else:
              self.enviarMensagem([chat_id, chat_id], response['response'])
          elif response['type'] == 'erro':
            self.enviarMensagem([from_id, chat_id], response['response'])
          elif response['type'] == 'whisper':
            self.enviarMensagem([response['to_id'], from_id], response['response'])
          elif response['type'] == 'comando':
#            mensagem = comandos.parse(chat_id, from_id, [''.join(['/', response['response'][0]]), response['response'][1:]])
            self.enviarMensagem([chat_id, from_id], mensagem['response'])
          else:
            self.enviarMensagem([self.config['admin']['group'], self.config['admin']['id']], log_str.debug(response['debug']))
        except Exception as e:
          self.log(log_str.debug(u'%s de %s para %s falhou.\nResponse: %s\nException: %s' % (command_list, from_id, chat_id, response, e)))

  def pedidos_pendentes(self):
    velivery_pedidos_grupos = json.loads(self.config['velivery_pedidos']['grupos'])
    velivery_pedidos_usuarios = json.loads(self.config.get("velivery_pedidos", "usuarios"))
    grupo_debug = self.config['admin']['group']
    usuario_debug = self.config['admin']['id']
    mensagem = comandos.parse(
      {
        'chat_id': int(velivery_pedidos_usuarios[0]),
        'from_id': int(velivery_pedidos_grupos[0]),
        'command_list': ['/atrasados'],
        'bot': self.bot,
        'config': self.config,
      }
    )
    if mensagem['status']:
      self.log(log_str.cmd(mensagem['debug']))
      self.enviarMensagem([velivery_pedidos_grupos[0], grupo_debug], mensagem['response'])
      for velivery_pedidos_usuario in velivery_pedidos_usuarios:
        self.enviarMensagem([velivery_pedidos_usuario, grupo_debug], mensagem['response'])

