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

import datetime, json, locale, pytz, random

here = pytz.timezone('America/Sao_Paulo')
here_and_now = datetime.datetime.now(here)
locale.setlocale(locale.LC_ALL, 'pt_BR')

from matebot.ptb_matebot import (
  app,
  updaters,
)

import telegram

from telegram.ext import (
  Updater,
  CommandHandler,
  MessageHandler,
  Filters,
)

from telegram.error import (
  TelegramError,
  Unauthorized,
  BadRequest,
  TimedOut,
  ChatMigrated,
  NetworkError,
)

## Formatação da exceção
def update_text(update, text):
  text.append(
    u"Update %s:\n%s" % (
      str(update.update_id),
      json.dumps(
        {
          k:v for (k,v) in
          update.effective_message.__dict__.items()
          if v not in [
            None,
            [],
            '',
            False,
          ]
          and k not in [
            "_id_attrs",
            "bot",
            "chat",
            "from_user",
          ]
        },
        sort_keys = True,
        indent = 2,
        default = str,
      ),
    )
  )
  text.append(
    u"Chat:\n%s" % (
      json.dumps(
        {
          k:v for (k,v) in
          update.effective_chat.__dict__.items()
          if v not in [
            None,
            [],
            '',
            False,
          ]
          and k not in [
            "_id_attrs",
            "bot",
          ]
        },
        sort_keys = True,
        indent = 2,
        default = str,
      ),
    )
  )
  text.append(
    u"User:\n%s" % (
      json.dumps(
        {
          k:v for (k,v) in
          update.effective_user.__dict__.items()
          if v not in [
            None,
            [],
            '',
            False,
          ]
          and k not in [
            "_id_attrs",
            "bot",
          ]
        },
        sort_keys = True,
        indent = 2,
        default = str,
      ),
    )
  )

def error_callback(update, context):
  try:
    raise context.error
  except telegram.error.Unauthorized as e:
    # remove update.message.chat_id from conversation list
    text = list()
    text.append('#exception #unauthorized')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except telegram.error.BadRequest as e:
    # handle malformed requests - read more below!
    text = list()
    text.append('#exception #badrequest')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except telegram.error.TimedOut as e:
    # handle slow connection problems
    text = list()
    text.append('#exception #timedout')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except telegram.error.NetworkError as e:
    # handle other connection problems
    text = list()
    text.append('#exception #networkerror')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except telegram.error.ChatMigrated as e:
    # the chat_id of a group has changed, use e.new_chat_id instead
    text = list()
    text.append('#exception #chatmigrated')
    text.append(u"New chat: %s" % (str(e.new_chat_id)))
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except telegram.error.TelegramError as e:
    # handle all other telegram related errors
    text = list()
    text.append('#exception #telegramerror')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  except Exception as e:
    text = list()
    text.append('#exception #notetelegram')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
    )
  finally:
    context.bot.send_message(
      text = u"Tive um problema mas já avisei o pessoal que cuida do desenvolvimento.",
      chat_id = update.effective_chat.id,
      reply_to_message_id = update.effective_message.message_id,
    )
updaters[0].dispatcher.add_error_handler(error_callback)

def start(update, context):
  context.bot.send_message(
    chat_id = update.effective_chat.id,
    text = u"Oi oi oi me use me use", # lalenia
  )
start_handler = CommandHandler('start', start)
updaters[0].dispatcher.add_handler(start_handler)

## Papagaio
# ~ def echo(update, context):
  # ~ context.bot.send_message(
    # ~ chat_id = update.effective_chat.id,
    # ~ text = update.message.text,
  # ~ )
# ~ echo_handler = MessageHandler(
  # ~ Filters.text & (~Filters.command),
  # ~ echo,
# ~ )
# ~ updaters[0].dispatcher.add_handler(echo_handler)

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
updaters[0].dispatcher.add_handler(caps_handler)

## TODO: Inline não está funcionando
# ~ from telegram import (
  # ~ InlineQueryResultArticle,
  # ~ InputTextMessageContent,
# ~ )
# ~ def inline_caps(update, context):
  # ~ query = update.inline_query.query
  # ~ if not query:
    # ~ return
  # ~ results = list()
  # ~ results.append(
    # ~ InlineQueryResultArticle(
      # ~ ## Quando vira tudo letra maiúscula
      # ~ id = query.upper(),
      # ~ title = 'Caps',
      # ~ input_message_content = InputTextMessageContent(query.upper())
    # ~ )
  # ~ )
  # ~ context.bot.answer_inline_query(update.inline_query.id, results)
# ~ from telegram.ext import InlineQueryHandler
# ~ inline_caps_handler = InlineQueryHandler(inline_caps)
# ~ updaters[0].dispatcher.add_handler(inline_caps_handler)

