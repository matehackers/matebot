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
log_handler = {
  'critical': logging.basicConfig(
    filename='instance/critical.log',
    filemode='a',
    level=logging.CRITICAL,
  ),
  'error': logging.basicConfig(
    filename='instance/error.log',
    filemode='a',
    level=logging.ERROR,
  ),
  'warning': logging.basicConfig(
    filename='instance/warning.log',
    filemode='a',
    level=logging.WARNING,
  ),
  'info': logging.basicConfig(
    filename='instance/info.log',
    filemode='a',
    level=logging.INFO,
  ),
  'debug': logging.basicConfig(
    filename='instance/debug.log',
    filemode='a',
    level=logging.DEBUG,
  ),
  'notset': logging.basicConfig(
    filename='instance/all.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='a',
    level=logging.NOTSET,
  ),
}

### PTB
import telegram
from telegram.ext import (
  Updater,
  CommandHandler,
  MessageHandler,
  Filters,
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
bots = list()
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
  ),
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
dispatchers = list()
dispatchers.append(
  updaters[0].dispatcher,
)

from telegram.error import (
  TelegramError,
  Unauthorized,
  BadRequest,
  TimedOut,
  ChatMigrated,
  NetworkError,
)

def error_callback(update, context):
  try:
    # ~ context.bot.send_message(
      # ~ chat_id = app.config['LOG_GROUPS']['debug'],
      # ~ text = u"Tentando logar exceção...",
    # ~ )
    raise context.error
  except telegram.error.Unauthorized as e:
    # remove update.message.chat_id from conversation list
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = u"#exception #unauthorized\n\nException:\n%s\n\nUpdate:\n%s" % (
        str(e),
        str(update),
        # ~ json.dumps(
          # ~ update,
          # ~ sort_keys = True,
          # ~ indent = 2,
        # ~ ),
      # ~ ),
      ),
    )
  except telegram.error.BadRequest as e:
    # handle malformed requests - read more below!
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = u"#exception #badrequest\n\nException:\n%s\n\nUpdate:\n%s" % (
        str(e),
        str(update),
        # ~ json.dumps(
          # ~ update,
          # ~ sort_keys = True,
          # ~ indent = 2,
        # ~ ),
      # ~ ),
      ),
    )
  except telegram.error.TimedOut as e:
    # handle slow connection problems
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = u"#exception #timedout\n\nException:\n%s\n\nUpdate:\n%s" % (
        str(e),
        str(update),
        # ~ json.dumps(
          # ~ update,
          # ~ sort_keys = True,
          # ~ indent = 2,
        # ~ ),
      ),
    )
  except telegram.error.NetworkError as e:
    # handle other connection problems
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = u"#exception #networkerror\n\nException:\n%s\n\nUpdate:\n%s" % (
        str(e),
        str(update),
        # ~ json.dumps(
          # ~ update,
          # ~ sort_keys = True,
          # ~ indent = 2,
        # ~ ),
      ),
    )
  except telegram.error.ChatMigrated as e:
    # the chat_id of a group has changed, use e.new_chat_id instead
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = u"#exception #chatmigrated\n\nNew chat: %s\n\nException:\n%s\n\nUpdate:\n%s" % (
        e.new_chat_id,
        str(e),
        str(update),
        # ~ json.dumps(
          # ~ update,
          # ~ sort_keys = True,
          # ~ indent = 2,
        # ~ ),
      # ~ ),
      ),
    )
  except telegram.error.TelegramError as e:
    # handle all other telegram related errors
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = u"#exception #telegramerror\n\nException:\n%s\n\nUpdate:\n%s" % (
        str(e),
        str(update),
        # ~ json.dumps(
          # ~ update,
          # ~ sort_keys = True,
          # ~ indent = 2,
        # ~ ),
      # ~ ),
      ),
    )
  except Exception as e:
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = u"#exception #nottelegram\n\nException:\n%s" % (str(e)),
    )
  finally:
    pass
    # ~ context.bot.send_message(
      # ~ chat_id = app.config['LOG_GROUPS']['debug'],
      # ~ text = u"...não consegui.",
    # ~ )

dispatchers[0].add_error_handler(error_callback)

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

## 2020-08-25
## Plugin inútil pra converter texto em maiúsculas
def caps(update, context):
  ## Por que transformar uma lista de strings em uma string?
  text_caps = ' '.join(context.args).upper()
  context.bot.send_message(
    chat_id = update.effective_chat.id,
    text = text_caps,
  )
caps_handler = CommandHandler('caps', caps)
dispatchers[0].add_handler(caps_handler)

## TODO: Inline não está funcionando
from telegram import (
  InlineQueryResultArticle,
  InputTextMessageContent,
)
def inline_caps(update, context):
  query = update.inline_query.query
  if not query:
    return
  results = list()
  results.append(
    InlineQueryResultArticle(
      ## Quando vira tudo letra maiúscula
      id = query.upper(),
      title = 'Caps',
      input_message_content = InputTextMessageContent(query.upper())
    )
  )
  context.bot.answer_inline_query(update.inline_query.id, results)
from telegram.ext import InlineQueryHandler
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatchers[0].add_handler(inline_caps_handler)

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
## telegram.Update(update_id, message=None, edited_message=None, channel_post=None, edited_channel_post=None, inline_query=None, chosen_inline_result=None, callback_query=None, shipping_query=None, pre_checkout_query=None, poll=None, poll_answer=None, **kwargs)
def x9_callback(update, context):
  context.bot.send_message(
    chat_id = app.config['LOG_GROUPS']['debug'],
    text = json.dumps(
      str(update),
      sort_keys = True,
      indent = 2,
    ),
  )
x9_handler = MessageHandler(
  Filters.all,
  x9_callback,
)
dispatchers[0].add_handler(x9_handler)

## Tem que ser o último
def unknown(update, context):
  context.bot.send_message(
    chat_id = update.effective_chat.id,
    text = u"Vossa excelência enviardes um comando que nós não entendemos!"
  )
unknown_handler = MessageHandler(Filters.command, unknown)
dispatchers[0].add_handler(unknown_handler)

### MessageQueue (experimental!)
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
### Matebot
from matebot.ptb_matebot import views, models

updaters[0].start_polling()

### Flask Shell
@app.shell_context_processor
def make_shell_context():
  return {
    'bot': bots[0],
    'mq_bot': mq_bot,
  }
