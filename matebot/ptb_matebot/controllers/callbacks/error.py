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

### Tratamento de erros / exceções

from telegram.error import (
  TelegramError,
  Unauthorized,
  BadRequest,
  TimedOut,
  ChatMigrated,
  NetworkError,
)

from matebot.ptb_matebot import (
  app,
)

from matebot.ptb_matebot.controllers.utils import (
  update_text,
)

## Trata vários tipos de exceção (ou deveria tratar)
def error_callback(update, context):
  try:
    raise context.error
  except Unauthorized as e:
    # remove update.message.chat_id from conversation list
    text = list()
    text.append('#exception #unauthorized')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
      isgroup = True,
      queued = True,
    )
  except BadRequest as e:
    # handle malformed requests - read more below!
    text = list()
    text.append('#exception #badrequest')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['groups']['admin']['debug'],
      text = '\n\n'.join(text),
      isgroup = True,
      queued = True,
    )
  except TimedOut as e:
    # handle slow connection problems
    text = list()
    text.append('#exception #timedout')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['groups']['admin']['debug'],
      text = '\n\n'.join(text),
      isgroup = True,
      queued = True,
    )
  except NetworkError as e:
    # handle other connection problems
    text = list()
    text.append('#exception #networkerror')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['groups']['admin']['debug'],
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
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['LOG_GROUPS']['debug'],
      text = '\n\n'.join(text),
      isgroup = True,
      queued = True,
    )
  except TelegramError as e:
    # handle all other telegram related errors
    text = list()
    text.append('#exception #telegramerror')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['groups']['admin']['debug'],
      text = '\n\n'.join(text),
      isgroup = True,
      queued = True,
    )
  except Exception as e:
    text = list()
    text.append('#exception #notetelegram')
    text.append(u"Exception:\n%s" % (str(e)))
    if update:
      update_text(update,text)
    context.bot.send_message(
      chat_id = app.config['groups']['admin']['debug'],
      text = '\n\n'.join(text),
      isgroup = True,
      queued = True,
    )
  finally:
    context.bot.send_message(
      text = u"Tive um problema mas já avisei o pessoal que cuida do desenvolvimento.",
      chat_id = update.effective_chat.id,
      reply_to_message_id = update.effective_message.message_id,
      isgroup = (update.effective_chat.type in ["group", "supergroup"]),
      queued = True,
    )

def exception_callback(args):
  print(str(args))
