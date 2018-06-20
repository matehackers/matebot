# vim:fileencoding=utf-8
#    Plugin telegram para matebot: Comandos padrão de bots de telegram
#    Copyleft (C) 2016-2018 Desobediente Civil, Matehackers

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

def help(args):
  response = u'Meu nome é Vegga'
  return {
    'status': True,
    'type': args['command_type'],
    'response': response,
    'debug': 'help',
    'multi': False,
  }

