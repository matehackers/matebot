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
## App padrão se não for especificado nenhum no .env
from matebot.ptb_matebot import (
  app,
  updaters,
)

if __name__ == '__main__':
  try:
    app.run(threaded=True)
  except KeyboardInterrupt:
    print(u"Stopping updaters...")
    for updater in updaters:
      updater.stop()
    print(u"...done.")
  except Exception as e:
    print(u"Exception: {}".format(str(e)))
    raise
