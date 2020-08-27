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

import json

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
      chat_id = update.effective_chat.id,
      text = u"Tive um problema mas já avisei o pessoal que cuida do desenvolvimento.",
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

## Tem que ser o último
def unknown(update, context):
  context.bot.send_message(
    chat_id = update.effective_chat.id,
    text = u"Vossa excelência enviardes um comando que nós não entendemos!"
  )
unknown_handler = MessageHandler(Filters.command, unknown)
updaters[0].dispatcher.add_handler(unknown_handler)
