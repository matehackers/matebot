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

from matebot.ptb_matebot import (
  updaters,
)

from matebot.ptb_matebot.controllers.callbacks.error import (
  error_callback,
)

from matebot.ptb_matebot.controllers.handlers import (
  start_handler,
  echo_handler,
  caps_handler,
  inline_caps_handler,
  x9_handler,
  timer_handler,
  unknown_handler,
)

def all():
  ### Error Handlers
  updaters[0].dispatcher.add_error_handler(error_callback)

  ### Tutorial Handlers
  ## Lalenia
  updaters[0].dispatcher.add_handler(start_handler)
  ## Papagaio
  # ~ updaters[0].dispatcher.add_handler(echo_handler)
  ## CAPS
  updaters[0].dispatcher.add_handler(caps_handler)

  ### Inline Handlers
  # ~ updaters[0].dispatcher.add_handler(inline_caps_handler)

  ### Logging Handlers
  updaters[0].dispatcher.add_handler(x9_handler)

  ### FIXME Não tá funcionando
  updaters[0].dispatcher.add_handler(timer_handler)

  ### Tem que ser o último
  updaters[0].dispatcher.add_handler(unknown_handler)
