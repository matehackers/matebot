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

import os

### Flask
from flask import Flask
app = Flask(__name__, instance_relative_config = True)
# ~ try:
  # ~ ## Por padrão ./instance/config.py que deve estar ignorado pelo 
  # ~ ## .gitignore. Copiar ./default_config.py para ./instance/config.py 
  # ~ ## antes de rodar o flask.
  # ~ ## TODO hardcoding 'instance.config.developmentConfig' doesn't seem right
  # ~ try:
    # ~ app.config.from_object('.'.join([
      # ~ 'instance',
      # ~ 'config',
      # ~ ''.join([os.environ['FLASK_ENV'], 'Config']),
    # ~ ]))
  # ~ except Exception as e:
    # ~ print(u"Arquivo de configuração não encontrado. Exceção: %s" % (e))
    # ~ try:
      # ~ app.config.from_object('.'.join([
        # ~ 'instance',
        # ~ 'config',
        # ~ 'Config',
      # ~ ]))
    # ~ except Exception as e:
      # ~ print(u"Arquivo de configuração não encontrado. Exceção: %s" % (e))
      # ~ try:
        # ~ app.config.from_object('doc.default_config.Config')
      # ~ except Exception as e:
        # ~ print(u"Arquivo de configuração não encontrado. Exceção: %s" % (e))
  # ~ try:
    # ~ from instance.config import Config
    # ~ config = Config()
  # ~ except Exception as e:
    # ~ print(u"Arquivo de configuração não encontrado. Exceção: %s" % (e))
# ~ except Exception as e:
  # ~ print(u"Arquivo de configuração não encontrado. Exceção: %s" % (e))
  # ~ raise

from instance.config import Config
config = Config()

### PTB
## https://github.com/python-telegram-bot/python-telegram-bot/wiki
import telegram
from telegram.bot import (
  Bot,
)
from telegram.ext import (
  Updater,
  MessageHandler,
  Filters,
  messagequeue as mq,
)
from telegram.utils.request import (
  Request,
)
from telegram.error import (
  TelegramError,
  Unauthorized,
  BadRequest,
  TimedOut,
  ChatMigrated,
  NetworkError,
)

from matebot.ptb_matebot.controllers.callbacks.error import (
  error_callback,
  exception_callback,
)

### Terça Sem Fim

### MQ
## https://github.com/python-telegram-bot/python-telegram-bot/wiki/Avoiding-flood-limits
class MQBot(Bot):
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
    try:
      return super(MQBot, self).send_message(*args, **kwargs)
    except Unauthorized as e:
      # remove update.message.chat_id from conversation list
      text = list()
      text.append('#exception #unauthorized')
      text.append(u"Exception:\n%s" % (str(e)))
      self.send_message(
        chat_id = config.groups['admin']['debug'],
        text = '\n\n'.join(text),
        isgroup = True,
        queued = True,
      )
    except BadRequest as e:
      # handle malformed requests - read more below!
      text = list()
      text.append('#exception #badrequest')
      text.append(u"Exception:\n%s" % (str(e)))
      self.send_message(
        chat_id = config.groups['admin']['debug'],
        text = '\n\n'.join(text),
        isgroup = True,
        queued = True,
      )
    except TimedOut as e:
      # handle slow connection problems
      text = list()
      text.append('#exception #timedout')
      text.append(u"Exception:\n%s" % (str(e)))
      self.send_message(
        chat_id = config.groups['admin']['debug'],
        text = '\n\n'.join(text),
        isgroup = True,
        queued = True,
      )
    except NetworkError as e:
      # handle other connection problems
      text = list()
      text.append('#exception #networkerror')
      text.append(u"Exception:\n%s" % (str(e)))
      self.send_message(
        chat_id = config.groups['admin']['debug'],
        text = '\n\n'.join(text),
        isgroup = True,
        queued = True,
      )
    except ChatMigrated as e:
      # the chat_id of a group has changed, use e.new_chat_id instead
      text = list()
      text.append('#exception #chatmigrated')
      text.append(u"New chat: %s" % (str(e.new_chat_id)))
      text.append(u"Exception:\n%s" % (str(e)))
      self.send_message(
        chat_id = config.groups['admin']['debug'],
        text = '\n\n'.join(text),
        isgroup = True,
        queued = True,
      )
    except TelegramError as e:
      # handle all other telegram related errors
      text = list()
      text.append('#exception #telegramerror')
      text.append(u"Exception:\n%s" % (str(e)))
      self.send_message(
        chat_id = config.groups['admin']['debug'],
        text = '\n\n'.join(text),
        isgroup = True,
        queued = True,
      )
    except Exception as e:
      text = list()
      text.append('#exception #notetelegram')
      text.append(u"Exception:\n%s" % (str(e)))
      self.send_message(
        chat_id = config.groups['admin']['debug'],
        text = '\n\n'.join(text),
        isgroup = True,
        queued = True,
      )
