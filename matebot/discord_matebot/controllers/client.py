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

import logging

from discord import Client

class MateClient(Client):
  def __init__(self, *args, **kwargs):
    ## Tratando as configurações
    config = kwargs.get('config')
    name = kwargs.get('name', 'matebot')
    setattr(self, 'config_info',
      config.bots[name]['info'] or config.default_bot['info'])
    setattr(self, 'config_plugins',
      config.bots[name]['plugins'] or config.default_bot['plugins'])
    setattr(self, 'config_users',
      config.bots[name]['users'] or config.default_bot['users'])
    kwargs.pop('config', None)
    kwargs.pop('name', None)
    super().__init__(*args, **kwargs)

  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

  async def on_message(self, message):
    print('Message from {0.author}: {0.content}'.format(message))
