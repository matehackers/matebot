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
  
  ### Configuração padrão para todos bots:
  ### Os bots definidos posteriormente podem herdar as configurações padrão, ou
  ### Uma parte das configurações conforme a necessidade.
  default_bot: dict = {
  
    ### Informações exibidas em alguns comandos do bot
    'info': {
      'website': "https://matehackers.org",
      'repository': "https://github.com/matehackers/matebot",
      'group': "https://t.me/joinchat/CwFUFkf-dKW34FPBjEJs9Q",
      'channel': "@matebotnews",
      'admin': "@desobedientecivil",
      'dev': "@desobedientecivil",
      ## Plugin donate - doações
      'donate': {
        'btc': "1AG2SX3n9iFQiZExiyS3M5qCuZT5GhArn",
      },
      ## Plugin tropixel - colar os links aqui no lugar de "Não sei !"
      'tropixel': {
        'site': "Não sei!",
        'boteco': "Não sei!",
      },
      ## Plugin personalidades
      'personalidade': 'default',
    }, # info
    ## TelegramTecidoTextoTabelas
    'tecido': {
      'host': 'localhost',
      'port': 3000,
    }, # tecido

    ### Níveis de permissão (inspirados no Brave New World):
    ###
    ### Os usuários e grupos cujos ids estão na lista bot.users['alpha'] só
    ### vão ter acesso aos comandos que fazem parte dos plugins da lista
    ### bot.plugins['alpha']. Assim como a lista bot.users['beta'] é relativa à
    ### lista bot.plugins['beta'], e assim por diante. Esta é a única regra.
    ###
    ### Sinta-se livre para liberar o acesso a todos os comandos para qualquer
    ### pessoa ou grupo, ou para criar ainda mais níveis de controle de acesso.
    ###
    ### Se isto não estiver claro, veja os exemplos no arquivo README.md ou peça
    ### ajuda no grupo: https://t.me/joinchat/CwFUFkf-dKW34FPBjEJs9Q
    ###
    ### A lista bot.plugins['omega'] é especial e serve para dar acesso a 
    ### comandos para toda e qualquer pessoa ou grupo.
    ###
    'plugins': {
      ## Lista de plugins disponíveis somente para bot.users['alpha']
      ## Sugestão de uso: pessoa que criou o bot, etc.
      'alpha': ["admin",],
      ## Lista de plugins disponíveis somente para bot.users['beta']
      ## Sugestão de uso: administradora(e)s, moderadora(e)s, etc.
      'beta': ["admin",],
      ## Lista de plugins disponíveis somente para bot.users['gamma']
      ## Sugestão de uso: grupos e canais onde quem administra tem controle
      'gamma': ["donate",],
      ## Lista de plugins disponíveis somente para bot.users['delta']
      ## Sugestão de uso: grupos e canais onde quem administra acompanha mas não
      ## controla
      'delta': ["personalidades", "feedback", "welcome",],
      ## Lista de plugins disponíveis somente para bot.users['epsilon']
      ## Sugestão de uso: grupos, canais e usuários que usam o bot regularmente
      'epsilon': ["archive", "hashes", "mate_matica", "qr", "ytdl",],
      ## Lista de plugins ativos para todo mundo
      'omega': ["telegram",],
    }, # plugins
    
    'users': {
      ### telegram_id de usuária(o)s ou grupos
      ### Envie /start para descobrir o próprio id
      'alpha': [1,-1,],
      'beta': [],
      'gamma': [-481703172,],
      'delta': [-1001233916997,],
      'epsilon': [777000,-1001207858341,],
      ## Plugin Welcome
      'pegadinha': [-1001233916997,],
      ## Plugin Tropixel
      'tropixel': [-1001233916997,],
      ### Não tem 'omega' porque 'omega' é qualquer outro id
      ### Usuários e grupos especiais (que são referenciados pelo nome da chave)
      'special': {
        ## Conta de serviço do telegram
        'service': 777000,
        ## Grupo público para desenvolvedora(e)s e usuária(o)s
        ## https://t.me/joinchat/CwFUFkf-dKW34FPBjEJs9Q
        'pub': -1001207858341, 
        ## Grupo para onde vão mensagens de informação
        ## https://t.me/joinchat/CwFUFhy2NQRi_9Cc60v_aA
        'info': -481703172,
        ## Grupo para onde são logados os erros / exceções
        ## https://t.me/joinchat/CwFUFhy2NQRi_9Cc60v_aA
        'debug': -481703172,
        ## Grupo para onde vão as mensagens do comando /feedback
        ## https://t.me/joinchat/CwFUFhy2NQRi_9Cc60v_aA
        'feedback': -481703172,
        ## Grupo para testar bots
        ## https://t.me/joinchat/CwFUFhbgApLHBMLoNnkiRg
        'test': -1001233916997,
      },
    }, # users
    
  } # default_bot

  bots: dict = {
    ### O nome da chave (por exemplo 'matebot') é o nome do bot como parâmetro ao
    ### invocar o script. Isto permite usar múltiplos bots.
    ### As chaves 'production', 'testing' e 'development' podem ser utilizadas
    ### juntamente com as variáveis de ambiente do FLASK e do QUART.
    'matebot': {
      ## Obtenha um token com @BotFather no Telegram
      'token': "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
      'info': default_bot['info'],
      'plugins': default_bot['plugins'],
      'users': default_bot['users'],
      'tecido': default_bot['tecido'],
    }, # matebot
    'production': {
      'token': "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
      'info': default_bot['info'],
      'plugins': default_bot['plugins'],
      'users': default_bot['users'],
      'tecido': default_bot['tecido'],
    }, # production
    'testing': {
      'token': "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
      'info': default_bot['info'],
      'plugins': default_bot['plugins'],
      'users': default_bot['users'],
      'tecido': default_bot['tecido'],
    }, # testing
    'development': {
      'token': "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
      ## Exemplo para mudar só a personalidade
      'info': dict(default_bot['info'].copy, personalidade = 'metarec'),
      'plugins': default_bot['plugins'],
      ## Exemplo (ruim) para herdar configurações padrão alterando algumas
      'users': dict(default_bot['users'].copy(), special = {
        'debug': -481703172,
        'feedback': -481703172,
        'info': -481703172,
      }),
      'tecido': default_bot['tecido'],
    }, # development
  } # bots
