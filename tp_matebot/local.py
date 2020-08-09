# vim:fileencoding=utf-8
## Métodos e funções deste bot
## Escreva código aqui e pare de defenestrar o __init__.py
## TODO implementar isto no upstream
## TODO implementado no upstream!
## TODO fazer um local/__init__.py estatico e botar os demais arquivos de local/ no .gitignore
## TODO ou então usar um instance/ que nem o flask

import time, datetime, json, telepot, curses
from curses import wrapper
from tp_matebot import comandos
from plugins.log import log_str
from plugins.totalvoice import shiva_1

class local:

  def __init__(self, args):
    self.config = args['config']
    if 'bot' in args.keys():
      self.bot = args['bot']
    self.grupos_local = json.loads(self.config.get("plugins_grupos", "local"))
    self.usuarios_local = json.loads(self.config.get("plugins_usuarios", "local"))
    self.grupos_debug = json.loads(self.config['plugins_grupos']['admin'])
    self.usuarios_debug = json.loads(self.config['plugins_usuarios']['admin'])

  ## Verifica se tem uma publicação nova no blog e envia para o grupo de telegram
  ## Na verdade não existe este comando, mas se alguém escrever o código, poderia existir!
  ## Este é só um exemplo de como o MateBot pode ou poderia fazer ações automáticas
  def loop_blog(self):
    time.sleep(0.001)
    response = comandos.parse(
      {
        'chat_id': int(str(self.grupos_local[0])),
        'from_id': int(str(self.grupos_local[0])),
        'command_list': "/cmd_blog_matehackers",
        'command_type': 'grupo',
        'bot': self.bot,
        'config': self.config,
      }
    )
    if response['status']:
      print(log_str.cmd(response['debug']))
      try:
        self.bot.sendMessage(self.grupos_local[0], str(response['response']))
      except telepot.exception.TelegramError as e:
        print(log_str.debug(e))
        pass

  def loop_pendentes(self):
    time.sleep(0.001)
    response = comandos.parse(
      {
        'chat_id': int(str(self.usuarios_local[0])),
        'from_id': int(str(self.usuarios_local[0])),
        'command_list': "/pendentes",
        'command_type': 'grupo',
        'bot': self.bot,
        'config': self.config,
      }
    )
    if response['status']:
      print(log_str.cmd(response['debug']))
#      for grupo_local in self.grupos_local:
#        self.enviarMensagem([grupo_local, grupos_debug[0]], response['response'], response['parse_mode'])
#      for grupo_local in grupos_local:
#        self.enviarMensagem([grupo_local, grupos_debug[0]], response['response'], response['parse_mode'])
      try:
        self.bot.sendMessage(self.grupos_local[0], str(response['response']))
      except telepot.exception.TelegramError as e:
        print(log_str.debug(e))
        pass

  def loop_husky(self):
    time.sleep(0.001)
    response = comandos.parse(
      {
        'chat_id': int(str(self.grupos_local[0])),
        'from_id': int(str(self.grupos_local[0])),
        'command_list': "/husky_pendentes",
        'command_type': 'grupo',
        'bot': self.bot,
        'config': self.config,
      }
    )
    if response['status']:
      print(log_str.cmd(response['debug']))
      try:
#        self.bot.sendMessage(self.usuarios_local[0], str(response['response']))
#        self.bot.sendMessage(self.grupos_local[0], str(response['response']))
        self.bot.sendMessage(self.grupos_local[0], str(response['response']))
        shiva_1({
          'numero': self.config['agenda']['numero_3'],
          'config': self.config,
          'bot': self.bot,
          'telefones': response['response']['telefones'],
        })
      except telepot.exception.TelegramError as e:
        print(log_str.debug(e))
        pass

  def loop_atrasados(self):
    time.sleep(0.001)
    response = comandos.parse(
      {
        'chat_id': int(str(self.usuarios_local[0])),
        'from_id': int(str(self.usuarios_local[0])),
        'command_list': "/atrasados",
        'command_type': 'grupo',
        'bot': self.bot,
        'config': self.config,
      }
    )
    if response['status']:
      print(log_str.cmd(response['debug']))
      try:
        self.bot.sendMessage(self.grupos_local[0], str(response['response']))
      except telepot.exception.TelegramError as e:
        print(log_str.debug(e))
        pass

#  def cli_wrapper(self, stdscr):
#    stdscr.clear()
#    stdscr.refresh()
#    stdscr.getkey()

  def loop_cli(self, stdscr):
#    wrapper(cli_wrapper)
    stdscr.addstr(u"Enviar (c)omando\tEscrever (v)elivery\t(s)air: ")
    while True:
      cmd = stdscr.getch()
      if cmd == ord('c'):
        stdscr.clear()
        stdscr.refresh()
        stdscr.addstr(u"Digite o comando (vazio para cancelar): ")
        command_list = stdscr.getstr(1, 0, 140)
        if command_list != "":
          time.sleep(0.001)
          response = comandos.parse(
            {
              'chat_id': int(str(self.usuarios_debug[0])),
              'from_id': int(str(self.usuarios_debug[0])),
              'command_list': str(command_list.decode('utf-8')),
              'command_type': "curses",
              'config': self.config,
              'stdscr': stdscr,
            }
          )
          if response['status']:
            stdscr.addstr(log_str.cmd(u"%s\n" % (response['debug'])))
            try:
              stdscr.addstr(u"%s\n" % (': '.join([str(self.usuarios_debug[0]), str(response['response'])])))
            except Exception as e:
              stdscr.addstr(u"%s\n" % (log_str.debug(e)))
          else:
            try:
              stdscr.addstr(u"%s\n" % (': '.join([str(self.usuarios_debug[0]), str(response['response'])])))
              stdscr.addstr(u"%s\n" % (': '.join([u"Debug", str(response['debug'])])))
            except Exception as e:
              stdscr.addstr(u"%s\n" % (log_str.debug(e)))
          stdscr.refresh()
        else:
          pass
        return 0
      elif cmd == ord('v'):
        stdscr.addstr(u"\nVelivery")
        return 0
      elif cmd == ord('s'):
        stdscr.addstr(u"\nTchau!")
        stdscr.refresh()
        time.sleep(1)
        return 1
      else:
        pass

  def loop_automatico(self):
    
    time.sleep(datetime.timedelta(minutes=3).total_seconds())

  def loop(self):
    try:
      time.sleep(datetime.timedelta(days=1).total_seconds())
#      time.sleep(datetime.timedelta(minutes=30).total_seconds())
#      time.sleep(datetime.timedelta(minutes=4).total_seconds())
#      time.sleep(datetime.timedelta(minutes=3).total_seconds())
      print(u"Terminou mais um loop")
#      print(log_str.info("3 minutos se passaram"))
#      self.loop_blog()
#      self.loop_husky()
#      self.loop_pendentes()
#      self.loop_atrasados()
#      self.loop_automatico()
#      pass
    except Exception as e: 
      print(log_str.debug(e))
      pass

