#!/usr/bin/env python
# vim:fileencoding=utf-8
## If `./start.py` doesn't work for you, try `python3 start.py`.
## Sugerido rodar com `pipenv run python start.py flask matebot`

import subprocess, sys

from matebot.tp_matebot import bot as telepot_bot

if __name__ == "__main__":
  #mode = 'telepot'
  mode = 'flask'
  ## Este é o arquivo instance/.matebot.config.py
  config_file = 'matebot'
  ## TODO fazer validação de verdade
  if len(sys.argv) > 1:
    mode = sys.argv[1]
    print(u"Modo de operação: %s" % (mode))
    if len(sys.argv) > 2:
      config_file = sys.argv[2]
      print(
        u"Usando arquivo de configuração instance/.%s.config.py"
        % (config_file)
      )
    else:
      print(
        u"Arquivo de configuração não informado, instance/.%s.config.py \
        presumido"
        % (config_file)
      )
  else:
    print(u"Modo de operação não informado, %s presumido." % (mode))
    print(
      u"Arquivo de configuração não informado, instance/.%s.config.py presumido"
      % (config_file)
    )
  if mode == 'flask':
    subprocess.run(['pipenv', 'run', 'flask', 'run'])
  elif mode == 'telepot':
    telepot_bot(mode, config_file)
  else:
    print(u"Not sure what to do. RTFM. Exiting.")