## Manda todos updates pro CAOS
def x9_callback(update, context):
  text = list()
  if update:
    update_text(update,text)
  context.bot.send_message(
    chat_id = app.config['LOG_GROUPS']['caos'],
    text = '\n\n'.join(text),
  )
x9_handler = MessageHandler(
  Filters.all,
  x9_callback,
)
updaters[0].dispatcher.add_handler(x9_handler)

### 2020-08-29
## Testando com job queue
## https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.jobqueue.html
## run_repeating
# ~ def callback_minute(context: telegram.ext.CallbackContext):
  # ~ context.bot.send_message(
    # ~ chat_id = app.config['LOG_GROUPS']['info'],
    # ~ text = '...e nos dezoito segundos seguintes...',
  # ~ )
# ~ updaters[0].job_queue.run_repeating(
  # ~ callback_minute,
  # ~ interval=18,
  # ~ first=datetime.datetime.utcnow(),
# ~ )
def hourly(context):
  texto = random.choice([
    u"É hora de lanchar",
    u"É hora de alegria",
    u"Toda hora isso bicho",
    u"De hora em hora eu tenho que mandar uma mensagem",
    u"De hora em hora o Sílvio Santos dá o resultado da telesena",
    u"É hora de dar tchau",
    u"É hora dos bottubbies",
    u"Meia noite é o horário oficial do óleo de macaco",
    u"Poderia ser 4:20 agora né",
  ])
  context.bot.send_message(
    text = u"Agora são {time:%H} horas. {text}.".format(
      time = datetime.datetime.now(here),
      text = texto,
    ),
    chat_id = app.config['LOG_GROUPS']['info'],
  )
updaters[0].job_queue.run_repeating(
  hourly,
  interval = datetime.timedelta(hours = 1),
  first = datetime.datetime(
    year = here_and_now.year,
    month = here_and_now.month,
    day = here_and_now.day,
    hour = here_and_now.hour,
    minute = 0,
    # ~ second = 0,
    # ~ microsecond = 0,
    # ~ tzinfo = here,
  ),
)
def daily(context):
  texto = random.choice([
    u"Meia noite é o horário oficial do óleo de macaco",
    u"Mais um dia nessa vida maravilhosa",
    u"Dia de bondade",
    u"Todo dia isso bicho",
  ])
  context.bot.send_message(
    text = u"Hoje é {time:%A}, {time:%d} de {time:%B}. {text}.".format(
      time = datetime.datetime.now(here),
      text = texto,
    ),
    chat_id = app.config['LOG_GROUPS']['info'],
  )
updaters[0].job_queue.run_repeating(
  daily,
  interval = datetime.timedelta(days = 1),
  first = datetime.datetime(
    year = here_and_now.year,
    month = here_and_now.month,
    day = here_and_now.day,
    hour = 0,
    # ~ minute = 0,
    # ~ second = 0,
    # ~ microsecond = 0,
    # ~ tzinfo = here,
  ),
)
def its420(context):
  context.bot.send_message(
    text = u"É 4:20 meus consagrados",
    chat_id = app.config['LOG_GROUPS']['info'],
  )
updaters[0].job_queue.run_daily(
  its420,
  ## Hoje às 16:20
  time = datetime.datetime(
    year = here_and_now.year,
    month = here_and_now.month,
    day = here_and_now.day,
    hour = 16,
    minute = 20,
    # ~ second = 0,
    # ~ microsecond = 0,
    # ~ tzinfo = here,
  ),
)

## run_once
def script_start(context):
  context.bot.send_message(
    chat_id = app.config['LOG_GROUPS']['info'], 
    text = u'Pai tá on',
  )
updaters[0].job_queue.run_once(
  script_start,
  0,
)

## FIXME Não tá funcionando
def callback_alarm(context: telegram.ext.CallbackContext):
  context.bot.send_message(
    chat_id = context.job.context,
    text = 'ALARME',
  )
def callback_timer(
  update: telegram.Update,
  context: telegram.ext.CallbackContext,
):
  context.bot.send_message(
    text = 'Em nove segundos',
    chat_id = update.effective_chat_id,
  )
  context.job_queue.run_once(
    callback_alarm,
    9,
    context = update.effective_chat_id,
  )
  # ~ updaters[0].job_queue.run_once(
    # ~ callback_alarm,
    # ~ 9,
    # ~ context = update.effective_chat_id,
  # ~ )
timer_handler = CommandHandler('timer', callback_timer)
updaters[0].dispatcher.add_handler(timer_handler)

## Tem que ser o último
def unknown(update, context):
  context.bot.send_message(
    chat_id = update.effective_chat.id,
    text = u"Vossa excelência enviardes um comando que nós não entendemos!"
  )
unknown_handler = MessageHandler(Filters.command, unknown)
updaters[0].dispatcher.add_handler(unknown_handler)
