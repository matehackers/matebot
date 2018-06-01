# vim:fileencoding=utf-8
#    Plugin donate para matebot: Indica formas de receber doações
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

def doar(info_dict, bot_dict, addr_dict, command_list):
  response = u'Página no site do Matehackers com todas as opções atualizadas para ajudar a manter o hackerspace: https://matehackers.org/renda\n\nLinks para doar em bitcoins (use o que funcionar no teu dispositivo):\nbitcoin:%s\nhttps://blockchain.info/payment_request?address=%s&message=https://matehackers.org/renda\nhttps://blockchainbdgpzk.onion/payment_request?address=%s&message=https://matehackers.org/renda\n\nOutros métodos de doação:\nhttps://apoia.se/matehackers\n' % (addr_dict['btc'], addr_dict['btc'], addr_dict['btc'])
  return {
    'status': True,
    'type': 'mensagem',
    'response': response,
    'debug': 'doar',
  }