# for test purposes limit global throughput to 3 messages per 3 seconds
q = mq.MessageQueue(
  all_burst_limit = 3,
  all_time_limit_ms = 3000,
  exc_route = exception_callback,
)
# set connection pool size for bot 
request = Request(con_pool_size=8)
testbot = MQBot(
  config.bots[os.environ['FLASK_ENV']]['token'],
  request = request,
  mqueue = q,
)
setattr(testbot, 'info', config.bots[os.environ['FLASK_ENV']]['info'])
setattr(testbot, 'users', config.bots[os.environ['FLASK_ENV']]['users'])
setattr(testbot, 'plugins', config.bots[os.environ['FLASK_ENV']]['plugins'])
upd = Updater(bot = testbot, use_context=True)
upd.dispatcher.add_error_handler(error_callback)

# ~ def reply(update, context):
  # ~ # tries to echo 10 msgs at once
  # ~ chatid = update.message.chat_id
  # ~ msgt = update.message.text
  # ~ print(msgt, chatid)
  # ~ for ix in range(10):
    # ~ context.bot.send_message(chat_id=chatid, text='%s) %s' % (ix + 1, msgt))
# ~ hdl = MessageHandler(Filters.text, reply)
# ~ upd.dispatcher.add_handler(hdl)
# ~ upd.start_polling()

### Updaters

## Updater
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

## Usar token diretamente
# ~ updaters.append(
  # ~ Updater(
    # ~ token = app.config['BOTFATHER']['token'],
    # ~ use_context = True,
  # ~ )
# ~ )

## Usar bot pré instanciado
# ~ updaters.append(
  # ~ Updater(
    # ~ bot = bots[0],
    # ~ use_context = True,
  # ~ ),
# ~ )

## Usar MQbot
updaters.append(upd)

### PTB Matebot
from matebot.ptb_matebot import (
  models,
  views,
  controllers,
)

from matebot.ptb_matebot.controllers import (
  add_handlers,
  add_jobqueues,
)
add_handlers.all()
add_jobqueues.all()

### Flask Shell
@app.shell_context_processor
def make_shell_context():
  return {
    'bot': updaters[0].bot,
  }

### Procastinação: Código que eu esqueci de apagar ou que não era pra ter 
###   comentado

## Reinicia todos bots
# ~ for updater in updaters:
  # ~ try:
    # ~ updater.stop()
  # ~ except Exception as e:
    # ~ print(str(e))
  # ~ updater.start_polling()

### Logging
## TODO issue 44 - mandar log para os grupos # NÃO É A 44!
# ~ import logging
# ~ logging.basicConfig(
  # ~ filename='instance/ptb_matebot.log',
  # ~ format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  # ~ filemode='w',
  # ~ level=logging.INFO,
# ~ )

## Dispatcher
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

## Bot
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

## Adicionar toda a lista de tokens
# ~ for token in app.config['BOTFATHER']['tokens']:
  # ~ bots.append(telegram.Bot(token = token))

## Adicionar só um bot
# ~ bots.append(
  # ~ telegram.Bot(
    # ~ token = app.config['BOTFATHER']['token'],
  # ~ ),
# ~ )

## Usar MQbot
# ~ bots.append(testbot)
