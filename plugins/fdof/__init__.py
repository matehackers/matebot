# vim:fileencoding=utf-8
#  Plugin fdof para matebot: Comandos Greatful para Fábrica do Futuro
#  Copyleft (C) 2019 Greatful

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random

## Avisa que chegou por primeiro na Fábrica do Futuro
def cmd_chegreat(args):
  return cmd_cheguei(args)

def cmd_cheguei(args):
  response = u"Chegou chegando, desnorteando a Fábrica toda!"
  return {
    'status': True,
    'type': args['command_type'],
    'response': response,
    'debug': 'cheguei',
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Avisa que foi embora da Fábrica do Futuro
def cmd_larguei(args):
  return cmd_vazei(args)

def cmd_fui(args):
  return cmd_vazei(args)

def cmd_vazei(args):
  response = u"A Fábrica é boa, mas não dá pra morar aí!"
  return {
    'status': True,
    'type': args['command_type'],
    'response': response,
    'debug': 'vazei',
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Avisa que fez uma merda
def cmd_fertilizei(args):
  return cmd_adubei(args)

def cmd_adubei(args):
  responses = [
    u"Adubando a gente dá.\nO ato de dar gera abundância.\nEntão, dar abunda!",
    u"Todo adubo é fertilizante para o limoeiro.\nTodo limão é uma limonada.",
    u"Plante as sementes.\nColha os milhões.",
    u"Vós sois padawan e terdes tempo pra aprender.",
    u"Tentai outra vez."
  ]
  response = random.choice(responses)
  return {
    'status': True,
    'type': args['command_type'],
    'response': response,
    'debug': 'adubei',
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

