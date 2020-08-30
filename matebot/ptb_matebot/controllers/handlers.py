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

### Handlers para Terça Sem Fim / Tutorial

from telegram.ext import (
  CommandHandler,
  MessageHandler,
  Filters,
  InlineQueryHandler,
)

from matebot.ptb_matebot.controllers.callbacks.tutorial import (
  start_callback,
  echo_callback,
  caps_callback,
  unknown_callback,
)

from matebot.ptb_matebot.controllers.callbacks.inline import (
  inline_caps_callback,
)

from matebot.ptb_matebot.controllers.callbacks.log import (
  x9_callback,
)

from matebot.ptb_matebot.controllers.callbacks.jobqueue import (
  callback_timer,
)

### Tutorial
start_handler = CommandHandler('start', start_callback)
echo_handler = MessageHandler(
  Filters.text & (~Filters.command),
  echo_callback,
)
caps_handler = CommandHandler('caps', caps_callback)

### Inline
inline_caps_handler = InlineQueryHandler(inline_caps_callback)

### Logging
x9_handler = MessageHandler(
  Filters.all,
  x9_callback,
)

### JobQueue
## Não funciona
timer_handler = CommandHandler('timer', callback_timer)

### Tem que ser o último
unknown_handler = MessageHandler(Filters.command, unknown_callback)
