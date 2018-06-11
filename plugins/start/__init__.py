# vim:fileencoding=utf-8
#    Plugin start para matebot: Payload feio e ruim
#    Copyleft (C) 2018 Desobediente Civil, Matehackers, Velivery

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

import hashlib

def start(info_dict, bot_dict, addr_dict, command_list, command_type):
  if not (len(command_list) > 0):
    response = u'Este bot por enquanto só serve para criar qrcodes e calcular hashes. Use o comando /qr\nExemplo de comando para gerar um qr code para o site do Matehackers: /qr %s\n\nPara gerar um hash de qualquer texto, use o comando /hash\nExemplo: /hash md5 matehackers\n\nAlgoritmos disponíveis: %s\n\nPara enviar sugestões, elogios ou vilipêndios, digite /feedback seguido do texto a ser enviado para nós.\n\nPara ajudar o hackerspace a se manter, use o comando /doar\n\nO código fonte deste bot está em %s\n\nMatehackers no telegram: %s' % (info_dict['website'], ', '.join(sorted(hashlib.algorithms_guaranteed)).lower(), info_dict['code_repository'], info_dict['telegram_group'])
    return {
      'status': True,
      'type': command_type,
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
      'response': command_list,
      'debug': u'comando',
      'multi': False,
    }

