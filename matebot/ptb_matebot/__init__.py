#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Matebot
#  
#  Copyleft 2012-2020 Iuri Guilherme <https://github.com/iuriguilherme>,
#     Matehackers <https://github.com/matehackers>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os

### Flask
from flask import Flask
app = Flask(__name__, instance_relative_config = True)
try:
  ## Por padrão ./instance/config.py que deve estar ignorado pelo 
  ## .gitignore. Copiar ./default_config.py para ./instance/config.py 
  ## antes de rodar o flask.
  ## TODO hardcoding 'instance.config.developmentConfig' doesn't seem right
  app.config.from_object('doc.default_config.Config')
  app.config.from_object('.'.join([
    'instance',
    'config',
    ''.join([os.environ['FLASK_ENV'], 'Config']),
  ]))
except Exception as e:
  print(u"Arquivo de configuração não encontrado. Exceção: %s" % (e))
  raise

### Logging
## TODO issue 44 - mandar log para os grupos
import logging
logging.basicConfig(
  # ~ filename='instance/ptb_matebot.log',
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  # ~ filemode='w',
  level=logging.INFO,
)

### PTB
import telegram
from telegram.ext import (
  Updater,
)

### Terça Sem Fim
# ~ telegram.Bot(
  # ~ token,
  # ~ base_url=None,
  # ~ base_file_url=None,
  # ~ request=None,
  # ~ private_key=None,
  # ~ private_key_password=None,
  # ~ defaults=None
# ~ )
## TODO suporte para múltiplos bots?
##  É simples quanto instanciar novos telegram.Bot, um com cada token
## TODO Alterar o sistema de confgiuração para lista de tokens, cada usuário
##  do telegram consegue criar até 20 bots.
# ~ bots = list()
# ~ bots.append(
  # ~ telegram.Bot(
    # ~ token = app.config['BOTFATHER']['token'],
  # ~ ),
# ~ )
# ~ for token in app.config['BOTFATHER']['tokens']:
  # ~ bots.append(telegram.Bot(token = token))

# ~ telegram.ext.Updater(
  # ~ token=None,
  # ~ base_url=None,
  # ~ workers=4,
  # ~ bot=None,
  # ~ private_key=None,
  # ~ private_key_password=None,
  # ~ user_sig_handler=None,
  # ~ request_kwargs=None,
  # ~ persistence=None,
  # ~ defaults=None,
  # ~ dispatcher=None,
  # ~ base_file_url=None
# ~ )
updaters = list()
## @matehackers_devbot
updaters.append(
  Updater(
    token = app.config['BOTFATHER']['token'],
    use_context = True,
  )
)
# ~ updaters.append(
  # ~ Updater(
    # ~ bot = bots[0],
    # ~ use_context = True,
  # ~ ),
# ~ )

# ~ telegram.ext.Dispatcher(
  # ~ bot,
  # ~ update_queue,
  # ~ workers=4,
  # ~ exception_event=None,
  # ~ job_queue=None,
  # ~ persistence=None,
# ~ )
# ~ dispatchers = list()
# ~ dispatchers.append(
  # ~ updaters[0].dispatcher,
# ~ )

## Reinicia todos bots
# ~ for updater in updaters:
  # ~ try:
    # ~ updater.stop()
  # ~ except Exception as e:
    # ~ print(str(e))
  # ~ updater.start_polling()

## TODO Blueprints
### Matebot
from matebot.ptb_matebot import views, models, controllers

### Flask Shell
@app.shell_context_processor
def make_shell_context():
  return {
    'bot': updaters[0].bot,
    # ~ 'mq_bot': mq_bot,
  }


### MessageQueue (experimental!)
# ~ import telegram.bot
# ~ from telegram.ext import (
  # ~ messagequeue as mq,
# ~ )
# ~ from telegram.utils.request import(
  # ~ Request,
# ~ )
# ~ class MQBot(telegram.bot.Bot):
  # ~ '''A subclass of Bot which delegates send method handling to MQ'''
  # ~ def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
    # ~ super(MQBot, self).__init__(*args, **kwargs)
    # ~ # below 2 attributes should be provided for decorator usage
    # ~ self._is_messages_queued_default = is_queued_def
    # ~ self._msg_queue = mqueue or mq.MessageQueue()
  # ~ def __del__(self):
    # ~ try:
      # ~ self._msg_queue.stop()
    # ~ except:
      # ~ pass
  # ~ @mq.queuedmessage
  # ~ def send_message(self, *args, **kwargs):
    # ~ '''Wrapped method would accept new `queued` and `isgroup`
    # ~ OPTIONAL arguments'''
    # ~ return super(MQBot, self).send_message(*args, **kwargs)
# ~ # for test purposes limit global throughput to 3 messages per 3 seconds
# ~ q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
# ~ # set connection pool size for bot 
# ~ mq_request = Request(con_pool_size=8)
# ~ mq_bot = MQBot(
  # ~ token = app.config['BOTFATHER']['token'],
  # ~ request = mq_request,
  # ~ mqueue = q,
# ~ )
# ~ mq_updater = telegram.ext.updater.Updater(
  # ~ bot = mq_bot,
  # ~ use_context = True
# ~ )

# ~ print(updaters)
# ~ print(updaters[0])
