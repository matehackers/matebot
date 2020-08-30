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


## Flask
from flask import (
  jsonify,
  redirect,
  render_template,
  url_for,
)

## Matebot / aiogram
from matebot.aio_matebot import (
  # ~ app,
  # ~ bots,
  dispatchers,
)

from aiogram import (
  executor,
)

@app.route("/")
def index():
  retorno = list()
  for dispatcher in dispatchers:
    executor.start_polling(dispatcher, skip_updates=True)
    retorno.append('OK')
  return jsonify(
    json.dumps(
      ''.join(retorno),
      sort_keys = True,
      indent = 2,
      default = str,
    )
  )
