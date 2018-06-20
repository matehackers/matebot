# vim:fileencoding=utf-8

import importlib

def parse(args):
  config = args['config']
  try:
    plugins_disponiveis = config.get("bot", "plugins")
    plugins_admin = config.get("bot", "plugins_admin")
    args.update(
      {
        'info_dict': dict(config.items('info')),
        'bot_dict': dict(config.items('bot')),
        'addr_dict': dict(config.items('crypto_addresses')),
        'plugins_list': plugins_disponiveis,
      }
    )
  except configparser.Exception as e:
    return {
      'status': False, 
      'type': 'erro', 
      'response': u'Erro do config parser', 
      'debug': u'Erro do configparser: %s' % (e),
    }
  
  ## Se chat_id for negativo, estamos falando com um grupo.
  if int(args['chat_id']) < 0:
    ## Grupo de administração
    if str(args['chat_id']) == str(config['admin']['group']):
      args.update(plugins_list = plugins_disponiveis + ',' + plugins_admin)
    ## Grupo comum
    else:
      pass
  ## Admnistrador
  elif str(args['chat_id']) == str(config['admin']['id']):
    args.update(plugins_list = plugins_disponiveis + ',' + plugins_admin)
  ## Usuário comum
  else:
    pass
  
  comando = str(args['command_list'][0].split("/")[1])
  args.update(command_list = args['command_list'][1:])
  for plugin in args['plugins_list'].split(','):
    try:
      return getattr(importlib.import_module('.'.join(['plugins', plugin])), comando)(args)
    except AttributeError:
      pass
    except ImportError:
      pass
  return {
    'status': False,
    'type': 'nada',
    'response': u'Esta mensagem nunca deve aparecer no telegram',
    'debug': 'Nada aconteceu. command_list: %s' % (str(args['command_list'])),
  }
