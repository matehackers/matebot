# vim:fileencoding=utf-8
#  Plugin cryptoforex para matebot: Comandos para conversão de 
#   criptomoedas
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

import datetime, locale, logging
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

from matebot.aio_matebot.controllers.callbacks import (
    command_callback,
    error_callback,
    message_callback,
)

from matebot.plugins.cryptoforex.api_coinmarketcap import price_v1\
    as coinmarketcap_price

async def price(dispatcher, message, converts, comando):
    # Presumindo bitcoin quando não há argumentos
    moeda = "BTC"
    if message.get_args() != "":
        moeda = message.get_args()
    ## TODO verificar se a moeda existe
    try:
        resposta = await coinmarketcap_price(
            dispatcher.bot.info['coinmarketcap_token'], moeda, converts)
        logging.info(resposta)
        logging.info(type(resposta))
        if resposta['status']['error_code'] > 0:
            await error_callback(resposta['status']['error_message'],
                                 message, None,
                                 ['cryptoforex', 'coinmarketcap', 'price'])
            await message.reply(u"""Erro tentando calcular preço. O pessoa\
l que cuida do desenvolvimento já foi avisado, eu acho. Verifique se a moeda e\
xiste e o símbolo está correto (por exemplo BTC, LTC, ETH)...""")
        else:
            text = """
Price information for {nome} (from coinmarketcap.com)

Price of 1 {simbolo} at {data}:
U$$ {preco_dolar} USD

Marketcap: U$$ {marketcap}

Price change since last
hour: {variacao_1h}%
day: {variacao_1d}%
week: {variacao_1s}%
month: {variacao_1m}%
two months: {variacao_2m}%
three months: {variacao_3m}%

Last 24 hours volume: U$$ {volume_1d}
Last week volume: U$$ {volume_1s}
Last month volume: U$$ {volume_1m}

Available supply: {oferta} {simbolo}
Total supply: {oferta_total} {simbolo}
""".format(
                nome = resposta['data'][moeda]['name'],
                # '2021-05-03T22:52:02.000Z'
                data = datetime.datetime.strptime(
                    resposta['data'][moeda]['last_updated'],
                    '%Y-%m-%dT%H:%M:%S.000Z').strftime('%c'),
                marketcap = '{:,.2f}'.format(float(
                    resposta['data'][moeda]['quote']['USD']['market_cap'])),
                simbolo = resposta['data'][moeda]['symbol'],
                preco_dolar = '{:,.2f}'.format(float(
                    resposta['data'][moeda]['quote']['USD']['price'])),
                ## FIXME converter pra euro e real
                ## tem que pagar um plano mais caro da api da coinmarketcap
                ## e usar o parâmetro convert com EUR,BRL,BTC
                preco_euro='{:,.2f}'.format(
                    resposta['data'][moeda]['quote']['USD']['price']),
                preco_real='{:,.2f}'.format(
                    resposta['data'][moeda]['quote']['USD']['price']),
                preco_btc='{:,.8f}'.format(
                    resposta['data'][moeda]['quote']['USD']['price']),
                variacao_1h='{:,.2f}'.format(
                    resposta['data'][moeda]['quote']['USD'][
                        'percent_change_1h']),
                variacao_1d='{:,.2f}'.format(
                    resposta['data'][moeda]['quote']['USD'][
                        'percent_change_24h']),
                variacao_1s='{:,.2f}'.format(
                    resposta['data'][moeda]['quote']['USD'][
                        'percent_change_7d']),
                variacao_1m='{:,.2f}'.format(
                    resposta['data'][moeda]['quote']['USD'][
                        'percent_change_30d']),
                variacao_2m='{:,.2f}'.format(
                    resposta['data'][moeda]['quote']['USD'][
                        'percent_change_60d']),
                variacao_3m='{:,.2f}'.format(
                    resposta['data'][moeda]['quote']['USD'][
                        'percent_change_90d']),
                volume_1d='{:,.2f}'.format(
                    resposta['data'][moeda]['quote']['USD']['volume_24h']),
                volume_1s='{:,.2f}'.format(
                    resposta['data'][moeda]['quote']['USD']['volume_7d']),
                volume_1m='{:,.2f}'.format(
                    resposta['data'][moeda]['quote']['USD']['volume_30d']),
                oferta='{:,.8f}'.format(
                    resposta['data'][moeda]['circulating_supply']),
                oferta_total='{:,.8f}'.format(
                    resposta['data'][moeda]['total_supply']),
            )
            command = await message.reply(text)
            await command_callback(command, [comando, message.chat.type])
    except Exception as exception:
        await error_callback(u"Erro contatando coinmarketcap.com", message,
                             exception, ['cryptoforex', 'price'])
        await message.reply(u"""Erro tentando calcular preço. O pessoal qu\
    e cuida do desenvolvimento já foi avisado, eu acho...""")

## Aiogram
async def add_handlers(dispatcher):
    ## Lista o "preço" atual da criptomoeda
    @dispatcher.message_handler(
        commands=['price', 'p'],
    )
    async def price_callback(message):
        await message_callback(message, ['price', message.chat.type])
        await price(dispatcher, message, 'USD', 'price')

    # ## Dados de exchanges brasileiras
    # @dispatcher.message_handler(
    #     commands=['preco'],
    # )
    # async def preco_callback(message):
    #     await message_callback(message, ['preco', message.chat.type])
    #     await price(dispatcher, message, 'BRL', 'preco')
