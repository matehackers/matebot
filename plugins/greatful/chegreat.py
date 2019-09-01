# vim:fileencoding=utf-8
## Ponto Greatful

import dataset, datetime, pytz, random, sqlite3

## Avisa que chegou na Fábrica do Futuro
def cheguei(args):
  hoje = datetime.datetime.isocalendar(datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
  responses = [
    u"Chegou chegando, desnorteando a Fábrica toda!",
    u"Hoje é um great dia!",
    u"Bom dia!",
    u"\U0001f64f",
    u"\U0001f64f\U0001f3fb",
    u"\U0001f64f\U0001f3fc",
    u"\U0001f64f\U0001f3fd",
    u"\U0001f64f\U0001f3fe",
    u"\U0001f64f\U0001f3ff",
    u"\U0001f64c",
    u"\U0001f64c\U0001f3fb",
    u"\U0001f64c\U0001f3fc",
    u"\U0001f64c\U0001f3fd",
    u"\U0001f64c\U0001f3fe",
    u"\U0001f64c\U0001f3ff",
    u"\U0001f44f",
    u"\U0001f44f\U0001f3fb",
    u"\U0001f44f\U0001f3fc",
    u"\U0001f44f\U0001f3fd",
    u"\U0001f44f\U0001f3fe",
    u"\U0001f44f\U0001f3ff",
    u"\U0001f91d"
  ]
  try:
    semana_db = dataset.connect('sqlite:///semana.db')
    semana_db['chegada'].insert(dict(
      pessoa = args['from_id'],
      ano = hoje[0],
      semana = hoje[1],
      dia = hoje[2],
      hora = datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).hour,
      texto = ' '.join(args['command_list'])
    ))
    return {
      'status': True,
      'type': args['command_type'],
      'response': random.choice(responses),
      'debug': 'cheguei',
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  except sqlite3.ProgrammingError as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós chegardes agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (cheguei) falhou.\nExceção sqlite: %s" % (e)
  except Exception as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós chegardes agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (cheguei) falhou.\nExceção: %s" % (e)
  return {
    'status': False,
    'type': 'erro',
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Avisa que foi embora da Fábrica do Futuro
def vazei(args):
  hoje = datetime.datetime.isocalendar(datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
  responses = [
    u"A Fábrica é boa, mas não dá pra morar aí!",
    u"Hoje foi um great dia!",
    u"Amanhã vai ser outro dia!",
    u"Banoite!",
    u"Obrigada pelo dia de hoje!",
    u"\U0001f540",
    u"\U0001f540\U0001f3fb",
    u"\U0001f540\U0001f3fc",
    u"\U0001f540\U0001f3fd",
    u"\U0001f540\U0001f3fe",
    u"\U0001f540\U0001f3ff",
    u"\U0001f91f",
    u"\U0001f91f\U0001f3fb",
    u"\U0001f91f\U0001f3fc",
    u"\U0001f91f\U0001f3fd",
    u"\U0001f91f\U0001f3fe",
    u"\U0001f91f\U0001f3ff",
    u"✌️",
    u"✌️\U0001f3fb",
    u"✌️\U0001f3fc",
    u"✌️\U0001f3fd",
    u"✌️\U0001f3fe",
    u"✌️\U0001f3ff",
    u"\U0001f44b"
    u"\U0001f44b\U0001f3fb",
    u"\U0001f44b\U0001f3fc",
    u"\U0001f44b\U0001f3fd",
    u"\U0001f44b\U0001f3fe",
    u"\U0001f44b\U0001f3ff"
  ]
  try:
    semana_db = dataset.connect('sqlite:///semana.db')
    semana_db['vazada'].insert(dict(
      pessoa = args['from_id'],
      ano = hoje[0],
      semana = hoje[1],
      dia = hoje[2],
      hora = datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).hour,
      texto = ' '.join(args['command_list'])
    ))
    return {
      'status': True,
      'type': args['command_type'],
      'response': random.choice(responses),
      'debug': 'vazei',
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  except sqlite3.ProgrammingError as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós vazardes agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (vazei) falhou.\nExceção sqlite: %s" % (e)
  except Exception as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós vazardes agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (vazei) falhou.\nExceção: %s" % (e)
  return {
    'status': False,
    'type': 'erro',
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Avisa que fez uma merda
def adubei(args):
  hoje = datetime.datetime.isocalendar(datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
  responses = [
    u"Adubando a gente dá.\nO ato de dar gera abundância.\nEntão, dar abunda!",
    u"Todo adubo é fertilizante para o limoeiro.\nTodo limão é uma limonada.",
    u"Plante as sementes.\nColha os milhões.",
    u"Vós sois padawan e terdes tempo pra aprender.",
    u"Tentai outra vez.",
    u"\U0001f4a9",
    u"\U0001f4a9\U0001f4a9\U0001f4a9",
    u"\U0001f4a9\U0001f4a9\U0001f4a9\U0001f4a9\U0001f4a9\U0001f4a9\U0001f4a9\U0001f4a9\U0001f4a9"
  ]
  response = random.choice(responses)
  try:
    semana_db = dataset.connect('sqlite:///semana.db')
    semana_db['adubada'].insert(dict(
      pessoa = args['from_id'],
      ano = hoje[0],
      semana = hoje[1],
      dia = hoje[2],
      hora = datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).hour,
      texto = ' '.join(args['command_list'])
    ))
    return {
      'status': True,
      'type': args['command_type'],
      'response': random.choice(responses),
      'debug': 'adubei',
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  except sqlite3.ProgrammingError as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós adubardes agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (adubei) falhou.\nExceção sqlite: %s" % (e)
  except Exception as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós adubardes agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (adubei) falhou.\nExceção: %s" % (e)
  return {
    'status': False,
    'type': 'erro',
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

