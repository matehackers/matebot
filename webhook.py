#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Matebot
#  
#  Copyleft 2012-2020 Iuri Guilherme <https://github.com/iuriguilherme>,
#     Matehackers <https://github.com/matehackers>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import logging
import ssl
import sys
import proxy
from proxy.common import pki
from proxy.plugin import RedirectToCustomServerPlugin

import tornado.ioloop
import maproxy.proxyserver

logging.basicConfig(level=logging.DEBUG)

ca_crt_file = "instance/matebotca.pem"
ca_key_file = "instance/matebotca.key"
csr_file = "instance/matebot.csr"
crt_file = "instance/matebot.pem"
key_file = "instance/matebot.key"
password = "password"

class MateBotRedirectToCustomServerPlugin(RedirectToCustomServerPlugin):
  def __init__(self, upstream, *args, **kwargs):
    self.UPSTREAM_SERVER = upstream
    super().__init__(*args, **kwargs)

if __name__ == '__main__':
  bot = 'matebot'
  host = 'localhost.localdomain' # Não vai funcionar!
  upstream = None
  config = None
  try:
    from instance.config import Config
    config = Config()
    if len(sys.argv) > 1:
      bot = sys.argv[1]
    if config.bots.get(bot, None) is None:
      logging.warning(u"""Não existe bot de nome {} no arquivo de configuração!\
Usando 'matebot'...""".format(str(bot)))
      bot = 'matebot'
  except Exception as e:
    logging.warning(u"""Arquivo de configuração não encontrado ou mal formado. \
Leia o manual.\n{0}""".format(repr(e)))
    raise
  try:
    host = config.bots[bot]['telegram']['webhook']['host']
    port = config.bots[bot]['telegram']['webhook']['port']
    upstream = ':'.join([host, str(port)])
    localhost = config.bots[bot]['telegram']['webhook']['localhost']
    localport = config.bots[bot]['telegram']['webhook']['localport']
  except Exception as e:
    logging.warning(u"""Opção não encontrada no arquivo de configuração.\n{0}
""".format(repr(e)))
    raise
  try:
    # ~ if not pki.gen_private_key(
      # ~ key_path = ca_key_file,
      # ~ password = password,
      # ~ bits = 2048,
      # ~ timeout = 10,
    # ~ ):
      # ~ logging.debug(u"Não foi possível gerar a chave privada de CA.")
    # ~ if not pki.gen_public_key(
      # ~ public_key_path = ca_crt_file,
      # ~ private_key_path = ca_key_file,
      # ~ private_key_password = password,
      # ~ subject = """/C=BR/ST=Rio Grande do Sul/L=Porto Alegre/O=Matehackers/CN={\
# ~ }""".format(host),
      # ~ validity_in_days = 365,
      # ~ timeout = 10,
    # ~ ):
      # ~ logging.debug(u"Não foi possível gerar a chave pública de CA.")

    # ~ if not pki.gen_csr(
      # ~ csr_path = csr_file,
      # ~ key_path = ca_key_file,
      # ~ password = password,
      # ~ crt_path = crt_file,
      # ~ timeout = 10,
    # ~ ):
      # ~ logging.debug(u"Não foi possível gerar a CSR.")
    # ~ if not pki.sign_csr(
      # ~ csr_path = csr_file,
      # ~ crt_path = crt_file,
      # ~ ca_key_path = ca_key_file,
      # ~ ca_key_password = password,
      # ~ ca_crt_path = ca_crt_file,
      # ~ serial = password,
      # ~ alt_subj_names = None,
      # ~ extended_key_usage = None,
      # ~ validity_in_days = 365,
      # ~ timeout = 10,
    # ~ ):
      # ~ logging.debug(u"Não foi possível assinar a CSR.")

    # ~ if not pki.remove_passphrase(
      # ~ key_in_path = ca_key_file,
      # ~ password = password,
      # ~ key_out_path = ca_key_file,
      # ~ timeout = 10,
    # ~ ):
      # ~ logging.debug(u"Não foi possível remover a senha da chave privada de CA.")

    if not pki.gen_private_key(
      key_path = key_file,
      password = password,
      bits = 2048,
      timeout = 10,
    ):
      logging.debug(u"Não foi possível gerar a chave privada.")
    if not pki.gen_public_key(
      public_key_path = crt_file,
      private_key_path = key_file,
      private_key_password = password,
      subject = """/C=BR/ST=Rio Grande do Sul/L=Porto Alegre/O=Matehackers/CN={\
}""".format(host),
      validity_in_days = 365,
      timeout = 10,
    ):
      logging.debug(u"Não foi possível gerar a chave pública.")
    if not pki.remove_passphrase(
      key_in_path = key_file,
      password = password,
      key_out_path = key_file,
      timeout = 10,
    ):
      logging.debug(u"Não foi possível remover a senha da chave privada.")

    # ~ proxy.main([
      # ~ '--enable-web-server',
      # ~ '--plugins', 'proxy.plugin.WebServerPlugin',
      # ~ '--plugins', 'proxy.plugin.ReverseProxyPlugin',
      # ~ '--hostname', '0.0.0.0', #'::1',
      # ~ '--port', '8443',
      # ~ '--cert-file', 'instance/matebot.pem',
      # ~ '--key-file', 'instance/matebot.key',
    # ~ ])

    # HTTPS->HTTP
    ssl_options = {
      'certfile':  crt_file,
      'keyfile': key_file,
      # ~ 'ca_certs': ca_crt_file,
      # ~ 'ssl_version': ssl.PROTOCOL_TLS,
      # ~ 'ssl_version': ssl.PROTOCOL_TLS_CLIENT,
      # ~ 'ssl_version': ssl.PROTOCOL_TLS_SERVER,
      # ~ 'server_hostname': host,
      # ~ 'server_side': True,
    }
    # "client_ssl_options=ssl_certs" simply means "listen using SSL"
    server = maproxy.proxyserver.ProxyServer(
      localhost,
      localport,
      client_ssl_options = ssl_options,
      server_ssl_options = dict(ssl_options.copy(), server_hostname = host),
    )
    server.listen(port)
    logging.info(u"""Iniciando proxy reverso em https://0.0.0.0:{1} -> http://{\
2}:{3}""".format(
      host,
      port,
      localhost,
      localport,
    ))
    tornado.ioloop.IOLoop.instance().start()

  except Exception as e:
    logging.debug(repr(e))
    raise
