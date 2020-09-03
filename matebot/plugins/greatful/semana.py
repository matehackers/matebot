# vim:fileencoding=utf-8
#  Plugin greatful para matebot: Comandos para Greatful
#  Copyleft (C) 2019-2020 Iuri Guilherme, 2019-2020 Matehackers, 
#   2019 Greatful, 2019-2020 Fábrica do Futuro
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

## Agenda hebdomadária

import dataset, datetime, pytz, random, sqlite3

## Acrescenta relatório do dia na agenda hebdomadária
def hoje(args):
#  args['bot'].sendMessage(
#    args['chat_id'],
#    u"Hoje é um great dia!",
#    parse_mode = None,
#    reply_to_message_id = args['message_id']
#  )
  hoje = datetime.datetime.isocalendar(datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
  responses = [
    u"Parabéns pela atividade registrada!",
    u"Hoje é um great dia!",
    u"Mais um gol da Greatful!",
    u"Chupa muskinho!",
    u"Chupa zuckinho!",
    u"Muito obrigado por se organizar!"
  ]
  try:
    if len(args['command_list']) > 0:
      try:
        semana_db = dataset.connect('sqlite:///instance/semana.db')
        semana_db['relatorio'].insert(dict(
          pessoa = args['from_id'],
          texto = ' '.join(args['command_list']),
          ano = hoje[0],
          semana = hoje[1],
          dia = hoje[2]
        ))
        return {
          'status': True,
          'type': args['command_type'],
          'response': random.choice(responses),
          'hoje': ' '.join(args['command_list']),
          'debug': u"Workrave de hoje bem sucedido",
          'multi': False,
          'parse_mode': None,
          'reply_to_message_id': args['message_id'],
        }
      except sqlite3.ProgrammingError as e:
        response = u"Não consegui enviar para a agenda hebdomadária o vosso dia de hoje. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
        debug = u"Workrave (hoje) falhou.\nExceção sqlite: %s" % (e)
      except Exception as e:
        response = u"Não consegui enviar para a agenda hebdomadária o vosso dia de hoje. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
        debug = u"Workrave (hoje) falhou.\nExceção: %s" % (e)
    else:
      response = u"Calma, eu quero te ajudar mas por favor entendais as minhas limitações temporárias. Vós deveis me dizer o que fez no dia de hoje seguindo este modelo:\n\n/hoje eu fiz tudo o que eu falei, que é..."
      debug = u"Workrave (hoje) falhou, mensagem vazia"
  except Exception as e:
    response = u"Não consegui enviar para a agenda hebdomadária o vosso dia de hoje. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (hoje) falhou.\nExceção: %s" % (e)
  return {
    'status': False,
    'type': 'erro',
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Exibe a agenda hebdomadária
def semana(args):
#  args['bot'].sendMessage(
#    args['chat_id'],
#    u"Esta é uma great semana!",
#    parse_mode = None,
#    reply_to_message_id = args['message_id']
#  )
  hoje = datetime.datetime.isocalendar(datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
  planetas = {
    '0': u"☼ Domingo (sol):",
    '1': u"☾ Segunda (lua):",
    '2': u"♂ Terça (marte):",
    '3': u"☿ Quarta (mercúrio):",
    '4': u"♃ Quinta (júpiter):",
    '5': u"♀ Sexta (vênus):",
    '6': u"♄ Sábado (saturno):",
    '7': u"♌ Domingo (sol):"
  }
  nadas = [
    u"☃️",
    u"\u26c4",
    u"\U0001f37c",
    u"\U0001f40c",
    u"\U0001f422",
    u"\U0001f47b",
    u"\U0001f4a9",
    u"\U0001f648",
    u"\U0001f649",
    u"\U0001f64a",
    u"\U0001f6af",
    u"\U0001f912",
    u"\U0001f915",
    u"\U0001f924",
    u"\U0001f925",
    u"\U0001f974"
  ]
  try:
    semana_db = dataset.connect('sqlite:///instance/semana.db')
    relatorios = semana_db['relatorio']
    chegadas = semana_db['chegada']
    vazadas = semana_db['vazada']
    adubos = semana_db['adubada']
    aguas = semana_db['agua']
    cafes = semana_db['cafe']
    regadas = semana_db['regada']
    respostas = [u"A minha semana nº %s do ano %s depois da Greatful foi assim:" % (str(hoje[1]), str(2019 - hoje[0]))]
    for dia in range(7):
      diario = list()
      diario.append(u"*%s*" % (planetas.get(str(dia), u"♾️ Sempre (terra):")))
      diario.append(str())
      diario.append(next((u"\t\t\t\t← Cheguei às %s" % (chegada['hora']) for chegada in chegadas if chegada['pessoa'] == args['from_id'] and chegada['ano'] == hoje[0] and chegada['semana'] == hoje[1] and chegada['dia'] == dia), u"\t\t\t\t_↓ /cheguei sem dar oi_"))
      diario.append(str())
      diario.append(u"\t\t\t\t=== === ===")
      diario.extend([''.join([u"\t\t\t\t→ ", relatorio['texto'], u";"]) for relatorio in relatorios if relatorio['pessoa'] == args['from_id'] and relatorio['ano'] == hoje[0] and relatorio['semana'] == hoje[1] and relatorio['dia'] == dia])
      diario.append(u"\t\t\t\t=== === ===")
      diario.append(str())
      
      adubo = [str(adubo['hora']) for adubo in adubos if adubo['pessoa'] == args['from_id'] and adubo['ano'] == hoje[0] and adubo['semana'] == hoje[1] and adubo['dia'] == dia]
      if len(adubo) > 0:
        diario.append(u"\t\t\t\t↓ Adubei %s vezes" % (len(adubo)))
#      else:
#        diario.append(u"\t\t\t\t_← não /adubei_")
      agua = [str(agua['hora']) for agua in aguas if agua['pessoa'] == args['from_id'] and agua['ano'] == hoje[0] and agua['semana'] == hoje[1] and agua['dia'] == dia]
      if len(agua) > 0:
        diario.append(u"\t\t\t\t← Tomei %s copos de água: Às %s." % (len(agua), u", ".join(agua)))
#      else:
#        diario.append(u"\t\t\t\t_↓ não tomei /agua_")
      cafe = [str(cafe['hora']) for cafe in cafes if cafe['pessoa'] == args['from_id'] and cafe['ano'] == hoje[0] and cafe['semana'] == hoje[1] and cafe['dia'] == dia]
      if len(cafe) > 0:
        diario.append(u"\t\t\t\t↓ Tomei %s xícaras de café: Às %s." % (len(cafe), u", ".join(cafe)))
#      else:
#        diario.append(u"\t\t\t\t_← não tomei /cafe_")
      regada = [str(regada['hora']) for regada in regadas if regada['pessoa'] == args['from_id'] and regada['ano'] == hoje[0] and regada['semana'] == hoje[1] and regada['dia'] == dia]
      if len(regada) > 0:
        diario.append(u"\t\t\t\t← Reguei a planta %s vezes. Às %s." % (len(regada), u", ".join(regada)))
#      else:
#        diario.append(u"\t\t\t\t_↓ não /reguei a planta_")
        
      diario.append(next((u"\t\t\t\t↓ Vazei às %s" % (vazada['hora']) for vazada in vazadas if vazada['pessoa'] == args['from_id'] and vazada['ano'] == hoje[0] and vazada['semana'] == hoje[1] and vazada['dia'] == dia), u"\t\t\t\t_↓ /vazei sem dar tchau_"))
      print(len(diario))
      if len(diario) > 8:
        respostas.append(u"\n".join(diario))
    if not len(respostas) > 1:
      respostas.append(u"\t\t\t\t%s Nadei #adubão" % (random.choice(nadas)))
    respostas.append(
      u"#semana%s do #ano%s\n``` %s chegadas ← %s vazadas ← %s plantas regadas ← %s copos de água ← %s xícaras de café ← %s adubadas ```" % (
        str(hoje[1]),
        str(2019 - hoje[0]),
        len([chegada for chegada in chegadas if chegada['pessoa'] == args['from_id'] and chegada['ano'] == hoje[0] and chegada['semana'] == hoje[1]]),
        len([vazada for vazada in vazadas if vazada['pessoa'] == args['from_id'] and vazada['ano'] == hoje[0] and vazada['semana'] == hoje[1]]),
        len([regada for regada in regadas if regada['pessoa'] == args['from_id'] and regada['ano'] == hoje[0] and regada['semana'] == hoje[1]]),
        len([agua for agua in aguas if agua['pessoa'] == args['from_id'] and agua['ano'] == hoje[0] and agua['semana'] == hoje[1]]),
        len([cafe for cafe in cafes if cafe['pessoa'] == args['from_id'] and cafe['ano'] == hoje[0] and cafe['semana'] == hoje[1]]),
        len([adubo for adubo in adubos if adubo['pessoa'] == args['from_id'] and adubo['ano'] == hoje[0] and adubo['semana'] == hoje[1]])
      )
    )
    return {
      'status': True,
      'type': args['command_type'],
      'response': '\n\n'.join(respostas),
      'hoje': ' '.join(args['command_list']),
      'debug': u"Workrave da semana bem sucedido",
      'multi': False,
      'parse_mode': 'Markdown',
      'reply_to_message_id': args['message_id'],
    }
  except sqlite3.ProgrammingError as e:
    response = u"/adubei Não consegui encontrar a vossa agenda hebdomadária. Foi em decorrência de algum problema relacionado à programação do banco de dados. Então alguém em algum momento resolverá este adubo. Desculpe não poder ajudar, hoje eu /fertilizei."
    debug = u"Workrave (semana) falhou.\nExceção sqlite: %s" % (e)
    raise
  except Exception as e:
    response = u"Não consegui encontrar a vossa agenda hebdomadária. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (semana) falhou.\nExceção: %s" % (e)
    raise
  return {
    'status': False,
    'type': 'erro',
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

