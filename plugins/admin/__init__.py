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

def teste(info_dict, bot_dict, addr_dict, command_list):
  return {
    'status': True,
    'type': 'mensagem',
    'response': str(command_list),
    'debug': u'teste',
    'multi': False,
  }

def enviar(info_dict, bot_dict, addr_dict, command_list):
  try:
    if len(command_list) > 1:
      if command_list[0].isdigit():
        telegram_id = command_list[0]
        mensagem = ' '.join(command_list[1::1])
        return {
          'status': True,
          'type': 'whisper',
          'response': mensagem,
          'to_id': telegram_id,
          'debug': u'Sucesso enviando %s para %s' % (mensagem, telegram_id),
          'multi': False,
        }
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'response': u'Erro tentando enviar %s para %s.' % (mensagem, telegram_id),
      'debug': u'Erro enviando %s para %s.\nExceção: %s' % (mensagem, telegram_id, e),
      'multi': False,
    }
  return {
    'status': False,
    'type': 'erro',
    'response': u'Vossa Excelência está usando este comando de forma incorreta. Este comando tem um jeito certo e tem que usar o comando do jeito certo. E eu não vou deixar ninguém usar do jeito errado.\n\nExplicar-vos-ei o uso correto, certo do comando: /enviar 1 mensagem\nOnde 1 é o número do telegram_id do alvo e `mensagem` é a mensagem.',
    'debug': u'Erro enviando %s para %s.',
    'multi': False,
  }

