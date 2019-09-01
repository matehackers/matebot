# vim:fileencoding=utf-8
#  Plugin start para matebot: Payload feio e ruim
#  Copyleft (C) 2018-2019 Desobediente Civil, 2018-2019 Matehackers,
#    2018-2019 Velivery, 2019 Greatful
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

def start(args):
  if not (len(args['command_list']) > 0):
    response = u'Meu nome é Vegga'
    return {
      'status': True,
      'type': args['command_type'],
      'response': response,
      'debug': u'start',
      'multi': False,
    }
  else:
    # TODO deixei o trabalho pela metade devido a estafa, abortar missão e usar inline. https://core.telegram.org/bots/api#replykeyboardmarkup ass: @desci
#    response = ''.join(command_list).split('_')
#    print(response)
    return {
      'status': True,
      'type': 'comando',
      'response': u'Isto não está implementado!',
      'debug': u'comando',
      'multi': False,
    }

