# vim:fileencoding=utf-8
#    Plugin hash para matebot: retorna message digest / secure hash de um texto em um determinado algoritmo
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

## Documentação do hashlib - https://docs.python.org/3/library/hashlib.html

import hashlib

def hash(info_dict, bot_dict, addr_dict, command_list, command_type):
  algo = command_list[0].lower()
  text = str(command_list[1:])
  lista = ', '.join(sorted(hashlib.algorithms_guaranteed)).lower()
  if len(command_list) > 1:
    try:
      if command_list[0].lower() in [testing.lower() for testing in hashlib.algorithms_guaranteed]:
        response = u"hash %s de %s:\n\n%s" % (algo, text, getattr(hashlib, algo, None)(text.encode('utf-8')).hexdigest())
      else:
        response = u'Desculpe, estou rodando em um servidor sem suporte para \'%s\', ou \'%s\' não é um algoritmo.\n\nAlgoritmos suportados: %s' % (algo, algo, get_hashes())
      return {
        'status': True,
        'type': command_type,
        'response': response,
        'debug': u'hash bem sucedido',
        'multi': False,
      }
    except Exception as e:
      response = u'Erro tentando calcular o hash %s de %s.\n\nOs desenvolvedores vão ser notificados de qualquer forma. Mas tente novamente, por favor.\n\nAlgoritmos suportados: %s' % (algo, text, get_hashes())
      return {
        'status': False,
        'type': 'erro',
        'response': response,
        'debug': u'hash falhou\nExceção: %s' % (e),
        'multi': False,
      }
  else:
    response = u'Vossa excelência está tentando usar o bot de uma maneira incorreta, errada, equivocada. Vamos tentar novamente?\n\nA sintaxe deve ser exatamente assim:\n\n/hash (algoritmo) (mensagem)\n\nExemplo: /hash md5 Agora sim eu aprendi a usar o comando\n\nOutro exemplo: /hash sha256 MinhaSenhaSecreta1234\n\nAlgoritmos disponíveis: %s' % (lista)
    return {
      'status': False,
      'type': 'erro',
      'response': response,
      'debug': u'hash falhou, erro do usuário',
      'multi': False,
    }


