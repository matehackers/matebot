# vim:fileencoding=utf-8
#  Plugin personalidades para matebot: Robô também é gente?
#  Copyleft (C) 2020 Iuri Guilherme, 2020 Matehackers
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

### Lista de textos gerados aleatoriamente
## FIXME Sentenças adicionadas manualmente a partir das respostas de usuários.
## Nenhuma dessas frases é criação ou responsabilidade dos desenvolvedores, são
## as pessoas no Telegram ensinando a bot. Criar um sistema de filtro com banco
## de dados e machine learning vai diminuir o trabalho manual, mas também vai
## criar resultados potencialmente indesejados (por razões óbvias).

import random

try:
  import instance.random_texts_pave as pave
except:
  import matebot.plugins.personalidades.pave.random_texts as pave

def bebidas():
  return pave.bebidas()

def adjetivos():
  return random.choice([pave.adjetivos(), random.choice([
    u"direitopata",
    u"esquerdopata",
    u"gentalha",
  ])])

def respostas_bebida():
  return pave.respostas_bebida()

def respostas_quanto():
  return pave.respostas_quanto()

def piadas():
  return pave.piadas()

def respostas_ignorante(admin):
  return random.choice([pave.respostas_ignorante(admin), piadas(), adjetivos()])

def versiculos_md():
  return pave.versiculos_md()

def rimas_ao():
  return random.choice([
    u"e tu, que é um trouxão?",
  ])

def start(message):
  return pave.start(message)

def welcome(message, count, admin):
  return pave.welcome(message, count, admin)
