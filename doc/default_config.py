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

from pydantic import BaseSettings

class Config(BaseSettings):
  ## Obtenha um token com @BotFather no Telegram
  ## O nome da chave (por exemplo 'matebot') é o nome do bot como parâmetro ao
  ##  invocar o script. Isto permite usar múltiplos bots.
  tokens: dict = {
    'matebot': "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    'dev': "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    'test': "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    'outrobot': "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
  }
  
  ## Altere as informações do bot de acordo com as suas necessidades. Estas 
  ## informações aparecem em alguns comandos como por exemplo o /help
  info: dict = {
    'website': "https://matehackers.org",
    ## TODO Alterar para REPOSITORY
    'code_repository': "https://github.com/matehackers/tg-matebot",
    'telegram_group': "@matehackerspoa",
    'telegram_channel': "@matehackers",
    'telegram_admin': "@desobedientecivil",
    'telegram_dev': "@desobedientecivil",
    ## Endereços de criptomoedas para doações. Se vós não alterardes isto, as 
    ##  doações irão para matehackers.org
    ## TODO fazer dicionário / lista com mais endereços
    'donate': {
      'btc': "1AG2SX3n9iFQiZExiyS3M5qCuZT5GhArn",
    },
  }
  
  ### Controle de acesso para plugins
  ## É necessário existir pelo menos a lista 'geral'. Recomendando pelo menos
  ## ter o plugin 'telegram' nesta lista.
  ## Lista de plugins ativos para todo mundo
  plugins: dict = {
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
  users: dict = {
    'admin': {
      ## Telegram Services
      'services': 777000,
      'desobedientecivil': 1,
    },
    'local': [
      2,
      3,
    ],
  }
  groups: dict = {
    'admin': {
      'updates': -5,
      'debug': -6,
      'info': -7,
      'pub3': -1001207858341,
    }
    'local': [
      -2,
      -3,
      -4,
    ],
  }
