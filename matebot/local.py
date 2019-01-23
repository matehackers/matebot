# vim:fileencoding=utf-8
## Métodos e funções deste bot
## Escreva código aqui e pare de defenestrar o __init__.py
## TODO implementar isto no upstream
## TODO fazer um local/__init__.py estatico e botar os demais arquivos de local/ no .gitignore

import time, datetime, json, telepot, curses
from curses import wrapper
from matebot import comandos
from plugins.log import log_str
from plugins.totalvoice import shiva_1

class local:

  def __init__(self, args):
    self.config = args['config']
    if 'bot' in args.keys():
      self.bot = args['bot']
    self.velivery_pedidos_grupos = json.loads(self.config.get("plugins_grupos", "velivery_pedidos"))
    self.velivery_pedidos_usuarios = json.loads(self.config.get("plugins_usuarios", "velivery_pedidos"))
    self.grupos_debug = json.loads(self.config.get("plugins_grupos", "admin"))
    self.usuarios_debug = json.loads(self.config.get("plugins_usuarios", "admin"))

  def loop_pendentes(self):
    time.sleep(0.001)
    response = comandos.parse(
      {
        'chat_id': int(str(self.velivery_pedidos_usuarios[0])),
        'from_id': int(str(self.velivery_pedidos_usuarios[0])),
        'command_list': "/pendentes",
        'command_type': 'grupo',
        'bot': self.bot,
        'config': self.config,
      }
    )
    if response['status']:
      print(log_str.cmd(response['debug']))
#      for velivery_pedidos_grupo in self.velivery_pedidos_grupos:
#        self.enviarMensagem([velivery_pedidos_grupo, grupos_debug[0]], response['response'], response['parse_mode'])
#      for velivery_pedidos_usuario in velivery_pedidos_usuarios:
#        self.enviarMensagem([velivery_pedidos_usuario, grupos_debug[0]], response['response'], response['parse_mode'])
      try:
        self.bot.sendMessage(self.velivery_pedidos_grupos[0], str(response['response']))
      except telepot.exception.TelegramError as e:
        print(log_str.debug(e))
        pass

  def loop_husky(self):
    time.sleep(0.001)
    response = comandos.parse(
      {
        'chat_id': int(str(self.velivery_pedidos_grupos[0])),
        'from_id': int(str(self.velivery_pedidos_grupos[0])),
        'command_list': "/husky_pendentes",
        'command_type': 'grupo',
        'bot': self.bot,
        'config': self.config,
      }
    )
    if response['status']:
      print(log_str.cmd(response['debug']))
      try:
#        self.bot.sendMessage(self.velivery_pedidos_usuarios[0], str(response['response']))
        self.bot.sendMessage(self.velivery_pedidos_grupos[0], str(response['response']))
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
        'chat_id': int(str(self.velivery_pedidos_usuarios[0])),
        'from_id': int(str(self.velivery_pedidos_usuarios[0])),
        'command_list': "/atrasados",
        'command_type': 'grupo',
        'bot': self.bot,
        'config': self.config,
      }
    )
    if response['status']:
      print(log_str.cmd(response['debug']))
      try:
        self.bot.sendMessage(self.velivery_pedidos_grupos[0], str(response['response']))
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
#    time.sleep(datetime.timedelta(minutes=30).total_seconds())
#    time.sleep(datetime.timedelta(minutes=4).total_seconds())
#    time.sleep(datetime.timedelta(minutes=3).total_seconds())
#    self.loop_husky()
#    self.loop_pendentes()
#    self.loop_atrasados()
    self.loop_automatico()
#    print(log_str.info("3 minutos se passaram"))
#    pass

