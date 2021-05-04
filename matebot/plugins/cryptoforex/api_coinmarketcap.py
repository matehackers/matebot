# vim:fileencoding=utf-8
#  Plugin cryptoforex para matebot: Comandos para conversão de criptomoedas
#  Copyleft (C) 2016-2021 Iuri Guilherme, 2017-2021 Matehackers,
#    2018-2019 Velivery, 2019 Greatful, 2019-2021 Fábrica do Futuro
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

from matebot.aio_matebot.controllers.callbacks import (
    exception_callback,
)

## https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesLatest
async def price_v1(token, coin, converts):
    # This example uses Python 2.7 and the python-request library.

    from requests import Request, Session
    from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
    import json

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    parameters = {
        'symbol': coin,
        'aux': ','.join(['is_fiat', 'volume_7d',
                         'volume_30d', 'circulating_supply', 'total_supply']),
        # 'convert': ','.join(converts)
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': token,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        await exception_callback(e, ['cryptoforex', 'coinmarketcap', 'price',
                                     'price_v1'])
        raise
