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

### Logging callbacks

from matebot.ptb_matebot import (
  config,
)

from matebot.ptb_matebot.controllers.utils import (
  update_text,
)

key_error = u"""Mensagem não enviada para grupo de log. Para ativar log em grup\
os de telegram, coloque o bot em um grupo e use o chat_id do grupo no arquivo d\
e configuração."""

## Manda todos updates pro grupo de log
def x9_callback(update, context):
  text = list()
  if update:
    update_text(update,text)
  try:
    context.bot.send_message(
      chat_id = context.bot.users['special']['log'],
      text = '\n\n'.join(text),
      isgroup = True,
      queued = True,
    )
  except KeyError:
    print(u"[LOG] {}".format(key_error))
