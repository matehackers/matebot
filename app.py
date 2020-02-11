# vim:fileencoding=utf-8
#  MateBot: Bot de Telegram
#  
#  Copyleft 2016-2020 Iuri Guilherme, 2017-2020 Matehackers,
#     2018-2019 Velivery, 2019 Greatful, 2020 Fábrica do Futuro
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  

## Flask
from flask import (
  Flask,
  redirect,
  url_for,
)
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('default_config.Config')
try:
  app.config.from_pyfile(''.join([app.instance_path, '/config.py']))
except Exception as e:
  print(u"Config file not found. Exception: %s" % (e))

## Flask SQL Alchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

## Log
## TODO não sei se funciona desta forma os logs, provavelmente somente 
##  uma destas configurações (a última?) esteja funcionando de fato.
# ~ import logging
# ~ info_handler = logging.basicConfig(
  # ~ filename='instance/info.log',
  # ~ filemode='w',
  # ~ level=logging.INFO,
# ~ )
# ~ error_handler = logging.basicConfig(
  # ~ filename='instance/error.log',
  # ~ filemode='w',
  # ~ level=logging.ERROR,
# ~ )
# ~ debug_handler = logging.basicConfig(
  # ~ filename='instance/debug.log',
  # ~ filemode='w',
  # ~ level=logging.DEBUG,
# ~ )
# ~ warning_handler = logging.basicConfig(
  # ~ filename='instance/warning.log',
  # ~ filemode='w',
  # ~ level=logging.WARN,
# ~ )
# ~ from plugins.tenable_logs import LogSetup
# ~ app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "stream")
# ~ app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")
# File Logging Setup
# app.config['LOG_DIR'] = os.environ.get("LOG_DIR", "./")
# app.config['APP_LOG_NAME'] = os.environ.get("APP_LOG_NAME", "app.log")
# app.config['WWW_LOG_NAME'] = os.environ.get("WWW_LOG_NAME", "www.log")
# ~ app.config['LOG_MAX_BYTES'] = os.environ.get(
  # ~ "LOG_MAX_BYTES",
  # ~ 100_000_000
# ~ )  # 100MB in bytes
# app.config['LOG_COPIES'] = os.environ.get("LOG_COPIES", 5)
# ~ if __name__ != '__main__':
  # ~ gunicorn_logger = logging.getLogger('gunicorn.error')
  # ~ app.logger.handlers = gunicorn_logger.handlers
  # ~ app.logger.setLevel(gunicorn_logger.level)

# ~ logs = LogSetup()
# ~ logs.init_app(app)

## Blueprints
## API
## TODO API deve ser utilizada programaticamente como API propriamente 
## dita, ainda há trabalho a ser feito para se tornar uma API de fato.
#from blueprints.api import bp as api_bp
#app.register_blueprint(api_bp, url_prefix="/api")
## Web
# ~ from blueprints.web import bp as web_bp
# ~ app.register_blueprint(web_bp, url_prefix="/web")

## Index
@app.route("/")
def index():
  # ~ app.logger.debug('this is a DEBUG message')
  # ~ app.logger.info('this is an INFO message')
  # ~ app.logger.warning('this is a WARNING message')
  # ~ app.logger.error('this is an ERROR message')
  # ~ app.logger.critical('this is a CRITICAL message')
  return u"MateBot"

## flask shell
@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'map': app.url_map}

#db.init_app(app)
