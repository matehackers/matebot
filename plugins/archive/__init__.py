# vim:fileencoding=utf-8
#    Plugin archive para matebot: Salva URL na Wayback Machine.
#    Copyleft (C) 2019 Desobediente Civil, Matehackers

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

import requests

def cmd_a(args):
  wayback_machine_url = 'https://web.archive.org'
  try:
    requisicao = requests.get('/'.join([wayback_machine_url, 'save', ''.join(args['command_list'])]))
    if requisicao:
      response = u"Página salva com sucesso: %s" % (''.join([wayback_machine_url, requisicao.headers['Content-Location']]))
      debug = u"[#waybackmachine]: %s %s" % (str(requisicao), str(requisicao.headers))
    else:
      response = u"Não consegui salvar a página, erro: %s" % (requisicao.headers['X-Archive-Wayback-Runtime-Error'])
      debug = u"[#waybackmachine]: %s %s" % (str(requisicao), str(requisicao.headers))
    return {
      'status': True,
      'type': args['command_type'],
      'response': response,
      'debug': debug,
      'multi': False,
      'parse_mode': None,
    }
  except Exception as e:
    raise
    response = u"Não consegui salvar a página por problemas técnicos. Os desenvolvedores devem ter sido avisados já, eu acho."
    debug = u"[#waybackmachine]: [exception] %s" % (e)
  return {
    'status': False,
    'type': 'erro',
    'response':  response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
  }

## Aliases
def cmd_salvar(args):
  return a(args)
def cmd_arquivar(args):
  return a(args)
def cmd_arquivo(args):
  return a(args)
def cmd_wm(args):
  return a(args)

