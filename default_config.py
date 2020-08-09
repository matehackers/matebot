# vim:fileencoding=utf-8
#
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
##
## PT: Copiar este arquivo para instance/config.py e editar lá
##
## EN: Copy this file to instance/config.py and edit it there

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  DEBUG = False
  TESTING = False
  SECRET_KEY = "sou um seixo rolado na estrada do lado de la do sertao"
  # ~ WTF_CSRF_SECRET_KEY = "e ser tao humilhado e sinal de que o diabo e que \
  # ~ amassa o meu pao"
  # ~ SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'
  # ~ + os.path.join(basedir, 'instance', 'app.db')
  ## The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is set to False
  ## to disable a feature of Flask-SQLAlchemy that I do not need, which is to
  ## signal the application every time a change is about to be made in the
  ## database.
  # ~ SQLALCHEMY_TRACK_MODIFICATIONS = False
  
  ## Obtenha um token com @BotFather no Telegram
  BOTFATHER = {
    'token': os.environ.get('BOTFATHER_TOKEN') or
      "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
  }
  
  ## Altere as informações do bot de acordo com as suas necessidades. Estas 
  ## informações aparecem em alguns comandos como por exemplo o /help
  INFO = {
    'website': "https://matehackers.org",
    ## TODO Alterar para REPOSITORY
    'code_repository': "https://github.com/matehackers/tg-matebot",
    'telegram_group': "@matehackerspoa",
    'telegram_channel': "@matehackers",
    'telegram_admin': "@desobedientecivil",
    'telegram_dev': "@desobedientecivil",
  }
  
  ## Endereços de criptomoedas para doações. Se vós não alterardes isto, as 
  ## doações irão para matehackers.org
  ## TODO fazer dicionário / lista com mais endereços
  DONATE = {
    'btc': "1AG2SX3n9iFQiZExiyS3M5qCuZT5GhArn",
  }
  
  ### Controle de acesso para plugins
  ## É necessário existir pelo menos a lista 'geral'. Recomendando pelo menos
  ## ter o plugin 'telegram' nesta lista.
  ## Lista de plugins ativos para todo mundo
  PLUGINS_LISTAS = {
    'geral': [
      "telegram",
      "donate",
      "feedback",
      "qr",
      "hashes",
      "archive",
      "mate-matica",
    ],
    ## Plugins ativos somente para administrador
    'admin': [
      "admin",
      "totalvoice",
      "velivery_pedidos",
      "cr1pt0_almoco",
      "start",
      "velivery_admin",
      "workrave",
      "tesouro",
      "greatful",
      "fdof",
      "greatful_dev",
      "velivery_automatico",
      "velivery_bikeentregas",
      "velivery_relatorios",
      "hackerspace",
    ],
    ## Plugins ativos para configuração local (por exemplo: grupo do 
    ## matehackers)
    'local': [
      "ytdl",
    ],
  }
  
  ## Lista de usuários e grupos 'geral' não são necessárias, porque o controle
  ## de acesso 'geral' serve para todo e qualquer id de usuária(o) ou grupo.
  ## Inclua em 'local' todos ids de usuário e de grupos. Para descobrir o id, 
  ## mande mensagem para o bot e observe o console.
  ## (Opcional) coloque em 'admin' o id do telegram da(o)s administradoras(es) 
  ## do bot, e/ou de um ou mais grupo de administração do bot.
  PLUGINS_USUARIOS = {
    'admin': [1],
    'local': [1,2,3,4],
  }
  PLUGINS_GRUPOS = {
    'admin': [-1],
    'local': [-2,-3,-4],
  }

class ProductionConfig(Config):
  SECRET_KEY = "mas meu corpo e discente e civilizada a mente toca cheira ouve \
    e ve"
  BOTFATHER_TOKEN = os.environ.get('BOTFATHER_TOKEN_PRODUCTION') or 
    "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  # ~ WTF_CSRF_SECRET_KEY = "e com amor e anarquia goza que rosca e arrepia \
  # ~   rock en rolando em voce"
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' 
    + os.path.join(basedir, 'instance', 'production.db')

class DevelopmentConfig(Config):
  DEBUG = True
  BOTFATHER_TOKEN = os.environ.get('BOTFATHER_TOKEN_DEVELOPMENT') or 
    "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' 
    + os.path.join(basedir, 'instance', 'development.db')

class TestingConfig(Config):
  TESTING = True
  BOTFATHER_TOKEN = os.environ.get('BOTFATHER_TOKEN_TESTING') or 
    "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' 
    + os.path.join(basedir, 'instance', 'testing.db')
