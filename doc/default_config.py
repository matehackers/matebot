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
  ## Configuração padrão para todos bots
  default_bot: dict = {
    ### Informações exibidas no comando /info
    ### Alterar se necessário
    'info': {
      'website': "https://matehackers.org",
      'repository': "https://github.com/matehackers/matebot",
      'group': "@matehackerspoa",
      'channel': "@matehackers",
      'admin': "@desobedientecivil",
      'dev': "@desobedientecivil",
      'donate': {
        'btc': "1AG2SX3n9iFQiZExiyS3M5qCuZT5GhArn",
      },
    }, # info
      'plugins': {
        ### Níveis de permissão (inspirados no Brave New World):
        ### Isto pode ser qualquer coisa, serve simplesmente para fazer listas
        ### de usuária(o)s e grupos para controlar o acesso a plugins e 
        ### comandos. As descrições são meramente sugestões (que eu não uso).
        ### O que importa é que usuária(o)s e grupos na lista 'alpha' só vão
        ### conseguir acessar plugins da lista correspondente 'alpha' e assim
        ### por diante. Se isto não estiver claro, peça ajuda no grupo:
        ### https://t.me/joinchat/CwFUFkf-dKW34FPBjEJs9Q
        ###
        ### Comandos e plugins com controle de acesso vão verificar estas listas
        ### e permitir ou não que usuária(o)s e grupos usem determinados 
        ### comandos ou funções.
        ### Os grupos não herdam uns dos outros com a exceção do 'omega' que
        ### torna disponível o plugin sem nenhum controle de acesso.
        ## Lista de plugins disponíveis somente para a pessoa que criou a robô
        'alpha': ["admin",],
        ## Lista de plugins disponíveis para desenvolvedora(e)s, etc. da robô
        'beta': ["feedback","log","totalvoice",],
        ## Lista de plugins disponíveis para moderadora(e)s de grupos, etc.
        'gamma': ["feedback","log",],
        ## Lista de plugins ativos para alguns grupos
        'delta': ["archive","hashes","mate-matica","qr","random","ytdl",],
        ## Lista de plugins ativos para vários grupos
        'epsilon': ["hashes","mate-matica","random",],
        ## Lista de plugins ativos para todo mundo
        'omega': ["telegram","donate",],
      }, # plugins
      ### Controle de acesso para plugins
      'users': {
        ## telegram_id de usuária(o)s ou grupos
        'alpha': [1,-1,],
        'beta': [2,3,4,],
        'gamma': [5,],
        'delta': [-286513129,-1001233916997,],
        'epsilon': [777000,-1001207858341,],
        ## Não tem 'omega' porque 'omega' é qualquer outro id
        ### Mesma coisa que as listas de acesso mas com nomes de chaves
        'special': {
          ## Grupos para testar o matebot
          'debug': -1001233916997,
          'info': -1001233916997,
          'feedback': -1001233916997,
          'log': -1001233916997,
          'pub': -1001207858341,
          ## Conta de serviço do telegram
          'service': 777000,
        },
      }, # users
  } # default_bot

  bots: dict = {
    ## O nome da chave (por exemplo 'matebot') é o nome do bot como parâmetro ao
    ##  invocar o script. Isto permite usar múltiplos bots.
    'matebot': {
      ## Obtenha um token com @BotFather no Telegram
      'token': "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
      'info': default_bot['info'],
      'plugins': default_bot['plugins'],
      'users': default_bot['users'],
    }, # matebot
    ### (Opcional) Cada conta do telegram pode ter 20 bots! Configure outros
    ### aqui para iniciar um bot alternativo por exemplo:
    ### `pipenv run matebot outrobot`
    'outrobot': {
      'token': "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
      'info': {
        'website': "",'repository': "",'group': "",'channel': "",'admin': "",
        'dev': "",'donate': {'btc': "1AG2SX3n9iFQiZExiyS3M5qCuZT5GhArn",},
      } # info
      'plugins': {
        'alpha': ["admin",],
        'beta': ["totalvoice","donate","log","feedback",],
        'gamma': ["qr","hashes","archive","mate-matica","ytdl",],
        'delta': [],
        'epsilon': [],
        'omega': ["telegram"],
      } # plugins
      'users': {
        'alpha': [1,],'beta': [],'gamma': [],
        'delta': [-1001233916997,],
        'epsilon': [777000,-1001207858341,],
        'special': {'debug': -1001233916997,'info': -1001233916997,},
      }, # users
    }, # outrobot
  } # bots
