# vim:fileencoding=utf-8
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
        semana_db = dataset.connect('sqlite:///semana.db')
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
    semana_db = dataset.connect('sqlite:///semana.db')
    relatorios = semana_db['relatorio']
    respostas = [u"A minha semana nº %s do ano %s depois da Greatful foi assim:" % (str(hoje[1]), str(2019 - hoje[0]))]
    for dia in range(7):
      diario = list()
      diario.append(planetas.get(str(dia), u"Terra"))
      diario.append(str())
      diario.extend([''.join([u"\t\t\t\t→ ", relatorio['texto'], u";"]) for relatorio in relatorios if relatorio['pessoa'] == args['from_id'] and relatorio['ano'] == hoje[0] and relatorio['semana'] == hoje[1] and relatorio['dia'] == dia])
      if len(diario) > 2:
        respostas.append(u"\n".join(diario))
    if not len(respostas) > 1:
      respostas.append(u"%s Nadei #adubão" % (random.choice(nadas)))
    respostas.append(u"#semana%s #ano%s" % (str(hoje[1]), str(2019 - hoje[0])))
#      if not len(diario) > 2:
#        diario.append(u"\t\t\t\t← Nadei")
#      respostas.append(u"\n".join(diario))
#    respostas.append(u"#semana%s #ano%s" % (str(hoje[1]), str(2019 - hoje[0])))
    return {
      'status': True,
      'type': args['command_type'],
      'response': '\n\n'.join(respostas),
      'hoje': ' '.join(args['command_list']),
      'debug': u"Workrave da semana bem sucedido",
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  except sqlite3.ProgrammingError as e:
    response = u"/adubei Não consegui encontrar a vossa agenda hebdomadária. Foi em decorrência de algum problema relacionado à programação do banco de dados. Então alguém em algum momento resolverá este adubo. Desculpe não poder ajudar, hoje eu /fertilizei."
    debug = u"Workrave (semana) falhou.\nExceção sqlite: %s" % (e)
  except Exception as e:
    response = u"Não consegui encontrar a vossa agenda hebdomadária. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (semana) falhou.\nExceção: %s" % (e)
  return {
    'status': False,
    'type': 'erro',
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

