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

## Flask
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

## Logging
## TODO issue 44 - mandar log para os grupos
import logging
log_handler = {
  'notset': logging.basicConfig(
    filename='instance/all.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='a',
    level=logging.NOTSET,
  ),
  'debug': logging.basicConfig(
    filename='instance/debug.log',
    filemode='a',
    level=logging.DEBUG,
  ),
  'info': logging.basicConfig(
    filename='instance/info.log',
    filemode='a',
    level=logging.INFO,
  ),
  'warning': logging.basicConfig(
    filename='instance/warning.log',
    filemode='a',
    level=logging.WARNING,
  ),
  'error': logging.basicConfig(
    filename='instance/error.log',
    filemode='a',
    level=logging.ERROR,
  ),
  'critical': logging.basicConfig(
    filename='instance/critical.log',
    filemode='a',
    level=logging.CRITICAL,
  ),
}

## PTB
import telegram
from telegram.ext import (
  Updater,
  CommandHandler,
  MessageHandler,
  Filters,
)

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
bots = list()
bots.append(
  telegram.Bot(
    token = app.config['BOTFATHER']['token'],
  ),
)
for token in app.config['BOTFATHER']['tokens']:
  bots.append(telegram.Bot(token = token))

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
updaters.append(
  Updater(
    bot = bots[0],
    use_context = True,
  ),
)

# ~ telegram.ext.Dispatcher(
  # ~ bot,
  # ~ update_queue,
  # ~ workers=4,
  # ~ exception_event=None,
  # ~ job_queue=None,
  # ~ persistence=None,
# ~ )
dispatchers = list()
dispatchers.append(
  updaters[0].dispatcher,
)

## By default the handler listens to messages as well as edited messages. To 
##  change this behavior use ~Filters.update.edited_message in the filter 
##  argument.
# ~ telegram.ext.CommandHandler(
  # ~ command,
  # ~ callback,
  # ~ filters = None,
# ~ )
def start(update, context):
  context.bot.send_message(
    chat_id = update.effective_chat.id,
    text = "I'm a bot, please talk to me!",
  )
start_handler = CommandHandler('start', start)
dispatchers[0].add_handler(start_handler)

# ~ telegram.ext.MessageHandler(
  # ~ filters,
  # ~ callback,
  # ~ pass_update_queue = False,
  # ~ pass_job_queue = False,
  # ~ pass_user_data = False,
  # ~ pass_chat_data = False,
  # ~ message_updates = None,
  # ~ channel_post_updates = None,
  # ~ edited_updates = None
# ~ )
def echo(update, context):
  context.bot.send_message(
    chat_id = update.effective_chat.id,
    text = update.message.text,
  )
echo_handler = MessageHandler(
  Filters.text & (~Filters.command),
  echo,
)
dispatchers[0].add_handler(echo_handler)

updaters[0].start_polling()

## MessageQueue (experimental!)
import telegram.bot
from telegram.ext import (
  messagequeue as mq,
)
from telegram.utils.request import(
  Request,
)
class MQBot(telegram.bot.Bot):
  '''A subclass of Bot which delegates send method handling to MQ'''
  def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
    super(MQBot, self).__init__(*args, **kwargs)
    # below 2 attributes should be provided for decorator usage
    self._is_messages_queued_default = is_queued_def
    self._msg_queue = mqueue or mq.MessageQueue()
  def __del__(self):
    try:
      self._msg_queue.stop()
    except:
      pass
  @mq.queuedmessage
  def send_message(self, *args, **kwargs):
    '''Wrapped method would accept new `queued` and `isgroup`
    OPTIONAL arguments'''
    return super(MQBot, self).send_message(*args, **kwargs)
# for test purposes limit global throughput to 3 messages per 3 seconds
q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
# set connection pool size for bot 
mq_request = Request(con_pool_size=8)
mq_bot = MQBot(
  token = app.config['BOTFATHER']['token'],
  request = mq_request,
  mqueue = q,
)
mq_updater = telegram.ext.updater.Updater(
  bot = mq_bot,
  use_context = True
)

## TODO Blueprints
## Matebot
from matebot.ptb_matebot import views, models

## flask shell
@app.shell_context_processor
def make_shell_context():
  return {
    'bot': bots[0],
    'mq_bot': mq_bot,
  }
