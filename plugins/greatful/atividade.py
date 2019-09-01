# vim:fileencoding=utf-8
## Atividades paralelas

import dataset, datetime, pytz, random, sqlite3

## Avisa que tomou água
def agua(args):
  hoje = datetime.datetime.isocalendar(datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
  responses = [
    u"Mais um copo!",
    u"Olha, olha, olha, olha água mineral!",
    u"\U0001f95b"
  ]
  try:
    semana_db = dataset.connect('sqlite:///semana.db')
    semana_db['agua'].insert(dict(
      pessoa = args['from_id'],
      ano = hoje[0],
      semana = hoje[1],
      dia = hoje[2],
      hora = datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).hour,
    ))
    return {
      'status': True,
      'type': args['command_type'],
      'response': random.choice(responses),
      'debug': 'agua',
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  except sqlite3.ProgrammingError as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós tomardes água agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (água) falhou.\nExceção sqlite: %s" % (e)
  except Exception as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós tomardes água agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (água) falhou.\nExceção: %s" % (e)
  return {
    'status': False,
    'type': 'erro',
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Avisa que tomou café
def cafe(args):
  hoje = datetime.datetime.isocalendar(datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
  responses = [
    u"Mais uma caneca!",
    u"Já viu se café faz bem pro vosso tipo sanguíneo?",
    u"☕"
  ]
  try:
    semana_db = dataset.connect('sqlite:///semana.db')
    semana_db['cafe'].insert(dict(
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
      'debug': 'cafe',
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  except sqlite3.ProgrammingError as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós tomardes café agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (café) falhou.\nExceção sqlite: %s" % (e)
  except Exception as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós tomardes café agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (café) falhou.\nExceção: %s" % (e)
  return {
    'status': False,
    'type': 'erro',
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Avisa que regou a planta
def reguei(args):
  hoje = datetime.datetime.isocalendar(datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
  responses = [
    u"\U0001f331",
    u"\U0001f332",
    u"\U0001f333",
    u"\U0001f334",
    u"\U0001f335",
    u"\U0001f337",
    u"\U0001f338",
    u"\U0001f33a",
    u"\U0001f33b",
    u"\U0001f33c",
    u"\U0001f33e",
    u"\U0001f33f",
    u"\U0001f38b",
    u"\U0001f38d",
    u"\U0001f339",
    u"\U0001f340",
    u"\U0001f341",
    u"\U0001f342",
    u"\U0001f343",
    u"\U0001f344",
    u"\U0001f490",
    u"☘️"
  ]
  response = random.choice(responses)
  try:
    semana_db = dataset.connect('sqlite:///semana.db')
    semana_db['regada'].insert(dict(
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
      'debug': 'reguei',
      'multi': False,
      'parse_mode': None,
      'reply_to_message_id': args['message_id'],
    }
  except sqlite3.ProgrammingError as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós regardes agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (reguei) falhou.\nExceção sqlite: %s" % (e)
  except Exception as e:
    response = u"Não consegui enviar para a agenda hebdomadária que vós regardes agora. Os desenvolvedores serão notificados de qualquer forma. Mas tente novamente, por favor."
    debug = u"Workrave (reguei) falhou.\nExceção: %s" % (e)
  return {
    'status': False,
    'type': 'erro',
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