#         moeda = message.get_args()[1]
#         ## FIXME
#         response = [
#             '',
#             {
#                 'ticker': {
#                     'last': 1.0,
#                     'high': 1.0,
#                     'low': 1.0,
#                     'vol': 1.0,
#                     'buy': 1.0,
#                     'sell': 1.0,
#                 },
#             },
#         ]
#         texto = list()
#         texto.append('Informação das ultimas 24 horas para %s (de mercadobitco\
# in.com.br)' % (str(moeda)))
#         texto.append('\nValor')
#         texto.append('atual: R$ %s' % (
#             '{:,.2f}'.format(float(response[1]['ticker']['last']))))
#         texto.append('maior: R$ %s' % (
#             '{:,.2f}'.format(float(response[1]['ticker']['high']))))
#         texto.append('menor: R$ %s' % (
#             '{:,.2f}'.format(float(response[1]['ticker']['low']))))
#         texto.append('\nVolume: %s BTC' % (
#             '{:,.8f}'.format(float(response[1]['ticker']['vol']))))
#         texto.append('\nMaior oferta de')
#         texto.append('compra: R$ %s' % (
#             '{:,.2f}'.format(float(response[1]['ticker']['buy']))))
#         texto.append('venda: R$ %s' % (
#             '{:,.2f}'.format(float(response[1]['ticker']['sell']))))
#         command = await message.reply(texto)
#         await command_callback(command, ['preco', message.chat.type])

    ## Converte valores entre moedas (criptomoeda ou fiduciário)

    async def conv_erro(message):
        await message.reply("""Command not yet implemented, check curre\
nt status at @matebotnews""")
        # ~ await message.reply("""
# ~ Command usage: /{comando} 1 BTC USD

# ~ Where 1 is the desired amount to convert, BTC is the crypto/fiat to convert FR\
# ~ OM and USD is the crypto/fiat to convert TO. In this example we convert one bi\
# ~ tcoin to american dollars, which is the same behaviour of the /price command.
# ~ """.format(comando = message.get_command()))
        await error_callback(
            # ~ "Usaram o comando de forma incorreta: {}".format(
            "Tentaram usar um comando que ainda não existe: {}".format(
                message.get_full_command()),
            message,
            None,
            ['cryptoforex', 'conv'],
        )

    @dispatcher.message_handler(
        commands=['conv', 'convert', 'converter', 'c'],
    )
    async def conv_callback(message):
        await message_callback(message, ['conv', message.chat.type])
        mensagem = message.get_args()
        await conv_erro(message)
        # ~ if mensagem:
            # ~ if len(mensagem) == 4:
                # ~ ## /conv 1 BTC BRL
                # ~ parametros = {
                    # ~ 'valor': mensagem[1],
                    # ~ 'de': mensagem[2],
                    # ~ 'para': mensagem[3],
                # ~ }
                # ~ try:
                    # ~ float(parametros['valor'])
                # ~ except ValueError:
                    # ~ await conv_erro(message)
                # ~ ## FIXME dados fictícios
                # ~ ## https://coinmarketcap.com/api/documentation/v1/#operation/getV1ToolsPriceconversion
                # ~ resposta_da_api = {
                    # ~ "data": {
                        # ~ "symbol": "BTC",
                        # ~ "id": "1",
                        # ~ "name": "Bitcoin",
                        # ~ "amount": 50,
                        # ~ "last_updated": "2018-06-06T08:04:36.000Z",
                        # ~ "quote": {
                            # ~ "GBP": {
                                # ~ "price": 284656.08465608465,
                                # ~ "last_updated": "2018-06-06T06:00:00.000Z"
                            # ~ },
                            # ~ "LTC": {
                                # ~ "price": 3128.7279766396537,
                                # ~ "last_updated": "2018-06-06T08:04:02.000Z"
                            # ~ },
                            # ~ "USD": {
                                # ~ "price": 381442,
                                # ~ "last_updated": "2018-06-06T08:06:51.968Z"
                            # ~ }
                        # ~ }
                    # ~ },
                    # ~ "status": {
                        # ~ "timestamp": "2021-04-27T05:57:31.757Z",
                        # ~ "error_code": 0,
                        # ~ "error_message": "",
                        # ~ "elapsed": 10,
                        # ~ "credit_count": 1
                    # ~ }
                # ~ }
                # ~ ## TODO formatar fiat de forma diferente - $ {:,.2f}
                # ~ resultado = """
# ~ (from coinmarketcap.com):",
# ~ {amount_from} {symbol_from} = {amount_to} {symbol_to}
# ~ """.format(
                    # ~ amount_from = '{:,.8f}'.format(
                        # ~ resposta_da_api['data']['amount']),
                    # ~ symbol_from = resposta_da_api['data']['symbol'],
                    # ~ amount_to = '{:,.8f}'.format(
                        # ~ resposta_da_api['data']['quote'][
                            # ~ parametros['para']]['price']),
                    # ~ symbol_to = parametros['para']
                # ~ )
                # ~ command = await message.reply(resultado)
                # ~ await command_callback(command, ['conv', message.chat.type])
            # ~ else:
                # ~ await conv_erro(message)
        # ~ else:
            # ~ await conv_erro(message)
