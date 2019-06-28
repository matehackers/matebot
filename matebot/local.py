# vim:fileencoding=utf-8
## Métodos e funções deste bot
## Escreva código aqui e pare de defenestrar o __init__.py
## TODO implementar isto no upstream
## TODO implementado no upstream!
## TODO fazer um local/__init__.py estatico e botar os demais arquivos de local/ no .gitignore
## TODO ou então usar um instance/ que nem o flask

import time, datetime, json, telepot
from matebot import comandos
from plugins.log import log_str

class local:

  def __init__(self, args):
    self.config = args['config']
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
        'chat_id': int(str(self.grupos_matehackers[0])),
        'from_id': int(str(self.grupos_matehackers[0])),
        'command_list': "/blog_matehackers",
        'command_type': 'grupo',
        'bot': self.bot,
        'config': self.config,
      }
    )
    if response['status']:
      print(log_str.cmd(response['debug']))
      try:
        self.bot.sendMessage(self.grupos_matehackers[0], str(response['response']))
      except telepot.exception.TelegramError as e:
        print(log_str.debug(e))
        pass

  def loop(self):
    try:
      time.sleep(datetime.timedelta(days=1).total_seconds())
#      self.loop_blog()
      print(u"Terminou mais um loop")
    except Exception as e: 
      print(log_str.debug(e))
      pass

