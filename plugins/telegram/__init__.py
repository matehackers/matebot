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

import hashlib

def start(args):
  response = u'Este bot por enquanto só serve para criar qrcodes e calcular hashes. Use o comando /qr\nExemplo de comando para gerar um qr code para o site do Matehackers: /qr %s\n\nPara gerar um hash de qualquer texto, use o comando /hash\nExemplo: /hash md5 matehackers\n\nAlgoritmos disponíveis: %s\n\nPara enviar sugestões, elogios ou vilipêndios, digite /feedback seguido do texto a ser enviado para nós.\n\nPara ajudar o hackerspace a se manter, use o comando /doar\n\nO código fonte deste bot está em %s\n\nMatehackers no telegram: %s' % (args['info_dict']['website'], ', '.join(sorted(hashlib.algorithms_guaranteed)).lower(), args['info_dict']['code_repository'], args['info_dict']['telegram_group'])
  return {
    'status': True,
    'type': 'mensagem',
    'response': response,
    'debug': 'start',
  }

def help(args):
  response = u'Este bot por enquanto só serve para criar qrcodes e calcular hashes. Use o comando /qr\nExemplo de comando para gerar um qr code para o site do Matehackers: /qr %s\n\nPara gerar um hash de qualquer texto, use o comando /hash\nExemplo: /hash md5 matehackers\n\nAlgoritmos disponíveis: %s\n\nPara enviar sugestões, elogios ou vilipêndios, digite /feedback seguido do texto a ser enviado para nós.\n\nPara ajudar o hackerspace a se manter, use o comando /doar\n\nO código fonte deste bot está em %s\n\nMatehackers no telegram: %s' % (args['info_dict']['website'], ', '.join(sorted(hashlib.algorithms_guaranteed)).lower(), args['info_dict']['code_repository'], args['info_dict']['telegram_group'])
  return {
    'status': True,
    'type': 'mensagem',
    'response': response,
    'debug': 'help',
  }

