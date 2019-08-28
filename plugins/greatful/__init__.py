# vim:fileencoding=utf-8
#  Plugin greatful para matebot: Comandos para Greatful
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

import datetime, pytz
from babel.dates import format_timedelta

## Agenda hebdomadária
from plugins.greatful.semana import hoje as cmd_hoje, semana as cmd_semana

## Ponto Greatful
from plugins.greatful.chegreat import cheguei as cmd_cheguei, vazei as cmd_vazei, adubei as cmd_adubei
## Aliases
def cmd_fertilizei(args):
  return cmd_adubei(args)
def cmd_larguei(args):
  return cmd_vazei(args)
def cmd_fui(args):
  return cmd_vazei(args)
def cmd_chegreat(args):
  return cmd_cheguei(args)

## Atividades paralelas
from plugins.greatful.atividade import agua as cmd_agua, cafe as cmd_cafe, reguei as cmd_reguei
## Aliases
def cmd_água(args):
  return cmd_agua(args)
def cmd_bebi(args):
  return cmd_agua(args)
def cmd_café(args):
  return cmd_cafe(args)
def cmd_petróleo(args):
  return cmd_cafe(args)
def cmd_molhei(args):
  return cmd_reguei(args)

def cmd_g(args):
  return {
    'status': True,
    'type': args['command_type'],
    'response': u"Great!",
    'debug': 'g',
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Que great horas são
def cmd_agora(args):
  ## Momento da reunião com o BenHur e o Iuri no banco da Redenção
  ## Ano 2019, mês março, dia 22, hora 11 do calendário Gregoriano
  ## Na timezone America/SaoPaulo, horário de Brasília, UTC-3
  great_epoch = 1553263200
  great_delta =  datetime.datetime.now(pytz.timezone('America/Sao_Paulo')) - datetime.datetime.fromtimestamp(great_epoch, pytz.timezone('America/Sao_Paulo'))
  anos,resto = divmod(great_delta.days, 356)
  meses,dias = divmod(resto, 30)
  horas,resto = divmod(great_delta.seconds, 3600)
  minutos,segundos = divmod(resto, 60)
#  great_time = format_timedelta(great_delta, granularity='minute', threshold=1, add_direction=False, format='long', locale='pt_BR')
  return {
    'status': True,
    'type': args['command_type'],
#    'response': u"Se passaram %s desde Greatful" % (great_time),
    'response': u"%s/%s/%s, %s:%s:%s desde Greatful" % ("{:02d}".format(dias), "{:02d}".format(meses), "{:04d}".format(anos), "{:02d}".format(horas), "{:02d}".format(minutos), "{:02d}".format(segundos)),
    'debug': 'agora',
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

