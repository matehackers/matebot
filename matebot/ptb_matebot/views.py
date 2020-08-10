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

from datetime import datetime

## Flask
from flask import (
  jsonify,
  redirect,
  render_template,
  url_for,
)

## Matebot / PTB
from matebot.ptb_matebot import (
  app,
  bot,
  testbot,
  # ~ updater,
  # ~ dispatcher,
)

@app.route("/")
def index():
  return redirect(url_for('get_me'))

## Code Snippets
## https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets
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
  return jsonify(str(bot.send_message(chat_id=chat_id, text=text)))

@app.route("/send_photo/file/<chat_id>/<file_uri>")
def send_photo_file(chat_id=1, file_uri='/tmp/image.png'):
  return jsonify(bot.send_photo(chat_id=chat_id, photo=open(file_uri, 'rb')))

@app.route("/send_photo/link/<chat_id>/<link_url>")
def send_photo_link(chat_id=1, link_url='https://telegram.org/img/t_logo.png'):
  return jsonify(bot.send_photo(chat_id=chat_id, photo=link_url))

@app.route("/send_voice/<chat_id>/<file_uri>")
def send_voice(chat_id=1, file_uri='/tmp/voice.ogg'):
  return jsonify(bot.send_voice(chat_id=chat_id, voice=open(file_uri, 'rb')))

@app.route("/send_gif/<chat_id>/<gif_url>")
def send_gif(chat_id=1, gif_url=''):
  return jsonify(bot.send_animation(
    chat_id=chat_id,
    animation=gif_url,
    duration=None,
    width=None,
    height=None,
    thumb=None,
    caption=None,
    parse_mode=None,
    disable_notification=False,
    reply_to_message_id=None,
    reply_markup=None,
    timeout=20,
    **kwargs
  ))

# ~ bot.send_audio(chat_id=chat_id, audio=open('tests/test.mp3', 'rb'))
# ~ bot.send_document(chat_id=chat_id, document=open('tests/test.zip', 'rb'))

# ~ file_id = message.voice.file_id
# ~ newFile = bot.get_file(file_id)
# ~ newFile.download('voice.ogg')

## Matebot / Terça Sem Fim
@app.route("/dump_updates")
def dump_updates():
  updates = bot.get_updates()
  messages = list()
  for update in updates:
    text = list()
    text.append('{}'.format(str(update['update_id'])))
    if update['message']['chat']['type'] == 'supergroup':
      text.append(
        u"https://t.me/c/{message__chat__id}/{message__message_id}".format(
          message__chat__id = str(update['message']['chat']['id'])[4:],
          message__message_id = str(update['message']['message_id']),
        )
      )
    text.append('')
    text.append((
      u"{message__chat__title} at {message__date}{message__edit__date}").format(
        message__chat__title = str(update['message']['chat']['title']),
        message__date = str(update['message']['date']),
        message__edit__date = u" (edited at update['message']['edit_date'])" if 
          update['message']['edit_date'] else ''
      )
    )
    ## TODO y u no become dict
    from_dict = vars(update['message']).get('from', None)
    if from_dict is not None:
      from_text = list()
      from_text.append(u"From")
      from_first_name = vars(update['message']['from']).get('first_name', None)
      if from_first_name is not None:
        from_text.append(from_first_name)
      from_last_name = vars(update['message']['from']).get('last_name', None)
      if from_last_name is not None:
        from_text.append(from_last_name)
      from_username = vars(update['message']['from']).get('username', None)
      if from_username is not None:
        from_text.append(u"(@{})".format(from_username))
      from_id = vars(update['message']['from']).get('id', None)
      if from_id is not None:
        from_text.append(u"({})".format(from_id))
      text.append(' '.join(from_text))
    text.append('')
    if 'text' in vars(update['message']):
      text.append(str(update['message']['text']))
    testbot.send_message(
      chat_id = app.config['LOG_GROUPS']['updates'], 
      text = '\n'.join(text),
      parse_mode = None,
      disable_web_page_preview = True,
      disable_notification = True,
    )
  return u"OK"

@app.route("/list_plugins")
def list_plugins():
  pass

@app.route("/find_command/<comando>")
def find_command(comando='start'):
  response = u"Vossa excelência não terdes autorização para usar este comando, \
    ou o comando não existe."
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
