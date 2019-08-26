# vim:fileencoding=utf-8
## Agenda hebdomadária

import dataset, datetime, random, sqlite3

## Acrescenta relatório do dia na agenda hebdomadária
def hoje(args):
#  args['bot'].sendMessage(
#    args['chat_id'],
#    u"Hoje é um great dia!",
#    parse_mode = None,
#    reply_to_message_id = args['message_id']
#  )
  hoje = datetime.date.isocalendar(datetime.date.today())
  responses = [
    u"Parabéns pela atividade registrada!",
    u"Hoje é um great dia!",
    u"Mais um gol da Greatful!",
    u"Chupa marquinho!",
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
  hoje = datetime.date.isocalendar(datetime.date.today())
  planetas = {
    '0': u"Sol:",
    '1': u"Lua:",
    '2': u"Marte:",
    '3': u"Mercúrio:",
    '4': u"Júpiter:",
    '5': u"Vênus:",
    '6': u"Saturno:",
    '7': u"Sol:"
  }
  try:
    semana_db = dataset.connect('sqlite:///semana.db')
    relatorios = semana_db['relatorio']
    respostas = [u"A minha semana foi assim:"]
    for dia in range(7):
      diario = list()
      diario.append(planetas.get(str(dia), u"Terra"))
      diario.extend([''.join(["\t", relatorio['texto']]) for relatorio in relatorios if relatorio['pessoa'] == args['from_id'] and relatorio['ano'] == hoje[0] and relatorio['semana'] == hoje[1] and relatorio['dia'] == dia])
      if not len(diario) > 1:
        diario.append(u"\tFiz nada ou não registrei! #adubão")
      respostas.append('\n'.join(diario))
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

