# vim:fileencoding=utf-8
#  Plugin hash para matebot: retorna message digest / secure hash de um texto 
#   em um determinado algoritmo
#  Copyleft (C) 2016-2020 Iuri Guilherme, 2017-2020 Matehackers,
#    2018-2019 Velivery, 2019 Greatful, 2019-2020 Fábrica do Futuro
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

## Documentação do hashlib - https://docs.python.org/3/library/hashlib.html

import hashlib

from aiogram.utils.markdown import escape_md

def cmd_hash(args):
  type = 'nada'
  response = u"Que hash? De que algoritmo?"
  debug = u"Não consegui fazer o hash"
  parse_mode = None
  try:
    lista = ', '.join(sorted(hashlib.algorithms_guaranteed)).lower()
    if len(args['command_list']) > 1:
      try:
        algo = args['command_list'][0].lower()
        text = ' '.join(args['command_list'][1:]).encode('utf-8')
        if algo in [testing.lower() for testing in hashlib.algorithms_guaranteed]:
          response = u"`%s`" % getattr(hashlib, algo, None)(text).hexdigest()
          parse_mode = 'MarkdownV2'
        else:
          response = u"Desculpe, estou rodando em um servidor sem suporte para '%s', ou '%s' não é um algoritmo.\n\nAlgoritmos suportados: %s" % (algo, algo, lista)
        return {
          'status': True,
          'type': args['command_type'],
          'response': response,
          'debug': u"hash bem sucedido",
          'multi': False,
          'parse_mode' : parse_mode,
          'reply_to_message_id': args['message_id'],
        }
      except Exception as e:
        type = 'erro'
        response = u"Erro tentando calcular o hash %s de '%s'.\n\nOs desenvolvedores vão ser notificados de qualquer forma. Mas tente novamente, por favor.\n\nAlgoritmos suportados: %s" % (algo, ' '.join(args['command_list'][1:]), lista)
        debug = u"hash falhou\nExceção: %s" % (e)
    else:
      type = 'erro'
      response = u"Vossa excelência está tentando usar o bot de uma maneira incorreta, errada, equivocada. Vamos tentar novamente?\n\nA sintaxe deve ser exatamente assim:\n\n/hash (algoritmo) (mensagem)\n\nExemplo: /hash md5 Agora sim eu aprendi a usar o comando\n\nOutro exemplo: /hash sha256 MinhaSenhaSecreta1234\n\nAlgoritmos disponíveis: %s" % (lista)
      debug = u"hash falhou, erro do usuário"
  except Exception as e:
    type = 'erro'
    response = u"Erro tentando calcular hash.\n\nOs desenvolvedores vão ser notificados de qualquer forma. Quem estragou o plugin será responsabilizado."
    debug = u"hash falhou\nExceção: %s" % (e)
  return {
    'status': False,
    'type': type,
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': parse_mode,
    'reply_to_message_id': args['message_id'],
  }

## TODO apagar todos lugares onde isto e' utilizado e remover
def inner_hash(algo, text):
  return getattr(hashlib, algo, None)(text.encode('utf-8')).hexdigest()

## Aiogram
def add_handlers(dispatcher):
  from matebot.aio_matebot.controllers.callbacks import (
    command_callback,
    error_callback,
    message_callback,
  )
  
  ## Gera hashes a partir de texto
  @dispatcher.message_handler(
    commands = ['hash'],
  )
  async def hash_callback(message):
    await message_callback(message, ['hash', message.chat.type])
    ## lol
    try:
      hashes = cmd_hash({
        'command_type': None,
        'message_id': None,
        'command_list': message.get_args().split(),
        'parse_mode': None,
      })
      command = await message.reply(
        u"{}".format(hashes['response']),
        parse_mode = hashes['parse_mode'],
      )
    except Exception as exception:
      await error_callback(message, exception, ['hash'])
      command = await message.reply(u"""Não consegui calcular o hash por proble\
mas técnicos. Os (ir)responsáveis serão avisados...""")
    await command_callback(command, ['hash', message.chat.type])
