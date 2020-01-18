#!/usr/bin/env python
# vim:fileencoding=utf-8
## If `./start.py` doesn't work for you, try `python3 start.py`.
## Sugerido rodar com `pipenv run python start.py telepot matebot`

import sys

from matebot import bot

if __name__ == "__main__":
  mode = 'telepot'
  ## Este é o arquivo config/.matebot.cfg
  config_file = 'matebot'
  ## TODO fazer validação de verdade
  if len(sys.argv) > 1:
    mode = sys.argv[1]
    print(u"Modo de operação: %s" % (mode))
    if len(sys.argv) > 2:
      config_file = sys.argv[2]
      print(
        u"Usando arquivo de configuração instance/.%s.cfg"
        % (config_file)
      )
    else:
      print(
        u"Arquivo de configuração não informado, instance/.%s.cfg \
        presumido"
        % (config_file)
      )
  else:
    print(u"Modo de operação não informado, %s presumido." % (mode))
    print(
      u"Arquivo de configuração não informado, config/.%s.cfg presumido"
      % (config_file)
    )
  bot(mode, config_file)

