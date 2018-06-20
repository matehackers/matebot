# vim:fileencoding=utf-8
#    Plugin admin para matebot: Plugin de administração
#    Copyleft (C) 2018 Desobediente Civil, Matehackers

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

def teste(args):
  return {
    'status': True,
    'type': 'mensagem',
    'response': str(args['command_list']),
    'debug': u'teste',
  }

def enviar(args):
  try:
    if len(args['command_list']) > 1:
      if args['command_list'][0].isdigit():
        telegram_id = args['command_list'][0]
        mensagem = ' '.join(args['command_list'][1::1])
        return {
          'status': True,
          'type': 'whisper',
          'response': mensagem,
          'to_id': telegram_id,
          'debug': u'Sucesso enviando %s para %s' % (mensagem, telegram_id),
        }
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'response': u'Erro tentando enviar mensagem.',
      'debug': u'Erro enviando mensagem.\nExceção: %s' % (e),
    }
  return {
    'status': False,
    'type': 'erro',
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /enviar 1 mensagem\nOnde 1 é o número do telegram_id do alvo e `mensagem` é a mensagem.',
    'debug': u'Erro enviando mensagem.',
  }

