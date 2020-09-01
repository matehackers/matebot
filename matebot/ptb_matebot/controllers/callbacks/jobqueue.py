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

### 2020-08-29
## Testando com job queue
## https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.jobqueue.html

## FIXME Tudo dando errado!

import datetime, locale, pytz, random

from matebot.ptb_matebot import (
  app,
)

here = pytz.timezone('America/Sao_Paulo')
here_and_now = datetime.datetime.now(here)
locale.setlocale(locale.LC_ALL, 'pt_BR')

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
def hourly_callback(context):
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
    chat_id = app.config['groups']['admin']['info'],
    isgroup = True,
    queued = True,
  )

def daily_callback(context):
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
    chat_id = app.config['groups']['admin']['info'],
    isgroup = True,
    queued = True,
  )

def its420_callback(context):
  context.bot.send_message(
    text = u"É 4:20, {pronome}".format(
      pronome = random.choice([
        u"meus consagrados",
        u"minhas consagradas",
        u"mis consagrades",
      ]),
    ),
    chat_id = app.config['groups']['admin']['info'],
    isgroup = True,
    queued = True,
  )

def script_start_callback(context):
  context.bot.send_message(
    text = u"Pai tá on",
    chat_id = app.config['groups']['admin']['info'], 
    isgroup = True,
    queued = True,
  )

def callback_alarm(context):
  context.bot.send_message(
    chat_id = context.job.context,
    text = u"ALARME",
    queued = True,
  )
def callback_timer(update, context):
  context.bot.send_message(
    text = u"Em nove segundos",
    chat_id = update.effective_chat.id,
    reply_to_message_id = update.effective_message.message_id,
    isgroup = (update.effective_chat.type in ["group", "supergroup"]),
    queued = True,
  )
  context.job_queue.run_once(
    callback_alarm,
    9,
    context = update.effective_chat.id,
  )
