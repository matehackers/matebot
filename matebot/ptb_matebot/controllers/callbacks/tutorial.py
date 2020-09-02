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

### Terça Sem Fim / Tutorial

def start_callback(update, context):
  context.bot.send_message(
    text = u"Oi oi oi me use me use", # lalenia
    chat_id = update.effective_chat.id,
    isgroup = (update.effective_chat.type in ["group", "supergroup"]),
    queued = True,
  )

## Papagaio
def echo_callback(update, context):
  context.bot.send_message(
    text = update.message.text,
    chat_id = update.effective_chat.id,
    isgroup = (update.effective_chat.type in ["group", "supergroup"]),
    queued = True,
  )

## 2020-08-25
## Plugin inútil pra converter texto em maiúsculas
def caps_callback(update, context):
  context.bot.send_message(
    text = ' '.join(context.args).upper(),
    chat_id = update.effective_chat.id,
    isgroup = (update.effective_chat.type in ["group", "supergroup"]),
    queued = True,
  )

def unknown_callback(update, context):
  context.bot.send_message(
    text = u"Vossa excelência enviardes um comando que nós não entendemos!",
    chat_id = update.effective_chat.id,
    isgroup = (update.effective_chat.type in ["group", "supergroup"]),
    queued = True,
  )
