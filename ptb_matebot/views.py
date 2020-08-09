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
#  

import importlib, json

## Flask
from flask import (
  redirect,
  render_template,
  url_for,
)

## Matebot
from matebot import (
  app,
  bot,
  # ~ updater,
  # ~ dispatcher,
)

@app.route("/")
def index():
  return redirect(url_for('get_me'))

@app.route("/get_me")
def get_me():
  return json.dumps(
    str(bot.get_me()),
    sort_keys=True,
    indent=2,
  )

@app.route("/get_updates")
def get_updates():
  return render_template(
    "get_updates.html",
    title = bot.get_me()['first_name'],
    updates = bot.get_updates(),
  )

@app.route("/send_message/<chat_id>/<text>")
def send_message(chat_id=1, text=u"Nada"):
  return json.dumps(str(bot.send_message(chat_id=chat_id, text=text)))

@app.route("/list_plugins")
def list_plugins():
  pass

@app.route("/find_command/<comando>")
def find_command(comando='start'):
  response = u"Vossa excelência não terdes autorização para usar este comando, ou o comando não existe."
  debug = u"Nada aconteceu."
  ## TODO todos plugins
  plugins_list = app.config['PLUGINS_LISTAS']['geral']
  plugins_list = plugins_list + app.config['PLUGINS_LISTAS']['admin']
  plugins_list = plugins_list + app.config['PLUGINS_LISTAS']['local']
  args = {
    'chat_id': app.config['PLUGINS_USUARIOS']['admin'][0],
    'from_id': app.config['PLUGINS_USUARIOS']['admin'][0],
    'command_list': "/start",
    'command_type': 'user',
    'bot': bot,
    'config': app.config,
    'info_dict': app.config['INFO'],
    'message_id': 10,
  }
  contents = list()
  for plugin in plugins_list:
    try:
      contents.append(getattr(
        importlib.import_module(
          '.'.join(['plugins', plugin])),
          '_'.join([u"cmd", comando])
      )(args))
    except AttributeError as e:
      contents.append({
        'status': False,
        'response': u"AttributeError",
        'debug': str(e),
      })
    except ImportError as e:
      contents.append({
        'status': False,
        'response': u"ImportError",
        'debug': str(e),
      })
    except Exception as e:
      contents.append({
        'status': False,
        'response': u"Exception",
        'debug': str(e),
      })
      raise
  return render_template(
    "find_command.html",
    contents = contents,
    response = response,
    debug = debug,
  )

## TODO ACL
# ~ from functools import wraps

# ~ LIST_OF_ADMINS = [12345678, 87654321]

# ~ def restricted(func):
    # ~ @wraps(func)
    # ~ def wrapped(update, context, *args, **kwargs):
        # ~ user_id = update.effective_user.id
        # ~ if user_id not in LIST_OF_ADMINS:
            # ~ print("Unauthorized access denied for {}.".format(user_id))
            # ~ return
        # ~ return func(update, context, *args, **kwargs)
    # ~ return wrapped

# ~ @restricted
# ~ def my_handler(update, context):
    # ~ pass  # only accessible if `user_id` is in `LIST_OF_ADMINS`.
