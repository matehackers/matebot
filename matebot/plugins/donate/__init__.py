# vim:fileencoding=utf-8
#  Plugin donate para matebot: Indica formas de receber doações
#  Copyleft (C) 2016-2020 Iuri Guilherme, 2017-2020 Matehackers, 
#     2018-2019 Velivery, 2019 Greatful, 2019-2020 Fábrica do Futuro
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

def cmd_doar(args):
  return {
    'status': True,
    'type': args['command_type'],
    'response': u"Página no site do Matehackers com todas as opções \
      atualizadas para ajudar a manter o hackerspace: \
      https://matehackers.org/renda\n\nLinks para doar em bitcoins (use o que \
      funcionar no teu dispositivo):\
      \nbitcoin:%s\nhttps://blockchain.info/payment_request?address=%s&message=\
      https://matehackers.org/renda\nhttps://blockchainbdgpzk.onion/payment_req\
      uest?address=%s&message=https://matehackers.org/renda\n\nOutros métodos \
      de doação:\nhttps://apoia.se/matehackers\n" % (
        args['config']['info']['donate']['btc'],
        args['config']['info']['donate']['btc'],
        args['config']['info']['donate']['btc'],
      ),
    'debug': "doar",
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

