# vim:fileencoding=utf-8
#  Plugin telegram para matebot: Comandos padrão de bots de telegram
#  Copyleft (C) 2016-2019 Desobediente Civil, Matehackers
#  Copyleft (C) 2019 Greatful

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

## TODO Repensar este plugin, para que seja consistente com upstream

def cmd_help(args):
  response = u'Meu nome é Greta'
  return {
    'status': True,
    'type': args['command_type'],
    'response': response,
    'debug': 'help',
    'multi': False,
    'parse_mode': None,
  }

def cmd_ajuda(args):
  response = list()
  response.append(u"Lista de comandos:")
  response.append(u"")
  # TODO acentuacao
  response.append(u"`/ajuda`\nSe estardes lendo este texto, entao nao e necessaria explanacao acerca deste comando")
  response.append(u"`/feedback <texto>`\nEnvia feedback para os desenvolvedores")
  response.append(u"`/qr <texto>`\nGera QR code a partir do texto fornecido")
  response.append(u"")
  response.append(u"Plugin Velivery Pedidos")
  response.append(u"`/pedido <id>`\nExibe descrição completa de um pedido (fornecer código)")
  # TODO acentuacao
  response.append(u"`/pedidos [limite]`\nListar todos os pedidos (limite padrao 3)")
  response.append(u"`/pendentes`\nListar pedidos pendentes (inclusive os agendados)")
  response.append(u"`/atrasados`\nListar pedidos atrasados que ainda não foram atendidos")
  response.append(u"")
  response.append(u"Plugin Totalvoice")
  response.append(u"`/ligar_1 <numero>`\nEnvia audio `shiva_1` para numero de telefone de estabelecimento")
  response.append(u"`/ligar_2 <numero>`\nEnvia audio `shiva_2` para numero de telefone de estabelecimento")
  response.append(u"`/ligar_3 <numero>`\nEnvia audio `shiva_3` para numero de telefone de estabelecimento")
  response.append(u"`/ligar_4 <numero>`\nEnvia audio `shiva_4` para numero de telefone de estabelecimento")
  response.append(u"")
  response.append(u"Plugin Bike Entregas")
  # TODO acentuacao
  response.append(u"`/husky_geo <endereco>`\nFornece coordenadas geograficas a partir de endereco (google maps api)")
  response.append(u"`/husky_pendentes`\nListar pedidos aceitos pelo estabelecimento que ainda não foram enviados para o gerenciador da Husky")
  response.append(u"`/husky_pedido <id>`\nEnvia pedido para a Husky (fornecer código)")
  response.append(u"`/husky_atendidos [id]`\nLista pedidos que já foram atendidos pela Husky, ou adiciona manualmente um pedido na lista")
  # TODO acentuacao
  response.append(u"")
  response.append(u"Plugin Velivery Relatorios")
  response.append(u"`/relatorio_recompra`\nExibe a taxa de recompra do Velivery")
  response.append(u"`/relatorio_recompra_total`\nExibe a taxa de recompra do Velivery de todo período e gera arquivo CSV")
  response.append(u"`/relatorio_recompra_ano <ano>`\nExibe a taxa de recompra do Velivery para o ano especificado e gera arquivo CSV")
  response.append(u"`/relatorio_vendas [ano] [mes]`\nExibe o total de vendas no Velivery total ou por periodo")
  response.append(u"`/relatorio_vendas_total`\nExibe o total de vendas no Velivery de todo período")
  response.append(u"`/relatorio_vendas_ano`\nExibe o total de vendas do Velivery para o ano especificado")
  response.append(u"`/relatorio_vendas_mes`\nExibe o total de vendas do Velivery para o mês e ano especificados")
  response.append(u"`/relatorio_usuarios`\nExibe informações sobre usuárias(os) do Velivery")
  response.append(u"`/relatorio_uf`\nExibe total de pedidos, usuárias(os) e usuárias(os) únicos por período")
  response.append(u"`/dados_estabelecimentos`\nExibe informações sobre estabelecimentos cadastrados no Velivery")
  response.append(u"`/exportar_280`\nCria arquivo csv com todos pedidos do Velivery")
  # TODO testar e descobri o que e
  response.append(u"")
  response.append(u"`/taxa_recompra`\nComando criado nao lembro pra que")
  response.append(u"`/relatorio_dre`\nComando criado nao lembro pra que")
  response.append(u"`/relatorio_ltv`\nComando criado nao lembro pra que")
  response.append(u"`/relatorio_recompra2`\nComando criado nao lembro pra que")
  response.append(u"`/relatorio_usuarios_unicos`\nComando criado nao lembro pra que")
  response.append(u"`/relatorio_usuarios_pedidos`\nComando criado nao lembro pra que")
  response.append(u"`/relatorio_vendas_2`\nComando criado nao lembro pra que")
  response.append(u"`/resumo_vendas_2`\nComando criado nao lembro pra que")
  response.append(u"`/mailing`\nComando criado nao lembro pra que")
  response.append(u"`/inativos`\nComando criado nao lembro pra que")
  response.append(u"`/veganweek`\nComando criado nao lembro pra que")
  response.append(u"`/vegcoinweek_cac`\nComando criado nao lembro pra que")
  ## TODO verificar se o markdown está funcionando
  return {
    'status': True,
    'type': args['command_type'],
    'response': "\n".join(response),
    'debug': 'ajuda',
    'multi': False,
    'parse_mode': 'Markdown',
  }

