# vim:fileencoding=utf-8
#  Plugin mate-matica para matebot: Mate Mática
#  Copyleft (C) 2019-2020 Iuri Guilherme, 2019-2020 Matehackers,
#    2019 Velivery, 2019 Greatful, 2019-2020 Fábrica do Futuro
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
#  

import math, binascii, os

## π
def cmd_pi(args):
  try:
    tamanho = 51
    ## Eu não faço args['command_list'][0] pra evitar IndexError
    if ''.join(args['command_list']).isdigit():
      tamanho = int(''.join(args['command_list'])) + 2 ## Ignorar o '3.'
    constante = 4 * math.atan(1) ## Esta é uma boa aproximação de pi
    response = str(constante)[:tamanho]
    return {
      'status': True,
      'type': 'grupo',
      'response': response,
      'debug': u"pi calculado",
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  except Exception as e:
      return {
        'status': False,
        'type': 'erro',
        'response': u"Erro tentando calcular pi.",
        'debug': u"Pi falhou, exceção: %s" % (e),
        'multi': False,
        'parse_mode': None,
        'reply_to_message_id': args['message_id'],
      }

## φ
def cmd_phi(args):
  try:
    tamanho = 51
    ## Eu não faço args['command_list'][0] pra evitar IndexError
    if ''.join(args['command_list']).isdigit():
      tamanho = int(''.join(args['command_list'])) + 2 ## Ignorar o '1.'
    constante = ( 1 + math.sqrt(5) ) / 2 ## Esta é uma boa aproximação de phi
    response = str(constante)[:tamanho]
    return {
      'status': True,
      'type': 'grupo',
      'response': response,
      'debug': u"phi calculado",
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  except Exception as e:
      return {
        'status': False,
        'type': 'erro',
        'response': u"Erro tentando calcular phi.",
        'debug': u"Phi falhou, exceção: %s" % (e),
        'multi': False,
        'parse_mode': None,
        'reply_to_message_id': args['message_id'],
      }

## String hexadecimal suficientemente aleatória
def cmd_random(args):
  try:
    tamanho = 8
    response = list()
    ## Eu não faço args['command_list'][0] pra evitar IndexError
    ## Mas tem outras formas de testar isto, ler o manual do dict()
    argumento = ''.join(args['command_list'])
    if argumento:
      if argumento.isdigit() and int(argumento) <= 872 and int(argumento) > 2:
        tamanho = int(argumento)
      else:
        response.append(u"Tamanho deve ser entre 1 e 872, %s não serve! Revertendo para %s...\n" % (str(argumento), str(tamanho)))
    aleatorio = os.urandom(tamanho)
    response.append(u"<b>HEX</b>:\n<pre>%s</pre>\n" % binascii.hexlify(aleatorio).decode('utf-8'))
    response.append(u"<b>B64</b>:\n<pre>%s</pre>" % binascii.b2a_base64(aleatorio).decode('utf-8'))
    response.append(u"<b>HQX</b>:\n<pre>%s</pre>" % binascii.b2a_hqx(binascii.rlecode_hqx(aleatorio)).decode('utf-8'))
    return {
      'status': True,
      'type': 'grupo',
      'response': '\n'.join(response),
      'debug': u"Número aleatório gerado",
      'multi': False,
      'parse_mode': 'HTML',
      'reply_to_message_id': args['message_id'],
    }
  except Exception as e:
    return {
      'status': False,
      'type': 'erro',
      'response': u"Erro tentando gerar número aleatório.",
      'debug': u"Random falhou, exceção: %s" % (e),
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }

def cmd_r(args):
  return cmd_random(args)

## Aiogram
def add_handlers(dispatcher):
  from matebot.aio_matebot.controllers.callbacks import (
    command_callback,
    error_callback,
    message_callback,
  )

  ## Gera números aleatórios
  @dispatcher.message_handler(
    commands = ['random', 'rand', 'r'],
  )
  async def random_callback(message):
    await message_callback(message, ['random', message.chat.type])
    ## lol
    r = cmd_r({
      'message_id': None,
      'command_list': message.get_args(),
    })
    command = await message.reply(
      u"{}".format(r['response']),
      parse_mode = r['parse_mode'],
    )
    await command_callback(command, ['random', message.chat.type])

  ## Uma boa aproximação de pi
  @dispatcher.message_handler(
    commands = ['pi'],
  )
  async def pi_callback(message):
    await message_callback(message, ['pi', message.chat.type])
    command = await message.reply(str(math.pi))
    await command_callback(command, ['pi', message.chat.type])

  ## Uma boa aproximação de φ
  @dispatcher.message_handler(
    commands = ['phi'],
  )
  async def phi_callback(message):
    await message_callback(message, ['phi', message.chat.type])
    command = await message.reply(
      str(( 1 + math.sqrt(5) ) / 2),
    )
    await command_callback(command, ['phi', message.chat.type])
