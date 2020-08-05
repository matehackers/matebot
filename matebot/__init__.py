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

## Flask
from flask import Flask
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('default_config.Config')
try:
  ## Por padrão ./instance/config.py que deve estar ignorado pelo 
  ## .gitignore. Copiar ./default_config.py para ./instance/config.py 
  ## antes de rodar o flask.
  app.config.from_pyfile(''.join([app.instance_path, '/config.py']))
except Exception as e:
  print(u"Arquivo de configuração não encontrado. Exceção: %s" % (e))

## Logging
import logging
logging.basicConfig(
  level=logging.DEBUG,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

## PTB
import telegram
## TODO suporte para múltiplos bots?
bot = telegram.Bot(token=app.config['BOTFATHER']['token'])
# ~ from telegram.ext import Updater
# ~ updater = Updater(
  # ~ token=app.config['BOTFATHER']['token'],
  # ~ use_context=True,
# ~ )
# ~ dispatcher = updater.dispatcher
# ~ from telegram.ext import CommandHandler
# ~ start_handler = CommandHandler('start', start)
# ~ dispatcher.add_handler(start_handler)

## TODO Blueprints
## Matebot
from matebot import views, models

## flask shell
@app.shell_context_processor
def make_shell_context():
  return {'bot': bot}

## TODO Não lembro se vai ser pertinente manter estas linhas
def main():
  
  return 0

if __name__ == '__main__':
  main()
