# vim:fileencoding=utf-8
#    Plugin velivery_bikeentregas para matebot: Gerencia entregas de Bike pelo
#    Velivery
#    Copyleft (C) 2018 Desobediente Civil, Velivery

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

### Imports
import requests

def address_latlng(args):
  requisicao_geocode = dict()
  requisicao_geocode.update(url = str(args['config']['velivery_bikeentregas']['geocode_url']))
  requisicao_geocode.update(url = requisicao_geocode['url'] + "json")
  requisicao_geocode.update(url = requisicao_geocode['url'] + "?")
  requisicao_geocode['data'] = dict()
  requisicao_geocode['data'].update(key = str(args['config']['velivery_bikeentregas']['geocode_key']))
  requisicao_geocode['data'].update(address = args['geocode_address'])
  request_geocode = requests.get(requisicao_geocode['url'], params = requisicao_geocode['data'])
  if request_geocode.json()['status']:
    ## TODO Debug
#    print(request_geocode.json())
    return {
      'status': request_geocode.json()['status'],
      'type': args['command_type'],
      'multi': False,
      'destino': 'telegram',
      'response': u"Ŝucesso!",
      'debug': u"Sucesso!",
      'parse_mode': None,
      'location': request_geocode.json()['results'][0]['geometry']['location'],
    }
  else:
    return {
      'status': request_geocode.json()['status'],
      'type': args['command_type'],
      'multi': False,
      'destino': 'telegram',
      'response': u"Falhou tentando buscar coordenadas: %s" % (str(request_geocode.json())),
      'debug': u"Falhou tentando buscar coordenadas: %s" % (str(request_geocode.json())),
      'parse_mode': None,
    }

