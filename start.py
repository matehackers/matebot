#!/usr/bin/env python
# vim:fileencoding=utf-8
## If `./start.py` doesn't work for you, try `python3 start.py`.
## Sugerido rodar com `pipenv run python start.py aiogram matebot`

import subprocess, sys

from matebot.tp_matebot import bot as telepot_bot
from matebot.ptb_matebot import app as flask_bot
from matebot.aio_matebot import run as aiogram_bot

if __name__ == "__main__":
  mode = 'aiogram'
  bot = 'matebot'
  ## TODO fazer validação de verdade
  if len(sys.argv) > 1:
    mode = sys.argv[1]
    print(u"Modo de operação: %s" % (mode))
    if len(sys.argv) > 2:
      bot = sys.argv[2]
      print(
        u"Usando token do bot \"{}\" do arquivo de configuração.\
          ".format(bot)
      )
    else:
      print(u"Nome do bot não informado, {} presumido".format(bot))
  else:
    print(u"Modo de operação não informado, {} presumido.".format(mode))
    print(u"Nome do bot não informado, {} presumido".format(bot))
  if mode == 'aiogram':
    aiogram_bot(bot)
  elif mode == 'flask':
    flask_bot.run()
  elif mode == 'telepot':
    telepot_bot(mode, bot)
  else:
    print(u"Not sure what to do. RTFM. Exiting.")
