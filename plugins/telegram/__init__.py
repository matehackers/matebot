# vim:fileencoding=utf-8
#    Plugin telegram para matebot: Comandos padrão de bots de telegram
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

## TODO Repensar este plugin, para que seja consistente com upstream

def help(args):
  response = u'Meu nome é Vegga'
  return {
    'status': True,
    'type': args['command_type'],
    'response': response,
    'debug': 'help',
    'multi': False,
    'parse_mode': None,
  }

def ajuda(args):
  response = list()
  response.append(u"Lista de comandos:")
  response.append(u"`/pedido - Exibe descrição completa de um pedido (fornecer código)`")
  response.append(u"`/pedidos - Listar todos os pedidos`")
  response.append(u"`/pendentes - Listar pedidos pendentes (inclusive os agendados)`")
  response.append(u"`/atrasados - Listar pedidos atrasados que ainda não foram atendidos`")
  response.append(u"`/husky_pendentes - Listar pedidos aceitos pelo estabelecimento que ainda não foram enviados para o gerenciador da Husky`")
  response.append(u"`/husky_pedido - Envia pedido para a Husky (fornecer código)`")
  response.append(u"`/husky_atendidos - Lista pedidos que já foram atendidos pela Husky, ou adiciona manualmente um pedido na lista`")
  response.append(u"`/relatorio_recompra - Exibe a taxa de recompra do Velivery`")
  response.append(u"`/relatorio_recompra_total - Exibe a taxa de recompra do Velivery de todo período e gera arquivo CSV`")
  response.append(u"`/relatorio_recompra_ano - Exibe a taxa de recompra do Velivery para o ano especificado e gera arquivo CSV`")
  response.append(u"`/relatorio_vendas_total - Exibe o total de vendas no Velivery de todo período`")
  response.append(u"`/relatorio_vendas_ano - Exibe o total de vendas do Velivery para o ano especificado`")
  response.append(u"`/relatorio_vendas_mes - Exibe o total de vendas do Velivery para o mês e ano especificados`")
  response.append(u"`/relatorio_usuarios - Exibe informações sobre usuárias(os) do Velivery`")
  response.append(u"`/relatorio_uf - Exibe total de pedidos, usuárias(os) e usuárias(os) únicos por período`")
  response.append(u"`/dados_estabelecimentos - Exibe informações sobre estabelecimentos cadastrados no Velivery`")
  response.append(u"`/exportar_280 - Cria arquivo csv com todos pedidos do Velivery`")
  response.append(u"`/qr - Gera QR code a partir do texto fornecido`")
  ## TODO verificar se o markdown está funcionando
  return {
    'status': True,
    'type': args['command_type'],
    'response': "\n".join(response),
    'debug': 'ajuda',
    'multi': False,
    'parse_mode': 'Markdown',
  }

