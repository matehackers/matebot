# vim:fileencoding=utf-8

import importlib,json
from plugins.log import log_str

def parse(args):
  config = args['config']
  try:
    ## TODO mover tudo isto para um formato ainda mais automático que permita o escalonamento de plugins
    ## TODO tentar entender o que eu quis dizer na frase acima
    plugins_disponiveis = json.loads(config['plugins_listas']['geral'])
    plugins_admin = json.loads(config['plugins_listas']['admin'])
    plugins_matehackers = json.loads(config['plugins_listas']['matehackers'])
    args.update(
      {
        'info_dict': dict(config.items('info')),
        'bot_dict': {'handle': args['bot'].getMe()['username'], 'name': args['bot'].getMe()['first_name']},
        'addr_dict': dict(config.items('donate')),
        'plugins_list': plugins_disponiveis,
      }
    )
    args.update(command_type = 'grupo')
    if (int(args['chat_id']) > 0):
      args.update(command_type = 'mensagem')
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'response': u'Erro processando o comando. Os desenvolvedores foram ou deveriam ter sido avisados.',
      'debug': u'Exceção %s\ncommand_list: %s' % (e, str(args['command_list'])),
      'multi': False,
      'parse_mode': None,
    }

  ## Administradora(e)s
  if args['chat_id'] in json.loads(config['plugins_usuarios']['admin']):
    args.update(plugins_list = args['plugins_list'] + plugins_admin)
  ## Grupo de administração
  if args['chat_id'] in json.loads(config['plugins_grupos']['admin']):
    args.update(plugins_list = args['plugins_list'] + plugins_admin)
  ## Grupo Matehackers
  if args['chat_id'] in json.loads(config['plugins_grupos']['matehackers']):
    args.update(plugins_list = args['plugins_list'] + plugins_matehackers)
  ## Usuária(o)s Matehackers
  if args['chat_id'] in json.loads(config['plugins_usuarios']['matehackers']):
    args.update(plugins_list = args['plugins_list'] + plugins_matehackers)
  ## Grupo comum
  if int(args['chat_id']) < 0:
    pass
  ## Usuário comum
  if int(args['chat_id']) > 0:
    pass

  comando = str(args['command_list'].split(' ')[0].split('/', 1)[1].split('@', 1)[0])
  args.update(command_list = args['command_list'].split(' ')[1::])
  for plugin in args['plugins_list']:
    try:
      return getattr(importlib.import_module('.'.join(['plugins', plugin])), comando)(args)
    except AttributeError as e:
      print(log_str.err(e))
      pass
    except ImportError as e:
      print(log_str.err(e))
      pass
    except Exception as e:
      raise
      return {
        'status': False,
        'type': 'erro',
        'response': u'Erro processando o comando. Os desenvolvedores foram ou deveriam ter sido avisados.',
        'debug': u'Exceção %s, command_list: %s' % (str(e), str(args['command_list'])),
        'multi': False,
        'parse_mode': None,
      }
  return {
    'status': False,
    'type': 'erro',
    'response': u'Vossa excelência não terdes autorização para usar este comando, ou o comando não existe.',
    'debug': u'Nada aconteceu. command_list: %s' % (str(args['command_list'])),
    'multi': False,
    'parse_mode': None,
  }

