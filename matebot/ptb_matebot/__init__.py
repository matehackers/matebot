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
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.DEBUG,
  # ~ level=logging.INFO,
)

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
  return {'bot': bots[0]}

## TODO Não lembro se vai ser pertinente manter estas linhas
# ~ def main():
  
  # ~ return 0

# ~ if __name__ == '__main__':
  # ~ main()

## TODO Código antigo

## Flask SQL Alchemy
# ~ from flask_sqlalchemy import SQLAlchemy
# ~ from flask_migrate import Migrate
# ~ db = SQLAlchemy(app)
# ~ migrate = Migrate(app, db)

## Log
## TODO não sei se funciona desta forma os logs, provavelmente somente 
##  uma destas configurações (a última?) esteja funcionando de fato.
# ~ import logging
# ~ info_handler = logging.basicConfig(
  # ~ filename='instance/info.log',
  # ~ filemode='w',
  # ~ level=logging.INFO,
# ~ )
# ~ error_handler = logging.basicConfig(
  # ~ filename='instance/error.log',
  # ~ filemode='w',
  # ~ level=logging.ERROR,
# ~ )
# ~ debug_handler = logging.basicConfig(
  # ~ filename='instance/debug.log',
  # ~ filemode='w',
  # ~ level=logging.DEBUG,
# ~ )
# ~ warning_handler = logging.basicConfig(
  # ~ filename='instance/warning.log',
  # ~ filemode='w',
  # ~ level=logging.WARN,
# ~ )
# ~ from plugins.tenable_logs import LogSetup
# ~ app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "stream")
# ~ app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")
# File Logging Setup
# app.config['LOG_DIR'] = os.environ.get("LOG_DIR", "./")
# app.config['APP_LOG_NAME'] = os.environ.get("APP_LOG_NAME", "app.log")
# app.config['WWW_LOG_NAME'] = os.environ.get("WWW_LOG_NAME", "www.log")
# ~ app.config['LOG_MAX_BYTES'] = os.environ.get(
  # ~ "LOG_MAX_BYTES",
  # ~ 100_000_000
# ~ )  # 100MB in bytes
# app.config['LOG_COPIES'] = os.environ.get("LOG_COPIES", 5)
# ~ if __name__ != '__main__':
  # ~ gunicorn_logger = logging.getLogger('gunicorn.error')
  # ~ app.logger.handlers = gunicorn_logger.handlers
  # ~ app.logger.setLevel(gunicorn_logger.level)

# ~ logs = LogSetup()
# ~ logs.init_app(app)

## Blueprints
## API
## TODO API deve ser utilizada programaticamente como API propriamente 
## dita, ainda há trabalho a ser feito para se tornar uma API de fato.
#from blueprints.api import bp as api_bp
#app.register_blueprint(api_bp, url_prefix="/api")
## Web
# ~ from blueprints.web import bp as web_bp
# ~ app.register_blueprint(web_bp, url_prefix="/web")

## Index
# ~ @app.route("/")
# ~ def index():
  # ~ app.logger.debug('this is a DEBUG message')
  # ~ app.logger.info('this is an INFO message')
  # ~ app.logger.warning('this is a WARNING message')
  # ~ app.logger.error('this is an ERROR message')
  # ~ app.logger.critical('this is a CRITICAL message')
  # ~ return u"MateBot"
