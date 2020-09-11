# vim:fileencoding=utf-8
#  Plugin telegram para matebot: Comandos padrão de bots de telegram
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

import hashlib

def cmd_start(args):
  response = u'Este bot por enquanto só serve para criar qrcodes e calcular \
    hashes. Use o comando /qr\nExemplo de comando para gerar um qr code para o \
    site do Matehackers: /qr %s\n\nPara gerar um hash de qualquer texto, use o \
    comando /hash\nExemplo: /hash md5 matehackers\n\nAlgoritmos disponíveis: \
    %s\n\nPara enviar sugestões, elogios ou vilipêndios, digite /feedback \
    seguido do texto a ser enviado para nós.\n\nPara ajudar o hackerspace a se \
    manter, use o comando /doar\n\nO código fonte deste bot está em %s\n\n\
    Matehackers no telegram: %s' % (
      args['config']['info']['website'],
      ', '.join(sorted(hashlib.algorithms_guaranteed)).lower(),
      args['config']['info']['repository'],
      args['config']['info']['group'],
    )
  return {
    'status': True,
    'type': args['command_type'],
    'response': response,
    'debug': 'start',
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

def cmd_help(args):
  return cmd_start(args)

def cmd_ajuda(args):
  response = list()
  response.append(u"Lista de comandos:")
  response.append(u"")
  # TODO acentuacao
  response.append(u"`/ajuda`\nSe estardes lendo este texto, entao nao e necessaria explanacao acerca deste comando")
  response.append(u"`/feedback <texto>`\nEnvia feedback para os desenvolvedores")
  response.append(u"`/qr <texto>`\nGera QR code a partir do texto fornecido")
  response.append(u"")
  # ~ response.append(u"Plugin Velivery Pedidos")
  # ~ response.append(u"`/pedido <id>`\nExibe descrição completa de um pedido (fornecer código)")
  # TODO acentuacao
  # ~ response.append(u"`/pedidos [limite]`\nListar todos os pedidos (limite padrao 3)")
  # ~ response.append(u"`/pendentes`\nListar pedidos pendentes (inclusive os agendados)")
  # ~ response.append(u"`/atrasados`\nListar pedidos atrasados que ainda não foram atendidos")
  # ~ response.append(u"")
  # ~ response.append(u"Plugin Totalvoice")
  # ~ response.append(u"`/ligar_1 <numero>`\nEnvia audio `shiva_1` para numero de telefone de estabelecimento")
  # ~ response.append(u"`/ligar_2 <numero>`\nEnvia audio `shiva_2` para numero de telefone de estabelecimento")
  # ~ response.append(u"`/ligar_3 <numero>`\nEnvia audio `shiva_3` para numero de telefone de estabelecimento")
  # ~ response.append(u"`/ligar_4 <numero>`\nEnvia audio `shiva_4` para numero de telefone de estabelecimento")
  # ~ response.append(u"")
  # ~ response.append(u"Plugin Bike Entregas")
  # TODO acentuacao
  # ~ response.append(u"`/husky_geo <endereco>`\nFornece coordenadas geograficas a partir de endereco (google maps api)")
  # ~ response.append(u"`/husky_pendentes`\nListar pedidos aceitos pelo estabelecimento que ainda não foram enviados para o gerenciador da Husky")
  # ~ response.append(u"`/husky_pedido <id>`\nEnvia pedido para a Husky (fornecer código)")
  # ~ response.append(u"`/husky_atendidos [id]`\nLista pedidos que já foram atendidos pela Husky, ou adiciona manualmente um pedido na lista")
  # TODO acentuacao
  # ~ response.append(u"")
  # ~ response.append(u"Plugin Velivery Relatorios")
  # ~ response.append(u"`/relatorio_recompra`\nExibe a taxa de recompra do Velivery")
  # ~ response.append(u"`/relatorio_recompra_total`\nExibe a taxa de recompra do Velivery de todo período e gera arquivo CSV")
  # ~ response.append(u"`/relatorio_recompra_ano <ano>`\nExibe a taxa de recompra do Velivery para o ano especificado e gera arquivo CSV")
  # ~ response.append(u"`/relatorio_vendas [ano] [mes]`\nExibe o total de vendas no Velivery total ou por periodo")
  # ~ response.append(u"`/relatorio_vendas_total`\nExibe o total de vendas no Velivery de todo período")
  # ~ response.append(u"`/relatorio_vendas_ano`\nExibe o total de vendas do Velivery para o ano especificado")
  # ~ response.append(u"`/relatorio_vendas_mes`\nExibe o total de vendas do Velivery para o mês e ano especificados")
  # ~ response.append(u"`/relatorio_usuarios`\nExibe informações sobre usuárias(os) do Velivery")
  # ~ response.append(u"`/relatorio_uf`\nExibe total de pedidos, usuárias(os) e usuárias(os) únicos por período")
  # ~ response.append(u"`/dados_estabelecimentos`\nExibe informações sobre estabelecimentos cadastrados no Velivery")
  # ~ response.append(u"`/exportar_280`\nCria arquivo csv com todos pedidos do Velivery")
  # TODO testar e descobri o que e
  # ~ response.append(u"")
  # ~ response.append(u"`/taxa_recompra`\nComando criado nao lembro pra que")
  # ~ response.append(u"`/relatorio_dre`\nComando criado nao lembro pra que")
  # ~ response.append(u"`/relatorio_ltv`\nComando criado nao lembro pra que")
  # ~ response.append(u"`/relatorio_recompra2`\nComando criado nao lembro pra que")
  # ~ response.append(u"`/relatorio_usuarios_unicos`\nComando criado nao lembro pra que")
  # ~ response.append(u"`/relatorio_usuarios_pedidos`\nComando criado nao lembro pra que")
  # ~ response.append(u"`/relatorio_vendas_2`\nComando criado nao lembro pra que")
  # ~ response.append(u"`/resumo_vendas_2`\nComando criado nao lembro pra que")
  # ~ response.append(u"`/mailing`\nComando criado nao lembro pra que")
  # ~ response.append(u"`/inativos`\nComando criado nao lembro pra que")
  # ~ response.append(u"`/veganweek`\nComando criado nao lembro pra que")
  # ~ response.append(u"`/vegcoinweek_cac`\nComando criado nao lembro pra que")
  ## TODO verificar se o markdown está funcionando
  return {
    'status': True,
    'type': args['command_type'],
    'response': "\n".join(response),
    'debug': 'ajuda',
    'multi': False,
    'parse_mode': 'Markdown',
    'reply_to_message_id': args['message_id'],
  }

## Aiogram
def add_handlers(dispatcher):
  from matebot.aio_matebot.controllers.callbacks import command_callback

  @dispatcher.message_handler(
    commands = ['start'],
  )
  async def start_callback(message):
    await command_callback(message, 'start')
    await message.reply(u"""Oi oi oi {first_name} {last_name}, me use, me use\.\
 O teu id no telegram é `{telegram_id}`""".format(
      first_name = message.from_user.first_name,
      last_name = message.from_user.last_name,
      telegram_id = message.from_user.id,
    ),
      parse_mode="MarkdownV2",
    )

  ## Lista de comandos
  @dispatcher.message_handler(
    commands = ['help', 'lista', 'ajuda'],
  )
  async def help_callback(message):
    await command_callback(message, 'help')
    lista = list()
    lista.append(u"""/ajuda : Se estiver lendo este texto, então não é \
necessário explicar o que faz este comando... Pode ser também: /lista ou /help\
""")
    ## Matebot
    lista.append(u"""/feedback <texto> : Envia feedback para o pessoal que \
desenvolve (bugs, erros, sugestões, solicitações, elogios, etc.) Pode ser també\
m: /f""")
    lista.append(u"""/qr <texto> : Gera QR code a partir do texto fornecido. Po\
de ser também: /qrcode""")
    lista.append(u"""/doar : Lista opções de doação para ajudar o Hackerspace M\
atehackers. Pode ser também: /donate""")
    lista.append(u"""/hash <algoritmo> <texto>: Calcula soma hash de um texto e\
m um algoritmo específico.""")
    lista.append(u"/pi : Uma boa aproximação de pi")
    lista.append(u"/phi : Uma boa aproximação de phi")
    lista.append(u"""/random - Gera número hexadecimal aleatório. Pode ser tamb\
ém: /r""")
    lista.append(u"""/archive <link>: Arquiva um site na Wayback Machine. Pode \
ser também: /a /wm /arquivar /savar""")
    lista.append(u"""/ytdl <link> : Extrai e envia como vídeo para o Telegram u\
m vídeo do Youtube, Facebook, Instagram ou áudio do Soundcloud, entre outros. P\
ode ser também: /y /youtube /baixar""")
    ## Gê
    # ~ lista.append(u"/hoje : Avisar que fez alguma coisa")
    # ~ lista.append(u"/agua : Avisar que tomou água")
    # ~ lista.append(u"/cafe : Avisar que tomou café")
    # ~ lista.append(u"/cheguei : Avisar que chegou")
    # ~ lista.append(u"/vazei : Avisar que saiu")
    # ~ lista.append(u"/adubei : Avisar que fertilizou")
    # ~ lista.append(u"/reguei : Avisar que regou a planta")
    # ~ lista.append(u"/semana : Ver como foi a semana")
    # ~ lista.append(u"/agora : Que horas são?")
    # ~ lista.append(u"/g - Great!")
    ## Cryptoforexbot
    # ~ lista.append(u"/info - About Crypto Forex Bot and source code")
    # ~ lista.append(u"/price - Show price information for a given coin")
    # ~ lista.append(u"/conv - Convert value from a currency to another")
    # ~ lista.append(u"/list - List available currencies")
    await message.reply(
      u"Lista de comandos:\n{lista}".format(lista = "\n".join(lista))
    )
    await command_callback(message, 'help')
