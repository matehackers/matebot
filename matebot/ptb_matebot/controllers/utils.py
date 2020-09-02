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

### Métodos genéricos

import json

## Formatação de updates para log em grupos
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
